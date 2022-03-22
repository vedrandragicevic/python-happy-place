"""
The __str__ function in Python is simply used to return the output of the Python functions in a string format.
This function is mainly used with the user-defined functions since their outputs are generally not in the string format.
For an easier understanding of those outputs, they must be converted into the string format.
"""


# CUSTOM EXCEPTIONS
class MyException(Exception):
    pass


class ValueTooSmallError(MyException):
    def __init__(self, input_number):
        self.input_number = input_number
        self.message = f"VALUE {input_number} TO SMALL!"

    def __str__(self):
        return self.message


class ValueTooLargeError(MyException):
    def __init__(self, input_number):
        self.input_number = input_number
        self.message = f"VALUE {input_number} TO LARGE!"

    def __str__(self):
        return self.message
