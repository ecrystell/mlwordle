import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("mlheroes.db")

def insert_hero(name, role, herotype, lane, year, gold, diamond):
    serial = conn.execute('''SELECT max(Serial) FROM heroes''').fetchone()[0]
    check = conn.execute('''SELECT Name, Serial FROM heroes WHERE Name = ?''', (name,)).fetchone()
    if not(check):
        conn.execute('''
                    INSERT INTO heroes
                    VALUES(?,?,?,?,?,?,?,?)
                    ''', (serial+1, name, role, herotype, lane, year, gold, diamond))
        
        conn.commit()
        return '{} inserted'.format(name)
    else:
        print(check)
        print("{} exists at {}".format(check[0], check[1]))

def add_column(name, columntype):
    try:
        conn.execute('''ALTER TABLE heroes
                        ADD {} {};'''.format(name,columntype))
        print('colum inserted')
    except Error as e:
        print(e)

def insert_data(heroes, colum, value):
    for h in heroes:
        conn.execute('''UPDATE heroes
                        SET {} = ?
                        WHERE Name = ?'''.format(colum), (value, h))
        
        conn.commit()
        check = conn.execute('''SELECT {} FROM heroes
                             WHERE Name = ?'''.format(colum),(h,)).fetchone()
        if check:
            print("updated {} for {}".format(colum, h))
        
    
# #insert_hero("Freya", "Fighter", "Chase | Damage", "EXP Laner", 2017, 0, 599)
# #insert_hero("Odette", "Mage", "Burst | Poke", "Mid Laner", 2017, 32000, 599)
# #add_column("Race", "TEXT")

insert_data(["Tigreal", "Alucard", "Franco", "Clint", "Zilong", "Fanny",
            "Hayabusa", "Natalia", "Layla", "Kagura", "Chou", "Ruby",
            "Yi Sun-shin", "Hilda", "Lapu-Lapu", "Harley", "Odette", "Lancelot",
            "Lesley", "Gusion", "Valir", "Hanabi", "Aldous", "Claude", "Vale",
            "Kimmy", "Minsitthar", "Badang", "Granger", "Guinevere", "Esmeralda"
            "Ling", "Lylia", "Baxia", "Wanwan", "Silvanna", "Popol", "Luo Yi", "Benedetta",
            "Khaleed", "Brody", "Mathilda", "Paquito", "Melissa",
            "Julian", "Fredrinn", "Ixia", "Masha", "Yu Zhong",
            "Roger", "Gord", "Pharsa", "Beatrix", "Aamon", "Natan",
            "Valentina", "Yin" ], "Race", "Human")

insert_data(["Lolita", "Irithel", "Lunox", "Eudora",
              "Xavier", "Miya", "Estes", "Nana", "Harith",
                "Aulus", "Joy", "Karina", "Selena", "Floryn"], "Race", "Elf")

insert_data(["Saber", "Bruno", "Johnson", "Alpha", "X.Borg", "Jawhead", "Angela", "Atlas"], "Race", "Mechanical")

insert_data(["Alice", "Carmilla", "Cecilion", "Moskov", "Selena", "Terizla", "Dyrroth", "Phoveus", "Arlott", "Hanzo", "Thamuz"], "Race", "Demon")

insert_data(["Balmond"], "Race", "Orc")


insert_data(["Akai"], "Race", "Panda")
insert_data(["Sun"], "Race", "Monkey")
insert_data(["Diggie"], "Race", "Owl")
insert_data(["Bane"], "Race", "Squid")
insert_data(["Atlas"], "Race", "Abyssal Creature")
insert_data(["Vexana", "Khufra", "Faramis", "Leomord"], "Race", "Undead")
insert_data(["Rafaela", "Argus"], "Race", "Angel")
insert_data(["Freya", "Aurora", "Gatotkaca",
             "Chang'e", "Lunox", "Kadita", "Edith",
             "Martis"], "Race", "Celestial")
insert_data(["Minotaur"], "Race", "Minoan")
insert_data(["Hylos"], "Race", "Centaur")
insert_data(["Zhask", "Yve"], "Race", "Extraterrestrial")
insert_data(["Cyclops"], "Race", "Giant")
insert_data(["Karrie"], "Race", "Yasson")
insert_data(["Grock"], "Race", "Stone Titan")
insert_data(["Helcurt"], "Race", "Shadowbringer")
insert_data(["Uranus"], "Race", "Aethereal")
insert_data(["Kaja"], "Race", "Nazar")
insert_data(["Belerick"], "Race", "Tree Nymph")
insert_data(["Barats"], "Race", "Politan")
insert_data(["Gloo"], "Race", "Daktec")
insert_data(["Novaria"], "Race", "Star")
            
import csv
add_column("Gender", "TEXT")
female = []
male = []
unknown = []
with open("gender.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        if row[-1] == "female":
            female.append(row[1])
        elif row[-1] == "male":
            male.append(row[1])
        else:
            unknown.append(row[1])

insert_data(female, "Gender", "Female")
insert_data(male, "Gender", "Male")
insert_data(unknown, "Gender", "Genderless")

conn.close()