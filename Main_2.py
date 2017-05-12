from graph_tool.all import *
from blockchain import blockexplorer
from blockchain.blockexplorer import Block,Input,Output,Transaction
import pickle
from sets import Set
import numpy as np
import collections as cl
from Entity import Entity
from Transaction import Transaction
from graph_tool.draw import graphviz_draw as gd
import graph_tool.all as gt
import gc
import matplotlib.pyplot as plt
import math

NUM_BLOCKS_TO_BE_PROCESSED = 150
STARTING_NUM_BLOCK = 15000
graphObj = None
entityAddr = None
edgeWeight = None
addressList = Set()
addrVertexDict = {}
amtTransObjDict = {}
entityList = []
transactList = []

def initializeGraphProperties():
    global entityAddr,edgeWeight
    g = Graph()
    entityAddr = g.new_vertex_property("vector<string>")
    edgeWeight = g.new_edge_property("long")
    g.vertex_properties["listOfAddress"] = entityAddr
    g.edge_properties["TransactionValues"] = edgeWeight
    return g


def collectDataFromBitcoinDataSet():
    global NUM_BLOCKS_TO_BE_PROCESSED,STARTING_NUM_BLOCK,amtTransObjDict
    startBlockNum = STARTING_NUM_BLOCK
    endBlockNum = startBlockNum-NUM_BLOCKS_TO_BE_PROCESSED
    while startBlockNum > endBlockNum:
        pickledFileName = "testdata/Block" + str(startBlockNum) + ".pickle"
        fileHandler = open(pickledFileName, 'r+')
        bitcoinBlock = pickle.load(fileHandler)
        transactionObj = bitcoinBlock.transactions
        # Starting from 1, as 1st transaction has no input.
        for obj in transactionObj[1:]:
            addrInp = obj.inputs
            addrOut = obj.outputs
            for adrO in addrOut:
                tAmt = adrO.value
                if (tAmt not in amtTransObjDict.keys()):
                    amtTransObjDict[tAmt] = [[addrInp, adrO]]
                else:
                    amtTransObjDict[tAmt].append([addrInp, adrO])
        startBlockNum -= 1


def processDataAndCreateEntities():
    global amtTransObjDict,entityList,transactList
    sortedTransactionDict = cl.OrderedDict(reversed(sorted(amtTransObjDict.items())))
    print sortedTransactionDict.keys()
    print sortedTransactionDict.__len__()
    topTenPercent = sortedTransactionDict.__len__() * 0.005

    print topTenPercent
    listRequired = list(sortedTransactionDict)
    print listRequired[0]

    elm = 0
    addressEntityMap = {}

    while (topTenPercent > 1):
        keyVal = listRequired[elm]
        ElementList = sortedTransactionDict[keyVal]
        for Element in ElementList:
            addrInp = Element[0]
            adrO = Element[1]
            # print "Inputs ----------------------"
            flag = 0
            list = []
            foundAddress = []
            sourceEntity = None
            sinkEntity = None
            for adrI in addrInp:
                if (adrI.address not in list):
                    list.append(adrI.address)
                if (adrI.address in addressEntityMap.keys()):
                    flag = 1
                    foundAddress.append(adrI.address)

            if (flag == 0):
                sourceEntity = Entity(list)
                entityList.append(sourceEntity)
                for element in list:
                    addressEntityMap[element] = sourceEntity
            else:
                Elist = []
                for eachAddr in foundAddress:
                    if (addressEntityMap[eachAddr] not in Elist):
                        Elist.append(addressEntityMap[eachAddr])

                parentEntity = Elist[0]
                for addr in list:
                    if addr not in parentEntity.getAddrList():
                        parentEntity.addAddress(addr)
                        addressEntityMap[addr] = parentEntity

                if (Elist.__len__() > 1):
                    for ent in Elist[1:]:
                        addrHold = ent.getAddrList()
                        inTrans = ent.getInTransact()
                        outTrans = ent.getOutTransact()
                        for addr in addrHold:
                            parentEntity.addAddress(addr)
                            addressEntityMap[addr] = parentEntity
                        for inT in inTrans:
                            inT.updateDest(parentEntity)
                            parentEntity.addInTransact(inT)
                        for outT in outTrans:
                            outT.updateOrigin(parentEntity)
                            parentEntity.addOutTransact(outT)
                        entityList.remove(ent)
                sourceEntity = parentEntity
            # v1 = g.add_vertex()
            # entityAddr[v1] = list

            # print "Outputs ----------------------"
            # v2 = g.add_vertex()
            if (adrO.address in addressEntityMap.keys()):
                sinkEntity = addressEntityMap[adrO.address]
            else:
                sinkEntity = Entity([adrO.address])
                entityList.append(sinkEntity)
                addressEntityMap[adrO.address] = sinkEntity

            transactObj = Transaction(sourceEntity, sinkEntity, adrO.value)
            sourceEntity.addOutTransact(transactObj)
            sinkEntity.addInTransact(transactObj)
            transactList.append(transactObj)
            # entityAddr[v2] = [adrO.address]
            # edgeTrans = g.add_edge(v1, v2)
            # edgeWeight[edgeTrans] = adrO.value
            # transactionHashValue[edgeTrans] = transObj.hash
        print elm
        elm += 1
        topTenPercent -= 1



def createGraphAndDumpGraphData():
    global graphObj,entityList,transactList
    for ent in entityList:
        vtx = graphObj.add_vertex()
        entityAddr[vtx] = ent.getAddrList()

    for trans in transactList:
        entSr = trans.getSourceEntity()
        entSi = trans.getSinkEntity()
        vertexSr = graphObj.vertex(entityList.index(entSr))
        vertexSi = graphObj.vertex(entityList.index(entSi))
        edgeTrans = graphObj.add_edge(vertexSr, vertexSi)
        edgeWeight[edgeTrans] = trans.getTransValue()
        #transactionHashValue[edgeTrans] = transObj.hash

    graphObj.save("graphDumpFor150BlocksTopPointFivePercent_1.2_16122016.dot",fmt='dot')

def main():
    global graphObj
    graphObj = initializeGraphProperties()
    collectDataFromBitcoinDataSet()
    processDataAndCreateEntities()
    createGraphAndDumpGraphData()


if __name__=='__main__':
    main()