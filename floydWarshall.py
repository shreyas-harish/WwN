# This file contains shortest path between all pairs of nodes algorithm related helper functions throughfloyd warshall & another dynamic programming approach
from graphDefs import *
from readInput import *

# Function to format string with padding spaces


def formatPadding(inp):
    output = "{0:>6}".format(inp)
    return output

# Function to print the distance matrix in grid form


def gridPrint(g, dist):
    nodeToNumberMap = []
    for n in g.nodes.keys():
        nodeToNumberMap.append(g.nodes[n].nodeID)
    print(formatPadding(""), end="")
    for i in range(len(nodeToNumberMap)):
        print("|", end="")
        print(formatPadding(nodeToNumberMap[i]), end="")

    print("")
    for i in range(len(nodeToNumberMap)):
        print(formatPadding(nodeToNumberMap[i]), end="")
        for j in range(len(nodeToNumberMap)):
            print("|", end="")
            print(formatPadding(str(dist[i][j])), end="")
        print("")


# Function to copy a 2D array
def arrayCopy(arr):
    rowNo = 0
    colNo = 0
    rowCount = len(arr)
    colCount = len(arr[0])
    copyArr = [[None for i in range(colCount)] for j in range(rowCount)]
    for row in arr:
        colNo = 0
        for col in row:
            copyArr[rowNo][colNo] = col
            colNo += 1
        rowNo += 1

    return copyArr

# Function to compare 2 a 2D arrays


def arrayCompare(arr1, arr2):
    rowNo = 0
    colNo = 0
    rowCount = len(arr1)
    colCount = len(arr1[0])
    sameArr = True
    if not ((len(arr2) == rowCount) and (len(arr2[0]) == colCount)):
        sameArr = False
    copyArr = [[None for i in range(colCount)] for j in range(rowCount)]
    for row in arr1:
        colNo = 0
        for col in row:
            if not arr2[rowNo][colNo] == col:
                sameArr = False
            colNo += 1
        rowNo += 1

    return sameArr

# Function to compare current distances vs distance through intermediary and make change if need be


def compareDist(currentDist, distance1, distance2):
    if currentDist == None:
        if ((distance1 == None) or (distance2 == None)):
            return None
        else:
            return (distance1+distance2)
    else:
        if ((distance1 == None) or (distance2 == None)):
            return currentDist
        else:
            if currentDist > (distance1+distance2):
                return (distance1+distance2)
            else:
                return currentDist

# Function to return all pairs shortest paths through dynamic programming in O(V^4)


def dynamicAllPairsShortestPaths(g):
    # Initialising the distances array
    nodeCount = len(g.nodes)
    directCost = [[None for i in range(nodeCount)] for j in range(nodeCount)]
    nodeToNumberMap = []
    for n in g.nodes.keys():
        nodeToNumberMap.append(g.nodes[n].nodeID)
        nodeNumber = len(nodeToNumberMap)-1
        directCost[nodeNumber][nodeNumber] = 0
    nodeNumber = 0
    for n in g.nodes.keys():
        for ed in g.nodes[n].edgesOut.keys():
            directCost[nodeNumber][nodeToNumberMap.index(
                ed)] = g.nodes[n].edgesOut[ed].cost
        nodeNumber += 1

    dist = arrayCopy(directCost)
    # Iterate V times
    for iter in range(nodeCount):
        distCopy = arrayCopy(dist)
        # Iterate through all start nodes
        for i in range(nodeCount):
            # Iterate through all end nodes
            for j in range(nodeCount):
                # Iterate through all incoming nodes
                for k in range(nodeCount):
                    distCopy[i][j] = compareDist(
                        distCopy[i][j], dist[i][k], directCost[k][j])
        print("iteration ", (iter+1))
        gridPrint(g, distCopy)
        dist = distCopy

    return dist

# Function to return all pairs shortest paths through dynamic programming in O(V^3log(V))


def dynamicAllPairsShortestPathsFaster(g):
    # Initialising the distances array
    nodeCount = len(g.nodes)
    directCost = [[None for i in range(nodeCount)] for j in range(nodeCount)]
    nodeToNumberMap = []
    for n in g.nodes.keys():
        nodeToNumberMap.append(g.nodes[n].nodeID)
        nodeNumber = len(nodeToNumberMap)-1
        directCost[nodeNumber][nodeNumber] = 0
    nodeNumber = 0
    for n in g.nodes.keys():
        for ed in g.nodes[n].edgesOut.keys():
            directCost[nodeNumber][nodeToNumberMap.index(
                ed)] = g.nodes[n].edgesOut[ed].cost
        nodeNumber += 1

    dist = arrayCopy(directCost)
    # Iterate V times
    for iter in range(nodeCount):
        distCopy = arrayCopy(dist)
        # Iterate through all start nodes
        for i in range(nodeCount):
            # Iterate through all end nodes
            for j in range(nodeCount):
                # Iterate through all incoming nodes
                for k in range(nodeCount):
                    distCopy[i][j] = compareDist(
                        distCopy[i][j], dist[i][k], dist[k][j])

        print("iteration ", (iter+1))
        gridPrint(g, distCopy)
        if arrayCompare(dist, distCopy):
            return dist
        else:
            dist = distCopy

    return dist

# Function to return all pairs shortest paths through floyd warshall algorithm


def floydWarshall(g):
    # Initialising the distances array
    nodeCount = len(g.nodes)
    dist = [[None for i in range(nodeCount)] for j in range(nodeCount)]
    nodeToNumberMap = []
    for n in g.nodes.keys():
        nodeToNumberMap.append(g.nodes[n].nodeID)
        nodeNumber = len(nodeToNumberMap)-1
        dist[nodeNumber][nodeNumber] = 0
    nodeNumber = 0
    for n in g.nodes.keys():
        for ed in g.nodes[n].edgesOut.keys():
            dist[nodeNumber][nodeToNumberMap.index(
                ed)] = g.nodes[n].edgesOut[ed].cost
        nodeNumber += 1

    iter = 0
    # Iterate through all incoming nodes
    for k in range(nodeCount):
        # Iterate through all start nodes
        for i in range(nodeCount):
            # Iterate through all end nodes
            if (not i == k):
                for j in range(nodeCount):
                    if (not j == k):
                        dist[i][j] = compareDist(
                            dist[i][j], dist[i][k], dist[k][j])
        iter += 1
        print("iteration ", (iter), " intermediary node ", nodeToNumberMap[k])
        gridPrint(g, dist)

    return dist
