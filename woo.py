import csv
import random
import sqlite3
from sqlite3 import Error
idx = random.randint(1,121)

def connect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print("database connected.")
        return conn
    except Error as e:
        print(e)

        
db_filename = "mlheroes.db"
conn = connect_db(db_filename)

def create_table(conn):
    sql = '''CREATE TABLE heroes(
            Serial INTEGER UNIQUE PRIMARY KEY,
            Name TEXT UNIQUE,
            Role TEXT,
            Type TEXT,
            Lane TEXT,
            Year INTEGER,
            Gold INTEGER,
            Diamond INTEGER
    )'''
    try:
        conn.execute(sql)
    except Error as e:
        print(e)

create_table(conn)
   
def write_db(conn,data):
    sql = '''INSERT INTO heroes VALUES(?,?,?,?,?,?,?,?)'''
    try:
        conn.execute(sql,data)
    except Error as e:
        print(e)

def read_csv(filepath):
    csvfile = open(filepath)
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    out = []
    for item in csvreader:
        item = tuple(item)
        write_db(conn,item)
    conn.commit()
    csvfile.close()
read_csv('realmlheroes.csv')
conn.close()

