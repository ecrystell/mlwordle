from flask import Flask, render_template, request, url_for


import csv
import random
import sqlite3
from sqlite3 import Error


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

def all_heroes(conn):
    return conn.execute('''SELECT Name FROM heroes''').fetchall()


def doiwin(g, ans, attempt, conn):
    
    guess = list(conn.execute('''SELECT * FROM heroes WHERE Name = ?''', (g,)).fetchone())
    corrects = [attempt,None, None, None, None, "higher", None, None, None, None]
    if guess[1] == ans[1]:
        print('win')
    for i in range(2, len(guess)):
        if i == 5:
            if guess[5] < ans[5]:
                corrects[5] = "higher"
            elif guess[5] > ans[5]:
                corrects[5] = "lower"
            else:
                corrects[5] = True
            continue
        if guess[i] == ans[i]:
            corrects[i] = True
        else:
            corrects[i] = False
        
    guess[0] = attempt
    return guess, corrects



app = Flask(__name__)
attempt = 0
answer = ''
headers = ["Attempt","Hero Name","Hero Role","Hero Type","Hero Lane","Release Year","Gold","Diamond","Race", "Gender"]
totalguess = []
totalcorrects = []


@app.route('/index/')
@app.route('/', methods = ["POST", "GET"])
def index():
    global answer
    global attempt
    global totalguess
    global totalcorrects
    if request.method == "POST":
        db_filename = "mlheroes.db"
        conn = connect_db(db_filename)
        hero = request.form["hero"]
        # print(hero)
        # print(all_heroes(conn))
        if (hero,) in all_heroes(conn):

            guess, corrects = doiwin(hero, answer, attempt, conn)
            # print(answer)
            # print(guess)
            totalguess.append(guess)
            totalcorrects.append(corrects)
            # print(totalguess)
            attempt += 1
        conn.close()
        return render_template('index.html', totalguess=totalguess, totalcorrects=totalcorrects, headers=headers, attempt=attempt)
    else:
        db_filename = "mlheroes.db"
        conn = connect_db(db_filename)
        answer = generate_hero(conn)
        print(answer)
        conn.close()
        totalguess = []
        totalcorrects = []
        attempt = 0
        return render_template('index.html', totalguess=[], totalcorrects=[], headers=headers, attempt=0)
           

if __name__ == "__main__":
    app.run(debug=True)

