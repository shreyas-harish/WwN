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
from minCost import *

g1 = inputFile("/Users/shreyasharish/Documents/WwN/input2.txt")
flow = pushRelabelHeuristics(g1,"7","29")
#print(flow["flow"])
#flow["flowGraph"].printGraph()
#minCostFlow2 = cycleCancelling(g1,"0","39",98)
#print(minCostFlow2["cost"])

i = 1
matchCount = 0
missCount = 0
while i <= flow["flow"]:
    minCostFlow1 = capacityScaling(g1,"7","29",i)
    minCostFlow2 = cycleCancelling(g1,"7","29",i)
    if minCostFlow1["cost"] == minCostFlow2["cost"]:
        matchCount += 1
        #print("flow volume ",i," -> cost ",minCostFlow1["cost"])
    else:
        missCount += 1
        print("flow volume ",i," -> cost1 ",minCostFlow1["cost"]," cost2 ",minCostFlow2["cost"])
        #print("Graph 1")
        #minCostFlow1["flowGraph"].printGraph()
        #print("Graph 2")
        #minCostFlow2["flowGraph"].printGraph()
    i += 1


#print(minCostFlow["cost"])
print("matches ",matchCount)
print("misses ",missCount)
#print(minCostFlow["cost"])
#minCostFlow["flowGraph"].printGraph()
"""
flow = pushRelabel(g1,"0","5")
print(flow["flow"])

flow = edmondsKarps(g1,"0","7")
print(flow["flow"])
"""