from flask import Flask, render_template, request, url_for, jsonify
import datetime
import pymongo
import random

import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('URI')

def connect_db():
    
    global client
    client = pymongo.MongoClient(uri, server_api=pymongo.server_api.ServerApi(
    version="1", strict=True, deprecation_errors=True))
    
    db = client["ml"]
    col = db["heroes"]
    return col



def generate_hero(conn):
    heroidx = random.randint(1, 123)
    hero = conn.find_one({"Serial": heroidx}, {"_id":0})
    #print(hero)
    return hero

def all_heroes(conn):
    result = []
    cursor = conn.find({},{"_id":0, "Name":1})
    for item in cursor:
        result.append(item)
    #print(result)
    return result


def doiwin(g, ans, attempt, conn):
    
    guess = conn.find_one({"Name": g}, {"_id": 0, "Serial": 0})
    corrects = {}
    print(guess, ans)
    if guess["Name"] == ans["Name"]:
        print('win')
    else:
        corrects["Name"] = False

    
    for header in guess.keys():
        if header == "Year":
            if guess[header] < ans[header]:
                corrects[header] = "higher"
            elif guess[header] > ans[header]:
                corrects[header] = "lower"
            else:
                corrects[header] = True
        elif header == "Type":
            if guess[header] == ans[header]:
                corrects[header] = True

            else:
                if len(guess[header]) == 1:
                    if guess[header] in ans[header]:
                        corrects[header] = "partial"
                elif len(ans[header]) == 1:
                    if ans[header] in guess[header]:
                        corrects[header] = "partial"
                
                elif len(set(guess[header]) & set(ans[header])) > 0:
                    corrects[header] = "partial"
        
                else:
                    corrects[header] = False

        else:

            if guess[header] == ans[header]:
                corrects[header] = True
            else:
                corrects[header] = False
        
    #guess["Attempt"] = attempt
    print(guess, corrects)
    
    print(guess, corrects)
    return guess, corrects



app = Flask(__name__)
attempt = 1
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
        
        conn = connect_db()
        hero = request.get_json()[0]["hero"]
        # print(all_heroes(conn))
        if {"Name": hero} in all_heroes(conn):

            guess, corrects = doiwin(hero, answer, attempt, conn)
            # print(answer)
            # print(guess)
            h = list(guess.keys())
            guess = list(guess.values())
            corrects = list(corrects.values())
            #print(totalcorrects)
            #print(totalguess)
            attempt += 1
        client.close()
        result = {"guess": guess,
                  "corrects": corrects,
                  "headers": h,
                  "attempt": attempt-1}
        
        return jsonify(result)
    else:
        
        conn = connect_db()
        answer = generate_hero(conn)
        print(answer)
        client.close()
        totalguess = []
        totalcorrects = []
        attempt = 1
        return render_template('index.html', totalguess=[], totalcorrects=[], headers=headers)
           

if __name__ == "__main__":
    # app.run(debug=True,port=8889)
    app.run(debug=True)

