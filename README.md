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

### mean.txt

mean.txt must be in format
```
("2560/1", "gat", 123.93)
("2560/1", "gat_1", 83.70)
("2560/1", "gat_2", 40.36)
("2560/1", "pat1", 42.82)
("2560/1", "pat2", 79.59)
```

### How to run

edit main.py (bad code for saperate module)

- Define header list for data file, data file name, score list (for collected saperate by year)
- Define head list for major criteria, score list, filename
- Load student,faculty,mean file to rule object
- Edit rule object to map string to function
- Edit score calculator function
- Edit match function
- Run solve function