# This file contains shortest path algorithm related helper functions through dijkstra's implementation
from graphDefs import *
from readInput import *

# Function to find the closest currently reachable node in the graph


def closest(g):
    min = None
    closeNode = None
    for n in g.nodes.keys():
        nod = g.nodes[n]
        # Check if node has been visited yet
        if nod.category == 1:
            if min == None:
                min = nod.distance
                closeNode = n
            elif nod.distance < min:
                min = nod.distance
                closeNode = n
    return closeNode

# Function to return index of parent of a given node (index) in min heap


def parentIndex(pos):
    if pos == 1:
        return 1
    elif pos % 2 == 0:
        return int(pos/2)
    else:
        return int((pos-1)/2)

# Function to swap 2 elements in a list


def swapPosition(lis, pos1, pos2):
    lis[pos1-1], lis[pos2-1] = lis[pos2-1], lis[pos1-1]
    return lis

# Function to compare 2 elements and return the lower value index


def minPosition(g, lis, pos1, pos2):
    if g.nodes[lis[pos1-1]].distance < g.nodes[lis[pos2-1]].distance:
        return pos1
    else:
        return pos2

# Function to check if heap rules are followed at pos, and make required changes at pos if need be
# For each change made at pos, it will move up and keep checking


def heapRulesUp(g, lis, pos):
    parPos = parentIndex(pos)
    if not minPosition(g, lis, pos, parPos) == parPos:
        lis = swapPosition(lis, pos, parPos)
        lis = heapRulesUp(g, lis, parPos)
    return lis

# Function to move down he heap tree and fill in a gap at pos


def heapRulesDown(g, lis, pos):
    childPos1 = pos*2
    childPos2 = (pos*2)+1
    if len(lis) >= childPos2:
        lowestPos = minPosition(g, lis, childPos1, childPos2)
        lis = swapPosition(lis, pos, lowestPos)
        return heapRulesDown(g, lis, lowestPos)
    elif len(lis) == childPos1:
        lowestPos = childPos1
        lis = swapPosition(lis, pos, lowestPos)
        return heapRulesDown(g, lis, lowestPos)
    else:
        lis = swapPosition(lis, pos, len(lis))
        lis.pop(len(lis)-1)
        if pos < len(lis):
            return heapRulesUp(g, lis, pos)
        else:
            return lis

# Function to push an element into a heap


def heapPush(g, lis, el):
    lis.append(el)
    pos = len(lis)
    return heapRulesUp(g, lis, pos)

# Function to pop an element from a heap


def heapPop(g, lis):
    el = lis[0]
    lis = heapRulesDown(g, lis, 1)
    return el

# Function to convert a list into a heap


def makeHeap(g, lis):
    newLis = []
    for n in lis:
        newLis = heapPush(g, newLis, n)
    return newLis


# Function to print the distances of all nodes in the graph
def distances(g):
    dist = {}
    for n in g.nodes.keys():
        nod = g.nodes[n]
        dist[n] = nod.distance
    print(dist)
    return dist

# Function to implement djikstra's algorithm in O(v^2)


def dijkstra(g, s):
    current = g.nodes[s]
    current.setDistance(0)
    current.setCategory(2)
    count = 1
    while not current == None:
        print("iteration ", count)
        print("parent ", current.nodeID)
        for n in current.edgesOut.keys():
            nod = g.nodes[n]
            newDistance = current.distance+current.edgesOut[n].cost
            if not nod.category == 2:
                if (nod.distance == None) or (nod.distance > newDistance):
                    print("node changed ")
                    nod.printNode()
                    print("distance change ", nod.distance, " to ", newDistance)
                    nod.setDistance(newDistance)
                    nod.setCategory(1)
                    nod.setParent(current.nodeID)
        if not closest(g) == None:
            current = g.nodes[closest(g)]
            current.setCategory(2)
        else:
            current = None
        count += 1
    return distances(g)

# Function to implement djikstra's algorithm in O(elog(v))


def dijkstraMinHeap(g, s):
    heapList = []
    current = g.nodes[s]
    current.setDistance(0)
    current.setCategory(2)
    count = 1
    while not current == None:
        print("iteration ", count)
        print("parent ", current.nodeID)
        for n in current.edgesOut.keys():
            nod = g.nodes[n]
            newDistance = current.distance+current.edgesOut[n].cost
            if not nod.category == 2:
                if (nod.distance == None) or (nod.distance > newDistance):
                    print("node changed ")
                    nod.printNode()
                    print("distance change ", nod.distance, " to ", newDistance)
                    nod.setDistance(newDistance)
                    if nod.category == 0:
                        nod.setCategory(1)
                        heapPush(g, heapList, n)
                    nod.setParent(current.nodeID)
        if len(heapList) > 0:
            current = g.nodes[heapPop(g, heapList)]
            current.setCategory(2)
        else:
            current = None
        count += 1
    return distances(g)
