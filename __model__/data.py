import json
from __model__.humans import Student, Teacher, Assistant

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
    with open('__data__/students.json', 'w') as file:
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
    with open('__data__/teacher.json', 'w') as file:
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
    with open('__data__/assistant.json', 'w') as file:
        json.dump(data, file, indent=2)

def read_json_students():
    """Read students from JSON file"""
    students = []
    with open('__data__/students.json', 'r') as file:
        data = json.load(file)
        for item in data:
            student = Student(item['name'], item['id'], item['grade'], item['speciality'])
            students.append(student)
    return students

def read_json_teachers():
    """Read teachers from JSON file"""
    teachers = []
    with open('__data__/teacher.json', 'r') as file:
        data = json.load(file)
        for item in data:
            teacher = Teacher(item['name'], item['id'], item['salary'], item['department'], item['subject'])
            teachers.append(teacher)
    return teachers

def read_json_assistants():
    """Read assistants from JSON file"""
    assistants = []
    with open('__data__/assistant.json', 'r') as file:
        data = json.load(file)
        for item in data:
            assistant = Assistant(item['name'], item['id'], item['salary'], item['department'])
            assistants.append(assistant)
    return assistants
