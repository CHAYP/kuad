from loader import load_file
from loader import load_student 
from loader import load_faculty
from loader import load_applicant
# Run this file as main to test load data
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
