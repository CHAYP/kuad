import csv
from student import Student
from faculty import Faculty

# Run loader.py as main to test load data
# ==== EDIT FOR TEST LOADER ONLY ====
_gatpat_list = ["id","prefix","first_name","last_name","year","gat_1","gat_2","gat","pat1","pat2","pat3","pat4","pat5","pat6","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"]
_udat_list = ["id","prefix","first_name","last_name","year","u09","u19","u29","u39","u49","u59","u69","u89","u99"]
_onet_list = ["id","prefix","first_name","last_name","year","x01","x02","x03","x04","x05"]
_appl_list = ["id","prefix","gpa","x","plan"]

_gatpat_file_name = "tcas3-testdata/gatpat-small.csv"
_udat_file_name = "tcas3-testdata/udat-small.csv"
_onet_file_name = "tcas3-testdata/o-net-small.csv"
_appl_file_name = "tcas3-testdata/applicants-small.csv"

# _gatpat_file_name = "tcas3-testdata/gatpat.csv"
# _udat_file_name = "tcas3-testdata/udat.csv"
# _onet_file_name = "tcas3-testdata/o-net.csv"
# _appl_file_name = "tcas3-testdata/applicants.csv"

_gatpat_score_list = _gatpat_list[5:]
_udat_score_list = _udat_list[5:]
_onet_score_list = _onet_list[5:]

_major_list = ["id","name","cap","gpa","plan","gat","pat1","pat2","pat3","pat4","pat5","pat7","gatpat","u09","u19","u29","u39","u49","u59","u69","udat","x03","x04","x05","onet"]
_major_file_name = "final_major.csv"
_major_score_list = _major_list[5:]
# ==== EDIT FOR TEST LOADER ONLY ====

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
        students[score["id"]].loadDataByYear(score["year"],score_data)

def load_applicant(data, students):
    for appl in data:
        if appl["id"] in students:
            students[appl["id"]].prefix = appl["prefix"]
            students[appl["id"]].plan = appl["plan"]
            students[appl["id"]].gpa = _val_to_float(appl["gpa"])

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

def test():
    stds = {}

    gatpat_data = load_file(_gatpat_file_name, _gatpat_list)
    onet_data = load_file(_onet_file_name, _onet_list)
    udat_data = load_file(_udat_file_name, _udat_list)
    appl_data = load_file(_appl_file_name, _appl_list)

    load_student(gatpat_data, _gatpat_score_list, stds)
    load_student(onet_data, _onet_score_list, stds)
    load_student(udat_data, _udat_score_list, stds)
    load_applicant(appl_data, stds)

    facs = {}

    fac_data = load_file(_major_file_name, _major_list)
    load_faculty(fac_data, _major_score_list, facs)

if __name__ == "__main__":
    test()