#This file contains shortest path algorithm related helper functions
from graphDefs import *
from readInput import *

#Function to find the closest currently reachable node in the graph
def closest(g):
    min = None
    closeNode = None
    for n in g.nodes.keys():
        nod = g.nodes[n]
        #Check if node has been visited yet
        if nod.category == 1:
            if min == None:
                min = nod.distance
                closeNode = n
            elif nod.distance < min:
                min = nod.distance
                closeNode = n
    return closeNode

#Function to print the distances of all nodes in the graph
def distances(g):
    for n in g.nodes.keys():
        nod = g.nodes[n]
        print(n," - ",nod.distance)

#Function to implement djikstra's algorithm
def dijkstra(g,s):
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
                    nod.setCategory(1)
        if not closest(g) == None:
            current = g.nodes[closest(g)]
            current.setCategory(2)
        else:
            current = None
    distances(g)