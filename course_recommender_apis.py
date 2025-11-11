import pyodbc
from fastapi import HTTPException
from typing import List, Dict, Any

# This file contains common database utility functions 
# used by other modules like course_recommender_apis.py.
# Database connection parameters
# Read database settings from environment variables
DB_SERVER = os.environ.get('DB_SERVER', 'mist-mikky.database.windows.net')
DB_DATABASE = os.environ.get('DB_DATABASE', 'Course_Recommender_MikkyDB')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DRIVER = '{ODBC Driver 18 for SQL Server}'  # Use 18 for Azure SQL

def get_db_connection():
    """
    Returns a pyodbc connection to the Azure SQL Database.
    Raises HTTPException(500) if connection fails.
    """
    try:
        conn_str = (
            f'DRIVER={DB_DRIVER};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_DATABASE};'
            f'UID={DB_USERNAME};'
            f'PWD={DB_PASSWORD};'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

def _rows_to_dicts(cursor, rows) -> List[Dict[str, Any]]:
    """
    Converts a pyodbc cursor row list to a list of dictionaries.
    Each dictionary represents a row with column names as keys.
    """
    cols = [c[0] for c in cursor.description] if cursor.description else []
    result = []
    for row in rows:
        row_dict = {}
        for idx, col in enumerate(cols):
            row_dict[col] = row[idx]
        result.append(row_dict)
    return result