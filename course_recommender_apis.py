import os
import pyodbc
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env (optional for local development)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# FastAPI app
from fastapi import FastAPI

app = FastAPI(title="Course Recommender API")

# -----------------------------
# Database Connection Function
# -----------------------------
def get_db_connection():
    """
    Connect to Azure SQL Database using environment variables.
    """
    env = 'PRODUCTION'  # or use os.getenv("ENVIRONMENT")

    if env == 'PRODUCTION':
        DB_SERVER = os.getenv('DB_SERVER')  # e.g., tcp:mist-mikky.database.windows.net,1433
        DB_DATABASE = os.getenv('DB_DATABASE')  # Course_Recommender_MikkyDB
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')

        # Remove tcp: prefix if present
        if DB_SERVER.startswith("tcp:"):
            DB_SERVER = DB_SERVER[4:]

        connection_string = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_DATABASE};'
            f'UID={DB_USERNAME};'
            f'PWD={DB_PASSWORD};'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
    else:
        # Local development
        DB_SERVER = "localhost"
        DB_DATABASE = "Course_Recommender_MikkyDB"

        connection_string = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_DATABASE};'
            'Trusted_Connection=yes;'
            'TrustServerCertificate=yes;'
            'Encrypt=yes;'
            'Connection Timeout=30;'
        )

    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Utility Function
# -----------------------------
def _rows_to_dicts(cursor, rows):
    """
    Convert database rows to list of dictionaries.
    """
    cols = [c[0] for c in cursor.description] if cursor.description else []
    result = []
    for row in rows:
        row_dict = {}
        for idx, col in enumerate(cols):
            row_dict[col] = row[idx]
        result.append(row_dict)
    return result


# -----------------------------
# Example Endpoint
# -----------------------------
@app.get("/test-db")
def test_db_connection():
    """
    Test endpoint to verify database connection.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 * FROM sys.tables")  # simple test query
        rows = cursor.fetchall()
        return {"tables": _rows_to_dicts(cursor, rows)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
