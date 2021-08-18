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

#For mac file referencing
#g1 = inputFile("/Users/shreyasharish/Documents/WwN/input.txt")
g1 = inputFile(r"C:\Users\shrey\Downloads\WwN-main\WwN-main\input.txt")

#BFS Functions
"""
#Reset all global variables
breadthFirstReset()
#BFS
foundBoolean = breadthFirstSearch(g1,"0","1")
#Identify which nodes are reachable and unreachable from start node
reachSet = breadthFirstReach(g1,"0")
#Build up a Breadth First Forest and print details
g2 = breadthFirstForestBuilder(g1)
"""

#DFS Functions
"""
#Reset all global variables
depthFirstReset()
#DFS
foundBoolean =  depthFirstSearch(g1,"0","1")
#Identify which nodes are reachable and unreachable from start node
reachSet = depthFirstReach(g1,"0")
#Build up a Depth First Forest and print details
g2 = depthFirstForestBuilder(g1)
"""

#Bellman Ford Functions (works for negative arcs, not cycles)
"""
#Prints distances of all nodes in the graph
distanceDictionary = distances(g1)
#Returns a complete list of all edges (edge object) from a graph
edgeList = graphToEdgeList(g1)
#Shortest path s to all nodes via Bellman Ford
distanceDictionary = bellmanFord(g1,"0")
#Shortest path s to all nodes with better expected run-time (distance changes are direct, and not on a copy)
distanceDictionary = modifiedBellmanFord(g1,"0")
"""

#Dijkstra's Functions (doesn't work for negative arcs)
"""
#Shortest path s to all nodes via Dijkstra's O(v^2)
distanceDictionary = dijkstra(g1,"0")
#Shortest path s to all nodes in O(elogv) using min heaps
distanceDictionary = dijkstraMinHeap(g1,"0")
"""

#Floyd Warshall Functions (All pairs shortest path) (negative cycles discovered in matrix diagonal)
"""
#Dynamic Programming approach to all pairs shortest path (Ov^4)
distanceMatrix = dynamicAllPairsShortestPaths(g1)
#Dynamic Programming approach to all pairs shortest path with heuristic (Ov^3logv)
distanceMatrix = dynamicAllPairsShortestPathsFaster(g1)
#All pairs shortest path through Floyd Warshall
distanceMatrix = floydWarshall(g1)
#Print all pairs distances as a matrix
gridPrint(g1,distanceMatrix)
"""

#Yen's Algorithm for Kth Shortest Path Functions
"""
#Array containing path (of node objects) till node t
arrayPath = pathToArray(g1,"t")
#Dijkstra's shortest path s-t returned as an array
arrayPath = dijkstraOnePath(g1,"0","1")
#Functions to copy graph elements
edgeCopy = copyEdge(ed)
nodeCopy = copyNode(n)
graphCopy = copyGraph(g1)
#Returns all of the k shortest paths in increasing length order
shortestPaths = yenKSP(g1,"0","1","3")
#Prints a path given a path array
printPath(arrayPath)
"""

#A* Functions to Warm Start Dijkstra's
"""
#Setup A* through dijkstra's and set required variables
distanceMatrix = setAStar(g1)
#Shortest path s-t given changes to original graph (provide distance matrix from setAStar and updated version of graph)
arrayPath = aStar(distanceMatrix,g1,"0","1")
#Prints a path given a path array
printPath(arrayPath)
"""

#Max Flow Functions
"""
#Create a residual graph for a given starting graph (boolean is true if reverse edges should be negative)
residualGraph = convertToResidualGraph(g1,False)
#Remove all empty edges from a graph
positiveCapacityGraph = removeEmptyEdges(g1)
#Returns bottleneck flow possible in array of nodes (node object)
criticalFlow = criticalFlowInPath(arrayPath)
#Returns a graph as a difference between g1 & g2
differenceGraph = graphDifference(g1,g2)
#Maximum flow in a graph through Edmonds Karps
maximumFlow = edmondsKarps(g1,"0","1")
#Print flow volume and graph of flow
print("maximum flow = ",maximumFlow["flow"])
maximumFlow["flowGraph"].printGraph()
#Maximum Flow in a graph through Push Relabel Algorithm
maximumFlow = pushRelabelHeuristics(g1,"0","1")
"""

#Min Cost Functions
"""
#Returns bottleneck flow  and cost per unit flow possible in array of nodes (node object). Returned object is a dictionary with "cost" and "capacity"
costAndFlow = costAndFlowOfPath(arrayPath)
#Minimum cost flow for a given volume of flow between s-t using capacity scaling
minCostFlow = capacityScaling(g1,"0","1","10")
#Minimum cost flow for a given volume of flow between s-t using cycle cancelling
minCostFlow = cycleCancelling(g1,"0","1","10")
#Print flow volume, cost and graph of flow
print("maximum flow = ",minCostFlow["flow"])
print("minimum cost = ",minCostFlow["cost"])
minCostFlow["flowGraph"].printGraph()
#Find negative cycles and return them as a path (array of nodes)
negativeCycleArray = negativeCycleBelmanFord(g1)
"""
