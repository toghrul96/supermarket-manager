import csv 
import os
import re
import bcrypt
from datetime import date

class UserDatabase:
    """Secure user management system with role-based access control and password hashing."""
    
    def __init__(self, filename):
        """
        Initialize the user database with file storage and predefined roles.

        Args:
            filename (str): The path to the CSV file for user data storage.
        """
        self.filename = filename
        # Define CSV structure for consistent user records
        self.fieldnames = ["Username", "Password", "Role", "Created At"]
        # Predefined roles enforce access control hierarchy
        self.roles = ["Admin", "Manager", "Cashier"]

        # Ensure the folder exists before file creation
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        # Initialize data file with headers if missing
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
            # Add default user
            default_user = UserValidator("dev54321", "dev54321")
            created_at = date.today().strftime("%d/%m/%Y")
            self.__save_user(default_user, "Admin", created_at)

    def add_user(self, username, password, role):
        """
        Securely register a new user with input validation and password hashing.

        Args:
            username (str): Desired username for the new account.
            password (str): Raw password string to be hashed and stored securely.
            role (str): Role assigned to the user; must be one of predefined roles.
        """
        # Validate credentials and normalize inputs
        user = UserValidator(username, password)
        role = role.capitalize()  # Standardize role capitalization

        # Enforce role-based access control
        if role not in self.roles:
            raise ValueError(f"Invalid role: '{role}'. Must be one of: {', '.join(self.roles)}")

        # Prevent duplicate accounts
        if self.username_exist(user.username):
            raise ValueError("Username already taken")
        
        # Record account creation date for auditing
        created_at = date.today().strftime("%d/%m/%Y")
    
        # Securely store user credentials
        self.__save_user(user, role, created_at)

    def update_user(self, username, new_password, new_role):
        """
        Update credentials and role of an existing user with validation.

        Args:
            username (str): Username of the user to update.
            new_password (str): New password to hash and store.
            new_role (str): New role to assign to the user.
        """
        updated = False  # Track mutation success
        # Re-validate credentials even for updates
        user = UserValidator(username, new_password)

        # Read all users for in-memory update
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            users = list(reader)

            # Locate and update user record
            for row in users:
                if row.get("Username") == username:
                    row["Password"] = user.password  # Store newly hashed password
                    row["Role"] = new_role  # Update permissions
                    updated = True

        if not updated:
            raise ValueError(f"User '{username}' not found.")

        # Atomic write operation prevents corruption
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writeheader()
            writer.writerows(users)

    def search(self, keyword):
        """
        Search users by username prefix, case-insensitive.

        Args:
            keyword (str): Partial username to search for.
        """
        keyword = keyword.lower()
        matched_users = []

        with open(self.filename, "r", newline="") as file:
            reader = csv.reader(file)
            users = list(reader)[1:]  # Skip header

            # Simple prefix matching for responsive UI
            for row in users:
                if row[0].startswith(keyword):
                    matched_users.append(row)

        return matched_users

    def delete(self, username):
        """
        Delete a user account by username, removing all associated data.

        Args:
            username (str): Username of the account to delete.
        """
        # Filter out target user while reading
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            users = [row for row in reader if row.get("Username") != username]

        # Rewrite remaining users
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(users)

    def authenticate_user(self, username_input, password_input):
        """
        Verify user credentials securely using bcrypt hashing.

        Args:
            username_input (str): Username entered by the user.
            password_input (str): Raw password entered by the user.

        Returns:
            bool: True if authentication succeeds.
        """
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("Username") == username_input:             
                    # Constant-time comparison prevents timing attacks
                    if bcrypt.checkpw(password_input.encode(), row["Password"].encode()):
                        return True
                    else:
                        raise ValueError("Incorrect password.")
            # Generic error prevents username enumeration
            raise ValueError("Username does not exist.")

    def username_exist(self, username):
        """
        Check if a username already exists in the user database.

        Args:
            username (str): Username to check.

        Returns:
            bool: True if username exists, False otherwise.
        """
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("Username") == username:
                    return True       
        return False

    def __save_user(self, user, role, creation_date):
        """
        Save a new user record securely to the CSV file.

        Args:
            user (UserValidator): Validated user object with hashed password.
            role (str): User role to assign.
            creation_date (str): Date string when the user was created.
        """
        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writerow({
                "Username": user.username, 
                "Password": user.password,  # Already hashed
                "Role": role, 
                "Created At": creation_date
            })

    def count_users(self, role=None):
        """
        Count users in the database, optionally filtered by role.

        Args:
            role (str, optional): Role to filter by (case-insensitive). Counts all users if None.

        Returns:
            int: Number of users matching the criteria.
        """
        total = 0
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not role:  # Total user count
                    total += 1
                elif row.get("Role").lower() == role.lower():  # type: ignore
                    total += 1
        return total

    def get_role(self, username):
        """
        Retrieve the role assigned to a given username.

        Args:
            username (str): Username whose role is requested.

        Returns:
            str or None: Role string if found, otherwise None.
        """
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"].strip().lower() == username.strip().lower():
                    return row["Role"]


class UserValidator:
    """Utility class for validating user credentials and securely hashing passwords."""
    
    def __init__(self, username, password):
        """
        Initialize validator by setting username and password with validation.

        Args:
            username (str): The username to validate and store.
            password (str): The raw password to validate and hash securely.
        """
        self.username = username  # Triggers @username.setter
        self.password = password  # Triggers @password.setter

    @property
    def username(self):
        """
        Get the validated and normalized username.

        Returns:
            str: The username in lowercase.
        """
        return self.__username

    @username.setter
    def username(self, value):
        """
        Validate and set the username.

        Enforces allowed characters (letters, numbers, underscores, hyphens),
        minimum length 3, and maximum length 20. Normalizes to lowercase.

        Args:
            value (str): The username to validate and set.
        """
        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise ValueError("Username can only contain letters, numbers, underscores, or hyphens.")
        elif len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        elif len(value) > 20:
            raise ValueError("Username cannot be longer than 20 characters")
        
        self.__username = value.lower()  # Normalize case

    @property
    def password(self):
        """
        Get the hashed password string.

        Returns:
            str: The bcrypt hashed password.
        """
        return self.__password

    @password.setter
    def password(self, value):
        """
        Validate and hash the password.

        Enforces minimum length 4 and maximum length 64.
        Uses bcrypt with automatic salting for secure hashing.

        Args:
            value (str): The raw password to validate and hash.
        """
        if len(value) < 4:
            raise ValueError("Password must be at least 4 characters long.")
        elif len(value) > 64:
            raise ValueError("Password cannot be longer than 64 characters.")
        
        # Salted hashing protects against rainbow tables
        hashed = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        self.__password = hashed.decode()  # Store as string