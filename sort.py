import sqlite3
import pymongo
import csv

uri = "mongodb+srv://cherry:aWNCvzjkSjXFpH0o@cluster0.kyh3c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri, server_api=pymongo.server_api.ServerApi(
 version="1", strict=True, deprecation_errors=True))
data = []
with open("heroes.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)
    for row in csvreader:
        data.append(row)

print(headers)

result = []
for hero in data:
    if '|' in hero[2]:
        hero[2] = hero[2].split(' | ')
    if '|' in hero[3]:
        hero[3] = hero[3].split(' | ')

    doc = {}
    for i in range(len(hero)):
        print(headers[i], hero[i])
        if type(hero[i]) == str and hero[i].isdigit():
            doc[headers[i]] = int(hero[i])
        else:
            doc[headers[i]] = hero[i]
    result.append(doc)


db = client["ml"]
db.drop_collection("heroes")
col = db["heroes"]

col.insert_many(result)

client.close()