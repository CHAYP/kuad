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
        
    def GREATER_THAN(self, std, fac, subj, val):
        score = std.get_max_score_by_subject(subj)
        if not score: return False
        return score[0] >= val

    def ONE_GREATER_THAN_MEAN(self, std, fac, subj_list, val):
        for subj in subj_list:
            if self.is_used(fac, subj) == False: continue
            if self.GREATER_THAN_MEAN(std, fac, subj, val): return True
        return False

    def GREATER_THAN_MEAN(self, std, fac, subj, val):
        score = std.get_score_by_subject(subj)
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
            score = std.get_max_score_by_subject(subj)
            if not score: return False
            sum_score += score[0]
        return sum_score >= val

    def DIFF_GREATER_THAN(self, std, fac, subj_list, val):
        sum_diff = 0
        for subj in subj_list:
            if self.is_used(fac, subj) == False: continue            
            subj_score = std.get_score_by_subject(subj)
            if not subj_score: return False
            subj_diff = -1000000
            for score in subj_score:
                subj_diff = max(subj_diff,score[0]-self.mean[score[1]][subj])
            sum_diff += subj_diff
        return sum_diff >= val