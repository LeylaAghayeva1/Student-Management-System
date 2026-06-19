import tkinter as tk
from tkinter import ttk
class DashboardFrame(tk.Frame):
    """
    Main dashboard screen.
    Displays:
    - Welcome message
    - Current user role
    - System summary cards
    - Role-specific information
    Business calculations are handled by
    StudentManagementSystem.
    Complexity:
        O(n) during initialization because
        summary information may require counting.
    """
    def __init__(self, parent, system, user):
        """
        Initializes dashboard.
        Args:
            parent:
                Parent tkinter widget.
            system:
                StudentManagementSystem instance.
            user:
                Currently logged-in user.
        """
        super().__init__(parent)
        self._system = system
        self._user = user
        # Role -> section mapping
        self._role_sections = {
            "Student":
                self.create_student_section
        }
        self.create_header()
        self.create_summary_cards()
        self.load_role_section()
        
    def load_role_section(self):
        """
        Loads dashboard section depending on user role.
        Avoids hardcoding role checks.
        Complexity:
            O(1)
        """
        role = self._user.get_role()
        section = self._role_sections.get(role)
        if section:
            section()

    def create_header(self):
        """
        Creates dashboard header.
        Shows:
        - User name
        - User role
        Complexity:
            O(1)
        """
        ttk.Label(
            self,
            text=f"Welcome, {self._user.get_name()}",
            font=("Arial", 18)
        ).pack(
            pady=10
        )
        ttk.Label(
            self,
            text=f"Role: {self._user.get_role()}"
        ).pack(
            pady=5
        )

    def create_summary_cards(self):
        """
        Creates system summary cards.
        Displays:
        - Total students
        - Total courses
        - Total grades
        - Average GPA
        Complexity:
            O(n)
        """
        container = ttk.Frame(self)
        container.pack(
            pady=20
        )
        self.create_card(
            container,
            "Students",
            len(self._system.get_all_students())
        )
        self.create_card(
            container,
            "Courses",
            len(self._system.get_all_courses())
        )
        self.create_card(
            container,
            "Grades",
            len(self._system.get_all_grades())
        )
        self.create_card(
            container,
            "Average GPA",
            round(
                self.calculate_average_gpa(),
                2
            )
        )

    def create_card(self, parent, title, value):
        """
        Creates one dashboard card.
        Complexity:
            O(1)
        """
        card = ttk.Frame(
            parent,
            relief="solid",
            borderwidth=1
        )
        card.pack(
            side="left",
            padx=10,
            ipadx=20,
            ipady=10
        )
        ttk.Label(
            card,
            text=title
        ).pack()
        ttk.Label(
            card,
            text=str(value),
            font=("Arial", 16)
        ).pack()

    def calculate_average_gpa(self):
        """
        Calculates average GPA of all students.
        Complexity:
            O(n)
        """
        students = self._system.get_all_students()
        if not students:
            return 0
        total = 0
        for student in students:
            total += self._system.calculate_gpa(
                student.get_id()
            )
        return total / len(students)

    def create_student_section(self):
        """
        Displays student-specific information.
        Shows:
        - Own GPA
        - Own grades
        - Course names
        Complexity:
            O(n)
        """
        frame = ttk.Frame(self)
        frame.pack(
            fill="both",
            expand=True,
            pady=20
        )
        student_id = self._user.get_id()
        ttk.Label(
            frame,
            text=f"My GPA: {round(self._system.calculate_gpa(student_id),2)}",
            font=("Arial",14)
        ).pack(
            pady=10
        )
        ttk.Label(
            frame,
            text="My Grades",
            font=("Arial",14)
        ).pack()
        grades = self._system.get_student_grades(
            student_id
        )
        if not grades:
            ttk.Label(
                frame,
                text="No grades available"
            ).pack()
            return
        for grade in grades:
            course = self._system.get_course(
                grade.get_course_crn()
            )
            course_name = (
                course.get_name()
                if course
                else str(grade.get_course_crn())
            )
            ttk.Label(
                frame,
                text=(
                    f"{course_name} | "
                    f"Score: {grade.get_score()} | "
                    f"Grade: {grade.get_letter_grade()}"
                )
            ).pack(
                pady=3
            )