import tkinter as tk
from tkinter import ttk, messagebox
import random
from models.course import Course
from models.grade import Grade
class CoursesFrame(tk.Frame):
    """
    Course management screen.
    Features:
    - Display courses
    - Add courses
    - Edit courses
    - Delete courses
    - View course grades
    - Add grades
    GUI handles only input/display.
    Business logic remains in StudentManagementSystem.
    """
    def __init__(self, parent, system):
        """
        Initializes courses screen.
        Args:
            parent:
                Parent tkinter widget.
            system:
                StudentManagementSystem instance.
        Complexity:
            O(n)
        """
        super().__init__(parent)
        self._system = system
        # Stores real Course objects.
        # Avoids depending on displayed values.
        self._course_map = {}
        self.create_course_table()
        self.create_buttons()
        self.create_grade_section()
        self.load_courses()
        
    def create_course_table(self):
        """
        Creates course Treeview.
        Columns:
        - CRN
        - Name
        - Teacher
        - Capacity
        - Credits
        Complexity:
            O(1)
        """
        columns = (
            "CRN",
            "Name",
            "Teacher",
            "Capacity",
            "Credits"
        )
        self.course_table = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.course_table.heading(
                col,
                text=col
            )
            self.course_table.column(
                col,
                width=120
            )
        self.course_table.pack(
            fill="both",
            expand=True,
            pady=10
        )
        
    def create_buttons(self):
        """
        Creates CRUD buttons.
        Complexity:
            O(1)
        """
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        ttk.Button(
            frame,
            text="Add",
            command=self.add_course
        ).pack(
            side="left",
            padx=5
        )
        ttk.Button(
            frame,
            text="Edit",
            command=self.edit_course
        ).pack(
            side="left",
            padx=5
        )
        ttk.Button(
            frame,
            text="Delete",
            command=self.delete_course
        ).pack(
            side="left",
            padx=5
        )

    def load_courses(self):
        """
        Loads courses into table.
        Complexity:
            O(n)
        """
        self.course_table.delete(
            *self.course_table.get_children()
        )
        self._course_map.clear()
        for course in self._system.get_all_courses():
            teacher = self._system.get_teacher(
                course.get_teacher_id()
            )
            teacher_name = (
                teacher.get_name()
                if teacher
                else "Unknown"
            )
            row = self.course_table.insert(
                "",
                "end",
                values=(
                    course.get_crn(),
                    course.get_name(),
                    teacher_name,
                    course.get_max_capacity(),
                    course.get_credits()
                )
            )
            self._course_map[row] = course

    def add_course(self):
        """
        Opens add course popup.
        Complexity:
            O(1)
        """
        self.course_form()

    def edit_course(self):
        """
        Opens edit course popup.
        Complexity:
            O(1)
        """
        selected = self.course_table.selection()
        if not selected:
            messagebox.showerror(
                "Error",
                "Select course first"
            )
            return
        course = self._course_map[
            selected[0]
        ]
        self.course_form(course)

    def delete_course(self):
        """
        Deletes selected course.
        Complexity:
            O(1)
        """
        selected = self.course_table.selection()
        if not selected:
            messagebox.showerror(
                "Error",
                "Select course first"
            )
            return
        course = self._course_map[
            selected[0]
        ]
        if messagebox.askyesno(
            "Delete",
            "Delete this course?"
        ):
            self._system.delete_course(
                course.get_crn()
            )
            self.load_courses()

    def course_form(self, course=None):
        """
        Creates add/edit course popup.
        Complexity:
            O(1)
        """
        window = tk.Toplevel(self)
        labels = [
            "Name",
            "Teacher ID",
            "Capacity",
            "Credits"
        ]
        entries = {}
        for label in labels:
            ttk.Label(
                window,
                text=label
            ).pack()
            entry = ttk.Entry(window)
            entry.pack()
            entries[label] = entry
        if course:
            entries["Name"].insert(
                0,
                course.get_name()
            )
            entries["Teacher ID"].insert(
                0,
                course.get_teacher_id()
            )
            entries["Capacity"].insert(
                0,
                course.get_max_capacity()
            )
            entries["Credits"].insert(
                0,
                course.get_credits()
            )

        def save():
            name = entries["Name"].get()
            try:
                teacher_id = int(
                    entries["Teacher ID"].get()
                )
                capacity = int(
                    entries["Capacity"].get()
                )
                credits = int(
                    entries["Credits"].get()
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Numbers must be valid"
                )
                return
            if course:
                self._system.update_course(
                    course.get_crn(),
                    name,
                    teacher_id,
                    set(),
                    capacity,
                    credits
                )
            else:
                crn = random.randint(
                    1000,
                    9999
                )
                new_course = Course(
                    crn,
                    name,
                    teacher_id,
                    set(),
                    capacity,
                    credits
                )
                self._system.add_course(
                    new_course
                )
            window.destroy()
            self.load_courses()
        ttk.Button(
            window,
            text="Save",
            command=save
        ).pack(
            pady=10
        )

    # ================= GRADES =================

    def create_grade_section(self):
        """
        Creates grade management section.
        Complexity:
            O(1)
        """
        frame = ttk.LabelFrame(
            self,
            text="Course Grades"
        )
        frame.pack(
            fill="both",
            expand=True
        )
        self.grade_text = tk.Text(
            frame,
            height=8
        )
        self.grade_text.pack(
            fill="both",
            expand=True
        )
        ttk.Button(
            frame,
            text="Show Grades",
            command=self.show_course_grades
        ).pack(
            pady=5
        )
        ttk.Button(
            frame,
            text="Add Grade",
            command=self.add_grade_popup
        ).pack(
            pady=5
        )

    def show_course_grades(self):
        """
        Displays grades of selected course.
        Complexity:
            O(n)
        """
        selected = self.course_table.selection()
        if not selected:
            return
        course = self._course_map[
            selected[0]
        ]
        self.grade_text.delete(
            "1.0",
            tk.END
        )
        grades = self._system.get_course_grades(
            course.get_crn()
        )
        for grade in grades:
            student = self._system.get_student(
                grade.get_student_id()
            )
            student_name = (
                student.get_name()
                if student
                else "Unknown"
            )
            self.grade_text.insert(
                tk.END,
                f"{student_name} | "
                f"{grade.get_score()} | "
                f"{grade.get_letter_grade()}\n"
            )

    def add_grade_popup(self):
        """
        Opens add grade popup.
        Complexity:
            O(1)
        """
        window = tk.Toplevel(self)
        window.title(
            "Add Grade"
        )
        fields = [
            "Student ID",
            "Course CRN",
            "Score",
            "Semester"
        ]
        entries = {}
        for field in fields:
            ttk.Label(
                window,
                text=field
            ).pack()
            entry = ttk.Entry(window)
            entry.pack()
            entries[field] = entry
        def save():
            try:
                student_id = int(
                    entries["Student ID"].get()
                )
                crn = int(
                    entries["Course CRN"].get()
                )
                score = float(
                    entries["Score"].get()
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Invalid numeric input"
                )
                return
            semester = entries["Semester"].get()
            grade = Grade(
                student_id,
                crn,
                score,
                semester
            )
            self._system.add_grade(
                grade
            )
            window.destroy()
        ttk.Button(
            window,
            text="Save",
            command=save
        ).pack(
            pady=10
        )