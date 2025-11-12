import os
import pyodbc
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pathlib import Path

# -----------------------------
# Load environment variables
# -----------------------------
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Course Recommender API")

# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    env = "PRODUCTION"

    if env == "PRODUCTION":
        DB_SERVER = os.getenv("DB_SERVER")  # tcp:mist-mikky.database.windows.net,1433
        DB_DATABASE = os.getenv("DB_DATABASE")  # Course_Recommender_MikkyDB
        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        if DB_SERVER.startswith("tcp:"):
            DB_SERVER = DB_SERVER[4:]

        connection_string = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
    else:
        DB_SERVER = "localhost"
        DB_DATABASE = "Course_Recommender_MikkyDB"
        connection_string = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
            "Encrypt=yes;"
            "Connection Timeout=30;"
        )

    try:
        return pyodbc.connect(connection_string)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


# -----------------------------
# Utility
# -----------------------------
def _rows_to_dicts(cursor, rows):
    cols = [c[0] for c in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in rows]


# -----------------------------
# Test DB Connection
# -----------------------------
@app.get("/test-db")
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 name FROM sys.tables")
        rows = cursor.fetchall()
        return {"tables": _rows_to_dicts(cursor, rows)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
#                Import Functionality Modules
# ==========================================================
from validate_user import validate_user
from check_prereqs import check_prereqs
from find_current_semester_course_offering import find_current_semester_course_offerings
from find_prerequisites import find_prerequisites
from get_student_enrolled_course_offerings import get_student_enrolled_course_offerings
from enroll_student import enroll_student
from drop_student import drop_student


# ==========================================================
#                Define API Endpoints
# ==========================================================

@app.get("/validate_user/")
def validate_user_api(student_id: str):
    return validate_user(student_id)


@app.get("/check_prereqs/")
def check_prereqs_api(student_id: str, subject_code: str):
    return check_prereqs(student_id, subject_code)


@app.get("/find_current_semester_course_offerings/")
def find_current_semester_course_offerings_api(subject_code: str, course_number: str):
    return find_current_semester_course_offerings(subject_code, course_number)


@app.get("/find_prerequisites/")
def find_prerequisites_api(subject_code: str):
    return find_prerequisites(subject_code)


@app.get("/get_student_enrolled_course_offerings/")
def get_student_enrolled_course_offerings_api(student_id: str):
    return get_student_enrolled_course_offerings(student_id)


@app.post("/enroll_student/")
def enroll_student_api(student_id: str, courseOfferingId: int):
    return enroll_student(student_id, courseOfferingId)


@app.delete("/drop_student/")
def drop_student_api(student_id: str, courseOfferingId: int):
    return drop_student(student_id, courseOfferingId)
