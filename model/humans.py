from caracteristica import Subject, Employee, Speciality

class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class Teacher(Employee, Subject):  # Teacher inherits from Employee
    def __init__(self, name, id, salary, department, subject):
        Employee.__init__(self, name, id, salary, department)
        Subject.__init__(self, subject)

class Student(Person, Speciality):  # Student inherits from Person
    def __init__(self, name, id, grade, speciality):
        Person.__init__(self, name, id)
        Speciality.__init__(self, speciality)
        self.grade = grade

class Assistant(Employee):  # Assistant inherits from Employee
    def __init__(self, name, id, salary, department):
        super().__init__(name, id, salary, department)