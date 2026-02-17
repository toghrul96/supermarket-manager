import os
import re
import bcrypt
from datetime import date
from dotenv import load_dotenv
from supabase import create_client

class UserDatabase():
    """Secure user management system with role-based access control and password hashing."""
    
    def __init__(self, filename=None):
        """Initialize user database with Supabase connection."""
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Missing Supabase credentials in .env file")
        
        # Initialize Supabase client for auth and data operations
        self.supabase = create_client(supabase_url, supabase_key)
        
        # Predefined roles enforce access control hierarchy
        self.roles = ["Admin", "Manager", "Cashier"]
       
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
        role = role.capitalize()

        # Enforce role-based access control
        if role not in self.roles:
            raise ValueError(f"Invalid role: '{role}'. Must be one of: {', '.join(self.roles)}")

        # Convert username to email format for Supabase Auth
        # Users only see/use usernames, email is internal requirement
        email = f"{user.username}@supermarket.local"

        # Prevent duplicate accounts
        try:
            response = self.supabase.table("users").select("username").eq(
                "username", user.username
            ).execute()
            if response.data and len(response.data) > 0:
                raise ValueError("Username already taken")
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to check username: {str(e)}")
        
        try:
            # Save current admin session before creating new user
            # sign_up() temporarily switches to new user's session
            admin_session = self.supabase.auth.get_session()
            if not admin_session:
                raise ValueError("No admin session found - please log in again")
            
            # Create user in Supabase Auth (handles password hashing)
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": user.username
                    }
                }
            })
            
            if not auth_response.user:
                raise ValueError("Failed to create auth user")
            
            new_user_id = auth_response.user.id
            
            # Restore admin session immediately after user creation
            # This ensures the INSERT operation runs with admin privileges
            self.supabase.auth.set_session(
                admin_session.access_token,
                admin_session.refresh_token
            )
            
            # Insert user into custom users table with role information
            self.supabase.table("users").insert({
                "id": new_user_id,
                "username": user.username,
                "role": role.lower(),
            }).execute()
            
        except ValueError:
            raise
        except Exception as e:
            error_msg = str(e).lower()
            if "already registered" in error_msg or "user already registered" in error_msg:
                raise ValueError("Username already taken (please contact admin to resolve)")
            raise ValueError(f"Failed to create user: {str(e)}")

    def update_user(self, username, new_password, new_role):
        """
        Update credentials and role of an existing user with validation.

        Args:
            username (str): Username of the user to update.
            new_password (str): New password to hash and store.
            new_role (str): New role to assign to the user.
        """
        # Re-validate credentials for updates
        user = UserValidator(username, new_password)
        new_role = new_role.capitalize()

        # Enforce role-based access control
        if new_role not in self.roles:
            raise ValueError(f"Invalid role: '{new_role}'. Must be one of: {', '.join(self.roles)}")

        try:
            # Update role in Supabase users table
            result = self.supabase.table("users").update({
                "role": new_role.lower()
            }).eq("username", username).execute()

            # Check if user was found and updated
            if not result.data:
                raise ValueError(f"User '{username}' not found.")

        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to update user: {str(e)}")

    def search(self, keyword):
        """
        Search users by username prefix, case-insensitive.

        Args:
            keyword (str): Partial username to search for.

        Returns:
            list: List of matching user records as lists.
        """
        try:
            # Query Supabase for users matching the keyword prefix
            response = self.supabase.table("users").select("*").ilike(
                "username", f"{keyword}%"
            ).execute()

            # Convert each row dict to a list for UI compatibility
            result = []
            for row in (response.data or []):
                if isinstance(row, dict):  # Type guard for Pylance
                    result.append(list(row.values()))
            return result

        except Exception as e:
            raise ValueError(f"Search failed: {str(e)}")

    def delete(self, username):
        """
        Delete a user account by username.

        Args:
            username (str): Username of the account to delete.
        """
        try:
            # Normalize username to match stored format
            username_norm = username.strip().lower()

            # Delete user from Supabase users table
            result = self.supabase.table("users").delete().eq(
                "username", username_norm
            ).execute()

            # If no row is returned, the user does not exist
            if not result.data:
                raise ValueError(f"User '{username}' not found.")

        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to delete user: {str(e)}")

    def authenticate_user(self, username_input, password_input):
        """
        Verify user credentials using Supabase Auth.

        Args:
            username_input (str): Username entered by the user.
            password_input (str): Raw password entered by the user.

        Returns:
            bool: True if authentication succeeds.
        """
        try:
            # Normalize username to lowercase and remove whitespace
            username_input = username_input.lower().strip()
            
            # Convert username to email format for Supabase Auth
            # Users only see/use usernames, email is internal requirement
            email = f"{username_input}@supermarket.local"
            
            # Authenticate with Supabase Auth
            # Supabase handles secure password comparison and session creation
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password_input
            })
            
            # Verify authentication was successful
            if not auth_response.user:
                raise ValueError("Login failed")
            
            # Verify session was created (required for subsequent authenticated requests)
            if not auth_response.session:
                raise ValueError("No session returned from authentication")
            
            return True
            
        except Exception as e:
            error_msg = str(e).lower()
            if "invalid login" in error_msg or "invalid credentials" in error_msg:
                raise ValueError("Incorrect password.")
            elif "email not confirmed" in error_msg:
                raise ValueError("Account not confirmed. Contact your administrator.")
            else:
                raise ValueError(f"Login error: {str(e)}")

    def username_exist(self, username):
        """
        Check whether a username already exists in the database.

        Args:
            username (str): Username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        try:
            # Normalize username to match stored format
            username_norm = username.strip().lower()

            # Query Supabase for the username
            response = self.supabase.table("users").select("username").eq(
                "username", username_norm
            ).execute()

            # Return True if any row is found
            return bool(response.data)

        except Exception as e:
            raise ValueError(f"Failed to check username existence: {str(e)}")

    def count_users(self, role=None):
        """
        Count users in the database, optionally filtered by role.

        Args:
            role (str, optional): Role to filter by (case-insensitive).
                                  If None, counts all users.

        Returns:
            int: Number of users matching the criteria.
        """
        try:
            if role:
                # Normalize role to match stored format
                role_norm = role.strip().lower()

                # Count users filtered by role
                response = self.supabase.table("users").select(
                    "username", count="exact" # type: ignore
                ).eq("role", role_norm).execute()
            else:
                # Count all users
                response = self.supabase.table("users").select(
                    "username", count="exact" # type: ignore
                ).execute()

            # Return count from Supabase response
            return response.count or 0

        except Exception as e:
            raise ValueError(f"Failed to count users: {str(e)}")

    def get_role(self, username):
        """
        Retrieve the role assigned to a given username.

        Args:
            username (str): Username whose role is requested.

        Returns:
            str or None: Role string if found, otherwise None.
        """
        try:
            # Normalize username to match stored format
            username_norm = username.strip().lower()

            # Query role for the given username
            response = self.supabase.table("users").select("role").eq(
                "username", username_norm
            ).execute()

            # Return role if user exists
            if response.data and isinstance(response.data[0], dict):
                return str(response.data[0].get("role"))

            return None

        except Exception as e:
            raise ValueError(f"Failed to retrieve user role: {str(e)}")


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