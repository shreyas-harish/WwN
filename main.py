from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *
from floydWarshall import *

g = inputFile()
dist1 = dynamicAllPairsShortestPaths(g)
dist2 = dynamicAllPairsShortestPathsFaster(g)
dist3 = floydWarshall(g)
print(arrayCompare(dist1,dist2))
print(arrayCompare(dist1,dist3))
gridPrint(g,dist3)