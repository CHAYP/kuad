#KU Admission

## Class Desciption

- Faculty
- Student

## File Description

### loader.py

#### load_file(*file_name*, *column_to_str*)

- read *file_name*(csv type) to list with name as in *column_to_str*

#### load_student(**score_data**, **score_score_list**, **stds**)

- load score to **stds** dict if none **stds**: create basic student object
- **score_data**: list with **score_score_list** as colum name
- **score_score_list**: column to str map for **score_data**
- **stds**: dict of student object with "id" as key
- note: score is float, "-" or "" is map -1(no score)

#### load_applicant(applicant_list, students)

- load prefix, gpa and chooses order(ie. "n_1","n_2","n_3","n_4") to student object

#### load_faculty(data_list, score_list, faculties)

- load rule data in score_list to faculty object, load basic infomation
- faculties: dict of faculty object with "id" as key
