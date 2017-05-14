from graph_tool.all import *
from blockchain import blockexplorer
from blockchain.blockexplorer import Block,Input,Output,Transaction
import pickle
from sets import Set
import numpy as np
import collections as cl

NUM_BLOCKS = 5000
g = Graph()
addressList = Set()
addrVertexDict = {}
entityAddr = g.new_vertex_property("vector<string>")
edgeWeight = g.new_edge_property("long")
transactionHashValue = g.new_edge_property("string")
g.vertex_properties["listOfAddress"] = entityAddr
g.edge_properties["TransactionValues"] = edgeWeight
g.edge_properties["TransactionHashValues"] = transactionHashValue
TObjects = []
amtTransObjDict = {}

while NUM_BLOCKS>4976:
    pickledFileName = "testdata/block_"+str(NUM_BLOCKS)+".pickle"
    fileHandler = open(pickledFileName,'r+')
    bitcoinBlock = pickle.load(fileHandler)
    transactionObj = bitcoinBlock.transactions
    print bitcoinBlock.hash
    print "--------------------------"
    # Starting from 1, as 1st transaction has no input.
    transactionAmounts = []
    for obj in transactionObj[1:]:
        addrInp = obj.inputs
        addrOut = obj.outputs
        tAmt = 0
        if(len(addrInp)<len(addrOut)):
            for adrI in addrInp:
                tAmt+= adrI.value
        else:
            for adrI in addrOut:
                tAmt += adrI.value

        #print tAmt
        if(tAmt not in amtTransObjDict.keys()):
            amtTransObjDict[tAmt] = [obj]
        else:
            amtTransObjDict[tAmt].append(obj)
    NUM_BLOCKS -= 1


sortedTransactionDict = cl.OrderedDict(reversed(sorted(amtTransObjDict.items())))
print sortedTransactionDict.keys()
print sortedTransactionDict.__len__()
topTenPercent = sortedTransactionDict.__len__()*0.1

print topTenPercent
listRequired = list(sortedTransactionDict)
print listRequired[0]

elm = 0
while(topTenPercent>1):
    keyVal = listRequired[elm]
    transObjList = sortedTransactionDict[keyVal]
    for transObj in transObjList:
        addrInp = transObj.inputs
        addrOut = transObj.outputs
        print "Inputs ----------------------"
        v1 = g.add_vertex()
        list = []
        for adrI in addrInp:
            print adrI.address
            list.append(adrI.address)
        entityAddr[v1] = list

        print "Outputs ----------------------"
        for adrO in addrOut:
            v2 = g.add_vertex()
            entityAddr[v2] = [adrO.address]
            edgeTrans = g.add_edge(v1, v2)
            edgeWeight[edgeTrans] = adrO.value
            transactionHashValue[edgeTrans] = transObj.hash
        print"\n\n"
        elm+=1
        topTenPercent-=1

g.save("graphInitialRun_v6.dot",fmt='dot')