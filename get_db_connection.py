# get_db_connection.py

import pyodbc
import os
from fastapi import HTTPException

from fastapi import FastAPI
from course_recommender_apis import get_db_connection, _rows_to_dicts

app = FastAPI(title="Course Recommender API")

def get_db_connection():
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER')};"
            f"DATABASE={os.environ.get('DB_DATABASE')};"
            f"UID={os.environ.get('DB_USERNAME')};"
            f"PWD={os.environ.get('DB_PASSWORD')};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return pyodbc.connect(connection_string)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
