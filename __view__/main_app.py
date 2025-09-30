import customtkinter

from __presenter__.data_presenter import StudentPresenter, TeacherPresenter, AssistantPresenter
from __view__.tab_views import StudentTabView, TeacherTabView, AssistantTabView


class DataManagerApp(customtkinter.CTk):
    """Main application window implementing MVP pattern"""
    
    def __init__(self):
        super().__init__()
        self.title("Data Manager - Students, Teachers, Assistants")
        self.geometry("900x700")
        
        # Create presenters
        self.student_presenter = StudentPresenter()
        self.teacher_presenter = TeacherPresenter()
        self.assistant_presenter = AssistantPresenter()
        
        # Create UI
        self._create_ui()
        
    def _create_ui(self):
        """Create the user interface"""
        # Create tabview
        self.tabview = customtkinter.CTkTabview(self, width=850, height=650)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Create tabs
        students_tab = self.tabview.add("Students")
        teachers_tab = self.tabview.add("Teachers")
        assistants_tab = self.tabview.add("Assistants")
        
        # Create tab views with their respective presenters
        self.student_view = StudentTabView(students_tab, self.student_presenter)
        self.teacher_view = TeacherTabView(teachers_tab, self.teacher_presenter)
        self.assistant_view = AssistantTabView(assistants_tab, self.assistant_presenter)


def main():
    """Main entry point"""
    app = DataManagerApp()
    app.mainloop()


if __name__ == "__main__":
    main()