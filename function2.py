import re

class Rule:
    def __init__(self, mean_file):
        self.mean = {}
        self._load_mean(mean_file)
        
        self.udat_score_list = ["u09","u19","u29","u39","u49","u59","u69"]
        self.gatpat_score_list = ["gat","pat1","pat2","pat3","pat4","pat5"]

    def _load_mean(self,file_name):
        with open(file_name,"r") as f:
            for line in f:
                year, subj, num = eval(line)
                if year not in self.mean: self.mean[year] = {}
                self.mean[year][subj] = num

    def is_used(self, fac, subj):
        if fac.data[subj] == "-": return False
        if fac.data[subj] == "": return False
        return True

    def find(self, std, fac, col ,val):
        def is_number(value):
            m = re.search(r"^\d+$",value)
            return m
        if val == "-": return True 
        if is_number(val) and col == "udat":
            return self.SUM_GREATER_THAN(std, fac, self.udat_score_list, float(val))
        if is_number(val) and col == "gatpat":
                return self.SUM_GREATER_THAN(std, fac, self.gatpat_score_list, float(val))
        if is_number(val): 
            return self.GREATER_THAN(std, fac, col, float(val))
        if val == "":
            return True
        if val == "/" and col == "pat7":
            return self.ONE_AMONG(std, fac, ["pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"], 0)
        if val == "/":
            return self.GREATER_THAN(std, fac, col, 0)
        if val == "x̅" and col == "gatpat":
            return self.ONE_GREATER_THAN_MEAN(std, fac, self.gatpat_score_list, 0)
        if val == "x̅":
            return self.GREATER_THAN_MEAN(std, fac, col, 0)
        if val == "x̅+10":
            return self.GREATER_THAN_MEAN(std, fac, col, 10)
        if val == "x̅+30":
            return self.GREATER_THAN_MEAN(std, fac, col, 30)
        if val == "GAT ตอน 2≥30":
            return self.GREATER_THAN(std, fac, "gat_2", 30)
        if val == "GAT ตอน 2≥40":
            return self.GREATER_THAN(std, fac, "gat_2", 40)
        if val == "GAT ตอน 2≥24":
            return self.GREATER_THAN(std, fac, "gat_2", 24)
        if val == "GAT ตอน 2≥75":
            return self.GREATER_THAN(std, fac, "gat_2", 75)          
        if val == "∑x̅" and col == "udat":
            subj_list = [i for i in self.udat_score_list if fac.data[i] != "-"]
            return self.DIFF_GREATER_THAN(std, fac, subj_list, 0)
        if val == "∑x̅+40" and col == "udat":
            subj_list = [i for i in self.udat_score_list if fac.data[i] != "-"]
            return self.DIFF_GREATER_THAN(std, fac, subj_list, 40)
        if val == "∑x̅" and col == "gatpat":
            subj_list = [i for i in self.gatpat_score_list if fac.data[i] != "-"]
            return self.DIFF_GREATER_THAN(std, fac, subj_list, 0)
        if val == "PAT 7 (77)":
            return self.GREATER_THAN(std, fac, "pat7_1", 0)
        if val == "PAT 7 (78)":
            return self.GREATER_THAN(std, fac, "pat7_2", 0)
        if val == " PAT 7 (78)≥135":
            return self.GREATER_THAN(std, fac, "pat7_2", 135)
        if val == "PAT 7 (80)":
            return self.GREATER_THAN(std, fac, "pat7_4", 0)
        if val == " PAT 7 (80)≥120":
            return self.GREATER_THAN(std, fac, "pat7_4", 120)
        if val == "เลือกสอบ PAT1 หรือ PAT 7 (77-81)":
            return self.ONE_AMONG(std, fac, ["pat1","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5"], 0)
        if val == "เลือกสอบ PAT 1 หรือ PAT 7 (77-82)":
            return self.ONE_AMONG(std, fac, ["pat1","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6"], 0)
        if val == "เลือกสอบ PAT1 หรือ PAT 7 (77-82)":
            return self.ONE_AMONG(std, fac, ["pat1","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6"], 0)            
        if val == "เลือกสอบ PAT1 หรือ PAT 7 (77-83)":
            return self.ONE_AMONG(std, fac, ["pat1","pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"], 0)            
        if val == "เลือก 1 วิชา" and col == "pat7":
            return self.ONE_AMONG(std, fac, ["pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"], 0)

        # print("No function for [{},{}]".format(col, val))
        # return False
        return True

    def GREATER_THAN(self, std, fac, subj, val):
        score = std.getMaxBySubject(subj)
        if not score: return False
        return score[0] >= val

    def ONE_GREATER_THAN_MEAN(self, std, fac, subj_list, val):
        for subj in subj_list:
            if self.is_used(fac, subj) == False: continue
            if self.GREATER_THAN_MEAN(std, fac, subj, val): return True
        return False

    def GREATER_THAN_MEAN(self, std, fac, subj, val):
        score = std.getBySubject(subj)
        if not score: return False
        for s in score:
            if s[0] >= self.mean[s[1]][subj] + val:
                return True
        return False

    def ONE_AMONG(self, std, fac, subj_list, val):
        # for pat7 only not depend on faculty data
        for subj in subj_list:
            # if self.is_used(fac, subj) == False: continue            
            if self.GREATER_THAN(std, fac, subj, val):
                return True
        return False

    def SUM_GREATER_THAN(self, std, fac, subj_list, val):
        sum_score = 0
        for subj in subj_list:
            if self.is_used(fac, subj) == False: continue
            score = std.getMaxBySubject(subj)
            if not score: return False
            sum_score += score[0]
        return sum_score >= val

    def DIFF_GREATER_THAN(self, std, fac, subj_list, val):
        sum_diff = 0
        for subj in subj_list:
            if self.is_used(fac, subj) == False: continue            
            subj_score = std.getBySubject(subj)
            if not subj_score: return False
            subj_diff = -1000000
            for score in subj_score:
                subj_diff = max(subj_diff,score[0]-self.mean[score[1]][subj])
            sum_diff += subj_diff
        return sum_diff >= val