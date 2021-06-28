#This file contains helper functions to read txt files and store the input in the form of a network/graph.
from graphDefs import *

#Function to process one line of input and add to a given graph
def inputLine(g, l, delimit=" ", inputType="directedArc"):
    if inputType=="directedArc":
        params = l.split(delimit)
        if len(params)==4:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0],params[1],cost=params[2],capacity=params[3])
    elif inputType=="bidirectionalArc":
        params = l.split(delimit)
        if len(params)==4:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0],params[1],cost=params[2],capacity=params[3])
            g.addEdge(params[1],params[0],cost=params[2],capacity=params[3])
    elif inputType=="directedEdge":
        params = l.split(delimit)
        if len(params)==2:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0],params[1])
    elif inputType=="bidirectionalEdge":
        params = l.split(delimit)
        if len(params)==2:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0],params[1])
            g.addEdge(params[1],params[0])
    return g
    
#Function to read file and create a graph output
def inputFile(delimit=" ", inputType="directedArc"):
    file1 = open('/Users/shreyasharish/Documents/WwN/input.txt','r')
    Lines = file1.readlines()
    count = 0
    g = graph()
    for lin in Lines:
        g = inputLine(g,lin.strip(),delimit,inputType)
        count += 1
    return g