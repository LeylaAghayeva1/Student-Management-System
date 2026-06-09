class Course:
    """
    Represents a course in the student management system.
    Stores course information such as CRN, name, teacher,
    enrolled students, prerequisites, capacity, and credits.
    """

    _crn: int
    _name: str
    _teacher_id: int
    _student_ids: list
    _prerequisites: set
    _max_capacity: int
    _credits: int

    def __init__(self, crn: int, name: str, teacher_id: int, prerequisites: set, max_capacity: int, credits: int):
        """
        Initializes a Course object with basic course information.
        """

        self._crn = crn
        self._name = name
        self._teacher_id = teacher_id
        self._student_ids = []
        self._credits = credits
        self._prerequisites = prerequisites
        self._max_capacity = max_capacity
        self._course_info = (crn, name, credits)

    #Getters and setters for the Course class, we need them to access and modify the attributes of the Course class because they are private and we want to encapsulate the data.
    
    def get_crn(self) -> int:
        """
        Returns the course CRN.
        """
        
        return self._crn

    def get_name(self) -> str:
        """
        Returns the course name.
        """
        
        return self._name

    def get_teacher_id(self) -> int:
        """
        Returns the teacher ID assigned to this course.
        """
        
        return self._teacher_id

    def get_credits(self) -> int:
        """
        Returns the number of credits of the course.
        """
        
        return self._credits

    def get_student_ids(self) -> list:
        """
        Returns the list of enrolled student IDs.
        """
        
        return self._student_ids

    def get_prerequisites(self) -> set:
        """
        Returns the set of prerequisite course CRNs.
        """
        
        return self._prerequisites

    def get_max_capacity(self) -> int:
        """
        Returns the maximum student capacity.
        """
        
        return self._max_capacity
    
    def get_course_info(self) -> tuple:
        """
        Returns immutable course information.
        The tuple contains:
        - Course CRN
        - Course name
        - Course credits
        """
        return self._course_info

    def set_name(self, name: str) -> None:
        """
        Updates the course name.
        Also refreshes the course information tuple
        to keep stored data synchronized.
        """
        
        self._name = name
        self._course_info=(self._crn, name, self._credits)

    def set_teacher_id(self, teacher_id: int) -> None:
        """
        Updates the assigned teacher ID.
        """
        
        self._teacher_id = teacher_id

    def set_credits(self, credits: int) -> None:
        """
        Updates course credits.
        Also refreshes the course information tuple
        to keep stored data synchronized.
        """
        
        self._credits = credits
        self._course_info=(self._crn, self._name, credits)

    def set_prerequisites(self, prerequisites: set) -> None:
        """
        Updates course prerequisites.
        """
        
        self._prerequisites = prerequisites

    def set_max_capacity(self, max_capacity: int) -> None:
        """
        Updates the maximum course capacity.
        """
        
        self._max_capacity = max_capacity


    def add_student(self, student_id: int) -> bool:
        """
        Adds a student to the course.
        The student is added only if:
        - The course has available capacity.
        - The student is not already enrolled.
        Returns:
        True if the student was successfully added.
        False if the course is full or the student is already enrolled.
        """

        if (len(self._student_ids) < self._max_capacity and student_id not in self._student_ids):
            self._student_ids.append(student_id)
            return True
        return False

    def remove_student(self, student_id: int) -> bool:
        """
        Removes a student from the course.
        Returns:
        True if the student was removed.
        False if the student was not enrolled.
        """

        if student_id in self._student_ids:
            self._student_ids.remove(student_id)
            return True
        return False

    def add_prerequisite(self, course_crn: int) -> None:
        """
        Adds a prerequisite course CRN.
        """
        
        self._prerequisites.add(course_crn)

    def remove_prerequisite(self, course_crn: int) -> None:
        """
        Removes a prerequisite course CRN.
        """

        if course_crn in self._prerequisites:
            self._prerequisites.remove(course_crn)

    def is_full(self) -> bool:
        """
        Checks whether the course reached maximum capacity.
        """

        return len(self._student_ids) >= self._max_capacity

    def __str__(self) -> str:
        """
        Returns a string representation of course information.
        """
        return "Course CRN: " + str(self._crn) + " - Name: " + self._name + " - Teacher ID: " + str(self._teacher_id) + " - Credits: " + str(self._credits) + " - Enrolled Students: " + str(len(self._student_ids)) + "/" + str(self._max_capacity) + " - Prerequisites: " + str(self._prerequisites)