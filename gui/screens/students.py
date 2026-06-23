import tkinter as tk
from tkinter import ttk, messagebox
from models.student import Student
class StudentsFrame(tk.Frame):
    """
    Student management screen.
    Features:
    - Display all students
    - Add student
    - Edit student
    - Delete student
    - Search students in real time
    GUI layer handles only:
    - User input
    - Display updates
    Business logic is handled by
    StudentManagementSystem.
    """
    def __init__(self, parent, system):
        """
        Initializes students screen.
        Args:
            parent:
                Parent tkinter widget.
            system:
                StudentManagementSystem instance.
        Complexity:
            O(n) because students are loaded.
        """
        super().__init__(parent)
        self._system = system
        self._search_var = tk.StringVar()
        self.create_search()
        self.create_table()
        self.create_buttons()
        self.load_students()
        
    def create_search(self):
        """
        Creates search area.
        Search updates table automatically.
        Complexity:
            O(1)
        """
        frame = ttk.Frame(self)
        frame.pack(
            fill="x",
            pady=5
        )
        ttk.Label(
            frame,
            text="Search:"
        ).pack(
            side="left",
            padx=5
        )
        entry = ttk.Entry(
            frame,
            textvariable=self._search_var
        )
        entry.pack(
            side="left",
            fill="x",
            expand=True
        )
        self._search_var.trace(
            "w",
            lambda *args:
                self.load_students()
        )
        ttk.Button(
            frame,
            text="Clear",
            command=self.clear_search
        ).pack(
            side="right",
            padx=5
        )

    def clear_search(self):
        """
        Clears search field.
        Complexity:
            O(1)
        """
        self._search_var.set("")

    def create_table(self):
        """
        Creates student table.
        Columns:
        - ID
        - Name
        - Surname
        - Email
        - Year
        Complexity:
            O(1)
        """
        columns = (
            "id",
            "name",
            "surname",
            "email",
            "year"
        )
        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )
        for column in columns:
            self.table.heading(
                column,
                text=column.capitalize()
            )
            self.table.column(
                column,
                width=120
            )
        self.table.pack(
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
        frame.pack(
            pady=10
        )
        ttk.Button(
            frame,
            text="Add",
            command=self.add_student
        ).pack(
            side="left",
            padx=5
        )
        ttk.Button(
            frame,
            text="Edit",
            command=self.edit_student
        ).pack(
            side="left",
            padx=5
        )
        ttk.Button(
            frame,
            text="Delete",
            command=self.delete_student
        ).pack(
            side="left",
            padx=5
        )

    def load_students(self):
        """
        Loads students into table.
        Supports real-time search.
        Complexity:
            O(n)
        """
        for row in self.table.get_children():
            self.table.delete(row)
        search = (
            self._search_var
            .get()
            .lower()
        )
        for student in self._system.get_all_students():
            name = student.get_name().lower()
            surname = student.get_surname().lower()
            if (
                search in name
                or search in surname
            ):
                self.table.insert(
                    "",
                    "end",
                    values=(
                        student.get_id(),
                        student.get_name(),
                        student.get_surname(),
                        student.get_email(),
                        student.get_year_of_study()
                    )
                )

    def add_student(self):
        """
        Opens add student form.
        Complexity:
            O(1)
        """
        self.student_popup()

    def edit_student(self):
        """
        Opens edit form.
        Complexity:
            O(1)
        """
        selected = self.table.selection()
        if not selected:
            messagebox.showerror(
                "Error",
                "Select a student first"
            )
            return
        values = self.table.item(
            selected[0]
        )["values"]
        self.student_popup(
            values
        )

    def student_popup(self, values=None):
        """
        Opens add/edit popup.
        Args:
            values:
                Existing student table data.
        Complexity:
            O(1)
        """
        popup = tk.Toplevel(self)
        popup.title(
            "Edit Student"
            if values
            else
            "Add Student"
        )
        fields = [
            "Name",
            "Surname",
            "Email",
            "Year"
        ]
        entries = {}
        for field in fields:
            ttk.Label(
                popup,
                text=field
            ).pack()
            entry = ttk.Entry(
                popup
            )
            entry.pack()
            entries[field] = entry
        if values:
            entries["Name"].insert(
                0,
                values[1]
            )
            entries["Surname"].insert(
                0,
                values[2]
            )
            entries["Email"].insert(
                0,
                values[3]
            )
            entries["Year"].insert(
                0,
                values[4]
            )

        def save():
            name = entries["Name"].get().strip()
            surname = entries["Surname"].get().strip()
            email = entries["Email"].get().strip()
            if not name or not surname or not email:
                messagebox.showerror(
                    "Error",
                    "All fields are required"
                )
                return
            try:
                year = int(
                    entries["Year"].get()
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Year must be a number"
                )
                return
            if values:
                student_id = int(
                    values[0]
                )
                self._system.update_student(
                    student_id,
                    name,
                    email
                )
            else:
                new_id = max(
                    (
                        student.get_id()
                        for student in
                        self._system.get_all_students()
                    ),
                    default=0
                ) + 1
                student = Student(
                    new_id,
                    name,
                    surname,
                    email,
                    year
                )
                self._system.add_student(
                    student
                )
            popup.destroy()
            self.load_students()
        ttk.Button(
            popup,
            text="Save",
            command=save
        ).pack(
            pady=10
        )

    def delete_student(self):
        """
        Deletes selected student.
        Complexity:
            O(n)
            because table reloads.
        """
        selected = self.table.selection()
        if not selected:
            messagebox.showerror(
                "Error",
                "Select student first"
            )
            return
        student_id = int(
            self.table.item(
                selected[0]
            )["values"][0]
        )
        confirm = messagebox.askyesno(
            "Delete",
            "Delete this student?"
        )
        if confirm:
            self._system.delete_student(
                student_id
            )
            self.load_students()