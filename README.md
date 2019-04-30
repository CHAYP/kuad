# KU Admission

## Class Desciption

- Faculty: Collected basic information, ie. cap, plan and data for score criterion.
- Student: Collected basic information, ie. prefix, first_name, last name.
Collected score in dictionary of **\[year\]\[subject\]** ans some function to get socre.
- Rule: Class for deal with criterion, rule to choose student.**Need edit up to criterion and rule of admission.**

## File Description

### loader.py

#### load_file(*file_name*, *column_to_str*)

- read *file_name*(csv type) to list with name as in *column_to_str*

#### load_student(*score_data*, *score_score_list*, *stds*)

- load score to *stds* dict if none *stds*: create basic student object
- *score_data*: list with *score_score_list* as colum name
- *score_score_list*: column to str map for *score_data*
- *stds*: dict of student object with "id" as key
- note: score is float, "-" or "" is map -1(no score)

#### load_applicant(applicant_list, students)

- load prefix, gpa and chooses order(ie. "n_1","n_2","n_3","n_4") to student object

#### load_faculty(data_list, *score_list*, *faculties*)

- load rule data in *score_list* to faculty object, load basic infomation
- *faculties*: dict of faculty object with "id" as key

### How to run

- Define header list for data file, data file name, score list (for collected saperate by year)
```
    gatpat_list = ["id","prefix","first_name","last_name","year","gat_1","gat_2","gat","pat1","pat2","pat3","pat4","pat5","pat6","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"]
    udat_list = ["id","prefix","first_name","last_name","year","u09","u19","u29","u39","u49","u59","u69","u89","u99"]
    onet_list = ["id","prefix","first_name","last_name","year","x01","x02","x03","x04","x05"]
    appl_list = ["id","prefix","gpa","x0","x1","x2","x3","n","n_1","n_2","n_3","n_4"]

    gatpat_file_name = "real-data/gatpat.csv"
    udat_file_name = "real-data/udat.csv"
    onet_file_name = "real-data/o-net.csv"
    appl_file_name = "real-data/anno-applicants-fixed-format2.csv"

    gatpat_score_list = gatpat_list[5:]
    udat_score_list = udat_list[5:]
    onet_score_list = onet_list[5:]
```
- Define head list for major criteria, score list, filename
```
    major_list = ["id","name","cap","gpa","plan","gat","pat1","pat2","pat3","pat4","pat5","pat7","gatpat","u09","u19","u29","u39","u49","u59","u69","udat","x03","x04","x05","onet"]
    major_file_name = "final_major.csv"
    major_score_list = major_list[5:]
```
- load student,faculty,mean file to rule object
```
    stds = {}

    gatpat_data = load_file(gatpat_file_name, gatpat_list)
    onet_data = load_file(onet_file_name, onet_list)
    udat_data = load_file(udat_file_name, udat_list)
    appl_data = load_file(appl_file_name, appl_list)

    load_student(gatpat_data, gatpat_score_list, stds)
    load_student(onet_data, onet_score_list, stds)
    load_student(udat_data, udat_score_list, stds)
    load_applicant(appl_data, stds)

    facs = {}

    fac_data = load_file(major_file_name, major_list)
    load_faculty(fac_data, major_score_list, facs)

    mean_file = "mean.txt"
    rule = Rule(mean_file)
```
- edit rule