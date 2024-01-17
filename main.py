from flask import Flask, render_template, request, url_for


import csv
import random
import sqlite3
from sqlite3 import Error
idx = random.randint(1,121)
answer = ''

def connect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print("database connected.")
        return conn
    except Error as e:
        print(e)


def generate_hero(conn):
    heroidx = random.randint(1, 123)
    hero = conn.execute('''SELECT * FROM heroes WHERE Serial = ?''', (heroidx,)).fetchone()
    return hero



def doiwin(g, ans, attempt, conn):
    
    guess = conn.execute('''SELECT * FROM heroes WHERE Name = ?''', (g,)).fetchone()
    corrects = [attempt, None, None, None, "higher", None, None, None, None]
    if guess[1] == ans[1]:
        return 'you win', None
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
        
    return guess, corrects



app = Flask(__name__)
attempt = 0

headers = ["Attempt","Hero Name","Hero Role","Hero Type","Hero Lane","Release Year","Gold","Diamond","Race", "Gender"]
totalguess = []
totalcorrects = []

@app.route('/index/')
@app.route('/', methods = ["POST", "GET"])
def index():
    global answer
    if request.method == "POST":
        db_filename = "mlheroes.db"
        conn = connect_db(db_filename)
        hero = request.form["hero"]
        guess, corrects = doiwin(hero, answer, attempt, conn)
        totalguess.append(guess)
        totalcorrects.append(corrects)
        conn.close()
        return render_template('index.html', totalguess=totalguess, totalcorrects=totalcorrects, headers=headers, attempt=attempt)
    else:
        db_filename = "mlheroes.db"
        conn = connect_db(db_filename)
       
        answer = generate_hero(conn)
        conn.close()
        return render_template('index.html', totalguess=totalguess, totalcorrects=totalcorrects, headers=headers, attempt=attempt)
           

if __name__ == "__main__":
    app.run(debug=True)

