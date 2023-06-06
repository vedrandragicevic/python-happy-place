#!/usr/bin/python
from dataclasses import dataclass


class Person:

    def __init__(self, name, age):

        self.name = name
        self.age = age

    def __repr__(self):

        return f'Person{{name: {self.name}, age: {self.age}}}'


p = Person('John Doe', 34)
print(p)


@dataclass
class Person:
    name: str
    age: int


p = Person('John Doe', 34)
p.occupation = 'gardener'

print(p)
print(p.occupation)
