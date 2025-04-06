# db.py
import duckdb
import pandas as pd

DB_PATH = "final_project.duckdb"

def get_connection():
    return duckdb.connect(DB_PATH)

def get_city_demographics():
    with get_connection() as con:
        return con.execute("SELECT * FROM city_demographics_view").df()