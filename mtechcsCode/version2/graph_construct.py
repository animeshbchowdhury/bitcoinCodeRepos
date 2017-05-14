# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import blockchain.blockexplorer as blx
from igraph import Graph
import pickle
import time

#Get all blocks for a particuar date. Adjust starthash and numblocks by getting
#the last block hash and number of blocks mined from blockchain.info
numblocks = 1500
startHash = '0000000000000000006e566f8f2bccd239a1967ea23c37629341539357d0eb2f'


h = startHash
for i in range(numblocks):
    file = open('/media/ritwiksadhu/2C8E33918E335316/Compre group project/bChain4/block' + str(i) + ".dat", mode = 'wb')
    bl = blx.get_block(h)
    pickle.dump(bl, file)
    file.close()
    h = bl.previous_block

#Extract transactions from the blocks, except the chain base transactions.
#Create a graph of addresses transacting with each other, with the weight being
#the volume of transactions.

tx_graph = Graph(directed = True)

#Create and save blockwise graphs
numblocks = 1500
count = 0
skiplist = []
for i in range(numblocks):
    st = time.time()
    g = Graph(directed=True)
    print('Block ' + str(i))
    file = open('/media/ritwiksadhu/2C8E33918E335316/Compre group project/bChain4/block' + str(i) + ".dat", mode = 'rb')
    bl = pickle.load(file)
    if(len(bl.transactions) == 1):
        skiplist.append(i)
        continue
    file.close()
    tx_list = bl.transactions
    l2 = sum([len(tx.outputs) for tx in tx_list[1:]])
    l1 = l2 + len(tx_list) - 1
    g.add_vertices(l1)
    j = 0
    e = 0
    for k,tx in enumerate(tx_list[1:]):
        g.add_edges([(j,j+l+1) for l in range(len(tx.outputs))])
        g.vs[j]['addr_list'] = set([inp.address for inp in tx.inputs])
        for k,output in enumerate(tx.outputs):
            g.vs[j+k+1]['addr_list'] = {output.address}
            g.es[e+k]['weight'] = output.value
        j += len(tx.outputs) + 1
        e += len(tx.outputs)
    pickle.dump(g, open('RawGraphs/g_block' + str(i) + '.dat', mode='wb'))
    
    del g
    del bl
    del tx_list
    print(str(time.time()-st) + 'seconds elapsed')
        
#combine the blockwise graphs
g_list = []
addr = []
weight = []
for i in range(numblocks):
    if i in skiplist:
        continue
    g = pickle.load(open('RawGraphs/g_block' + str(i) + '.dat', mode='rb'))
    addr += g.vs['addr_list']
    weight += g.es['weight']
    g_list.append(g)
print(type(weight[0]))
tx_graph = tx_graph.disjoint_union(g_list)
tx_graph.vs['addr_list'] = addr
tx_graph.es['weight'] = weight
print(tx_graph.summary())
#Remove self transaction edges and add weights of multiple transaction wedges 
#between same pair of entities, and collapse entities with common addresses
#into single entity


#Create mapping from from old vertex ids to new ones by combining entities with
#common addresses using union find algorithm

print("Combine addresses into entities")
st = time.time()
entity_map = {}
parent = {}

for i,entity in enumerate(tx_graph.vs["addr_list"]):
    for addr in entity:
        if addr not in entity_map.keys():
            entity_map[addr] = i
    idval = min([entity_map[addr] for addr in entity])
    parent[i] = idval

#Find function for union find
def find(i):
    if parent[i] == i:
        return i
    else:
        return find(parent[i])

mapping = [find(i) for i in range(len(tx_graph.vs))]
#Define a function to combine address lists of all vertices combined into
#new single vertex.
def combine_addr(entity_list):
    y = set()
    for entity in entity_list:
        y.update(entity)
    return y

#Contract the graph to newly obtained entities and remove self loop transactions
tx_graph.contract_vertices(mapping, combine_attrs = combine_addr)
tx_graph.vs.select(_degree = 0).delete()
tx_graph.simplify(combine_edges = "sum")
tx_graph.es.select(weight_eq = 0).delete()
print(str(time.time()-st) + ' seconds elapsed')
#Save the transaction graph to file.
f = open("DemoTransactionGraph.graphml", mode="wb")
tx_graph.save(f, format = "graphml")
pickle.dump(tx_graph, open("Graph_obj.dat", mode = "wb"))

