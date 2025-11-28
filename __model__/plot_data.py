from __model__.data import read_json_students, read_json_teachers, read_json_assistants

# Function to get number of persons by speciality/department
def get_students_by_speciality(students=None):
    if students is None:
        students = read_json_students()
    counts = {}
    for s in students:
        key = getattr(s, 'speciality', 'Unknown')
        counts[key] = counts.get(key, 0) + 1
    return counts

def get_teachers_by_department(teachers=None):
    if teachers is None:
        teachers = read_json_teachers()
    counts = {}
    for t in teachers:
        key = getattr(t, 'department', 'Unknown')
        counts[key] = counts.get(key, 0) + 1
    return counts

def get_assistants_count_by_department(assistants=None):
    if assistants is None:
        assistants = read_json_assistants()
    counts = {}
    for a in assistants:
        dept = getattr(a, 'department', 'Unknown')
        counts[dept] = counts.get(dept, 0) + 1
    return counts

# Function to get grade distribution among students
def get_students_grade_distribution(students=None):
    if students is None:
        students = read_json_students()
    counts = {}
    for s in students:
        key = getattr(s, 'grade', 'Unknown')
        counts[key] = counts.get(key, 0) + 1
    return counts

# Function to get average salary of persons by department
def get_teachers_avg_salary_by_department(teachers=None):
    if teachers is None:
        teachers = read_json_teachers()
    sums = {}
    counts = {}
    for t in teachers:
        dept = getattr(t, 'department', 'Unknown')
        try:
            val = float(getattr(t, 'salary', 0))
        except Exception:
            continue
        sums[dept] = sums.get(dept, 0.0) + val
        counts[dept] = counts.get(dept, 0) + 1
    avg = {}
    for dept in sums:
        avg[dept] = sums[dept] / counts.get(dept, 1)
    return avg

def get_assistants_avg_salary_by_department(assistants=None):
    if assistants is None:
        assistants = read_json_assistants()
    sums = {}
    counts = {}
    for a in assistants:
        dept = getattr(a, 'department', 'Unknown')
        try:
            val = float(getattr(a, 'salary', 0))
        except Exception:
            continue
        sums[dept] = sums.get(dept, 0.0) + val
        counts[dept] = counts.get(dept, 0) + 1
    avg = {}
    for dept in sums:
        avg[dept] = sums[dept] / counts.get(dept, 1)
    return avg

def get_teachers_count_by_subject(teachers=None):
    if teachers is None:
        teachers = read_json_teachers()
    counts = {}
    for t in teachers:
        subject = getattr(t, 'subject', 'Unknown')
        counts[subject] = counts.get(subject, 0) + 1
    return counts