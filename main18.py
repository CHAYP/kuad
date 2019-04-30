from lib.loader import *
from kuad18.function2 import Rule

def is_match(student, faculty, rule):
    result = []
    result.append((check_gender(student, faculty), "gender"))
    result.append((check_gpa(student, faculty), "gpa"))
    for col, val in faculty.data.items():
        res = rule.find(student, faculty, col, val)
        result.append([res,col])
    # so bad damn code
    if faculty.id == "52":
        u29 = [i for i in result if i[1] == "u29"]
        x03 = [i for i in result if i[1] == "x03"]
        u29[0][0] = x03[0][0] = u29[0][0] or x03[0][0]
    # if 183 <= int(faculty.id) and int(faculty.id) <= 196:
    #     gat = [i for i in result if i[1] == "gat"]
    #     pat1 = [i for i in result if i[1] == "pat1"]
    #     gat[0][0] = pat1[0][0] = gat[0][0] or pat1[0][0]
    # fuck code
    # [print(i) for i in result]
    return len(result) == sum([i[0] for i in result])

def check_gender(student, faculty):
    if faculty.gender == "both": return True
    return faculty.gender == student.prefix

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
    if faculty.id == "108": pat7 = student.get_max_score_by_subject("pat7_2")
    if faculty.id == "109": pat7 = student.get_max_score_by_subject("pat7_4")
    if not pat7: pat7 = [0]
    if is_used(faculty, "pat7"): return gatpat + pat7[0]
    return gatpat

def cal_udat(student, faculty):
    udat_list = [("u09",100),("u19",100),("u29",100),("u39",100),("u49",100),("u59",100),("u69",100)]
    return cal_any(student, faculty, udat_list)

def cal_onet(student, faculty):
    onet_list = [("x03",100),("x04",100),("x05",100)]
    return cal_any(student, faculty, onet_list)

def cal_any(student, faculty, subject_list):
    sum_score = 0
    max_score = 0
    used = False
    for subj, cap in subject_list:
        if faculty.data[subj] == "-": continue
        if faculty.data[subj] == "": continue
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
        score = student.get_max_score_by_subject(subj)
        if not score: return -1
        sum_score += (score[0]/cap)*ratio
    return sum_score

def cal_score(student, faculty):
    score = {
        "udat":cal_udat(student, faculty),
        "gatpat":cal_gatpat(student, faculty),
        "onet":cal_onet(student, faculty)
    }
    if faculty.data["gatpat"] == "สัดส่วนวิชาGAT = 20%PAT 2 = 10%PAT 4 = 50%":
        score["gatpat"] = cal_with_ratio(student, faculty, [("gat",300,0.2),("pat2",300,0.1),("pat4",300,0.5)])
        score["alter"] = (score["gatpat"]+score["onet"])*100
    if faculty.data["gatpat"] == "สัดส่วนวิชาGAT = 20%PAT 4 = 50%":
        score["gatpat"] = cal_with_ratio(student, faculty, [("gat",300,0.2),("pat4",300,0.5)])
        score["alter"] = (score["gatpat"]+score["onet"])*100
    if faculty.data["gatpat"] == "สัดส่วนวิชา 85=25%":
        score["gatpat"] = cal_with_ratio(student, faculty, [("gat",300,0.25)])
        score["alter"] = (score["gatpat"]+score["onet"])*100
    if faculty.data["onet"] == "สัดส่วนวิชา03, 04, 05 = 20%":
        score["onet"] = cal_with_ratio(student, faculty, [("x03",100,0.2/3),("x04",100,0.2/3),("x05",100,0.2/3)])        
        score["alter"] = (score["gatpat"]+score["onet"])*100
    if faculty.data["onet"] == "สัดส่วนวิชา03, 04, 05 = 30%":
        score["onet"] =cal_with_ratio(student, faculty, [("x03",100,0.3/3),("x04",100,0.3/3),("x05",100,0.3/3)])        
        score["alter"] = (score["gatpat"]+score["onet"])*100
    if faculty.data["onet"] == "สัดส่วนวิชา 03=75%":
        score["onet"] =cal_with_ratio(student, faculty, [("x03",100,0.75)])        
        score["alter"] = (score["gatpat"]+score["onet"])*100
    # print(score)
    if faculty.id == "52": return score["gatpat"]
    for i in ["alter","udat","gatpat"]:
        if score.get(i,-1) >= 0: return score[i]
    return -1

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

def xxx(stds, facs, rule):
    result = []

    for std in stds.values():
        for i in std.chooses:
            fac = facs[i]
            if is_match(std, fac, rule):
                score = cal_score(std, fac)
                result.append((fac.id, std.id, score))

    result.sort()
    [print("{},{},{:.6f}".format(*i)) for i in result]

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
    appl_list = ["id","prefix","gpa","x0","x1","x2","x3","n","n_1","n_2","n_3","n_4"]

    gatpat_file_name = "kuad18/real-data/gatpat.csv"
    udat_file_name = "kuad18/real-data/udat.csv"
    onet_file_name = "kuad18/real-data/o-net.csv"
    appl_file_name = "kuad18/real-data/anno-applicants-fixed-format2.csv"

    # gatpat_file_name = "kuad18/tcas3-testdata/gatpat-small.csv"
    # udat_file_name = "kuad18/tcas3-testdata/udat-small.csv"
    # onet_file_name = "kuad18/tcas3-testdata/o-net-small.csv"
    # appl_file_name = "kuad18/tcas3-testdata/applicants-small.csv"

    # gatpat_file_name = "kuad18/tcas3-testdata/gatpat.csv"
    # udat_file_name = "kuad18/tcas3-testdata/udat.csv"
    # onet_file_name = "kuad18/tcas3-testdata/o-net.csv"
    # appl_file_name = "kuad18/tcas3-testdata/applicants.csv"

    gatpat_score_list = gatpat_list[5:]
    udat_score_list = udat_list[5:]
    onet_score_list = onet_list[5:]

    major_list = ["id","name","cap","gpa","plan","gat","pat1","pat2","pat3","pat4","pat5","pat7","gatpat","u09","u19","u29","u39","u49","u59","u69","udat","x03","x04","x05","onet"]
    major_file_name = "kuad18/final_major.csv"
    major_score_list = major_list[5:]

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

    # facs["180"].gender = "นาย"
    # facs["181"].gender = "นาย"
    # facs["182"].gender = "นาย"

    mean_file = "kuad18/mean.txt"
    rule = Rule(mean_file)

    # print(len(facs.keys()),len(stds.keys()))
    
    # a_test(stds["6137670011895"], facs["105"], rule) # ... bug
    # a_test(stds["1234567890344"], facs["183"], rule) # ... bug
    # a_test(stds["1234567890344"], facs["19"], rule) # ... bug
    # std_to_all_facs(stds["1234567890149"], facs, rule)
    # fac_to_all_stds(stds, facs["52"], rule)
    # all_match(stds, facs, rule)

    xxx(stds, facs, rule)
    
