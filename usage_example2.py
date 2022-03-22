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


if __name__ == '__main__':
    number = 10
    try:
        i_num = int(input("ENTER INT: "))
        if i_num < number:
            raise ValueTooSmallError(i_num)
        if i_num > number:
            raise ValueTooLargeError(i_num)
        else:
            print("PERFECT!")
    except ValueTooSmallError:
        raise
    except ValueTooLargeError:
        raise
    except MyException:
        raise

    print("END OF THE SCRIPT")
