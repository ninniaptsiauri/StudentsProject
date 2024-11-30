from faker import Faker
from random import randint
import json

fake = Faker()

class Student:
    def __init__(self, name, roll_number, grade):
        self.name = name
        self.roll_number = roll_number
        self.grade = grade

    def __str__(self):
        return f"name(): {self.name}, Roll Number: {self.roll_number}, Grade: {self.grade}"

students = [Student(fake.name(), randint(1, 200), randint(0, 100)) for _ in range(50)]


def custom_serializer(obj):
    if isinstance(obj, Student):
        return {
            'name': obj.name,
            'roll_number': obj.roll_number,
            'grade': obj.grade
        }
    
    raise TypeError(f'Object of {type(obj)} is not JSON serializable')

    
with open('students.json', 'w') as file:
    json.dump(students, file, default=custom_serializer, indent=4)
