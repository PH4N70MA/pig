# Advanced file operations example
import json
from student.student import Student
from teacher.teacher import Teacher
from assistant.assistant import Assistant

def save_json_students(students):
    """Save students to JSON file"""
    data = []
    for student in students:
        data.append({
            'name': student.name,
            'id': student.id,
            'grade': student.grade,
            'speciality': student.speciality
        })
    with open('data/student.json', 'w') as file:
        json.dump(data, file, indent=2)

def save_json_teachers(teachers):
    """Save teachers to JSON file"""
    data = []
    for teacher in teachers:
        data.append({
            'name': teacher.name,
            'id': teacher.id,
            'salary': teacher.salary,
            'department': teacher.department,
            'subject': teacher.subject,
        })
    with open('data/teacher.json', 'w') as file:
        json.dump(data, file, indent=2)

def save_json_assistants(assistants):
    """Save assistants to JSON file"""
    data = []
    for assistant in assistants:
        data.append({
            'name': assistant.name,
            'id': assistant.id,
            'department': assistant.department,
            'salary': assistant.salary
        })
    with open('data/assistant.json', 'w') as file:
        json.dump(data, file, indent=2)
