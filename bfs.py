# This file contains depth first search related functions which operate on the graph defined earlier
from graphDefs import *
from readInput import *

# List which contains all of the nodes visited tus far
visited = []
# List which contains all of the active nodes
active = []

# Breadth First Algorithm to build up BFS tree and traverse graph from a starting node


def breadthFirstTreeBuilder(g, n, par=None):
    global visited
    global active
    visited.append(n)
    active.append(n)
    print(par, "->", n)
    while not len(active) == 0:
        n = active[0]
        for nod in g.nodes[n].edgesOut.keys():
            if not nod in visited:
                print(n, "->", nod)
                visited.append(nod)
                g.nodes[nod].parent = n
                active.append(nod)
            elif g.nodes[nod].parent == None:
                print(n, "->", nod)
                g.nodes[nod].parent = par
        active.pop(0)
    return g

# Breadth First Algorithm to build up BFS forest and fully traverse graph from a starting node


def breadthFirstForestBuilder(g):
    global visited
    for n in g.nodes.keys():
        if not n in visited:
            breadthFirstTreeBuilder(g, n, None)
    return g

# Breadth First Search Algorithm to check if target node can be found from starting node


def breadthFirstSearch(g, s, t, par=None):
    global visited
    global active
    visited.append(s)
    active.append(s)
    #print(par, "->", s)
    while not len(active) == 0:
        s = active[0]
        for nod in g.nodes[s].edgesOut.keys():
            if not nod in visited:
                #print(s, "->", nod)
                visited.append(nod)
                g.nodes[nod].parent = s
                if nod == t:
                    #print("found ", t)
                    return True
                active.append(nod)
        active.pop(0)
    return False

# Breadth First Search Algorithm to check which all nodes in the graph can and can't be reached from the start node


def breadthFirstReach(g, n, par=None):
    global visited
    global active
    visited.append(n)
    active.append(n)
    print(par, "->", n)
    while not len(active) == 0:
        n = active[0]
        for nod in g.nodes[n].edgesOut.keys():
            if not nod in visited:
                print(n, "->", nod)
                visited.append(nod)
                g.nodes[nod].parent = n
                active.append(nod)
            elif g.nodes[nod].parent == None:
                print(n, "->", nod)
                g.nodes[nod].parent = par
        active.pop(0)

    notReachable = []
    for n in g.nodes.keys():
        if not n in visited:
            notReachable.append(n)
    print("Reachable set ", visited)
    print("Not reachable set", notReachable)
    reachSet = {}
    reachSet["reachable"] = visited
    reachSet["unreachable"] = notReachable
    return reachSet


def breadthFirstReset():
    global visited
    global active
    visited = []
    active = []
