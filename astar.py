# This file contains warm start shortest path algorithm related helper functions through A* implementation
from graphDefs import *
from readInput import *
from floydWarshall import *
from yen import *

pathLengthsByNode = {}

# Function to reset path lengths for all nodes to None


def resetPathLengths(givenGraph):
    global pathLengthsByNode
    pathLengthsByNode.clear()
    for nod in givenGraph.nodes.keys():
        pathLengthsByNode[nod] = None

# Function to get the estimated distance from one node to any other node


def getEstimatedDistance(nodeID, endNodeID, distanceMatrix, matrixMap):
    rowNo = None
    colNo = None
    count = 0
    for nod in matrixMap:
        if nod == nodeID:
            rowNo = count
        if nod == endNodeID:
            colNo = count
        count += 1
    if (not rowNo == None) and (not colNo == None):
        return distanceMatrix[rowNo][colNo]
    else:
        return None

# Function to find the node with the lowest total path length from all active nodes


def closest(g):
    min = None
    closeNode = None
    for n in g.nodes.keys():
        nod = g.nodes[n]
        # Check if node has been visited yet
        if nod.category == 1:
            if min == None:
                min = pathLengthsByNode[n]
                closeNode = n
            elif pathLengthsByNode[n] < min:
                min = pathLengthsByNode[n]
                closeNode = n
    return closeNode

# Function to create node to node distance map for the A* algorithm


def setAStar(startGraph):
    # Mapping of nodes to the order in which they will be present in the distance matrix
    nodeToNumberMap = []
    for n in startGraph.nodes.keys():
        nodeToNumberMap.append(startGraph.nodes[n].nodeID)
    # Call floyd warshall to get the distance matrix
    distanceMatrix = floydWarshall(startGraph)

    return {"distanceMatrix": distanceMatrix, "matrixMap": nodeToNumberMap}

# Function to find the shortest path between any s & t, by providing a warm start to the dijkstra's algorithm (using the A* algorithm)


def aStar(distMatrix, currentGraph, startNode, endNode):
    # Get the distance matrix and the mapping of node number to row & column
    distanceMatrix = distMatrix["distanceMatrix"]
    matrixMap = distMatrix["matrixMap"]
    # Keep the global path lengths variable in place
    resetPathLengths(currentGraph)
    global pathLengthsByNode
    # Initialise the starting node as the current node
    current = currentGraph.nodes[startNode]
    current.setDistance(0)
    pathLengthsByNode[startNode] = getEstimatedDistance(
        startNode, endNode, distanceMatrix, matrixMap)
    current.setCategory(2)
    count = 1
    while not current == None:
        #print("iteration ", count)
        #print("parent ", current.nodeID)
        for n in current.edgesOut.keys():
            nod = currentGraph.nodes[n]
            newDistance = current.distance+current.edgesOut[n].cost
            if not nod.category == 2:
                if (nod.distance == None) or (nod.distance > newDistance):
                    #print("node changed ")
                    # nod.printNode()
                    #print("distance change ", nod.distance, " to ", newDistance)
                    nod.setDistance(newDistance)
                    #print("path length change from ", pathLengthsByNode[nod.nodeID]),
                    pathLengthsByNode[nod.nodeID] = nod.distance + getEstimatedDistance(
                        nod.nodeID, endNode, distanceMatrix, matrixMap)
                    #print(" to ", pathLengthsByNode[nod.nodeID])
                    if nod.category == 0:
                        nod.setCategory(1)
                    nod.setParent(current.nodeID)
        if not closest(currentGraph) == None:
            current = currentGraph.nodes[closest(currentGraph)]
            current.setCategory(2)
            if current.nodeID == endNode:
                return pathToArray(currentGraph, current)
        else:
            current = None
        count += 1

    return None