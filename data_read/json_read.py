# Advanced file operations example
import json
from student.student import Student
from teacher.teacher import Teacher
from assistant.assistant import Assistant

def read_json_students():
    """Read students from JSON file"""
    students = []
    with open('data/students.json', 'r') as file:
        data = json.load(file)
        for item in data:
            student = Student(item['name'], item['id'], item['grade'], item['speciality'])
            students.append(student)
    return students

def read_json_teachers():
    """Read teachers from JSON file"""
    teachers = []
    with open('data/teacher.json', 'r') as file:
        data = json.load(file)
        for item in data:
            teacher = Teacher(item['name'], item['id'], item['salary'], item['department'], item['subject'])
            teachers.append(teacher)
    return teachers

def read_json_assistants():
    """Read assistants from JSON file"""
    assistants = []
    with open('data/assistant.json', 'r') as file:
        data = json.load(file)
        for item in data:
            assistant = Assistant(item['name'], item['id'], item['salary'], item['department'])
            assistants.append(assistant)
    return assistants