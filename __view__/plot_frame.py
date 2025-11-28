import customtkinter



class PlotFrame(customtkinter.CTkFrame):
    """A CTkFrame that embeds matplotlib figures.

    Use by instantiating with a PlotPresenter instance and calling UI methods
    (e.g. the user selects a plot type and presses Render).
    """

    def __init__(self, master, presenter, **kwargs):
        super().__init__(master, **kwargs)
        self.presenter = presenter
        self.presenter_frame = None
        self._current_canvas = None

        # Pack this frame into the provided parent so it becomes visible
        # following the pattern used elsewhere in the project where views
        # create widgets directly inside their parent tab. Packing here keeps
        # PlotFrame self-contained and visible when the tab is activated.
        self.pack(fill='both', expand=True)

        self._build_ui()
        # Render the initial/default plot so the tab shows content immediately.
        try:
            self.render_selected()
        except RuntimeError:
            # If matplotlib isn't installed, avoid crashing during import/UI setup.
            # The user will see an error when trying to render manually.
            pass

    def _build_ui(self):
        header = customtkinter.CTkLabel(self, text="Charts", font=("Arial", 18, "bold"))
        header.pack(pady=(8, 10))

        control_frame = customtkinter.CTkFrame(self)
        control_frame.pack(padx=10, pady=8, fill='x')

        # Available plot types — keep in sync with presenter supported types
        self.plot_types = [
            ('Students by Speciality', 'students_by_speciality'),
            ('Teachers by Department', 'teachers_by_department'),
            ('Assistants by Department', 'assistants_by_department'),
            ('Grade Distribution', 'students_grade_distribution'),
            ('Teachers Avg Salary by Department', 'teachers_avg_salary_by_department'),
            ('Assistants Avg Salary by Department', 'assistants_avg_salary_by_department'),
            ('Teachers by Subject', 'teachers_count_by_subject'),
        ]

        labels = [p[0] for p in self.plot_types]
        self.option_menu = customtkinter.CTkOptionMenu(control_frame, values=labels)
        self.option_menu.set(labels[0])
        self.option_menu.grid(row=0, column=0, padx=8, pady=6, sticky='w')

        render_btn = customtkinter.CTkButton(control_frame, text="Render", command=self.render_selected)
        render_btn.grid(row=0, column=1, padx=8, pady=6)

        # area for the matplotlib canvas
        self.canvas_holder = customtkinter.CTkFrame(self)
        self.canvas_holder.pack(padx=10, pady=10, fill='both', expand=True)

    def render_selected(self):
        label = self.option_menu.get()
        # map label back to plot key
        key = None
        for l, k in self.plot_types:
            if l == label:
                key = k
                break
        if key is None:
            return
        fig = self.presenter.create_figure(key)
        self.show_figure(fig)

    def show_figure(self, fig):
        """Embed the given matplotlib Figure into this frame, removing previous canvas if any."""
        # destroy existing canvas
        if self._current_canvas is not None:
            try:
                self._current_canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self._current_canvas = None

        # Import the TkAgg canvas lazily to avoid hard dependency at module import
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ModuleNotFoundError as e:
            raise RuntimeError("matplotlib is required to display plots. Install it with `pip install matplotlib`") from e

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_holder)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill='both', expand=True)
        self._current_canvas = canvas
