from caracteristica.caracteristica import Subject, Employee

class Teacher(Employee, Subject):  # Teacher inherits from Employee
    def __init__(self, name, id, salary, department, subject):
        Employee.__init__(self, name, id, salary, department)
        Subject.__init__(self, subject)