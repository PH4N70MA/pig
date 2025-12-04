from __model__.humans import Student, Teacher, Assistant
from __model__.db.db_control import DBController
from config import host, user, password, db_name, port

class DataPresenter:
    
    def __init__(self, view=None):
        self.view = view
        self.data = []
        
    def set_view(self, view):
        self.view = view
        
    def load_data(self):
        raise NotImplementedError
        
    def save_data(self):
        raise NotImplementedError
        
    def add_item(self, **kwargs):
        raise NotImplementedError
        
    def delete_last_item(self):
        with DBController(host, user, password, db_name, port) as db:
            if isinstance(self.data[0] if self.data else None, Student):
                db.deleteStudent(deleted_item.id)
            elif isinstance(self.data[0] if self.data else None, Teacher):
                db.deleteTeacher(deleted_item.id)
            elif isinstance(self.data[0] if self.data else None, Assistant):
                db.deleteAssistant(deleted_item.id)
        if self.data:
            deleted_item = self.data.pop()
            if self.view:
                self.view.refresh_display()
                self.view.show_message(f"Deleted: {deleted_item.name} (ID: {deleted_item.id})")
            return deleted_item
        return None
        
    def sort_data(self, sort_key):
        if sort_key == "name":
            self.data.sort(key=lambda obj: obj.name.lower())
        elif sort_key == "salary" and hasattr(self.data[0] if self.data else None, "salary"):
            self.data.sort(key=lambda obj: float(obj.salary) if str(obj.salary).replace('.','').replace('-','').isdigit() else 0)
        else:
            self.data.sort(key=lambda obj: getattr(obj, sort_key, ""))
            
        if self.view:
            self.view.refresh_display()
            self.view.show_message(f"Data sorted by {sort_key}")
            
    def get_data(self):
        return self.data

class StudentPresenter(DataPresenter):
    
    def __init__(self, view=None):
        super().__init__(view)
        self.load_data()
        
    def load_data(self):

        with DBController(host, user, password, db_name, port) as db:
            self.data = []
            students = db.showStudents()
            for student in students:
                # Assuming the order of columns is (id, name, grade, speciality)
                _, name, grade, speciality = student
                self.data.append(Student(name, _, grade, speciality))
            
    def add_item(self, name, grade, speciality):
        """Add new student"""
        if not all([name.strip(), grade.strip(), speciality.strip()]):
            if self.view:
                self.view.show_message("Error: Please fill all fields")
            return False
            
        if speciality.startswith("Select"):
            if self.view:
                self.view.show_message("Error: Please select a valid speciality")
            return False
        
        with DBController(host, user, password, db_name, port) as db:
            db.addStudent(name, grade, speciality)
            # Re-fetch students and take the last one's id (assumes showStudents returns rows ordered by id)
            students = db.showStudents()
            student_id = students[-1][0] if students else None
            new_student = Student(name, student_id, grade, speciality)
            self.data.append(new_student)

        
        if self.view:
            self.view.refresh_display()
            self.view.clear_fields()
            self.view.show_message(f"Student added with ID: {new_student.id}")
        return True
        
    def get_sort_keys(self):
        """Get available sort keys for students"""
        return ["name", "grade", "speciality", "id"]
        
    def get_specialities(self):
        """Get available specialities"""
        return ["Computer Science", "Mathematics", "Physics", "Engineering"]


class TeacherPresenter(DataPresenter):
    """Presenter for managing teachers"""
    
    def __init__(self, view=None):
        super().__init__(view)
        self.load_data()
        
    def load_data(self):
        with DBController(host, user, password, db_name, port) as db:
            self.data = []
            teachers = db.showTeachers()
            for teacher in teachers:
                # Assuming the order of columns is (id, name, salary, department, subject)
                _, name, salary, department, subject = teacher
                self.data.append(Teacher(name, _, salary, department, subject))
            
    def add_item(self, name, salary, department, subject):
        """Add new teacher"""
        if not all([name.strip(), salary.strip(), department.strip(), subject.strip()]):
            if self.view:
                self.view.show_message("Error: Please fill all fields")
            return False
            
        if department.startswith("Select") or subject.startswith("Select"):
            if self.view:
                self.view.show_message("Error: Please select valid department and subject")
            return False
            
        with DBController(host, user, password, db_name, port) as db:
            db.addTeacher(name, salary, department, subject)
            teacher_id = db.showTeachers()[-1][0]  # Get the last added teacher's ID
            new_teacher = Teacher(name, teacher_id, salary, department, subject)
            self.data.append(new_teacher)
        
        if self.view:
            self.view.refresh_display()
            self.view.clear_fields()
            self.view.show_message(f"Teacher added with ID: {teacher_id}")
        return True
        
    def get_sort_keys(self):
        """Get available sort keys for teachers"""
        return ["name", "department", "subject", "salary", "id"]
        
    def get_departments(self):
        """Get available departments"""
        return ["Human Resources", "Finance", "Engineering", "Marketing"]
        
    def get_subjects(self):
        """Get available subjects"""
        return ["Mathematics", "Physics", "Chemistry", "Biology"]


class AssistantPresenter(DataPresenter):
    """Presenter for managing assistants"""
    
    def __init__(self, view=None):
        super().__init__(view)
        self.load_data()
        
    def load_data(self):
        with DBController(host, user, password, db_name, port) as db:
            self.data = []
            assistants = db.showAssistants()
            for assistant in assistants:
                # Assuming the order of columns is (id, name, department, salary)
                _, name, department, salary = assistant
                self.data.append(Assistant(name, _, salary, department))
            
    def add_item(self, name, salary, department):
        """Add new assistant"""
        if not all([name.strip(), salary.strip(), department.strip()]):
            if self.view:
                self.view.show_message("Error: Please fill all fields")
            return False
            
        if department.startswith("Select"):
            if self.view:
                self.view.show_message("Error: Please select a valid department")
            return False
            
        with DBController(host, user, password, db_name, port) as db:
            db.addAssistant(name, department, salary)
            assistant_id = db.showAssistants()[-1][0]  # Get the last added assistant's ID
            new_assistant = Assistant(name, assistant_id, salary, department)
            self.data.append(new_assistant)
        
        if self.view:
            self.view.refresh_display()
            self.view.clear_fields()
            self.view.show_message(f"Assistant added with ID: {assistant_id}")
        return True
        
    def get_sort_keys(self):
        """Get available sort keys for assistants"""
        return ["name", "department", "salary", "id"]
        
    def get_departments(self):
        """Get available departments"""
        return ["Human Resources", "Finance", "Engineering", "Marketing"]