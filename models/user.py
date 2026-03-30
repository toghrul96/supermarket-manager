import os
import re
from datetime import date
from dotenv import load_dotenv
from supabase import create_client

class UserDatabase:
    """Manages users securely with role-based access and Supabase integration."""

    def __init__(self):
        """Initialize Supabase connection and thread-local storage."""
        import threading
        load_dotenv()
        
        self._url = os.getenv("SUPABASE_URL")
        self._key = os.getenv("SUPABASE_KEY")
        if not self._url or not self._key:
            raise ValueError("Missing Supabase credentials in .env file")
        
        # Store tokens after authentication for thread-local clients
        self._access_token = None
        self._refresh_token = None

        # Each thread gets its own Supabase client to avoid pool corruption
        self._local = threading.local()

        # Predefined roles for access control
        self.roles = ["Admin", "Manager", "Cashier"]

    @property
    def supabase(self):
        """Return a thread-local Supabase client; create if missing."""
        if not hasattr(self._local, 'client'):
            client = create_client(self._url, self._key) #type: ignore
            # Propagate auth session to allow authenticated requests
            if self._access_token and self._refresh_token:
                try:
                    client.auth.set_session(self._access_token, self._refresh_token)
                except Exception:
                    pass
            self._local.client = client
        return self._local.client
       
    def add_user(self, username, password, role):
        """
        Register a new user with validation and role assignment.

        Converts username to email format for Supabase Auth and inserts into
        users table with role info.
        """
        user = UserValidator(username, password)
        role = role.capitalize()

        if role not in self.roles:
            raise ValueError(f"Invalid role: '{role}'. Must be one of: {', '.join(self.roles)}")

        email = f"{user.username}@supermarket.local"

        # Check for duplicates
        try:
            response = self.supabase.table("users").select("username").eq("username", user.username).execute()
            if response.data:
                raise ValueError("Username already taken")
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to check username: {str(e)}")
        
        try:
            # Save current admin session
            admin_session = self.supabase.auth.get_session()
            if not admin_session:
                raise ValueError("No admin session found - please log in again")
            
            # Create user in Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {"username": user.username}}
            })
            if not auth_response.user:
                raise ValueError("Failed to create auth user")
            new_user_id = auth_response.user.id
            
            # Restore admin session
            self.supabase.auth.set_session(admin_session.access_token, admin_session.refresh_token)
            
            # Insert user with role into table
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
                raise ValueError("Username already taken (contact admin)")
            raise ValueError(f"Failed to create user: {str(e)}")

    def update_user(self, username, new_password, new_role):
        """Update password and role of an existing user with validation."""
        user = UserValidator(username, new_password)
        new_role = new_role.capitalize()

        if new_role not in self.roles:
            raise ValueError(f"Invalid role: '{new_role}'. Must be one of: {', '.join(self.roles)}")

        try:
            result = self.supabase.table("users").update({"role": new_role.lower()}).eq("username", username).execute()
            if not result.data:
                raise ValueError(f"User '{username}' not found.")
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to update user: {str(e)}")

    def search(self, keyword):
        """Return list of users whose username starts with keyword (case-insensitive)."""
        try:
            response = self.supabase.table("users").select("username, role, created_at").ilike("username", f"{keyword}%").execute()
            return [[row.get("username"), row.get("role"), row.get("created_at")] for row in (response.data or []) if isinstance(row, dict)]
        except Exception as e:
            raise ValueError(f"Search failed: {str(e)}")

    def delete(self, username):
        """Delete user by username."""
        try:
            username_norm = username.strip().lower()
            result = self.supabase.table("users").delete().eq("username", username_norm).execute()
            if not result.data:
                raise ValueError(f"User '{username}' not found.")
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to delete user: {str(e)}")

    def authenticate_user(self, username_input, password_input):
        """Authenticate user using Supabase Auth and save session tokens."""
        try:
            username_input = username_input.lower().strip()
            password_input = password_input.strip()
            email = f"{username_input}@supermarket.local"
            auth_response = self.supabase.auth.sign_in_with_password({"email": email, "password": password_input})
            if not auth_response.user:
                raise ValueError("Login failed")
            if not auth_response.session:
                raise ValueError("No session returned")

            # Store session for thread-local clients
            self._access_token = auth_response.session.access_token
            self._refresh_token = auth_response.session.refresh_token
            self._local.client = getattr(self._local, 'client', create_client(self._url, self._key)) #type: ignore

            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "invalid login" in error_msg or "invalid credentials" in error_msg:
                raise ValueError("Invalid username or password.")
            elif "email not confirmed" in error_msg:
                raise ValueError("Account not confirmed. Contact admin.")
            else:
                raise ValueError(f"Login error: {str(e)}")

    def username_exist(self, username):
        """Return True if username exists, False otherwise."""
        try:
            username_norm = username.strip().lower()
            response = self.supabase.table("users").select("username").eq("username", username_norm).execute()
            return bool(response.data)
        except Exception as e:
            raise ValueError(f"Failed to check username existence: {str(e)}")

    def count_users(self, role=None):
        """Count users, optionally filtered by role."""
        try:
            if role:
                role_norm = role.strip().lower()
                response = self.supabase.table("users").select("username", count="exact").eq("role", role_norm).execute() #type: ignore
            else:
                response = self.supabase.table("users").select("username", count="exact").execute() #type: ignore
            return response.count or 0
        except Exception as e:
            raise ValueError(f"Failed to count users: {str(e)}")

    def get_role(self, username):
        """Return role of given username, or None if not found."""
        try:
            username_norm = username.strip().lower()
            response = self.supabase.table("users").select("role").eq("username", username_norm).execute()
            if response.data and isinstance(response.data[0], dict):
                return str(response.data[0].get("role")) #type: ignore
            return None
        except Exception as e:
            raise ValueError(f"Failed to retrieve user role: {str(e)}")


class UserValidator:
    """Validate username and password for correctness and constraints."""

    def __init__(self, username, password):
        """Set username and password with validation."""
        self.username = username
        self.password = password

    @property
    def username(self):
        """Return normalized username (lowercase)."""
        return self.__username

    @username.setter
    def username(self, value):
        """Validate allowed characters and length for username."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise ValueError("Username can only contain letters, numbers, underscores, or hyphens.")
        elif len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        elif len(value) > 20:
            raise ValueError("Username cannot be longer than 20 characters")
        self.__username = value.lower()

    @property
    def password(self):
        """Return password (handled securely by Supabase)."""
        return self.__password

    @password.setter
    def password(self, value):
        """Validate password length."""
        if len(value) < 4:
            raise ValueError("Password must be at least 4 characters long.")
        elif len(value) > 64:
            raise ValueError("Password cannot be longer than 64 characters.")
        self.__password = value