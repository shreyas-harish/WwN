# This file contains minimum cost flow identification problem relating helper functions through the capacity scaling and cycle cancelling algorithms
from graphDefs import *
from readInput import *
from bf import *
from yen import *
from dijkstras import *
from maxflow import *

# NOTE: In this file all residual graphs have different edge objects for edgeIn one node and edgeOut another node. The functions in this file are built to treat this separated edge style.

#Function to reset all parents, distances and categories of nodes in a graph to None, None and 0 respectively
def resetNodeVariables(residualGraph):
    for resetNode in residualGraph.nodes.keys():
        residualGraph.nodes[resetNode].distance = None
        residualGraph.nodes[resetNode].category = 0
        residualGraph.nodes[resetNode].parent = None

    return residualGraph

#Function to find the minimum cost positive capacity s-t path in a given residual graph through Bellman Ford


def positiveCapacityBellmanFord(residualGraph, sourceNode, sinkNode):
    edgeList = graphToEdgeList(residualGraph)
    
    #Reset all nodes' distances and categories
    residualGraph = resetNodeVariables(residualGraph)

    # Set the first node's distance and category
    residualGraph.nodes[sourceNode].setDistance(0)
    residualGraph.nodes[sourceNode].setCategory(1)
    flag = True
    # While the distances are still changing, check if any edge results in a change in distances
    while flag == True:
        flag = False
        for ed in edgeList:
            current = residualGraph.nodes[ed.startNode]
            if (current.category == 1) and (ed.capacity > 0):
                nod = residualGraph.nodes[ed.endNode]
                newDistance = current.distance+ed.cost
                if (nod.distance == None) or (nod.distance > newDistance):
                    nod.setDistance(newDistance)
                    nod.setCategory(1)
                    nod.setParent(current.nodeID)
                    flag = True
    
    if residualGraph.nodes[sinkNode].parent == None:
        return None
    return pathToArray(residualGraph,residualGraph.nodes[sinkNode])

#Function to accept a path and identify the capacity of flow that can pass through, as well as the associated cost
def costAndFlowOfPath(path):
    if len(path) < 2:
        return {"cost": 0, "capacity": 0}
    else:
        pos = 0
        cost = 0
        capacity = None
        while pos < (len(path)-1):
            cost += path[pos].edgesOut[path[pos+1].nodeID].cost
            if (capacity == None) or (capacity > path[pos].edgesOut[path[pos+1].nodeID].capacity):
                capacity = path[pos].edgesOut[path[pos+1].nodeID].capacity
            pos += 1
        return {"cost": cost, "capacity": capacity}

#Function that identifies the minimum cost flow through which a given amount of flow can be passed in a graph
def capacityScaling(startingGraph,sourceNode,sinkNode,amountOfFlow):
    #Create residual network where the reverse edges have negative costs
    residualGraph = convertToResidualGraph(startingGraph,negativeReverseEdges=True)
    #Initialise variables, such as current cost = 0 and flow remaining = amountOfFlow
    currentCost = 0
    remainingFlow = amountOfFlow
    #Call positiveCapacityBellmanFord to find the lowest cost s-t path with positive capacity
    minCostAugmentingPath = positiveCapacityBellmanFord(residualGraph,sourceNode,sinkNode)

    while (not minCostAugmentingPath == None) and (remainingFlow > 0):
        #Between remaining and max flow possible, find out how much flow can pass and propagate the flow, and update remaining
        costAndFlow = costAndFlowOfPath(minCostAugmentingPath)
        if costAndFlow["capacity"] > remainingFlow:
            augmentingFlow = remainingFlow
        else:
            augmentingFlow = costAndFlow["capacity"]
        remainingFlow -= augmentingFlow
        pushFlowInGraph(residualGraph,minCostAugmentingPath,augmentingFlow)
        #Update the cost counter
        currentCost += costAndFlow["cost"]*augmentingFlow
        #Update path with positiveCapacityBellmanFord
        minCostAugmentingPath = positiveCapacityBellmanFord(residualGraph,sourceNode,sinkNode)

    flowGraph = graphDifference(startingGraph, residualGraph)
    return {"cost": currentCost, "flow": amountOfFlow, "flowGraph": flowGraph}