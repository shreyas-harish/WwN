from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *
from floydWarshall import *
from yen import *
from astar import *

g1 = inputFile("/Users/shreyasharish/Documents/WwN/input.txt")
#"""
paths = yenKSP(g1,"0","7",5)
for p in paths:
    printPath(p)
#"""
#"""
g2 = inputFile("/Users/shreyasharish/Documents/WwN/input2.txt")
distMatrix = setAStar(g1)
path = aStar(distMatrix,g1,"0","7")
printPath(path)
path = aStar(distMatrix,g2,"0","7")
printPath(path)
#"""