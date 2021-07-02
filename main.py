from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *

g = inputFile()
dijkstra(g,"0")
g = inputFile()
dijkstraMinHeap(g,"0")