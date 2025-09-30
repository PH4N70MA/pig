from __model__.data import read_json_students, read_json_teachers, read_json_assistants
from __model__.data import save_json_students, save_json_teachers, save_json_assistants
from __model__.humans import Student, Teacher, Assistant
import random


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
        
    def generate_id(self, prefix, id_range):
        existing_ids = [obj.id for obj in self.data]
        while True:
            new_id = f"{prefix}{random.randint(*id_range)}"
            if new_id not in existing_ids:
                return new_id


class StudentPresenter(DataPresenter):
    
    def __init__(self, view=None):
        super().__init__(view)
        self.load_data()
        
    def load_data(self):
        """Load students from JSON file"""
        try:
            self.data = read_json_students()
        except FileNotFoundError:
            self.data = []
            
    def save_data(self):
        """Save students to JSON file"""
        save_json_students(self.data)
        if self.view:
            self.view.show_message("Students saved!")
            
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
            
        student_id = self.generate_id("STU", (1000, 9999))
        new_student = Student(name, student_id, grade, speciality)
        self.data.append(new_student)
        
        if self.view:
            self.view.refresh_display()
            self.view.clear_fields()
            self.view.show_message(f"Student added with ID: {student_id}")
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
        """Load teachers from JSON file"""
        try:
            self.data = read_json_teachers()
        except FileNotFoundError:
            self.data = []
            
    def save_data(self):
        """Save teachers to JSON file"""
        save_json_teachers(self.data)
        if self.view:
            self.view.show_message("Teachers saved!")
            
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
            
        teacher_id = self.generate_id("TCH", (100, 999))
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
        """Load assistants from JSON file"""
        try:
            self.data = read_json_assistants()
        except FileNotFoundError:
            self.data = []
            
    def save_data(self):
        """Save assistants to JSON file"""
        save_json_assistants(self.data)
        if self.view:
            self.view.show_message("Assistants saved!")
            
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
            
        assistant_id = self.generate_id("AST", (100, 999))
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