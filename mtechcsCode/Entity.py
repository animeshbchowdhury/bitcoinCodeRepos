# Animesh Change to Branch_v1
from sets import Set
import Transaction

class Entity:
    listOfAddress = None
    listOfOutTrans = None
    listOfInTrans = None
    
    def __init__(self,addrList):
        self.listOfAddress = []
        self.listOfInTrans = []
        self.listOfOutTrans = []
        for addr in addrList:
            self.listOfAddress.append(addr)

    def addAddress(self,addr):
        self.listOfAddress.append(addr)

    def addInTransact(self,inTrans):
        self.listOfInTrans.append(inTrans)

    def addOutTransact(self,outTrans):
        self.listOfOutTrans.append(outTrans)

    def getInTransact(self):
        return self.listOfInTrans

    def getOutTransact(self):
        return self.listOfOutTrans

    def getAddrList(self):
        return self.listOfAddress

