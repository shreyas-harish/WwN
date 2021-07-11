# This file contains depth first search related functions which operate on the graph defined earlier
from graphDefs import *
from readInput import *

# List which contains all of the nodes visited tus far
visited = []

# Depth First Algorithm to build up DFS tree and traverse graph from a starting node


def depthFirstTreeBuilder(g, n, par=None):
    global visited
    if n not in visited:
        print("visiting ", n)
        visited.append(n)
        g.nodes[n].parent = par
        for nod in g.nodes[n].edgesOut.keys():
            depthFirstTreeBuilder(g, nod, n)
        print("returning ", n)
    elif g.nodes[n].parent == None:
        g.nodes[n].parent = par
    return g

# Depth First Algorithm to build up DFS forest and fully traverse graph from a starting node


def depthFirstForestBuilder(g):
    global visited
    for n in g.nodes.keys():
        if not n in visited:
            depthFirstTreeBuilder(g, n, None)
    return g

# Depth First Search Algorithm to check if target node can be found from starting node


def depthFirstSearch(g, s, t, par=None):
    global visited
    if s == t:
        print("found ", s)
        visited.append(s)
        g.nodes[s].parent = par
        return True
    if s not in visited:
        print("visiting ", s)
        visited.append(s)
        g.nodes[s].parent = par
        for nod in g.nodes[s].edgesOut.keys():
            if depthFirstSearch(g, nod, t, s):
                return True
        print("returning ", s)
    return False

# Depth First Search Algorithm to check which all nodes in the graph can and can't be reached from the start node


def depthFirstReach(g, s, par=None):
    global visited
    if s not in visited:
        print("visiting ", s)
        visited.append(s)
        g.nodes[s].parent = par
        for nod in g.nodes[s].edgesOut.keys():
            depthFirstReach(g, nod, s)
        print("returning ", s)
    if par == None:
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


def depthFirstReset():
    global visited
    visited = []
