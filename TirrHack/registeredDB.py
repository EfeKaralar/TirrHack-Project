class DataBase:
    def __init__(self):
        self.famName = None
        self.famID = None
        self.famPass = None

    def getFamName(self):
        return self.famName

    def getFamID(self):
        return self.famName

    def getFamPass(self):
        return self.famPass

    def save(self, fName, fID, fPass):
        famName = fName
        famID = fID
        famPass = fPass