import csv
import json

file_name = 'data/criteria.csv'

with open(f"{file_name}", "r", encoding="utf-8-sig") as mfile:
    csv_file = csv.DictReader(mfile)
    for line in csv_file:
        if line['slot'] == None:
            print('skip')
            continue
        a, b = line['slot'].split(' ')
        line['id'] = b
        line['slot'] = a
        print(line)
        break


file_name = 'data/tcas3-1-criterias-updated-20210513-with-projectid.json'
with open(f"{file_name}", 'r', encoding="utf-8-sig") as mfile:
    data_file = json.load(mfile)
    print(len(data_file))
