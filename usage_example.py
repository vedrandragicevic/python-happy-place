from custom_exceptions_class import *

number = 10

i_num = int(input("ENTER INT: "))   # ENTER INT: 53
if i_num < number:
    raise ValueTooSmallError(i_num)
if i_num > number:
    raise ValueTooLargeError(i_num)
else:
    print("BOTH NUMBERS MATCH!")

print("END OF THE SCRIPT")

"""
    OUTPUT IF ValueTooLargeError raise:
    Traceback (most recent call last):
      File "/Users/dragicevic/PycharmProjects/developer tools/python-happy-place/usage_example.py", line 9, in <module>
        raise ValueTooLargeError(i_num)
    custom_exceptions_class.ValueTooLargeError: VALUE 53 TO LARGE!
"""