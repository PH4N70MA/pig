from person.person import Person

class Speciality:
    ALLOWED_SPECIALTIES = ["Computer Science", "Mathematics", "Physics", "Engineering"]

    def __init__(self, speciality):
        if speciality not in self.ALLOWED_SPECIALTIES:
            raise ValueError(f"Invalid specialty. Must be one of: {', '.join(self.ALLOWED_SPECIALTIES)}")
        self.speciality = speciality

class Subject:
    ALLOWED_SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology"]

    def __init__(self, subject):
        if subject not in self.ALLOWED_SUBJECTS:
            raise ValueError(f"Invalid subject. Must be one of: {', '.join(self.ALLOWED_SUBJECTS)}")
        self.subject = subject

class Departament:
    ALLOWED_DEPARTMENTS = ["Human Resources", "Finance", "Engineering", "Marketing"]

    def __init__(self, department):
        if department not in self.ALLOWED_DEPARTMENTS:
            raise ValueError(f"Invalid department. Must be one of: {', '.join(self.ALLOWED_DEPARTMENTS)}")
        self.department = department

class Employee(Person, Departament):  # Employee inherits from Person
    def __init__(self, name, id, salary, department):
        Person.__init__(self, name, id)
        Departament.__init__(self, department)
        self.salary = salary