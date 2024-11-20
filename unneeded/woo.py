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


db_filename = "mlheroes.db"
conn = connect_db(db_filename)
#create_table(conn)
#read_csv('realmlheroes.csv')


def generate_hero():
    heroidx = random.randint(1, 123)
    hero = conn.execute('''SELECT * FROM heroes WHERE Serial = ?''', (heroidx,)).fetchone()
    return hero

def all_heroes():
    return conn.execute('''SELECT Name FROM heroes''').fetchall()



    

attempt = 0
ans = generate_hero()

while True:
    attempt += 1
    g = ''
    checkheroes = all_heroes()
    #print(checkheroes)
    while (g,) not in checkheroes and g.lower() != "quit":
        g = input("Enter hero name: ")

    if g.lower() == 'quit':
        break
    
    guess = conn.execute('''SELECT * FROM heroes WHERE Name = ?''', (g,)).fetchone()
    corrects = [attempt, None, None, None, "higher", None, None, None, None]
    if guess[1] == ans[1]:
        print('win')
    for i in range(2, len(guess)):
        if i == 5:
            if guess[5] < ans[5]:
                corrects[4] = "higher"
            elif guess[5] > ans[5]:
                corrects[4] = "lower"
            else:
                corrects[4] = True
            continue
        if guess[i] == ans[i]:
            corrects[i-1] = True
        else:
            corrects[i-1] = False
        


        print(';{:<10};{:<25};{:<25};{:<15};{:<10};{:<6};{:<4};{:<20};{:<20}'.format(guess[1],guess[2],guess[3],guess[4],guess[5],guess[6],guess[7], guess[8], guess[9]))
        
        print(';Try: {:<5};{:<25};{:<25};{:<15};{:<10};{:<6};{:<4};{:<20};{:<20}'.format(corrects[0],corrects[1],corrects[2],corrects[3],corrects[4],corrects[5],corrects[6],corrects[7], corrects[8]))

    
conn.close()