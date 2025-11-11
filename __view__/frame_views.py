# import tkinter
import customtkinter
from PIL import Image

class BaseFrameTabView:

    def __init__(self, parent_tab, presenter):
        self.tab = parent_tab
        self.presenter = presenter
        self.presenter.set_view(self)
        self.widgets = {}
        self.person_frames = []
        
        # Get configuration from subclass
        self.config = self._get_config()
        
        self._build_ui()
        self.refresh_display()
    
    def _get_config(self):
        """Override in subclasses to provide field configuration"""
        raise NotImplementedError
        
    def _build_ui(self):
        """Build UI automatically from configuration"""
        # Title
        title = customtkinter.CTkLabel(self.tab, text=f"{self.config['name']} Management", 
                                     font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))
        
        # Input frame with dynamic fields
        self._build_input_frame()
        
        # Action and sort buttons
        self._build_buttons()
        
        # Scrollable display area
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.tab, width=800, height=400, label_text=f"All {self.config['name']}")
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    def _build_input_frame(self):
        """Build input frame dynamically from field configuration"""
        entry_frame = customtkinter.CTkFrame(self.tab)
        entry_frame.pack(pady=10, fill="x", padx=20)
        
        # Configure grid columns
        for i in range(len(self.config['fields'])):
            entry_frame.grid_columnconfigure(i, weight=1)
        
        # Create fields dynamically
        for i, field in enumerate(self.config['fields']):
            if field['type'] == 'entry':
                widget = customtkinter.CTkEntry(entry_frame, placeholder_text=field['label'])
            else:  # combobox
                widget = customtkinter.CTkComboBox(entry_frame, values=field['values'])
                widget.set(f"Select {field['label']}")
            
            widget.grid(row=0, column=i, padx=8, pady=10, sticky="ew")
            self.widgets[field['name']] = widget
    
    def _build_buttons(self):
        """Build action and sort buttons"""
        # Action buttons
        btn_frame = customtkinter.CTkFrame(self.tab)
        btn_frame.pack(pady=10)
        
        buttons = [
            (f"Add {self.config['name'][:-1]}", self._add_item),
            (f"Delete Last", self.presenter.delete_last_item),
            (f"Save", self.presenter.save_data)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = customtkinter.CTkButton(btn_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=10, pady=5)
        
        # Sort buttons
        sort_frame = customtkinter.CTkFrame(self.tab)
        sort_frame.pack(pady=5)
        
        for i, sort_key in enumerate(self.presenter.get_sort_keys()):
            btn = customtkinter.CTkButton(sort_frame, text=f"Sort by {sort_key.capitalize()}", 
                                        command=lambda k=sort_key: self.presenter.sort_data(k))
            btn.grid(row=0, column=i, padx=3, pady=5)
    
    def _create_person_frame(self, person, index):
        """Create frame for individual person"""
        person_frame = customtkinter.CTkFrame(self.scrollable_frame)
        person_frame.pack(pady=5, padx=10, fill="x")
        person_frame.grid_columnconfigure(1, weight=1)
        
        # Index
        customtkinter.CTkLabel(person_frame, text=f"#{index}", font=("Arial", 14, "bold"), 
                             width=50).grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        
        # Details frame
        details_frame = customtkinter.CTkFrame(person_frame)
        details_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self._populate_details(details_frame, person)
        
        # Action buttons
        actions_frame = customtkinter.CTkFrame(person_frame)
        actions_frame.grid(row=0, column=2, padx=(5, 10), pady=5)

        editImage = customtkinter.CTkImage(  light_image=Image.open('./img/edit.png'),
                                                        dark_image=Image.open('./img/edit.png'),
                                                        size=(20,20)  
                                        )
        customtkinter.CTkButton(actions_frame, text="", image=editImage, width=60, height=30,
                                fg_color="orange", hover_color="darkorange",
                                command=lambda: self._edit_person(person)).pack(pady=2)

        deleteImage = customtkinter.CTkImage(  light_image=Image.open('./img/delete.png'),
                                                dark_image=Image.open('./img/delete.png'),
                                                size=(20,20)  
                                            )
        customtkinter.CTkButton(actions_frame, text="", image=deleteImage, width=60, height=30,
                              fg_color="red", hover_color="darkred",
                              command=lambda: self._delete_person(person)).pack(pady=2)
        
        return person_frame
    
    def _populate_details(self, frame, person):
        """Populate person details dynamically"""
        for i in range(len(self.config['display_fields'])):
            frame.grid_columnconfigure(i, weight=1)
        
        for i, field in enumerate(self.config['display_fields']):
            # Label
            customtkinter.CTkLabel(frame, text=f"{field['label']}:", 
                                 font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5, sticky="w")
            # Value
            value = getattr(person, field['attr'])
            if field.get('prefix'):
                value = f"{field['prefix']}{value}"
            customtkinter.CTkLabel(frame, text=str(value)).grid(row=1, column=i, padx=5, pady=(0, 5), sticky="w")
    
    def refresh_display(self):
        """Refresh display by recreating frames"""
        for frame in self.person_frames:
            frame.destroy()
        self.person_frames.clear()
        
        for i, person in enumerate(self.presenter.get_data(), 1):
            frame = self._create_person_frame(person, i)
            self.person_frames.append(frame)
    
    def _add_item(self):
        """Add new item using field values"""
        values = []
        for field in self.config['fields']:
            widget = self.widgets[field['name']]
            if field['type'] == 'combobox':
                value = widget.get().strip()
                if value.startswith("Select"):
                    self.show_message(f"Error: Please select a {field['label'].lower()}")
                    return
            else:
                value = widget.get().strip()
                if not value:
                    self.show_message(f"Error: Please fill the {field['label'].lower()}")
                    return
            values.append(value)
        
        self.presenter.add_item(*values)
    
    def clear_fields(self):
        """Clear input fields"""
        for field in self.config['fields']:
            widget = self.widgets[field['name']]
            if field['type'] == 'combobox':
                widget.set(f"Select {field['label']}")
            else:
                widget.delete(0, customtkinter.END)
    
    def show_message(self, message):
        print(f"💬 {message}")
    
    def _edit_person(self, person):
        """Populate inputs for editing and turn Add button into Update."""
        # mark editing target
        self._editing_person = person

        # Populate fields from person attributes
        for field in self.config['fields']:
            widget = self.widgets[field['name']]
            # try to read attribute from person (field names are expected to match attrs)
            value = getattr(person, field['name'], "")
            if field['type'] == 'combobox':
                widget.set(str(value))
            else:
                widget.delete(0, customtkinter.END)
                widget.insert(0, str(value))

        # locate the "Add ..." button and modify it to perform an update
        def _find_add_button(widget):
            # recursive search for a CTkButton whose text starts with "Add "
            if isinstance(widget, customtkinter.CTkButton):
                try:
                    if str(widget.cget("text")).startswith("Add "):
                        return widget
                except Exception:
                    pass
            for child in widget.winfo_children():
                found = _find_add_button(child)
                if found:
                    return found
            return None

        add_btn = _find_add_button(self.tab)
        if add_btn is None:
            self.show_message("Error: Add button not found; cannot enter edit mode.")
            return

        orig_text = add_btn.cget("text")

        def do_update():
            # collect values with same validation as _add_item
            values = []
            for field in self.config['fields']:
                widget = self.widgets[field['name']]
                if field['type'] == 'combobox':
                    value = widget.get().strip()
                    if value.startswith("Select"):
                        self.show_message(f"Error: Please select a {field['label'].lower()}")
                        return
                else:
                    value = widget.get().strip()
                    if not value:
                        self.show_message(f"Error: Please fill the {field['label'].lower()}")
                        return
                values.append(value)

            # apply values to the person object (assumes field names match attributes)
            for field, val in zip(self.config['fields'], values):
                setattr(person, field['name'], val)

            # finish editing
            self.clear_fields()
            add_btn.configure(text=orig_text, command=self._add_item)
            # remove cancel button if present
            try:
                cancel_btn.destroy()
            except Exception:
                pass

            self._editing_person = None
            self.refresh_display()
            self.presenter.save_data()
            self.show_message(f"Updated {person.name} (ID: {person.id})")

        # cancel editing helper
        def cancel_edit():
            self.clear_fields()
            add_btn.configure(text=orig_text, command=self._add_item)
            try:
                cancel_btn.destroy()
            except Exception:
                pass
            self._editing_person = None
            self.show_message("Edit cancelled")

        # replace add button behaviour
        add_btn.configure(text="Update", command=do_update)

        # create a Cancel button next to the Add/Update button to abort edit
        try:
            parent = add_btn.master
            info = add_btn.grid_info()
            col = int(info.get("column", 0)) + 1
            cancel_btn = customtkinter.CTkButton(parent, text="Cancel", command=cancel_edit)
            cancel_btn.grid(row=info.get("row", 0), column=col, padx=10, pady=5)
        except Exception:
            # if grid placement fails, fall back to no cancel button
            cancel_btn = None

        self.show_message(f"Editing {person.name} (ID: {person.id}) - make changes and click Update")
    
    def _delete_person(self, person):
        data = self.presenter.get_data()
        if person in data:
            data.remove(person)
            self.refresh_display()
            self.show_message(f"Deleted {person.name} (ID: {person.id})")
            self.presenter.save_data()


class StudentFrameTabView(BaseFrameTabView):
    """Student management view"""
    
    def _get_config(self):
        return {
            'name': 'Students',
            'fields': [
                {'name': 'name', 'type': 'entry', 'label': 'Name'},
                {'name': 'grade', 'type': 'entry', 'label': 'Grade'},
                {'name': 'speciality', 'type': 'combobox', 'label': 'Speciality', 
                 'values': self.presenter.get_specialities()}
            ],
            'display_fields': [
                {'label': 'Name', 'attr': 'name'},
                {'label': 'ID', 'attr': 'id'},
                {'label': 'Grade', 'attr': 'grade'},
                {'label': 'Speciality', 'attr': 'speciality'}
            ]
        }


class TeacherFrameTabView(BaseFrameTabView):
    """Teacher management view"""
    
    def _get_config(self):
        return {
            'name': 'Teachers',
            'fields': [
                {'name': 'name', 'type': 'entry', 'label': 'Name'},
                {'name': 'salary', 'type': 'entry', 'label': 'Salary'},
                {'name': 'department', 'type': 'combobox', 'label': 'Department', 
                 'values': self.presenter.get_departments()},
                {'name': 'subject', 'type': 'combobox', 'label': 'Subject', 
                 'values': self.presenter.get_subjects()}
            ],
            'display_fields': [
                {'label': 'Name', 'attr': 'name'},
                {'label': 'ID', 'attr': 'id'},
                {'label': 'Salary', 'attr': 'salary', 'prefix': '$'},
                {'label': 'Department', 'attr': 'department'},
                {'label': 'Subject', 'attr': 'subject'}
            ]
        }


class AssistantFrameTabView(BaseFrameTabView):
    """Assistant management view"""
    
    def _get_config(self):
        return {
            'name': 'Assistants',
            'fields': [
                {'name': 'name', 'type': 'entry', 'label': 'Name'},
                {'name': 'salary', 'type': 'entry', 'label': 'Salary'},
                {'name': 'department', 'type': 'combobox', 'label': 'Department', 
                 'values': self.presenter.get_departments()}
            ],
            'display_fields': [
                {'label': 'Name', 'attr': 'name'},
                {'label': 'ID', 'attr': 'id'},
                {'label': 'Salary', 'attr': 'salary', 'prefix': '$'},
                {'label': 'Department', 'attr': 'department'}
            ]
        }