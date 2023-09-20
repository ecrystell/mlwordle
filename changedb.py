import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("mlheroes.db")

def insert_hero(name, role, herotype, lane, year, gold, diamond):
    serial = conn.execute('''SELECT max(Serial) FROM heroes''').fetchone()[0]
    conn.execute('''
                 INSERT INTO heroes
                VALUES(?,?,?,?,?,?,?,?)
                 ''', (serial+1, name, role, herotype, lane, year, gold, diamond))
    
    return '{} inserted'.format(name)

def add_column(name, columntype):
    try:
        conn.execute('''
                    ALTER TABLE heroes
                        ADD name ? ?)
                    ''', (name, columntype))
    except Error as e:
        print(e)