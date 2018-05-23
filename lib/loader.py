import csv
import re
from lib.student import Student
from lib.faculty import Faculty
#care above

def load_file(file_name, column_to_str):
    data = []
    with open(file_name,"r") as f:
        csv_data = csv.reader(f)
        for row in csv_data:
            tmp = {}
            for col, val in enumerate(row):
                tmp[column_to_str[col]] = val
            data.append(tmp)
    return data

def _filter_with_key(key_list, data, conv_func=0):
    result = {}
    for key in key_list:
        if conv_func != 0 : result[key] = conv_func(data[key])
        else: result[key] = data[key]
    return result

def _val_to_float(val):
    if val == "" : return -1
    if val == "-": return -1
    return float(val)

def _correct_gpa(val):
    if re.match(r"^[0-4](.\d+)*$",val):
        return float(val)
    return -1

def load_student(data, score_list, students):
    for score in data:
        if score["id"] not in students:
            students[score["id"]] = Student(
                score["id"],
                score["prefix"],
                score["first_name"],
                score["last_name"]
            )
        score_data = _filter_with_key(score_list, score, _val_to_float)
        students[score["id"]].load_data_with_year(score["year"],score_data)

def load_applicant(data, students):
    for appl in data:
        if appl["id"] in students:
            students[appl["id"]].prefix = appl["prefix"]
            students[appl["id"]].gpa = _correct_gpa(appl["gpa"])

            for i in ["n_1","n_2","n_3","n_4"]:
                if appl[i] != "":
                    students[appl["id"]].chooses.append(appl[i])


def load_faculty(data, score_list, faculties):
    for major in data:
        if major["id"] not in faculties:
            faculties[major["id"]] = Faculty(
                major["id"],
                major["name"],
                major["cap"],
                _val_to_float(major["gpa"]),
                major["plan"]
            )
        score_data = _filter_with_key(score_list, major)
        faculties[major["id"]].loadData(score_data)
