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
flow = pushRelabel(g1,"0","5")
print(flow["flow"])
flow["flowGraph"].printGraph()