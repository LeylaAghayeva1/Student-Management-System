from models.person import Person
class Student(Person):
    """
    Represents a student in the student management system.
    Extends the Person class and stores student-specific information
    such as enrolled courses and year of study.
    """

    _enrolled_courses: list
    _year_of_study: int

    # used the parent constructor to initialize the common attributes of the Person class
    # and then initialized the specific attributes of the Student class.

    def __init__(self, id: int, name: str, surname: str, email: str, year_of_study: int):
        """
        Initializes student information using the parent Person constructor.
        """
        
        # used parent class constructor inside the child class constructor
        super().__init__(id, name, surname, email)
        self._enrolled_courses = []
        self._year_of_study = year_of_study

        # tuple to uniquely identify the student
        self._identity = (id, name, surname)

    # getters and setters for the Student class, we need them to access and modify
    # the attributes of the Student class because they are private and we want
    # to encapsulate the data.

    def get_enrolled_courses(self) -> list:
        """
        Returns list of enrolled course IDs.
        """
        
        return self._enrolled_courses

    def get_year_of_study(self) -> int:
        """
        Returns student's year of study.
        """

        return self._year_of_study

    def get_identity(self) -> tuple:
        """
        Returns immutable student identity tuple.
        """

        return self._identity

    def set_year_of_study(self, year_of_study: int) -> None:
        """
        Updates student's year of study.
        """

        self._year_of_study = year_of_study

    def enroll_course(self, course_id: int) -> bool:
        """
        Adds a course ID to student's enrolled courses.
        Prevents duplicate enrollment.
        """

        if course_id not in self._enrolled_courses:
            self._enrolled_courses.append(course_id)
            return True
        return False

    def drop_course(self, course_id: int) -> None:
        """
        Removes a course ID from student's enrolled courses.
        """
        
        if course_id in self._enrolled_courses:
            self._enrolled_courses.remove(course_id)

    # implemented the abstract method get_role() from the Person class,
    # it returns the role of the user which is "Student" in this case.
    # It demonstrates polymorphism because different child classes
    # can have different implementations of get_role().

    def get_role(self) -> str:
        """
        Returns the role of the object.
        Overrides Person.get_role() and demonstrates polymorphism.
        """
        return "Student"

    def __str__(self) -> str:
        """
        Returns student information as a string.
        """
        return (
            super().__str__()
            + " - Year of Study: "
            + str(self._year_of_study)
        )