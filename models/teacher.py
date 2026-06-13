from models.person import Person
class Teacher(Person):
    """
    Represents a teacher in the student management system.
    Extends Person class and stores teacher-specific information
    such as department and assigned courses.
    """

    _department: str
    _teaching_courses: list

    def __init__(self, id: int, name: str, surname: str, email: str, department: str):
        """
        Initializes teacher information using Person constructor
        and adds teacher-specific attributes.
        """

        # used parent class constructor inside the child class constructor
        super().__init__(id, name, surname, email)

        self._department = department
        self._teaching_courses = []

        # tuple to uniquely identify the teacher
        self._identity = (id, name, surname)

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

    def set_department(self, department: str) -> None:
        """
        Updates teacher department.
        """

        self._department = department

    def assign_course(self, course_id: int) -> bool:
        """
        Assigns a course to the teacher.
        Returns:
            True if the course was assigned.
            False if the teacher already has this course.
        """
        
        if course_id not in self._teaching_courses:
            self._teaching_courses.append(course_id)
            return True
        return False

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
            + " - Department: "
            + self._department
        )
        
    def to_dict(self) -> dict:
        """
        Converts the Teacher object into a dictionary.

        Includes inherited Person attributes and teacher-specific
        attributes.

        Returns:
            dict: Dictionary representation of the teacher.
        """

        return {
            "id": self._id,
            "name": self._name,
            "surname": self._surname,
            "email": self._email,
            "department": self._department,
            "teaching_courses": self._teaching_courses,
            "identity": self._identity
        }
        
    @staticmethod
    def from_dict(data: dict):
        """
        Creates a Teacher object from dictionary data.

        Used when loading teacher information from storage.

        Args:
            data (dict): Dictionary containing teacher information.

        Returns:
            Teacher: Reconstructed Teacher object.
        """
        teacher = Teacher(
            data["id"],
            data["name"],
            data["surname"],
            data["email"],
            data["department"]
        )
        for course_id in data["teaching_courses"]:
            teacher.assign_course(course_id)
        return teacher