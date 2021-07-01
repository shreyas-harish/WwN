from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *

g = inputFile()
bellmanFord(g,"0")
g.printThroughParent("5")