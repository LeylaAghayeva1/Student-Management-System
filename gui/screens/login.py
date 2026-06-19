import tkinter as tk
from tkinter import ttk, messagebox
class LoginFrame(tk.Frame):
    """
    Login screen for the Student Management System.
    Allows users to:
    - Enter name
    - Select role
    - Login
    After successful login,
    sends the real user object
    back to the application.
    """
    def __init__(self, parent, login_callback, system):
        """
        Initializes login screen.
        Args:
            parent:
                Parent tkinter widget.
            login_callback:
                Function called after successful login.
            system:
                StudentManagementSystem instance.
        """
        super().__init__(parent)
        self._login_callback = login_callback
        self._system = system
        ttk.Label(
            self,
            text="Name:"
        ).pack(pady=5)
        self._name_entry = ttk.Entry(
            self,
            width=30
        )
        self._name_entry.pack(
            pady=5
        )
        ttk.Label(
            self,
            text="Role:"
        ).pack(pady=5)
        self._role_var = tk.StringVar()
        self._role_dropdown = ttk.Combobox(
            self,
            textvariable=self._role_var,
            state="readonly",
            values=self._system.get_available_roles()
        )
        self._role_dropdown.pack(
            pady=5
        )
        ttk.Button(
            self,
            text="Login",
            command=self.login
        ).pack(
            pady=15
        )
        
    def login(self):
        """
        Validates login information.
        Checks:
        - Name is not empty
        - Role is selected
        - User exists
        Complexity:
        O(n)
        """
        name = self._name_entry.get().strip()
        role = self._role_var.get()
        if not name:
            messagebox.showerror(
                "Login Error",
                "Name cannot be empty"
            )
            return
        if not role:
            messagebox.showerror(
                "Login Error",
                "Please select a role"
            )
            return
        user = self.find_user(
            name,
            role
        )
        if user is None:
            messagebox.showerror(
                "Login Error",
                "User not found"
            )
            return
        self._login_callback(user)

    def find_user(self, name: str, role: str):
        """
        Searches all available users.
        Matches:
        - name
        - role
        Returns:
            User object if found.
            None otherwise.
        Complexity:
            O(n)
        """
        users = (
            self._system.get_all_students()
            +
            self._system.get_all_teachers()
        )
        for user in users:
            if (
                user.get_name().lower() == name.lower()
                and
                user.get_role() == role
            ):
                return user
        return None