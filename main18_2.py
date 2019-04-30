from kuad18_2.loader import *
from kuad18_2.function2 import Rule
import sys

def is_match(student, faculty, rule):
    result = []
    result.append((check_gpa(student, faculty), "gpa"))
    for col, val in faculty.data.items():
        res = rule.find(student, faculty, col, val)
        result.append([res,col])
    # [print(i) for i in result]
    return len(result) == sum([i[0] for i in result])

def check_gpa(student, faculty):
    if student.gpa >= faculty.gpa: return True
    return False

def cal_gatpat(student, faculty):
    def is_used(fac, subj):
        if fac.data[subj] == "-": return False
        if fac.data[subj] == "": return False
        return True

    gatpat_list = [("gat",300),("pat1",300),("pat2",300),("pat3",300),("pat4",300),("pat5",300)]
    pat7_list = [("pat7_1",300),("pat7_2",300),("pat7_3",300),("pat7_4",300),("pat7_5",300),("pat7_6",300),("pat7_7",300)]
    gatpat = cal_any(student, faculty, gatpat_list)
    pat7 = student.getMaxPat7()
    # get max of pat7 sometimes wrong with faculty
    if faculty.id == "107": pat7 = student.get_max_score_by_subject("pat7_1")
    if not pat7: pat7 = [0]
    if is_used(faculty, "pat7"): return gatpat + pat7[0]
    return gatpat

def cal_udat(student, faculty):
    udat_list = [("u09",100),("u19",100),("u29",100),("u39",100),("u49",100),("u59",100),("u69",100)]
    return cal_any(student, faculty, udat_list)

def cal_onet(student, faculty):
    onet_list = [("x01",100),("x02",100),("x03",100),("x04",100),("x05",100)]
    return cal_any(student, faculty, onet_list)

def cal_any(student, faculty, subject_list):
    sum_score = 0
    max_score = 0
    used = False
    for subj, cap in subject_list:
        score = student.get_max_score_by_subject(subj)
        if not score: return -1
        sum_score += score[0]
        max_score += cap
        used = True
    # return sum_score / max_score
    if used: return sum_score
    return -1

def cal_with_ratio(student, faculty, subject_list):
    sum_score = 0
    for subj, cap, ratio in subject_list:
        score = 0
        if subj == "gpa": score = [student.gpa]
        elif subj == "onet": score = [cal_onet(student, faculty)]
        elif subj == "udat": score = [cal_udat(student, faculty)]
        elif subj == "pat7": score = student.getMaxPat7()
        elif subj == "pat7781": score = student.getMaxPat7(5)
        else: score = student.get_max_score_by_subject(subj)
        # print(score, subj)
        if not score: return -1
        sum_score += (score[0]/cap)*ratio
    return sum_score

def cal_score(student, faculty):
    if faculty.id in ["41","42","43","44"]:
        a = cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.3),("pat1",300,0.2)])
        b = cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.3),("pat7781",300,0.2)])
        return max(a,b)
    if faculty.id == "46":
        a = cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.3),("pat1",300,0.2)])
        b = cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.3),("pat7",300,0.2)])
        return max(a,b)
    if faculty.id == "45":
        return cal_with_ratio(student, faculty, [("gpa",4,0.1),("onet",500,0.3),("gat",300,0.2),("pat1",300,0.2),("pat2",300,0.2)])
    if faculty.id == "40":
        return cal_with_ratio(student, faculty, [("gpa",4,0.2),("gat",300,0.1),("pat1",300,0.1),("pat2",300,0.3),("onet",500,0.3)])
    if faculty.id == "39":
        return cal_with_ratio(student, faculty, [("onet",500,0.3),("gpa",4,0.2),("gat",300,0.3),("pat1",300,0.2)])
    if faculty.id == "18":
        return cal_with_ratio(student, faculty, [("gat",300,0.2),("pat1",300,0.4),("pat2",300,0.4)])
    if faculty.id == "19":
        return cal_with_ratio(student, faculty, [("gpa",4,0.2),("gat",300,0.15),("pat1",300,0.15),("udat",700,0.5)])
    if faculty.id == "56":
        return cal_with_ratio(student, faculty, [("gat",300,0.3),("gpa",4,0.2),("onet",500,0.3),("pat7_3",300,0.2)])
    if faculty.id in ["52","53","59","61","62"]:
        return cal_with_ratio(student, faculty, [("gat",300,0.5),("gpa",4,0.2),("onet",500,0.3)])
    if faculty.id == "60":
        a = cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.5)])
        b = cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.3),("pat7",300,0.2)])
        return max(a,b)
    if faculty.id == "57":
        return cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("pat7_4",300,0.5)])
    if faculty.id == "58":
        return cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.4),("gat",300,0.4)])
    if faculty.id == "67":
        return cal_with_ratio(student, faculty, [("gat2",150,0.3),("pat2",300,0.7)])
    # if faculty.id == "69":
    #     return cal_with_ratio(student, faculty, [("gpa",4,0.2),("gat",300,0.5/3),("pat1",300,0.5/3),("pat3",300,0.5/3)])
    if faculty.id == "71":
        return cal_with_ratio(student, faculty, [("gpa",4,0.2),("onet",500,0.3),("gat",300,0.2),("pat2",300,0.3)])
    return 0

def a_test(student, faculty, rule):
    print(student.data,student.gpa,student.prefix)
    is_match(student, faculty, rule)
    score = cal_score(student, faculty)
    print(score)

def all_match(stds, facs, rule):
    result = []
    cnt = {}

    for fac in facs.values():
        cnt[fac.id] = 0
        for std in stds.values():
            if is_match(std, fac, rule):
                score = cal_score(std, fac)
                if score >= 0: cnt[fac.id] += 1
                result.append((fac.id, std.id, score))
    # for i in cnt:
    #     print(i,cnt[i])
    result.sort()
    [print("{},{},{:.6f}".format(*i)) for i in result]

def xxx(stds, facs, rule, spc):
    result = []

    for std in stds.values():
        for i in std.chooses:
            fac = facs[i]
            if spc:
                if fac.id == spc[0]:
                    if is_match(std, fac, rule):
                        score = cal_score(std, fac)*100
                        result.append((fac.id, std.id, score))
                    else:
                        print(std.id)
            else:
                if is_match(std, fac, rule):
                    score = cal_score(std, fac)*100
                    score = max(score, 0)
                    result.append((fac.id, std.id, score))
                else:
                    result.append((fac.id, std.id, -1))

    result.sort(key=lambda x: (int(x[0]),x[0],-x[2]))
    [print("{},{},{:.3f}".format(*val)) for val in result]

def std_to_all_facs(std, facs, rule):
    for fac in facs.values():
        is_match(std, fac, rule)

def fac_to_all_stds(stds, fac, rule):
    for std in stds.values():
        if is_match(std, fac, rule):
            print(std.id, cal_score(std, fac))

if __name__ == "__main__":
    # เลขประจำตัวประชาชน,คำนำหน้า,ขื่อ,นามสกุล,year,gat_1,gat_2,gat,pat1,pat2,pat3,pat4,pat5,pat6,pat7_1,pat7_2,pat7_3,pat7_4,pat7_5,pat7_6,pat7_7
    # เลขประจำตัวประชาชน,คำนำหน้า,ขื่อ,นามสกุล,year,x01,x02,x03,x04,x05
    # เลขประจำตัวประชาชน,คำนำหน้า,ขื่อ,นามสกุล,year,u09,u19,u29,u39,u49,u59,u69,u89,u99

    gatpat_list = ["id","prefix","first_name","last_name","year","gat_1","gat_2","gat","pat1","pat2","pat3","pat4","pat5","pat6","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"]
    udat_list = ["id","prefix","first_name","last_name","year","u09","u19","u29","u39","u49","u59","u69","u89","u99"]
    onet_list = ["id","prefix","first_name","last_name","year","x01","x02","x03","x04","x05"]
    appl_list = ["id","fullname","gpa","plan_num","plan","x","province","n","n_1"]

    gatpat_file_name = "kuad18_2/dist/gatpat.csv"
    udat_file_name = "kuad18_2/dist/udat.csv"
    onet_file_name = "kuad18_2/dist/o-net.csv"
    appl_file_name = "kuad18_2/tcas5-applicants-final.csv"

    gatpat_score_list = gatpat_list[5:]
    udat_score_list = udat_list[5:]
    onet_score_list = onet_list[5:]

    # major_list = ["id","name","cap","gpa","plan","gat","pat1","pat2","pat3","pat4","pat5","pat7","gatpat","u09","u19","u29","u39","u49","u59","u69","udat","x03","x04","x05","onet"]
    major_list = ["id","name","subname","cap","x","gpa","plan","gat","pat1","pat2","pat3","pat4","pat5","pat7","gpcond","u09","u19","u29","u39","u49","u59","u69","ucond","x03","x04","x05","ocond"]
    major_file_name = "kuad18_2/tcas5-majors-use.csv"
    major_score_list = major_list[7:]

    stds = {}

    gatpat_data = load_file(gatpat_file_name, gatpat_list)
    onet_data = load_file(onet_file_name, onet_list)
    udat_data = load_file(udat_file_name, udat_list)
    appl_data = load_file(appl_file_name, appl_list)

    load_applicant(appl_data, stds)
    load_student(gatpat_data, gatpat_score_list, stds)
    load_student(onet_data, onet_score_list, stds)
    load_student(udat_data, udat_score_list, stds)

    facs = {}

    fac_data = load_file(major_file_name, major_list)
    load_faculty(fac_data, major_score_list, facs)

    rule = Rule('no mean file')

    xxx(stds, facs, rule, sys.argv[1:])