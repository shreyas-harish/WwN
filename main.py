from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *
from floydWarshall import *
from yen import *

g = inputFile()
distances = floydWarshall(g)
paths = yenKSP(g, "4", "7", 10)
print(len(paths))
for p in paths:
    printPath(p)