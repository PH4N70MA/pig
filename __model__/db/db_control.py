from config import host, user, password, db_name, port

class DBController:

    def __init__(self, host_=None, user_=None, password_=None, dbname_=None, port_=None):
        self.host = host_ or host
        self.user = user_ or user
        self.password = password_ or password
        self.dbname = dbname_ or db_name
        self.port = port_ or port
        # default connection timeout in seconds to avoid long hangs
        self.connect_timeout = 5
        self.connection = None

    def connect(self):
        try:
            import psycopg
        except ModuleNotFoundError as e:
            raise RuntimeError("psycopg is required to connect to PostgreSQL. Install with `pip install psycopg`") from e

        try:
            # set a short connect timeout to fail fast if DB is unreachable
            self.connection = psycopg.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.dbname,
                port=self.port,
                connect_timeout=self.connect_timeout,
            )
        except Exception as exc:
            # propagate the exception so caller can decide how to handle it
            raise

    def fetch_version(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            return cursor.fetchone()
        
    def addStudent(self, name, age, speciality):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO students (name, age, speciality) VALUES (%s, %s, %s);",
                (name, age, speciality)
            )
            self.connection.commit()
    
    def addTeacher(self, name, department, salary, subject):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO teachers (name, department, salary, subject) VALUES (%s, %s, %s, %s);",
                (name, department, salary, subject)
            )
            self.connection.commit()

    def addAssistant(self, name, department, salary):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO assistants (name, department, salary) VALUES (%s, %s, %s);",
                (name, department, salary)
            )
            self.connection.commit()
        
    def createStudentTable(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    age INT,
                    speciality VARCHAR(100)
                );
            """)
            self.connection.commit()

    def createTeacherTable(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    department VARCHAR(100),
                    salary NUMERIC,
                    subject VARCHAR(100)
                );
            """)
            self.connection.commit()

    def createAssistantTable(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assistants (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    department VARCHAR(100),
                    salary NUMERIC
                );
            """)
            self.connection.commit()

    def createAllTables(self): 
        self.createStudentTable()
        self.createTeacherTable()
        self.createAssistantTable()
    

    def close(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception:
                pass
            finally:
                self.connection = None

    def __enter__(self):
        if not self.connection:
            self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def show_tables(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
            tables = cursor.fetchall()
            return [table[0] for table in tables]
    
    def showStudents(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students;")
            students = cursor.fetchall()
            return students
        
    def showTeachers(self): 
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM teachers;")
            teachers = cursor.fetchall()
            return teachers
    
    def showAssistants(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM assistants;")
            assistants = cursor.fetchall()
            return assistants
        
    def getStudentSpecialities(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT speciality, COUNT(*) AS student_count
                FROM students
                GROUP BY speciality
                ORDER BY student_count DESC;
            """)
            rows = cursor.fetchall()
            return [(row[0], row[1]) for row in rows]
    
    def getTeacherDepartments(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT department, COUNT(*) AS teacher_count
                FROM teachers
                GROUP BY department
                ORDER BY teacher_count DESC;
            """)
            rows = cursor.fetchall()
            return [(row[0], row[1]) for row in rows]
        
    def getAssistantDepartments(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT department, COUNT(*) AS assistant_count
                FROM assistants
                GROUP BY department
                ORDER BY assistant_count DESC;
            """)
            rows = cursor.fetchall()
            return [(row[0], row[1]) for row in rows]
        
    def getStudentAgesRepartition(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT age, COUNT(*) AS age_count FROM students GROUP BY age ORDER BY age;")
            rows = cursor.fetchall()
            return [(row[0], row[1]) for row in rows]
        
    def getTeacherSalariesAVGByDepartment(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT department, AVG(salary) AS avg_salary
                FROM teachers
                GROUP BY department;
            """)
            rows = cursor.fetchall()
            return [(row[0], float(row[1])) for row in rows]
        
    def getAssistantSalariesAVGByDepartment(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT department, AVG(salary) AS avg_salary
                FROM assistants
                GROUP BY department;
            """)
            rows = cursor.fetchall()
            return [(row[0], float(row[1])) for row in rows]
        
    def getTeacherSubjects(self):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT subject, COUNT(*) AS subject_count
                FROM teachers
                GROUP BY subject
                ORDER BY subject_count DESC;
            """)
            rows = cursor.fetchall()
            return [(row[0], row[1]) for row in rows]
    
    def deleteStudent(self, id_):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id = %s;", (id_,))
            self.connection.commit()
            return True
    
    def deleteTeacher(self, id_):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM teachers WHERE id = %s;", (id_,))
            self.connection.commit()
            return True
        
    def deleteAssistant(self, id_):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM assistants WHERE id = %s;", (id_,))
            self.connection.commit()
            return True


if __name__ == "__main__":
    try:
        with DBController(host, user, password, db_name, port) as db:
            version = db.fetch_version()
            # db.createAllTables()
            # db.addAssistant("John Doe", "Engineering", 50000)
            # db.addTeacher("Jane Smith", "Mathematics", 60000, "Chemistry")
            # db.addStudent("Alice Johnson", 20, "Computer Science")

            tables = db.show_tables()
            students = db.showStudents()
            teachers = db.showTeachers()
            assistants = db.showAssistants()
            students_specialities = db.getStudentSpecialities()
            print(f"[INFO] Connected to PostgreSQL database. Version: {version}")
            print(f"[INFO] Tables in the database: {tables}")
            print(f"[INFO] Students: {students}")
            print(f"[INFO] Teachers: {teachers}")
            print(f"[INFO] Assistants: {assistants}")
            print(f"[INFO] Students' Specialities: {students_specialities}")
    except RuntimeError as err:
        print(f"[ERROR] {err}")
    except Exception as ex:
        print("[ERROR] Error while connecting to PostgreSQL", ex)