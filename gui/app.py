import tkinter as tk
from tkinter import ttk, messagebox
from core.system import StudentManagementSystem
from gui.screens.login import LoginFrame
from gui.screens.dashboard import DashboardFrame
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
        """Initializes application window and system data."""
        super().__init__()
        self.title("Student Management System")
        self.geometry("1000x700")
        self.resizable(True, True)
        self._system = StudentManagementSystem()
        self.current_user = None
        self.current_frame = None
        self.storage = Storage("students.db")
        self.storage.connect()
        self.storage.create_tables()
        self.storage.load_all(self._system)
        self._role_loaders = {
            "Student": self.load_student_interface,
            "Teacher": self.load_teacher_interface,
        }
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_login()

    def on_close(self):
        """Saves system data and closes application."""
        self.storage.save_all(self._system)
        self.storage.disconnect()
        self.destroy()

    def clear_window(self):
        """Removes current GUI frame."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = None

    def show_login(self):
        """Displays login screen."""
        self.clear_window()
        self.current_frame = LoginFrame(self, self.handle_login, self._system)
        self.current_frame.pack(fill="both", expand=True)

    def handle_login(self, user):
        """Handles successful login using role mapping."""
        self.current_user = user
        loader = self._role_loaders.get(user.get_role())
        if loader:
            loader()
        else:
            messagebox.showerror("Error", "Unknown user role")

    def create_tabs(self):
        """Creates and returns tab container."""
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill="both", expand=True)
        return notebook

    def load_student_interface(self):
        """
        Loads student interface.
        Tabs: Dashboard, Courses, Grades
        """
        self.clear_window()
        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(fill="both", expand=True)
        tabs = self.create_tabs()
        # Dashboard tab — wired to DashboardFrame
        dashboard = DashboardFrame(tabs, self._system, self.current_user)
        tabs.add(dashboard, text="Dashboard")
        courses = ttk.Frame(tabs)
        tabs.add(courses, text="Courses")
        grades = ttk.Frame(tabs)
        tabs.add(grades, text="Grades")

    def load_teacher_interface(self):
        """
        Loads teacher interface.
        Tabs: Dashboard, Students, Courses
        """
        self.clear_window()
        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(fill="both", expand=True)
        tabs = self.create_tabs()
        # Dashboard tab — wired to DashboardFrame
        dashboard = DashboardFrame(tabs, self._system, self.current_user)
        tabs.add(dashboard, text="Dashboard")
        students = ttk.Frame(tabs)
        tabs.add(students, text="Students")
        courses = ttk.Frame(tabs)
        tabs.add(courses, text="Courses")

def main():
    """Starts the application."""
    app = StudentManagementApp()
    app.mainloop()

if __name__ == "__main__":
    main()