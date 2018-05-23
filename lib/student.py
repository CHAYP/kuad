import csv

class Student:

    def __init__(self,id,prefix,first_name,last_name):
        self.id = id
        self.prefix = prefix
        self.first_name = first_name
        self.last_name = last_name

        self.plan = ""
        self.gpa = -1
        
        self.chooses = []
        self.score = {}
        self.data = {}

        self.min_year = "2560"
        # minimun year

    def load_data_with_year(self, year_str, data):
        for key in data:
            if year_str not in self.data: self.data[year_str] = {}
            self.data[year_str][key] = data[key]

    def get_max_score_by_subject(self, subject):
        tmp = self.get_score_by_subject(subject)
        if not tmp: return []
        return max(tmp)
    
    def get_score_by_subject(self, subject):
        # tmp = [(self.data[year][subject], year) for year in self.data if self.data[year].get(subject,-1) != -1 and year >= self.min_year]
        tmp = [(self.data[year][subject], year) for year in self.data if self.data[year].get(subject,-1) != -1]
        return tmp

    def getMaxPat7(self):
        pat7_list = ["pat7_1","pat7_2","pat7_3","pat7_4","pat7_5","pat7_6","pat7_7"]
        score = []
        for subj in pat7_list:
            tmp = self.get_max_score_by_subject(subj)
            if tmp: score.append(tmp)
        if not score: return []
        return max(score)

    def get_score(self, year, subject):
        return self.data[year][subject], year
