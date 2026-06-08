from abc import ABC, abstractmethod
class Person(ABC):
    """
    Abstract base class representing a person.
    Stores common information like ID, name, surname and email.
    Need it because we can have many types of users like students,
    teachers, and admins that share common attributes and methods.
    """

    _id: int
    _name: str
    _surname: str
    _email: str

    def __init__(self, id: int, name: str, surname: str, email: str):
        """
        Initializes common person information.
        """
        
        self._id = id
        self._name = name
        self._surname = surname
        self._email = email 

    # Getters and setters for the Person class, we need them to access and modify
    # the attributes of the Person class because they are private and we want
    # to encapsulate the data.

    def get_id(self) -> int:
        """
        Returns person's ID.
        """
        
        return self._id

    def get_name(self) -> str:
        """
        Returns person's first name.
        """
        
        return self._name

    def get_surname(self) -> str:
        """
        Returns person's surname.
        """
        
        return self._surname

    def get_email(self) -> str:
        """
        Returns person's email.
        """
        
        return self._email

    def set_name(self, name: str) -> None:
        """
        Updates person's name.
        """
        
        self._name = name

    def set_surname(self, surname: str) -> None:
        """
        Updates person's surname.
        """
        
        self._surname = surname

    def set_email(self, email: str) -> None:
        """
        Updates person's email.
        """
        
        self._email = email

    def set_id(self, id: int) -> None:
        """
        Updates person's ID.
        """
        
        self._id = id

    @abstractmethod
    def get_role(self) -> str:
        """
        Returns the role of the person.
        Must be implemented by child classes.
        """
        
        pass

    def __str__(self) -> str:
        """
        Returns person's information as a string.
        """

        return self._name + " " + self._surname + " (" + self._email + ")"