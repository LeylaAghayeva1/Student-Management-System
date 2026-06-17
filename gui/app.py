import tkinter as tk
from tkinter import ttk, messagebox
from core.system import StudentManagementSystem
from gui.screens.login import LoginFrame
from data.storage import Storage
class StudentManagementApp(tk.Tk):
    """
    Main application window.
    Responsibilities:
    - Launch application
    - Load saved data
    - Display login screen
    - Handle authentication
    - Load role-based interfaces
    - Save data before closing
    GUI layer does not contain business logic.
    """
    def __init__(self):
        """
        Initializes application window and system data.
        """
        super().__init__()
        self.title(
            "Student Management System"
        )
        self.geometry(
            "1000x700"
        )
        self.resizable(
            True,
            True
        )
        # Backend system
        self.system = StudentManagementSystem()
        # Current logged user
        self.current_user = None
        # Current GUI frame
        self.current_frame = None
        # Storage MUST be initialized before login
        self.storage = Storage(
            "students.db"
        )
        self.storage.connect()
        self.storage.create_tables()
        self.storage.load_all(
            self.system
        )
        # Role -> interface mapping
        self._role_loaders = {
            "Student":
                self.load_student_interface,
            "Teacher":
                self.load_teacher_interface,
            "Admin":
                self.load_admin_interface
        }
        # Save before closing
        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )
        # Show login after data is loaded
        self.show_login()

    def on_close(self):
        """
        Saves system data and closes application.
        Complexity:
        O(n)
        """
        self.storage.save_all(
            self.system
        )
        self.storage.disconnect()
        self.destroy()

    def clear_window(self):
        """
        Removes current GUI frame.
        Complexity:
        O(1)
        """
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        """
        Displays login screen.
        Successful login loads
        the correct dashboard.
        """
        self.clear_window()
        self.current_frame = LoginFrame(
            self,
            self.handle_login
        )
        self.current_frame.pack(
            fill="both",
            expand=True
        )

    def handle_login(self, user):
        """
        Handles successful login.
        Uses role mapping to select
        correct interface.
        Args:
            user:
                Logged-in user object.
        Complexity:
        O(1)
        """
        self.current_user = user
        role = user.get_role()
        loader = self._role_loaders.get(
            role
        )
        if loader:
            loader()
        else:
            messagebox.showerror(
                "Error",
                "Unknown user role"
            )

    def create_tabs(self):
        """
        Creates tab container.
        Returns:
            ttk.Notebook object.
        Complexity:
        O(1)
        """
        notebook = ttk.Notebook(
            self.current_frame
        )
        notebook.pack(
            fill="both",
            expand=True
        )
        return notebook

    def load_student_interface(self):
        """
        Loads student dashboard.
        Tabs:
        - Profile
        - Courses
        - Grades
        """
        self.clear_window()
        self.current_frame = ttk.Frame(
            self
        )
        self.current_frame.pack(
            fill="both",
            expand=True
        )
        tabs = self.create_tabs()
        profile = ttk.Frame(tabs)
        courses = ttk.Frame(tabs)
        grades = ttk.Frame(tabs)
        tabs.add(
            profile,
            text="Profile"
        )
        tabs.add(
            courses,
            text="Courses"
        )
        tabs.add(
            grades,
            text="Grades"
        )

    def load_teacher_interface(self):
        """
        Loads teacher dashboard.
        Tabs:
        - Profile
        - Courses
        - Students
        """
        self.clear_window()
        self.current_frame = ttk.Frame(
            self
        )
        self.current_frame.pack(
            fill="both",
            expand=True
        )
        tabs = self.create_tabs()
        profile = ttk.Frame(tabs)
        courses = ttk.Frame(tabs)
        students = ttk.Frame(tabs)
        tabs.add(
            profile,
            text="Profile"
        )
        tabs.add(
            courses,
            text="Courses"
        )
        tabs.add(
            students,
            text="Students"
        )

    def load_admin_interface(self):
        """
        Loads administrator dashboard.
        Admin manages:
        - Students
        - Teachers
        - Courses
        - Grades
        """
        self.clear_window()
        self.current_frame = ttk.Frame(
            self
        )
        self.current_frame.pack(
            fill="both",
            expand=True
        )
        tabs = self.create_tabs()
        students = ttk.Frame(tabs)
        teachers = ttk.Frame(tabs)
        courses = ttk.Frame(tabs)
        grades = ttk.Frame(tabs)
        tabs.add(
            students,
            text="Students"
        )
        tabs.add(
            teachers,
            text="Teachers"
        )
        tabs.add(
            courses,
            text="Courses"
        )
        tabs.add(
            grades,
            text="Grades"
        )

def main():
    """
    Starts the application.
    """
    app = StudentManagementApp()
    app.mainloop()

if __name__ == "__main__":
    main()