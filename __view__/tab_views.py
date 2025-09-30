import customtkinter


class BaseTabView:
    """Base class for tab views"""
    
    def __init__(self, parent_tab, presenter):
        self.tab = parent_tab
        self.presenter = presenter
        self.presenter.set_view(self)
        self.widgets = {}
        self._build_ui()
        self.refresh_display()
        
    def _build_ui(self):
        """Build the UI - to be implemented by subclasses"""
        raise NotImplementedError
        
    def refresh_display(self):
        """Refresh the display - to be implemented by subclasses"""
        raise NotImplementedError
        
    def clear_fields(self):
        """Clear input fields - to be implemented by subclasses"""
        raise NotImplementedError
        
    def show_message(self, message):
        """Show message to user"""
        print(message)


class StudentTabView(BaseTabView):
    """View for managing students"""
    
    def _build_ui(self):
        # Title
        title = customtkinter.CTkLabel(self.tab, text="Students Management", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))
        
        # Display area
        self.widgets["display"] = customtkinter.CTkTextbox(self.tab, width=800, height=350, font=("Courier New", 10))
        self.widgets["display"].pack(pady=10)
        
        # Entry frame
        entry_frame = customtkinter.CTkFrame(self.tab)
        entry_frame.pack(pady=10, fill="x", padx=20)
        
        # Input fields
        self.widgets["name"] = customtkinter.CTkEntry(entry_frame, placeholder_text="Name", width=200)
        self.widgets["name"].grid(row=0, column=0, padx=8, pady=10)
        
        self.widgets["grade"] = customtkinter.CTkEntry(entry_frame, placeholder_text="Grade", width=100)
        self.widgets["grade"].grid(row=0, column=1, padx=8, pady=10)
        
        self.widgets["speciality"] = customtkinter.CTkComboBox(entry_frame, values=self.presenter.get_specialities(), width=200)
        self.widgets["speciality"].set("Select Speciality")
        self.widgets["speciality"].grid(row=0, column=2, padx=8, pady=10)
        
        # Action buttons
        btn_frame = customtkinter.CTkFrame(self.tab)
        btn_frame.pack(pady=10)
        
        add_btn = customtkinter.CTkButton(btn_frame, text="Add Student", command=self._add_student)
        add_btn.grid(row=0, column=0, padx=10, pady=5)
        
        delete_btn = customtkinter.CTkButton(btn_frame, text="Delete Last Student", command=self._delete_student)
        delete_btn.grid(row=0, column=1, padx=10, pady=5)
        
        save_btn = customtkinter.CTkButton(btn_frame, text="Save Students", command=self._save_students)
        save_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Sort buttons
        sort_frame = customtkinter.CTkFrame(self.tab)
        sort_frame.pack(pady=5)
        
        sort_keys = self.presenter.get_sort_keys()
        for i, sort_key in enumerate(sort_keys):
            btn = customtkinter.CTkButton(sort_frame, text=f"Sort by {sort_key.capitalize()}", 
                                        command=lambda key=sort_key: self._sort_data(key))
            btn.grid(row=0, column=i, padx=3, pady=5)
    
    def _add_student(self):
        name = self.widgets["name"].get()
        grade = self.widgets["grade"].get()
        speciality = self.widgets["speciality"].get()
        self.presenter.add_item(name, grade, speciality)
    
    def _delete_student(self):
        self.presenter.delete_last_item()
    
    def _save_students(self):
        self.presenter.save_data()
    
    def _sort_data(self, key):
        self.presenter.sort_data(key)
    
    def refresh_display(self):
        """Refresh the display with current data"""
        display = self.widgets["display"]
        display.delete("1.0", customtkinter.END)
        
        header = f"{'#':<3} {'Name':<20} {'ID':<10} {'Grade':<8} {'Speciality':<20}\n"
        separator = "=" * 75 + "\n"
        display.insert("1.0", header + separator)
        
        for i, student in enumerate(self.presenter.get_data(), 1):
            line = f"{i:<3} {student.name:<20} {student.id:<10} {student.grade:<8} {student.speciality:<20}\n"
            display.insert(customtkinter.END, line)
    
    def clear_fields(self):
        """Clear input fields"""
        self.widgets["name"].delete(0, customtkinter.END)
        self.widgets["grade"].delete(0, customtkinter.END)
        self.widgets["speciality"].set("Select Speciality")


class TeacherTabView(BaseTabView):
    """View for managing teachers"""
    
    def _build_ui(self):
        # Title
        title = customtkinter.CTkLabel(self.tab, text="Teachers Management", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))
        
        # Display area
        self.widgets["display"] = customtkinter.CTkTextbox(self.tab, width=800, height=350, font=("Courier New", 10))
        self.widgets["display"].pack(pady=10)
        
        # Entry frame
        entry_frame = customtkinter.CTkFrame(self.tab)
        entry_frame.pack(pady=10, fill="x", padx=20)
        
        # Input fields
        self.widgets["name"] = customtkinter.CTkEntry(entry_frame, placeholder_text="Name", width=150)
        self.widgets["name"].grid(row=0, column=0, padx=8, pady=10)
        
        self.widgets["salary"] = customtkinter.CTkEntry(entry_frame, placeholder_text="Salary", width=120)
        self.widgets["salary"].grid(row=0, column=1, padx=8, pady=10)
        
        self.widgets["department"] = customtkinter.CTkComboBox(entry_frame, values=self.presenter.get_departments(), width=150)
        self.widgets["department"].set("Select Department")
        self.widgets["department"].grid(row=0, column=2, padx=8, pady=10)
        
        self.widgets["subject"] = customtkinter.CTkComboBox(entry_frame, values=self.presenter.get_subjects(), width=150)
        self.widgets["subject"].set("Select Subject")
        self.widgets["subject"].grid(row=0, column=3, padx=8, pady=10)
        
        # Action buttons
        btn_frame = customtkinter.CTkFrame(self.tab)
        btn_frame.pack(pady=10)
        
        add_btn = customtkinter.CTkButton(btn_frame, text="Add Teacher", command=self._add_teacher)
        add_btn.grid(row=0, column=0, padx=10, pady=5)
        
        delete_btn = customtkinter.CTkButton(btn_frame, text="Delete Last Teacher", command=self._delete_teacher)
        delete_btn.grid(row=0, column=1, padx=10, pady=5)
        
        save_btn = customtkinter.CTkButton(btn_frame, text="Save Teachers", command=self._save_teachers)
        save_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Sort buttons
        sort_frame = customtkinter.CTkFrame(self.tab)
        sort_frame.pack(pady=5)
        
        sort_keys = self.presenter.get_sort_keys()
        for i, sort_key in enumerate(sort_keys):
            btn = customtkinter.CTkButton(sort_frame, text=f"Sort by {sort_key.capitalize()}", 
                                        command=lambda key=sort_key: self._sort_data(key))
            btn.grid(row=0, column=i, padx=3, pady=5)
    
    def _add_teacher(self):
        name = self.widgets["name"].get()
        salary = self.widgets["salary"].get()
        department = self.widgets["department"].get()
        subject = self.widgets["subject"].get()
        self.presenter.add_item(name, salary, department, subject)
    
    def _delete_teacher(self):
        self.presenter.delete_last_item()
    
    def _save_teachers(self):
        self.presenter.save_data()
    
    def _sort_data(self, key):
        self.presenter.sort_data(key)
    
    def refresh_display(self):
        """Refresh the display with current data"""
        display = self.widgets["display"]
        display.delete("1.0", customtkinter.END)
        
        header = f"{'#':<3} {'Name':<15} {'ID':<8} {'Salary':<10} {'Department':<15} {'Subject':<12}\n"
        separator = "=" * 75 + "\n"
        display.insert("1.0", header + separator)
        
        for i, teacher in enumerate(self.presenter.get_data(), 1):
            line = f"{i:<3} {teacher.name:<15} {teacher.id:<8} {teacher.salary:<10} {teacher.department:<15} {teacher.subject:<12}\n"
            display.insert(customtkinter.END, line)
    
    def clear_fields(self):
        """Clear input fields"""
        self.widgets["name"].delete(0, customtkinter.END)
        self.widgets["salary"].delete(0, customtkinter.END)
        self.widgets["department"].set("Select Department")
        self.widgets["subject"].set("Select Subject")


class AssistantTabView(BaseTabView):
    """View for managing assistants"""
    
    def _build_ui(self):
        # Title
        title = customtkinter.CTkLabel(self.tab, text="Assistants Management", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))
        
        # Display area
        self.widgets["display"] = customtkinter.CTkTextbox(self.tab, width=800, height=350, font=("Courier New", 10))
        self.widgets["display"].pack(pady=10)
        
        # Entry frame
        entry_frame = customtkinter.CTkFrame(self.tab)
        entry_frame.pack(pady=10, fill="x", padx=20)
        
        # Input fields
        self.widgets["name"] = customtkinter.CTkEntry(entry_frame, placeholder_text="Name", width=200)
        self.widgets["name"].grid(row=0, column=0, padx=8, pady=10)
        
        self.widgets["salary"] = customtkinter.CTkEntry(entry_frame, placeholder_text="Salary", width=150)
        self.widgets["salary"].grid(row=0, column=1, padx=8, pady=10)
        
        self.widgets["department"] = customtkinter.CTkComboBox(entry_frame, values=self.presenter.get_departments(), width=200)
        self.widgets["department"].set("Select Department")
        self.widgets["department"].grid(row=0, column=2, padx=8, pady=10)
        
        # Action buttons
        btn_frame = customtkinter.CTkFrame(self.tab)
        btn_frame.pack(pady=10)
        
        add_btn = customtkinter.CTkButton(btn_frame, text="Add Assistant", command=self._add_assistant)
        add_btn.grid(row=0, column=0, padx=10, pady=5)
        
        delete_btn = customtkinter.CTkButton(btn_frame, text="Delete Last Assistant", command=self._delete_assistant)
        delete_btn.grid(row=0, column=1, padx=10, pady=5)
        
        save_btn = customtkinter.CTkButton(btn_frame, text="Save Assistants", command=self._save_assistants)
        save_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Sort buttons
        sort_frame = customtkinter.CTkFrame(self.tab)
        sort_frame.pack(pady=5)
        
        sort_keys = self.presenter.get_sort_keys()
        for i, sort_key in enumerate(sort_keys):
            btn = customtkinter.CTkButton(sort_frame, text=f"Sort by {sort_key.capitalize()}", 
                                        command=lambda key=sort_key: self._sort_data(key))
            btn.grid(row=0, column=i, padx=3, pady=5)
    
    def _add_assistant(self):
        name = self.widgets["name"].get()
        salary = self.widgets["salary"].get()
        department = self.widgets["department"].get()
        self.presenter.add_item(name, salary, department)
    
    def _delete_assistant(self):
        self.presenter.delete_last_item()
    
    def _save_assistants(self):
        self.presenter.save_data()
    
    def _sort_data(self, key):
        self.presenter.sort_data(key)
    
    def refresh_display(self):
        """Refresh the display with current data"""
        display = self.widgets["display"]
        display.delete("1.0", customtkinter.END)
        
        header = f"{'#':<3} {'Name':<20} {'ID':<8} {'Salary':<12} {'Department':<20}\n"
        separator = "=" * 75 + "\n"
        display.insert("1.0", header + separator)
        
        for i, assistant in enumerate(self.presenter.get_data(), 1):
            line = f"{i:<3} {assistant.name:<20} {assistant.id:<8} {assistant.salary:<12} {assistant.department:<20}\n"
            display.insert(customtkinter.END, line)
    
    def clear_fields(self):
        """Clear input fields"""
        self.widgets["name"].delete(0, customtkinter.END)
        self.widgets["salary"].delete(0, customtkinter.END)
        self.widgets["department"].set("Select Department")