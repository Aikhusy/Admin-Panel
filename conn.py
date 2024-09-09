import pyodbc
from tkinter import messagebox
import JsonConfig as jc

data= jc.get_json_config('config.json')

# Fungsi untuk membuat koneksi ke SQL Server
def connect_db():
    server = data['Server']  # Ganti dengan server SQL Server Anda
    database = data['Database']  # Ganti dengan nama database
    username = data['UID']  # Ganti dengan username SQL Server
    password = data['PWD']  # Ganti dengan password SQL Server
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None
