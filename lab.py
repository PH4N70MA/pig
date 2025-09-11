# Classs
from teacher.teacher import Teacher
from student.student import Student
from assistant.assistant import Assistant

# Graphic interface
import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")  # Increased window size
        self.title("School Management System")
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")

        # Main layout: left for controls, right for log
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left frame for controls
        self.left_frame = customtkinter.CTkFrame(self.main_frame, width=500)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)
        self.left_frame.pack_propagate(False)

        # Header
        self.header = customtkinter.CTkLabel(self.left_frame, text="School Management", font=("Arial", 28, "bold"))
        self.header.pack(pady=(20, 10))

        # Data type selection
        self.data_type_label = customtkinter.CTkLabel(self.left_frame, text="Select Type:", font=("Arial", 16))
        self.data_type_label.pack(pady=(10, 0))
        self.data_type = customtkinter.CTkOptionMenu(self.left_frame, values=["Teacher", "Student", "Assistant"], command=self.update_inputs)
        self.data_type.pack(pady=5)

        # Dynamic input fields
        self.inputs_frame = customtkinter.CTkFrame(self.left_frame, corner_radius=15)
        self.inputs_frame.pack(pady=10, padx=20, fill="x")
        self.input_widgets = {}
        self.create_inputs("Teacher")  # Default

        # Button frame
        self.button_frame = customtkinter.CTkFrame(self.left_frame, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.add_btn = customtkinter.CTkButton(self.button_frame, text="Add", command=self.add_data, width=120)
        self.add_btn.grid(row=0, column=0, padx=10)

        self.edit_btn = customtkinter.CTkButton(self.button_frame, text="Edit", command=self.edit_data, width=120)
        self.edit_btn.grid(row=0, column=1, padx=10)

        self.view_btn = customtkinter.CTkButton(self.button_frame, text="View All", command=self.view_data, width=120)
        self.view_btn.grid(row=0, column=2, padx=10)

        # Right frame for log
        self.right_frame = customtkinter.CTkFrame(self.main_frame, width=350, corner_radius=15)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)
        self.right_frame.pack_propagate(False)

        self.listbox_label = customtkinter.CTkLabel(self.right_frame, text="Records Log", font=("Arial", 16, "bold"))
        self.listbox_label.pack(pady=(10, 0))
        self.listbox = customtkinter.CTkTextbox(self.right_frame, width=320, height=520, font=("Consolas", 13))
        self.listbox.pack(pady=10, padx=10, fill="both", expand=True)

        self.data = {"Teacher": [], "Student": [], "Assistant": []}

    def create_inputs(self, dtype):
        # Clear previous widgets
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        self.input_widgets.clear()

        # Define fields for each type
        fields = {
            "Teacher": [
                ("Name", "entry"),
                ("ID", "entry"),
                ("Salary", "entry"),
                ("Department", "optionmenu", ["Human Resources", "Finance", "Engineering", "Marketing"]),
                ("Subject", "optionmenu", ["Mathematics", "Physics", "Chemistry", "Biology"])
            ],
            "Student": [
                ("Name", "entry"),
                ("ID", "entry"),
                ("Grade", "entry"),
                ("Speciality", "optionmenu", ["Computer Science", "Mathematics", "Physics", "Engineering"])
            ],
            "Assistant": [
                ("Name", "entry"),
                ("ID", "entry"),
                ("Salary", "entry"),
                ("Department", "optionmenu", ["Human Resources", "Finance", "Engineering", "Marketing"])
            ]
        }
        for field in fields[dtype]:
            label = customtkinter.CTkLabel(self.inputs_frame, text=field[0]+":", font=("Arial", 13))
            label.pack(pady=(8, 0), anchor="w", padx=10)
            if field[1] == "entry":
                entry = customtkinter.CTkEntry(self.inputs_frame, placeholder_text=f"Enter {field[0]}", width=350)
                entry.pack(pady=2, padx=10)
                self.input_widgets[field[0]] = entry
            elif field[1] == "optionmenu":
                option = customtkinter.CTkOptionMenu(self.inputs_frame, values=field[2], width=350)
                option.pack(pady=2, padx=10)
                self.input_widgets[field[0]] = option

    def update_inputs(self, dtype):
        self.create_inputs(dtype)

    def add_data(self):
        dtype = self.data_type.get()
        values = {}
        for field, widget in self.input_widgets.items():
            if isinstance(widget, customtkinter.CTkEntry):
                values[field] = widget.get()
            elif isinstance(widget, customtkinter.CTkOptionMenu):
                values[field] = widget.get()
        if all(values.values()):
            if dtype == "Teacher":
                obj = Teacher(
                    values["Name"],
                    values["ID"],
                    values["Salary"],
                    values["Department"],
                    values["Subject"]
                )
            elif dtype == "Student":
                obj = Student(
                    values["Name"],
                    values["ID"],
                    values["Grade"],
                    values["Speciality"]
                )
            else:
                obj = Assistant(
                    values["Name"],
                    values["ID"],
                    values["Salary"],
                    values["Department"]
                )
            self.data[dtype].append(obj)
            self.listbox.insert("end", f"✅ Added {dtype}: {values['Name']}\n")
            for widget in self.input_widgets.values():
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.delete(0, "end")
        else:
            self.listbox.insert("end", "⚠️ Please fill all fields\n")

    def edit_data(self):
        dtype = self.data_type.get()
        name = self.input_widgets.get("Name").get()
        found = False
        for obj in self.data[dtype]:
            if hasattr(obj, "name") and obj.name == name:
                # Update all fields except name
                for field, widget in self.input_widgets.items():
                    if field != "Name" and hasattr(obj, field.replace(" ", "_").lower()):
                        if isinstance(widget, customtkinter.CTkEntry):
                            setattr(obj, field.replace(" ", "_").lower(), widget.get())
                        elif isinstance(widget, customtkinter.CTkOptionMenu):
                            setattr(obj, field.replace(" ", "_").lower(), widget.get())
                obj.name = name + " (edited)"
                self.listbox.insert("end", f"✏️ Edited {dtype}: {obj.name}\n")
                found = True
                break
        if not found:
            self.listbox.insert("end", f"❌ {dtype} '{name}' not found for edit\n")

    def view_data(self):
        self.listbox.delete("1.0", "end")
        for dtype, objs in self.data.items():
            self.listbox.insert("end", f"--- {dtype}s ---\n")
            for obj in objs:
                attrs = [f"{attr}: {getattr(obj, attr)}" for attr in vars(obj)]
                self.listbox.insert("end", f"  • {', '.join(attrs)}\n")
            self.listbox.insert("end", "\n")

app = App()
app.mainloop()