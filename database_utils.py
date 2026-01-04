import sqlite3
import pandas as pd
import re

def clean_column_name(name):
    """Sanitizes CSV headers for SQL compatibility."""
    name = name.lower().strip().replace(' ', '_')
    return re.sub(r'[^a-z0-9_]', '', name)

def load_csv_to_db(csv_path, db_path):
    """The Engine: Loads your 3,000+ product library into SQLite."""
    df = pd.read_csv(csv_path)
    # Clean all column names automatically
    df.columns = [clean_column_name(c) for c in df.columns]
    
    conn = sqlite3.connect(db_path)
    # 'replace' ensures that if you update the CSV, the DB updates too
    df.to_sql("library", conn, index=False, if_exists="replace")
    conn.close()
    return list(df.columns)

def get_schema_details(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema_string = ""
    for table in tables:
        t_name = table[0]
        schema_string += f"\nTable: {t_name}\nColumns:\n"
        cursor.execute(f"PRAGMA table_info({t_name});")
        for col in cursor.fetchall():
            schema_string += f"  - {col[1]} ({col[2]})\n"
    conn.close()
    return schema_string

def execute_query(db_path, query):
    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        return f"SQL_ERROR: {str(e)}"
    finally:
        conn.close()