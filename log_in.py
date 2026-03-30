import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from ui.ui_login import Ui_LogInWindow
from main import MainWindow
from worker import run_worker


class LogInWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the login window UI and connect user interaction signals.

        Sets up the interface, configures password field behavior,
        connects input events (button click and Enter key),
        and prepares thread references for background authentication.
        """
        super().__init__()

        # Initialize UI from Qt Designer-generated class
        self.ui = Ui_LogInWindow()
        self.ui.setupUi(self)

        # Hide password input characters
        self.ui.password_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect button click and Enter key events to the same login handler
        self.ui.log_in_pushButton.clicked.connect(self.handle_log_in)
        self.ui.username_lineEdit.returnPressed.connect(self.handle_log_in)
        self.ui.password_lineEdit.returnPressed.connect(self.handle_log_in)

        # Keep references to thread and relay to prevent garbage collection
        self._thread = None
        self._relay = None

    def handle_log_in(self):
        """
        Handle login attempt triggered by user interaction.

        Validates input fields, disables the UI to prevent duplicate requests,
        and starts authentication in a background thread.

        On success:
            - Opens the main application window with authenticated user context.

        On failure:
            - Restores UI state and displays an error message.
        """
        # Read user input
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()

        # Basic validation: prevent empty submissions
        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter username and password.")
            return

        # Disable UI to prevent multiple login attempts
        self.ui.log_in_pushButton.setEnabled(False)
        self.ui.log_in_pushButton.setText("Signing in...")
        self.ui.username_lineEdit.setEnabled(False)
        self.ui.password_lineEdit.setEnabled(False)

        # Function that will run in a separate worker thread to keep the UI responsive
        def do_auth():
            """
            Perform authentication logic inside a worker thread.

            Creates a database instance, verifies user credentials,
            and retrieves the user's role.

            Returns:
                tuple: (UserDatabase instance, user role)
            """
            # Import here to ensure it runs inside worker thread
            from models.user import UserDatabase

            db = UserDatabase()

            # Authenticate user (raises exception if fails)
            db.authenticate_user(username, password)

            # Retrieve user role after successful authentication
            role = db.get_role(username)

            # Return db instance so it can be reused in main window
            return db, role

        # Called when worker finishes successfully
        def on_result(result):
            """
            Handle successful authentication result.

            Initializes and displays the main application window,
            passing authenticated user data, then closes login window.

            Args:
                result (tuple): Contains (UserDatabase instance, user role)
            """
            db, role = result

            # Open main application window with authenticated context
            self.main_window = MainWindow(username, db, role) #type: ignore
            self.main_window.showMaximized() #type: ignore

            # Close login window
            self.close()

        # Called when worker raises an error
        def on_error(msg):
            """
            Handle authentication failure.

            Restores UI state, clears sensitive input, and displays
            a simplified error message to the user.

            Args:
                msg (str): Error message returned from worker thread
            """
            # Re-enable UI for retry
            self.ui.log_in_pushButton.setEnabled(True)
            self.ui.log_in_pushButton.setText("Log In")
            self.ui.username_lineEdit.setEnabled(True)
            self.ui.password_lineEdit.setEnabled(True)

            # Clear password for security and focus it for quick retry
            self.ui.password_lineEdit.clear()
            self.ui.password_lineEdit.setFocus()

            # Extract the most relevant part of the error message
            first_line = msg.strip().splitlines()[-1]

            # Show error to user
            QMessageBox.warning(self, "Login Failed", first_line)

        # Run authentication in background thread to keep UI responsive
        self._thread, self._relay = run_worker(
            do_auth,
            on_result=on_result,
            on_error=on_error
        )


if __name__ == "__main__":
    """
    Application entry point.

    Creates the Qt application instance, initializes the login window,
    and starts the event loop.
    """
    # Standard Qt application object
    app = QApplication(sys.argv)

    # Create and show login window
    window = LogInWindow()
    window.show()

    # Start Qt event loop
    sys.exit(app.exec())
