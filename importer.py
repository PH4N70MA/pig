from __model__.db.db_control import DBController
from config import host, user, password, db_name, port


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
            print(f"[INFO] Connected to PostgreSQL database. Version: {version}")
            print(f"[INFO] Tables in the database: {tables}")
            print(f"[INFO] Students: {students}")
            print(f"[INFO] Teachers: {teachers}")
            print(f"[INFO] Assistants: {assistants}")
    except RuntimeError as err:
        print(f"[ERROR] {err}")
    except Exception as ex:
        print("[ERROR] Error while connecting to PostgreSQL", ex)