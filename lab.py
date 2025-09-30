from model.data import read_json_students, read_json_teachers, read_json_assistants
from model.data import save_json_students, save_json_teachers, save_json_assistants
from model.humans import Student, Teacher, Assistant

import customtkinter
import random

class DataManagerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Manager - Students, Teachers, Assistants")
        self.geometry("900x700")
        
        # Configuration for each data type
        self.config = {
            "students": {
                "class": Student,
                "data": read_json_students(),
                "save_func": save_json_students,
                "id_prefix": "STU",
                "id_range": (1000, 9999),
                "fields": [
                    {"name": "name", "type": "entry", "width": 200, "placeholder": "Name"},
                    {"name": "grade", "type": "entry", "width": 100, "placeholder": "Grade"},
                    {"name": "speciality", "type": "combo", "width": 200, "values": ["Computer Science", "Mathematics", "Physics", "Engineering"]}
                ],
                "display_format": "{'#':<3} {'Name':<20} {'ID':<10} {'Grade':<8} {'Speciality':<20}",
                "row_format": lambda i, obj: f"{i:<3} {obj.name:<20} {obj.id:<10} {obj.grade:<8} {obj.speciality:<20}",
                "sort_keys": ["name", "grade", "speciality", "id"]
            },
            "teachers": {
                "class": Teacher,
                "data": read_json_teachers(),
                "save_func": save_json_teachers,
                "id_prefix": "TCH",
                "id_range": (100, 999),
                "fields": [
                    {"name": "name", "type": "entry", "width": 150, "placeholder": "Name"},
                    {"name": "salary", "type": "entry", "width": 120, "placeholder": "Salary"},
                    {"name": "department", "type": "combo", "width": 150, "values": ["Human Resources", "Finance", "Engineering", "Marketing"]},
                    {"name": "subject", "type": "combo", "width": 150, "values": ["Mathematics", "Physics", "Chemistry", "Biology"]}
                ],
                "display_format": "{'#':<3} {'Name':<15} {'ID':<8} {'Salary':<10} {'Department':<15} {'Subject':<12}",
                "row_format": lambda i, obj: f"{i:<3} {obj.name:<15} {obj.id:<8} {obj.salary:<10} {obj.department:<15} {obj.subject:<12}",
                "sort_keys": ["name", "department", "subject", "salary", "id"]
            },
            "assistants": {
                "class": Assistant,
                "data": read_json_assistants(),
                "save_func": save_json_assistants,
                "id_prefix": "AST",
                "id_range": (100, 999),
                "fields": [
                    {"name": "name", "type": "entry", "width": 200, "placeholder": "Name"},
                    {"name": "salary", "type": "entry", "width": 150, "placeholder": "Salary"},
                    {"name": "department", "type": "combo", "width": 200, "values": ["Human Resources", "Finance", "Engineering", "Marketing"]}
                ],
                "display_format": "{'#':<3} {'Name':<20} {'ID':<8} {'Salary':<12} {'Department':<20}",
                "row_format": lambda i, obj: f"{i:<3} {obj.name:<20} {obj.id:<8} {obj.salary:<12} {obj.department:<20}",
                "sort_keys": ["name", "department", "salary", "id"]
            }
        }
        
        self.widgets = {}  # Store widget references
        
        # Create tabview and tabs
        self.tabview = customtkinter.CTkTabview(self, width=850, height=650)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        for data_type in self.config.keys():
            tab = self.tabview.add(data_type.capitalize())
            self._build_tab(tab, data_type)
    
    def generate_id(self, data_type):
        """Generate unique ID for any data type"""
        config = self.config[data_type]
        existing_ids = [obj.id for obj in config["data"]]
        while True:
            new_id = f"{config['id_prefix']}{random.randint(*config['id_range'])}"
            if new_id not in existing_ids:
                return new_id
    
    def _build_tab(self, tab, data_type):
        """Generic tab builder"""
        config = self.config[data_type]
        
        # Title
        title = customtkinter.CTkLabel(tab, text=f"{data_type.capitalize()} Management", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))
        
        # Display area
        display = customtkinter.CTkTextbox(tab, width=800, height=350, font=("Courier New", 10))
        display.pack(pady=10)
        self.widgets[f"{data_type}_display"] = display
        
        # Entry frame
        entry_frame = customtkinter.CTkFrame(tab)
        entry_frame.pack(pady=10, fill="x", padx=20)
        
        # Create input fields
        self.widgets[f"{data_type}_fields"] = {}
        for i, field in enumerate(config["fields"]):
            if field["type"] == "entry":
                widget = customtkinter.CTkEntry(entry_frame, placeholder_text=field["placeholder"], width=field["width"])
            else:  # combo
                widget = customtkinter.CTkComboBox(entry_frame, values=field["values"], width=field["width"])
                widget.set(f"Select {field['name'].capitalize()}")
            
            widget.grid(row=0, column=i, padx=8, pady=10)
            self.widgets[f"{data_type}_fields"][field["name"]] = widget
        
        # Action buttons
        btn_frame = customtkinter.CTkFrame(tab)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("Add", lambda dt=data_type: self.add_item(dt)),
            ("Delete Last", lambda dt=data_type: self.delete_item(dt)),
            ("Save", lambda dt=data_type: self.save_data(dt))
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = customtkinter.CTkButton(btn_frame, text=f"{text} {data_type[:-1].capitalize()}", command=command)
            btn.grid(row=0, column=i, padx=10, pady=5)
        
        # Sort buttons
        sort_frame = customtkinter.CTkFrame(tab)
        sort_frame.pack(pady=5)
        
        for i, sort_key in enumerate(config["sort_keys"]):
            btn = customtkinter.CTkButton(sort_frame, text=f"Sort by {sort_key.capitalize()}", 
                                        command=lambda key=sort_key, dt=data_type: self.sort_data(dt, key))
            btn.grid(row=0, column=i, padx=3, pady=5)
        
        self.refresh_display(data_type)
    
    def refresh_display(self, data_type):
        """Generic display refresh"""
        config = self.config[data_type]
        display = self.widgets[f"{data_type}_display"]
        
        display.delete("1.0", customtkinter.END)
        header = config["display_format"] + "\n"
        separator = "=" * 75 + "\n"
        display.insert("1.0", header + separator)
        
        for i, obj in enumerate(config["data"], 1):
            line = config["row_format"](i, obj) + "\n"
            display.insert(customtkinter.END, line)
    
    def add_item(self, data_type):
        """Generic add method"""
        config = self.config[data_type]
        fields = self.widgets[f"{data_type}_fields"]
        
        # Get values from fields
        values = {}
        for field_name, widget in fields.items():
            if isinstance(widget, customtkinter.CTkComboBox):
                value = widget.get().strip()
                if value.startswith("Select"):
                    print(f"Error: Please select a valid {field_name}")
                    return
            else:
                value = widget.get().strip()
                if not value:
                    print(f"Error: Please fill the {field_name} field")
                    return
            values[field_name] = value
        
        # Generate ID and create object
        auto_id = self.generate_id(data_type)
        args = [values[field["name"]] for field in config["fields"]]
        new_obj = config["class"](args[0], auto_id, *args[1:])  # name, id, other_args
        
        config["data"].append(new_obj)
        self.refresh_display(data_type)
        
        # Clear fields
        for field_name, widget in fields.items():
            if isinstance(widget, customtkinter.CTkComboBox):
                widget.set(f"Select {field_name.capitalize()}")
            else:
                widget.delete(0, customtkinter.END)
        
        print(f"{data_type[:-1].capitalize()} added with ID: {auto_id}")
    
    def delete_item(self, data_type):
        """Generic delete method"""
        config = self.config[data_type]
        if config["data"]:
            deleted_obj = config["data"].pop()
            self.refresh_display(data_type)
            print(f"Deleted {data_type[:-1]}: {deleted_obj.name} (ID: {deleted_obj.id})")
    
    def sort_data(self, data_type, key):
        """Generic sort method"""
        config = self.config[data_type]
        
        if key == "name":
            config["data"].sort(key=lambda obj: obj.name.lower())
        elif key == "salary":
            config["data"].sort(key=lambda obj: float(obj.salary) if str(obj.salary).replace('.','').replace('-','').isdigit() else 0)
        else:
            config["data"].sort(key=lambda obj: getattr(obj, key))
        
        self.refresh_display(data_type)
        print(f"{data_type.capitalize()} sorted by {key}")
    
    def save_data(self, data_type):
        """Generic save method"""
        config = self.config[data_type]
        config["save_func"](config["data"])
        print(f"{data_type.capitalize()} saved!")

# Run the app
if __name__ == "__main__":
    app = DataManagerApp()
    app.mainloop()