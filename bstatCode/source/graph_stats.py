#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 23:03:10 2017

@author: ritwiksadhu
"""
import math
from igraph import Graph, IN, OUT
import scipy.stats as stats
import numpy as np
from matplotlib import pyplot as plt
import pickle

f=open('/media/ritwiksadhu/2612F1F212F1C739/Users/Ritwik Sadhu/AnacondaProjects/Bitcoin/Graph_obj.dat', mode = 'rb')
g = pickle.load(f)

print("No. of entities: " + str(len(g.vs)))
print("No. of transactions: " + str(len(g.es)))

addr_count = [math.log(len(x)) for x in g.vs["addr_list"] if len(x) != 1]
plt.hist(addr_count, bins = 100)
plt.title("Address Stats (Single address entities excluded)")
plt.xlabel("# Addresses in Entity(log scale)")
plt.ylabel("# Entities")
plt.savefig("addr_distn.png")
plt.close()

log_vals = [math.log(x) for x in g.es["weight"] if x != 0.0]
plt.hist(log_vals, bins = 100)
plt.title("Transactions Stats")
plt.xlabel("Transaction Valuation (in log(Satoshi))")
plt.ylabel("# of Transactions")
plt.savefig("tx_distn.png")
plt.close()

g.vs['pagerank'] = g.pagerank()
log_vals = [-math.log(x) for x in g.vs["pagerank"]]
plt.hist(log_vals, bins = 100)
plt.title("PageRank Stats of Entities")
plt.xlabel("Pagerank of entities (-ve log scale)")
plt.ylabel("# of entities")
plt.savefig("pgrank_distn.png")
plt.close()

g.vs["tx_balance"] = (np.array(g.strength(mode = IN, weights = 'weight')) - np.array(g.strength(mode = OUT))).tolist()
q = np.percentile(g.vs['tx_balance'], 99)
tx_bal_log_robust = [math.log(x) for x in g.vs['tx_balance'] if x > 0 and x < q]
plt.hist(tx_bal_log_robust, bins = 100)
plt.title("Tx_Balance Stats of Entities (log scale, no-positive and outliers deleted)")
plt.xlabel("Day Tx. balance of entities")
plt.ylabel("# of entities")
plt.savefig("tx_bal_distn.png")
plt.close()


#Cliques in the graph
cliques_list = g.maximal_cliques(min = 4)
file = open('/media/ritwiksadhu/2612F1F212F1C739/Users/Ritwik Sadhu/AnacondaProjects/Bitcoin/Clique_info.txt', mode ='w')
file.writelines('Number of cliques in the graph (size >= 3): ' + str(len(cliques_list)))
file.writelines('Maximal clique size:' + str(g.clique_number()))
file.close()
