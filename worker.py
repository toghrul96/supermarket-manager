import traceback
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Signal, Qt

# A shared pool of persistent worker threads. Threads are reused across calls,
# so each thread's thread-local Supabase client (and its gotrue machinery) is
# created exactly once and then kept alive — eliminating the ~1 s cold-start
# penalty that appeared when a fresh thread (and therefore a fresh client) was
# spawned for every button click.
_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="worker")


class _Relay(QObject):
    """
    Lives on the main thread. Receives signals from the background thread
    and calls the Python callbacks on the main thread via Qt's queued
    connection mechanism.
    """
    _result_signal = Signal(object)
    _error_signal = Signal(str)

    def __init__(self, on_result=None, on_error=None):
        super().__init__()
        self._on_result = on_result
        self._on_error = on_error
        # QueuedConnection guarantees delivery on the main thread
        # because this QObject was constructed on the main thread.
        self._result_signal.connect(self._handle_result, Qt.ConnectionType.QueuedConnection)
        self._error_signal.connect(self._handle_error, Qt.ConnectionType.QueuedConnection)

    def _handle_result(self, result):
        if self._on_result:
            self._on_result(result)

    def _handle_error(self, message):
        if self._on_error:
            self._on_error(message)


def run_worker(fn, *args, on_result=None, on_error=None, **kwargs):
    """
    Run fn(*args, **kwargs) in a background thread from the shared pool.

    Threads are reused rather than created fresh each call, so thread-local
    Supabase clients survive between calls and avoid repeated cold-start
    overhead from create_client() / gotrue initialisation.

    on_result and on_error are guaranteed to run on the main thread because
    they are dispatched through a QObject relay constructed on the main thread
    using Qt's QueuedConnection mechanism.

    Returns (future, relay). Keep both references alive until the call finishes.
    """
    relay = _Relay(on_result=on_result, on_error=on_error)

    def target():
        try:
            result = fn(*args, **kwargs)
            relay._result_signal.emit(result)
        except Exception:
            traceback.print_exc()
            relay._error_signal.emit(traceback.format_exc())

    future = _pool.submit(target)
    # Return future and relay so caller can keep both alive.
    return future, relay