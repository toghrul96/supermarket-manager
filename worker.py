import traceback
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Signal, Qt

# Thread pool to run tasks in the background.
# Creates threads once and reuses them for all tasks.
_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="worker")


class _Relay(QObject):
    """
    Relay object to send results/errors from a background thread to the main UI thread.

    Ensures callbacks run on the main thread using Qt's signals.
    """
    _result_signal = Signal(object)  # Signal for successful result
    _error_signal = Signal(str)      # Signal for error messages

    def __init__(self, on_result=None, on_error=None):
        """
        Initialize relay with optional success and error callbacks.

        Args:
            on_result (callable, optional): Called with the result on success.
            on_error (callable, optional): Called with the error message on failure.
        """
        super().__init__()
        self._on_result = on_result
        self._on_error = on_error

        # Connect signals to handlers that run on the main thread
        self._result_signal.connect(self._handle_result, Qt.ConnectionType.QueuedConnection)
        self._error_signal.connect(self._handle_error, Qt.ConnectionType.QueuedConnection)

    def _handle_result(self, result):
        """
        Called when the background task succeeds.

        Runs the on_result callback on the main thread.
        """
        if self._on_result:
            self._on_result(result)

    def _handle_error(self, message):
        """
        Called when the background task fails.

        Runs the on_error callback on the main thread.
        """
        if self._on_error:
            self._on_error(message)


def run_worker(fn, *args, on_result=None, on_error=None, **kwargs):
    """
    Run a function in a background thread safely with result/error callbacks.

    Args:
        fn (callable): The function to run in the background.
        *args: Positional arguments for the function.
        on_result (callable, optional): Called with result when fn succeeds.
        on_error (callable, optional): Called with error message if fn fails.
        **kwargs: Keyword arguments for the function.

    Returns:
        tuple: (Future object, Relay object). Keep both alive until task finishes.
    """
    # Create a relay to handle signals and callbacks
    relay = _Relay(on_result=on_result, on_error=on_error)

    def target():
        """
        Function that runs in the background thread.

        Calls the target function and emits result or error via relay signals.
        """
        try:
            result = fn(*args, **kwargs)
            relay._result_signal.emit(result)  # Send result to main thread
        except Exception:
            traceback.print_exc()  # Print error to console
            relay._error_signal.emit(traceback.format_exc())  # Send error to main thread

    # Submit the target function to the thread pool
    future = _pool.submit(target)

    # Return both so caller can keep them alive
    return future, relay

