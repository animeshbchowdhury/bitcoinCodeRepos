from graph_tool.all import *
from graph_tool.draw import graphviz_draw as gd
import graph_tool.all as gt
import gc
import math

G = load_graph("graphDumpFor25BlocksTopPointFivePercent_1.2_16122016.dot")
pageRank = G.new_vertex_property("double")
G.vertex_properties["pageRank"] = pageRank
valuation = G.ep.TransactionValues
widthTrans = valuation.copy()
pageRank = gt.pagerank(G)
#gt.remove_parallel_edges(G)
gt.remove_self_loops(G)
pos = gt.sfdp_layout(G)

for e in G.edges():
    if (widthTrans[e] != 0):
        widthTrans[e] = int(math.log10(float(widthTrans[e]))/7)
graph_draw(G, pos = pos,vertex_size=pageRank,edge_pen_width=widthTrans,output="graphDumpFor25BlocksTopPointFivePercent_1.2_16122016.pdf")