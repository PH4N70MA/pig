import customtkinter

from __presenter__.data_presenter import StudentPresenter, TeacherPresenter, AssistantPresenter
from __view__.frame_views import StudentFrameTabView, TeacherFrameTabView, AssistantFrameTabView
from __presenter__.plot_presenter import PlotPresenter
from __view__.plot_frame import PlotFrame


class DataManagerApp(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("Data Manager")
        self.geometry("1200x800")
        
        # Tab configuration - easy to extend
        self.tabs = [
            {"name": "👨‍🎓 Students", "presenter": StudentPresenter, "view": StudentFrameTabView},
            {"name": "👨‍🏫 Teachers", "presenter": TeacherPresenter, "view": TeacherFrameTabView},
            {"name": "👨‍💼 Assistants", "presenter": AssistantPresenter, "view": AssistantFrameTabView},
            {"name": "📊 Charts", "presenter": PlotPresenter, "view": PlotFrame},
        ]
        
        self._create_ui()
    
    def _create_ui(self):
        """Create UI automatically from configuration"""
        # Create tabview
        self.tabview = customtkinter.CTkTabview(self, width=1150, height=750)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Create tabs automatically
        self.tab_views = {}
        for tab_config in self.tabs:
            tab = self.tabview.add(tab_config["name"])
            presenter = tab_config["presenter"]()
            view = tab_config["view"](tab, presenter)
            self.tab_views[tab_config["name"]] = view

def main():
    app = DataManagerApp()
    app.mainloop()


if __name__ == "__main__":
    main()