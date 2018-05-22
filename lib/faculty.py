class Faculty:
    def __init__(self,_id,name,cap,gpa,plan):
        self.id = _id
        self.name = name
        self.cap = cap
        self.gpa = gpa
        self.plan = plan
        self.gender = "both"
        self.data = {}
        
    def loadData(self, data):
        for key in data: self.data[key] = data[key]
        
