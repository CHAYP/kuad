import csv
import re
from os import walk
from os.path import join

data_path = "admission_data"

def is_rule(value):
    m = re.search(r"^\d+$",value)
    return m

def scan_all_file(file_list):
    for file_name in file_list:
        scan_file(file_name)

def scan_file(file_name):
    tmp = {}
    with open(join(data_path,file_name)) as f:
        data = csv.reader(f)
        for row in data:
            if is_rule(row[0]):
                for (col,value) in enumerate(row):
                    if tmp.get(col,False) == False:
                        tmp[col] = []
                    if value not in tmp[col]:
                        tmp[col].append(value)
    print(file_name,"col=",len(tmp))
    [print(i,len(tmp[i]),tmp[i]) for i in tmp]
    print()

def find_file(path):
    all_file = []
    for (dir_path, dir_name, file_name) in walk(path):
        all_file += file_name
    print(all_file)
    return all_file


if __name__ == "__main__":
    file_list = find_file(data_path)
    scan_all_file(file_list)
