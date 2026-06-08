from models.person import Person
class Teacher(Person):
    """
    Represents a teacher in the student management system.
    Extends Person class and stores teacher-specific information
    such as employee ID, department and assigned courses.
    """

    _employee_id: str
    _department: str
    _teaching_courses: list

    # unique identifier for the teacher, and its something like
    # "EMP-12345" -> EMP - employee number

    def __init__(self, id: int, name: str, surname: str, email: str, employee_id: str, department: str):
        """
        Initializes teacher information using Person constructor
        and adds teacher-specific attributes.
        """
        
        #used parent class constructor inside the child class constructor
        super().__init__(id, name, surname, email)
        self._employee_id = employee_id
        self._department = department
        self._teaching_courses = []
        
        # tuple to uniquely identify the teacher
        self._identity = (id, employee_id)

    def get_employee_id(self) -> str:
        """
        Returns teacher employee ID.
        """
        
        return self._employee_id

    def get_department(self) -> str:
        """
        Returns teacher department.
        """
        
        return self._department

    def get_teaching_courses(self) -> list:
        """
        Returns list of courses taught by the teacher.
        """
        
        return self._teaching_courses

    def get_identity(self) -> tuple:
        """
        Returns immutable teacher identity tuple.
        """
        
        return self._identity

    def set_employee_id(self, employee_id: str) -> None:
        """
        Updates teacher employee ID.
        """
        
        self._employee_id = employee_id

    def set_department(self, department: str) -> None:
        """
        Updates teacher department.
        """
        
        self._department = department

    def assign_course(self, course_id: int) -> None:
        """
        Assigns a course to the teacher.
        """

        self._teaching_courses.append(course_id)

    def remove_course(self, course_id: int) -> None:
        """
        Removes a course from teacher's assigned courses.
        """
        
        if course_id in self._teaching_courses:
            self._teaching_courses.remove(course_id)

    # Polymorphism because we can have many types of users like students,
    # teachers, and admins and they all have common attributes and methods
    # but they can have different implementations of the get_role() method.

    def get_role(self) -> str:
        """
        Returns the role of the object.
        Overrides Person.get_role() and demonstrates polymorphism.
        """

        return "Teacher"

    def __str__(self) -> str:
        """
        Returns teacher information as a string.
        """

        return (
            super().__str__()
            + " - Employee ID: "
            + self._employee_id
            + " - Department: "
            + self._department
        )