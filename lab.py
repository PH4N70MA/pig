from data_read.json_read import read_json_students, read_json_teachers, read_json_assistants
from data_save.json_save import save_json_students, save_json_teachers, save_json_assistants

from student.student import Student
from teacher.teacher import Teacher
from assistant.assistant import Assistant

# Test JSON operations
print("=== JSON Student File Operations ===")
json_students = read_json_students()
for student in json_students:
    print("Student:")
    print(f"  Name: {student.name}")
    print(f"  ID: {student.id}")
    print(f"  Grade: {student.grade}")
    print(f"  Speciality: {student.speciality}")
    print("-" * 30)

print("=== JSON Teacher File Operations ===")
json_teachers = read_json_teachers()
for teacher in json_teachers:
    print("Teacher:")
    print(f"  Name: {teacher.name}")
    print(f"  ID: {teacher.id}")
    print(f"  Salary: {teacher.salary}")
    print(f"  Department: {teacher.department}")
    print(f"  Subject: {teacher.subject}")
    print("-" * 30)

print("=== JSON Assistant File Operations ===")
json_assistants = read_json_assistants()
for assistant in json_assistants:
    print("Assistant:")
    print(f"  Name: {assistant.name}")
    print(f"  ID: {assistant.id}")
    print(f"  Salary: {assistant.salary}")
    print(f"  Department: {assistant.department}")
    print("-" * 30)

# Save back to a new JSON file
save_json_students(json_students)
save_json_teachers(json_teachers)
save_json_assistants(json_assistants)
print("JSON backup created!")

print(f"\nTotal students from JSON: {len(json_students)}")
print(f"Total teachers from JSON: {len(json_teachers)}")
print(f"Total assistants from JSON: {len(json_assistants)}")