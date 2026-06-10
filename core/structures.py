class Stack:
    """
    Represents a stack data structure using a list.
    Uses LIFO (Last In First Out) principle.
    Use case:
    Stores grade change history per student.
    """

    _items: list
    _max_size: int

    def __init__(self, max_size: int = None):
        """
        Initializes empty stack.
        Args:
            max_size: Maximum number of items allowed.
        """

        self._items = []
        self._max_size = max_size

    def push(self, item) -> bool:
        """
        Adds an item to the top of the stack.
        Complexity: O(1)
        """

        if self._max_size and len(self._items) >= self._max_size:
            return False
        self._items.append(item)
        return True

    def pop(self):
        """
        Removes and returns the top item.
        Raises:
        IndexError: If stack is empty.
        Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """
        Returns the top item without removing it.
        Raises:
        IndexError: If stack is empty.
        Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Cannot peek from an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Checks whether stack is empty.
        Complexity: O(1)
        """
        
        return len(self._items) == 0

    def size(self) -> int:
        """
        Returns number of items in stack.
        Complexity: O(1)
        """

        return len(self._items)
    
    
class Queue:
    """
    Represents a queue data structure using a list.
    Uses FIFO (First In First Out) principle.
    Use case:
    Stores course enrollment waitlist.
    """

    _items: list
    
    def __init__(self):
        """
        Initializes an empty queue.
        """
        self._items = []

    def enqueue(self, item) -> None:
        """
        Adds an item to the end of the queue.
        Complexity: O(1)
        """

        self._items.append(item)

    def dequeue(self):
        """
        Removes and returns the first item.
        Raises:
        IndexError: If queue is empty.
        Complexity: O(n) because removing the first
        element from a list shifts all other elements.
        For O(1) dequeue, use collections.deque instead of list
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.pop(0)

    def peek(self):
        """
        Returns the first item without removing it.
        Raises:
        IndexError: If queue is empty.
        Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Cannot peek from an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """
        Checks whether queue is empty.
        Complexity: O(1)
        """

        return len(self._items) == 0

    def size(self) -> int:
        """
        Returns number of items in queue.
        Complexity: O(1)
        """

        return len(self._items)