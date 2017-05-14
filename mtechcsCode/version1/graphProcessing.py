from graph_tool.all import *
from graph_tool.draw import graphviz_draw as gd
import graph_tool.all as gt
import gc

G = load_graph("graphInitialRun_v10_entity_trans_class.dot")
pageRank = G.new_vertex_property("double")
G.vertex_properties["pageRank"] = pageRank
valuation = G.ep.TransactionValues
widthTrans = valuation.copy()
pageRank = gt.pagerank(G)
#gt.remove_parallel_edges(G)
gt.remove_self_loops(G)
pos = gt.sfdp_layout(G)
graph_draw(G, pos = pos,vertex_size=pageRank,edge_color=valuation ,edge_pen_width=widthTrans,output="graphInitialRun_v10_entity_trans_class.pdf")