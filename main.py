from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *
from floydWarshall import *
from yen import *
from astar import *
from maxflow import *

g1 = inputFile("/Users/shreyasharish/Documents/WwN/input2.txt")
flow = pushRelabelHeuristics(g1,"0","5")
print(flow["flow"])
#flow["flowGraph"].printGraph()
"""
flow = pushRelabel(g1,"0","5")
print(flow["flow"])

flow = edmondsKarps(g1,"0","7")
print(flow["flow"])
"""