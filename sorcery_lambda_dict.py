"""
Lambda functions in Python, adding one dict to another, map function
"""
import json
from sorcery import dict_of


def p(n):
    for i in range(n):
        print(" "*(n-i-1), end="")
        print("* "*(i+1))
    for j in range(n-1, 0, -1):
        print(" "*(n-j), end="")
        print("* "*j)


# SIMPLE LAMBDA FUNCTION WITH MAP(FUNCTION, ITERABLE)
test_tuple_one = (5, 3, 1)
result = map(lambda x: x*2, test_tuple_one)
print(F"MAP FUNCTION RESULT: {list(result)}")
"""
    OUTPUT:
        MAP FUNCTION RESULT: [10, 6, 2]
"""

# ADDING 2 DICT INTO ONE
dict_one = {"vex": "test1", "vex2": "test2"}
dict_two = {"pile1": "testp1", "pile2": "testp2"}
dict_tree = {**dict_one, **dict_two}
print(f"COMBINED DICTS: {dict_tree}")
"""
    COMBINING TWO DICTIONARIES INTO ONE OUTPUT:
        COMBINED DICTS: {'vex': 'test1', 'vex2': 'test2', 'pile1': 'testp1', 'pile2': 'testp2'}
"""

# PRINTING STARTS
p(5)
"""
    OUTPUT:
            * 
           * * 
          * * * 
         * * * * 
        * * * * * 
         * * * * 
          * * * 
           * * 
            *
"""

# CHECK IF TEST STRING TWO IS IN TEST STRING ONE
test_string = "abcdefgh"
test_string_two = "abc"

result = (lambda test: True if test in test_tuple_one else False)(test_string_two)
print(F"LAMBDA FUNCTION BOOL RESULT: {result}")
"""
    OUTPUT:
        LAMBDA FUNCTION BOOL RESULT: False
"""

# CREATING DICT BASED ON VARIABLES NAMES AND VALUES
key1 = "test1"
key2 = "test2"
key3 = "test3"

sorcery_dict = dict_of(key1, key2, key3)
print(F"SORCERY DICT: {sorcery_dict}")
"""
    OUTPUT:
        SORCERY DICT: {'key1': 'test1', 'key2': 'test2', 'key3': 'test3'}
"""