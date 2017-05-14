from sets import Set
import Entity

class Transaction:
    tValue = None
    originEntity = None
    destEntity = None

    def __init__(self,oEnt,dEnt,tVal):
        self.tValue = tVal
        self.originEntity = oEnt
        self.destEntity = dEnt

    def updateOrigin(self,oEnt):
        self.originEntity = oEnt

    def updateDest(self,dEnt):
        self.destEntity = dEnt

    def getSourceEntity(self):
        return self.originEntity

    def getSinkEntity(self):
        return self.destEntity

    def getTransValue(self):
        return self.tValue
