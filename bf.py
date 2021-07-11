# This file contains shortest path algorithm related helper functions through bellman ford implementation
from graphDefs import *
from readInput import *

# Function to print the distances of all nodes in the graph


def distances(g):
    dist = {}
    for n in g.nodes.keys():
        nod = g.nodes[n]
        dist[n] = nod.distance
    print(dist)
    return dist

# Function to extract the complete edge list given a graph


def graphToEdgeList(g):
    edgeList = []
    for n in g.nodes.keys():
        nod = g.nodes[n]
        for ed in nod.edgesOut.keys():
            edgeList.append(nod.edgesOut[ed])
    return edgeList

# Function to implement Modified Bellman Ford algorithm


def modifiedBellmanFord(g, s, edgeFile=None):
    if edgeFile == None:
        edgeList = graphToEdgeList(g)
    else:
        edgeList = inputFileEdges(edgeFile)

    # Set the first node's distance and category
    g.nodes[s].setDistance(0)
    g.nodes[s].setCategory(1)
    count = 1
    flag = True
    # While the distances are still changing, check if any edge results in a change in distances
    while flag == True:
        print("iteration ", count)
        flag = False
        for ed in edgeList:
            current = g.nodes[ed.startNode]
            if current.category == 1:
                nod = g.nodes[ed.endNode]
                newDistance = current.distance+ed.cost
                if (nod.distance == None) or (nod.distance > newDistance):
                    print("node changed ")
                    nod.printNode()
                    print("distance change ", nod.distance, " to ", newDistance)
                    nod.setDistance(newDistance)
                    print("parent ", current.nodeID)
                    nod.setCategory(1)
                    nod.setParent(current.nodeID)
                    flag = True
        count += 1

    return distances(g)

# Function to implement Bellman Ford algorithm


def bellmanFord(g, s, edgeFile=None):
    if edgeFile == None:
        edgeList = graphToEdgeList(g)
    else:
        edgeList = inputFileEdges(edgeFile)

    # Set the first node's distance and category
    g.nodes[s].setDistance(0)
    g.nodes[s].setCategory(2)
    count = 1
    flag = True
    # While the distances are still changing, check if any edge results in a change in distances
    while flag == True:
        print("iteration ", count)
        flag = False
        for ed in edgeList:
            current = g.nodes[ed.startNode]
            if current.category == 2:
                nod = g.nodes[ed.endNode]
                newDistance = current.distance+ed.cost
                if (nod.distance == None) or (nod.distance > newDistance):
                    print("node changed ")
                    nod.printNode()
                    print("distance change ", nod.distance, " to ", newDistance)
                    nod.setDistance(newDistance)
                    print("parent ", current.nodeID)
                    nod.setCategory(1)
                    nod.setParent(current.nodeID)
                    flag = True
        for n in g.nodes.keys():
            current = g.nodes[n]
            if current.category == 1:
                current.category = 2
        count += 1

    return distances(g)
