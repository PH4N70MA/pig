from __model__ import plot_data as model_data
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
class PlotPresenter:

    def __init__(self):
        # no view here; the view will call create_figure and embed the returned Figure
        pass

    def create_figure(self, plot_type: str, **kwargs):
        # Import matplotlib lazily so module import does not fail when matplotlib
        # is not installed. This keeps the rest of the application usable.
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.subplots()
        


        if plot_type == 'students_by_speciality':
            counts = model_data.get_students_by_speciality()
            labels = list(counts.keys())
            values = [counts[k] for k in labels]
            if sum(values) == 0:
                ax.text(0.5, 0.5, 'No student data', ha='center')
            else:
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title('Students by Speciality')
                ax.axis('equal')

        elif plot_type == 'teachers_by_department':
            counts = model_data.get_teachers_count_by_subject()
            labels = list(counts.keys())
            values = [counts[k] for k in labels]
            if sum(values) == 0:
                ax.text(0.5, 0.5, 'No teacher data', ha='center')
            else:
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title('Teachers by Subject')
                ax.axis('equal')

        elif plot_type == 'assistants_by_department':
            counts = model_data.get_assistants_count_by_department()
            labels = list(counts.keys())
            values = [counts[k] for k in labels]
            if sum(values) == 0:
                ax.text(0.5, 0.5, 'No assistant data', ha='center')
            else:
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title('Assistants by Department')
                ax.axis('equal')

        elif plot_type == 'students_grade_distribution':
            counts = model_data.get_students_grade_distribution()
            labels = list(counts.keys())
            values = [counts[k] for k in labels]
            if sum(values) == 0:
                ax.text(0.5, 0.5, 'No grade data', ha='center')
            else:
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title('Grade Distribution')
                ax.axis('equal')

        elif plot_type == 'teachers_avg_salary_by_department':
            avg = model_data.get_teachers_avg_salary_by_department()
            labels = list(avg.keys())
            values = [avg[k] for k in labels]
            ax.bar(labels, values, color='tab:orange')
            ax.set_title('Teachers — Avg Salary by Department')
            ax.set_ylabel('Average Salary')
            ax.set_xticklabels(labels, rotation=30, ha='right')

        elif plot_type == 'assistants_avg_salary_by_department':
            avg = model_data.get_assistants_avg_salary_by_department()
            labels = list(avg.keys())
            values = [avg[k] for k in labels]
            ax.bar(labels, values, color='tab:purple')
            ax.set_title('Assistants — Avg Salary by Department')
            ax.set_ylabel('Average Salary')
            ax.set_xticklabels(labels, rotation=30, ha='right')

        elif plot_type == 'teachers_count_by_subject':
            counts = model_data.get_teachers_count_by_subject()
            labels = list(counts.keys())
            values = [counts[k] for k in labels]
            if sum(values) == 0:
                ax.text(0.5, 0.5, 'No teacher data', ha='center')
            else:
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title('Teachers by Subject')
                ax.axis('equal')

        else:
            ax.text(0.5, 0.5, f'Unknown plot type: {plot_type}', ha='center')

        fig.tight_layout()
        return fig
