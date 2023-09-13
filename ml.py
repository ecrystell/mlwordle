import csv
#ykafjhusvzdjck.szc

with open("ml heroes.csv", "r") as f:
    csvreader = csv.reader(f)
    prevrow = []
    result = []
    for oldrow in csvreader:
        row = []
        for real in oldrow:
            item = None
            if "Â" in real:
                real = real.replace('\xa0', '')
                real = real.split('Â')
                item = []
                for thing in real:
                  
                    if thing.isalpha():
                        item.append(thing)
            if item:
                row.append(item)
            else:
                row.append(real)
                

        while '' in row:
            row.remove('')
        if len(row) == 1:
            prevrow += row
            result.append(prevrow)
        prevrow = row
    
    for row in result:
        print(row)
        
with open("realmlheroes.csv", 'w') as newfile:
    for row in result[1:]:
        for item in row:
            if isinstance(item, list):
                item = str(item).replace(',', ' |')
                item = item.replace('[', '')
                item = item.replace(']', '')
                item = item.replace("'", '')


            newfile.write(item)
            newfile.write(',')
        newfile.write('\n')
    