import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from ui.ui_login import Ui_LogInWindow
from models.user import UserDatabase
from main import MainWindow

USER_DATA = "data/user_data.csv"

class LogInWindow(QMainWindow):
    """
    Main login window for the application.

    Handles user authentication through UI inputs, displays error messages on failure,
    and launches the main application window upon successful login.
    """

    def __init__(self):
        """
        Initialize the login window, setup UI components, and connect input events.
        """
        super().__init__()
        self.user_data = UserDatabase(USER_DATA)

        # Load and set up the UI
        self.ui = Ui_LogInWindow()
        self.ui.setupUi(self)

        # Hide characters in password field for security
        self.ui.password_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect login button and Enter key press events to login handler
        self.ui.log_in_pushButton.clicked.connect(self.handle_log_in)
        self.ui.username_lineEdit.returnPressed.connect(self.handle_log_in)
        self.ui.password_lineEdit.returnPressed.connect(self.handle_log_in)

    def handle_log_in(self):
        """
        Handle user login attempt by validating credentials.

        Retrieves input from username and password fields, then calls authentication logic.
        If successful, launches the main window. Otherwise, shows a warning message.
        """
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()  # Raw password input

        try:
            # Delegate authentication logic to UserDatabase
            if self.user_data.authenticate_user(username, password):
                # If valid: open main window and close login screen
                self.main_window = MainWindow(username)
                self.main_window.showMaximized()
                self.close()
        except ValueError as e:
            # Show error if login credentials are incorrect
            QMessageBox.warning(self, "Login Failed", str(e))

if __name__ == "__main__":
    # Entry point: create app and show login window
    app = QApplication(sys.argv)
    window = LogInWindow()
    window.show()
    sys.exit(app.exec())
