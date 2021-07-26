# This file contains shortest path algorithm related helper functions through dijkstra's implementation
from graphDefs import *
from readInput import *
from dijkstras import *

# Function to return an array with the path (node list) from s to t, given t & graph


def pathToArray(g, t):
    pathFromT = []
    pathFromT.append(t)
    parent = t.parent
    while not parent == None:
        pathFromT.append(g.nodes[parent])
        parent = g.nodes[parent].parent
    pathToT = []
    i = len(pathFromT)-1
    while i >= 0:
        pathToT.append(pathFromT[i])
        i = i-1
    return pathToT

# Function to implement djikstra's algorithm to get a path (node list) from s to t


def dijkstraOnePath(g, s, t):
    heapList = []
    current = g.nodes[s]
    current.setDistance(0)
    current.setCategory(2)

    while not current == None:
        for n in current.edgesOut.keys():
            nod = g.nodes[n]
            newDistance = current.distance+current.edgesOut[n].cost
            if not nod.category == 2:
                if (nod.distance == None) or (nod.distance > newDistance):
                    nod.setDistance(newDistance)
                    if nod.category == 0:
                        nod.setCategory(1)
                        heapPush(g, heapList, n)
                    nod.setParent(current.nodeID)
        if len(heapList) > 0:
            current = g.nodes[heapPop(g, heapList)]
            current.setCategory(2)
            if current.nodeID == t:
                return pathToArray(g, current)
        else:
            current = None
    return None

# Function to copy an edge


def copyEdge(ed):
    edgeCopy = edge(ed.startNode, ed.endNode)
    edgeCopy.setCapacity(ed.capacity)
    edgeCopy.setCost(ed.cost)
    edgeCopy.setCategory(ed.category)
    edgeCopy.setUtilization(ed.utilization)
    return edgeCopy

# Function to copy a node


def copyNode(n):
    nodeCopy = node(n.nodeID)
    nodeCopy.setCategory(n.category)
    nodeCopy.setDistance(n.distance)
    nodeCopy.setParent(n.parent)
    for ed in sorted(n.edgesIn.keys()):
        edgeToAdd = copyEdge(n.edgesIn[ed])
        nodeCopy.addEdgeIn(edgeToAdd)
    for ed in sorted(n.edgesOut.keys()):
        edgeToAdd = copyEdge(n.edgesOut[ed])
        nodeCopy.addEdgeOut(edgeToAdd)
    return nodeCopy

# Function to copy graph


def copyGraph(g):
    graphCopy = graph()
    for n in sorted(g.nodes.keys()):
        nodeToAdd = copyNode(g.nodes[n])
        graphCopy.nodes[nodeToAdd.nodeID] = nodeToAdd
    return graphCopy

# Function to check if the root path matches the start of comparison path


def rootMatches(root, otherPath):
    rootLength = len(root)
    for i in range(rootLength):
        if not root[i].nodeID == otherPath[i].nodeID:
            return False
    return True

# Function to return subpath after a certain point


def restOfPath(path, start):
    if len(path) > start:
        return path[start:]
    else:
        return []

# Function to remove a path from the given graph and return modified graph


def removePath(g, path):
    if len(path) < 2:
        return g
    else:
        pos = 0
        while pos < (len(path)-1):
            g.delEdge(path[pos].nodeID, path[pos+1].nodeID)
            pos += 1
        return g

# Function to check if the given path isn't present in an array


def notPresent(path, listOfPaths):
    if path == None:
        return False
    for p in listOfPaths:
        if rootMatches(path, p):
            return False
    return True

# Function to calculate the length of a given path


def lengthOfPath(path):
    if len(path) < 2:
        return 0
    else:
        pos = 0
        length = 0
        while pos < (len(path)-1):
            length += path[pos].edgesOut[path[pos+1].nodeID].cost
            pos += 1
        return length

# Function to sort the paths in an array basis path length


def sortPaths(listOfPaths):
    pathLengths = []
    for path in listOfPaths:
        pathLengths.append((lengthOfPath(path), path))
    pathLengths.sort(key=lambda x: x[0])
    sortedPaths = []
    for path in pathLengths:
        sortedPaths.append(path[1])
    return sortedPaths

# Function to implement yen's algo and return the kth shortest path between s and t


def yenKSP(g, s, t, k):
    # Initialise array to hold all shortest paths
    shortestPaths = []
    graphToUse = copyGraph(g)
    shortestPaths.append(dijkstraOnePath(graphToUse, s, t))
    potentialPaths = []
    # Iterate k times, till kth path found
    pathsFound = 1
    while pathsFound < k:
        # From the immediately previous path select each node as spur node one by one
        previousPath = shortestPaths[pathsFound-1]
        previousPathLength = len(previousPath)
        for i in range(previousPathLength-1):
            spurNode = previousPath[i]
            # Root path will be the start of the path being discovered
            rootPath = previousPath[:(i+1)]
            # Create a copy of the original graph
            graphToUse = copyGraph(g)
            # Remove next edge of all previous paths which start with root path
            for path in shortestPaths:
                # Check if root path matches
                if rootMatches(rootPath, path):
                    # Remove the edge that connects spur node to next node in the path
                    pos = len(rootPath)-1
                    graphToUse.delEdge(path[pos].nodeID, path[pos+1].nodeID)
            # Remove all nodes in root path except spur node
            for n in rootPath:
                # Remove node from graph copy
                if not n == spurNode:
                    graphToUse.delNode(n.nodeID)
            # Find shortest path from spur node to target
            nextPath = dijkstraOnePath(graphToUse, spurNode.nodeID, t)
            if not nextPath == None:
                nextPath = rootPath + nextPath[1:]
            # Add the full path (root + rest) to potential paths, if not already present
            if notPresent(nextPath, potentialPaths):
                potentialPaths.append(nextPath)
            # Sort potential paths & pop the shortest path into shortest paths
        if len(potentialPaths) > 0:
            potentialPaths = sortPaths(potentialPaths)
            shortestPaths.append(potentialPaths[0])
            potentialPaths.pop(0)
        else:
            return shortestPaths
        pathsFound += 1

    return shortestPaths

# Function to print a given path


def printPath(path):
    pathLength = lengthOfPath(path)
    print("path length ", pathLength)
    for n in path:
        print(n.nodeID, "->", end="")
    print("")
