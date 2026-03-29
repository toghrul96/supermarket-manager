import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from ui.ui_login import Ui_LogInWindow
from main import MainWindow
from worker import run_worker


class LogInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LogInWindow()
        self.ui.setupUi(self)

        # Do NOT create UserDatabase here — supabase-py's create_client()
        # starts gotrue's async auth-state machinery which interferes with
        # Qt's event loop. Create it only inside the worker thread.

        self.ui.password_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.log_in_pushButton.clicked.connect(self.handle_log_in)
        self.ui.username_lineEdit.returnPressed.connect(self.handle_log_in)
        self.ui.password_lineEdit.returnPressed.connect(self.handle_log_in)

        self._thread = None
        self._relay = None

    def handle_log_in(self):
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter username and password.")
            return

        self.ui.log_in_pushButton.setEnabled(False)
        self.ui.log_in_pushButton.setText("Signing in...")
        self.ui.username_lineEdit.setEnabled(False)
        self.ui.password_lineEdit.setEnabled(False)

        def do_auth():
            from models.user import UserDatabase
            db = UserDatabase()
            db.authenticate_user(username, password)
            role = db.get_role(username)
            # Return the authenticated db instance so MainWindow can use it
            return db, role

        def on_result(result):
            db, role = result
            self.main_window = MainWindow(username, db, role)
            self.main_window.showMaximized()
            self.close()

        def on_error(msg):
            self.ui.log_in_pushButton.setEnabled(True)
            self.ui.log_in_pushButton.setText("Log In")
            self.ui.username_lineEdit.setEnabled(True)
            self.ui.password_lineEdit.setEnabled(True)
            self.ui.password_lineEdit.clear()
            self.ui.password_lineEdit.setFocus()
            first_line = msg.strip().splitlines()[-1]
            QMessageBox.warning(self, "Login Failed", first_line)

        self._thread, self._relay = run_worker(do_auth, on_result=on_result, on_error=on_error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogInWindow()
    window.show()
    sys.exit(app.exec())