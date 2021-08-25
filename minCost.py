# This file contains minimum cost flow identification problem relating helper functions through the capacity scaling and cycle cancelling algorithms
from graphDefs import *
from readInput import *
from bf import *
from yen import *
from dijkstras import *
from maxflow import *

# NOTE: In this file all residual graphs have different edge objects for edgeIn one node and edgeOut another node. The functions in this file are built to treat this separated edge style.

# Function to reset all parents, distances and categories of nodes in a graph to None, None and 0 respectively


def resetNodeVariables(residualGraph):
    for resetNode in residualGraph.nodes.keys():
        residualGraph.nodes[resetNode].distance = None
        residualGraph.nodes[resetNode].category = 0
        residualGraph.nodes[resetNode].parent = None

    return residualGraph

# Function to find the minimum cost positive capacity s-t path in a given residual graph through Bellman Ford


def positiveCapacityBellmanFord(residualGraph, sourceNode, sinkNode):
    edgeList = graphToEdgeList(residualGraph)

    # Reset all nodes' distances and categories
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
    return pathToArray(residualGraph, residualGraph.nodes[sinkNode])

# Function to accept a path and identify the capacity of flow that can pass through, as well as the associated cost


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

# Function that identifies the minimum cost flow through which a given amount of flow can be passed in a graph through capcity scaling algorithm


def capacityScaling(startingGraph, sourceNode, sinkNode, amountOfFlow):
    # Create residual network where the reverse edges have negative costs
    residualGraph = convertToResidualGraph(
        startingGraph, negativeReverseEdges=True)
    # Initialise variables, such as current cost = 0 and flow remaining = amountOfFlow
    currentCost = 0
    remainingFlow = amountOfFlow
    # Call positiveCapacityBellmanFord to find the lowest cost s-t path with positive capacity
    minCostAugmentingPath = positiveCapacityBellmanFord(
        residualGraph, sourceNode, sinkNode)

    while (not minCostAugmentingPath == None) and (remainingFlow > 0):
        # Between remaining and max flow possible, find out how much flow can pass and propagate the flow, and update remaining
        costAndFlow = costAndFlowOfPath(minCostAugmentingPath)
        if costAndFlow["capacity"] > remainingFlow:
            augmentingFlow = remainingFlow
        else:
            augmentingFlow = costAndFlow["capacity"]
        remainingFlow -= augmentingFlow
        pushFlowInGraph(residualGraph, minCostAugmentingPath, augmentingFlow)
        # Update the cost counter
        currentCost += costAndFlow["cost"]*augmentingFlow
        # Update path with positiveCapacityBellmanFord
        minCostAugmentingPath = positiveCapacityBellmanFord(
            residualGraph, sourceNode, sinkNode)

    flowGraph = graphDifference(startingGraph, residualGraph)
    return {"cost": currentCost, "flow": (amountOfFlow-remainingFlow), "flowGraph": flowGraph}

# Function to identify the cycle, after running Bellman Ford, and return it as a path


def cycleFromNode(residualGraph, changedNode):
    tentativeCycle = []
    currentNode = residualGraph.nodes[changedNode]
    while True:
        tentativeCycle.append(currentNode)
        nextNodeID = currentNode.parent
        if nextNodeID == None:
            return None
        currentNode = residualGraph.nodes[nextNodeID]
        if currentNode in tentativeCycle:
            startPosition = tentativeCycle.index(currentNode)
            cyclePath = []
            cyclePath.append(currentNode)
            position = len(tentativeCycle)-1
            while(position >= startPosition):
                cyclePath.append(tentativeCycle[position])
                position -= 1
            return cyclePath

# Function to identify negative cycles in residual graph and return them as a path


def negativeCycleBelmanFord(residualGraph):
    edgeList = graphToEdgeList(residualGraph)
    for sourceNode in residualGraph.nodes.keys():
        # Reset all nodes' distances and categories
        residualGraph = resetNodeVariables(residualGraph)

        # Set threshold values
        maxIterations = len(residualGraph.nodes)
        currentIterations = 0

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
                        if currentIterations > maxIterations:
                            cyclePath = cycleFromNode(
                                residualGraph, nod.nodeID)
                            if not cyclePath == None:
                                return cyclePath
            currentIterations += 1

    return None

# Function that identifies the minimum cost flow through which a given amount of flow can be passed in a graph through cycle cancelling algorithm


def cycleCancelling(startingGraph, sourceNode, sinkNode, amountOfFlow):
    # Initialise variables for cost and flow
    currentCost = 0
    remainingFlow = amountOfFlow
    # Create residual network where the reverse edges have negative costs
    residualGraph = convertToResidualGraph(
        startingGraph, negativeReverseEdges=True)

    # Find augmenting paths to fill up required flow
    augmentingPath = findAugmentingPath(residualGraph, sourceNode, sinkNode)
    while((not augmentingPath == None) and (remainingFlow > 0)):
        # Find cost and flow of path and increment counters
        costAndFlow = costAndFlowOfPath(augmentingPath["path"])
        if remainingFlow < costAndFlow["capacity"]:
            augmentingFlow = remainingFlow
        else:
            augmentingFlow = costAndFlow["capacity"]
        remainingFlow -= augmentingFlow
        currentCost += costAndFlow["cost"]*augmentingFlow
        # Push flow and create a residual network output
        pushFlowInGraph(residualGraph, augmentingPath["path"], augmentingFlow)
        # Find augmenting paths to fill up required flow
        augmentingPath = findAugmentingPath(
            residualGraph, sourceNode, sinkNode)

    negativeCycle = negativeCycleBelmanFord(residualGraph)
    while(not negativeCycle == None):
        # Find cost and flow of path (negative cycle)
        costAndFlow = costAndFlowOfPath(negativeCycle)
        # Change cost of flow
        augmentingFlow = costAndFlow["capacity"]
        currentCost += costAndFlow["cost"]*augmentingFlow
        # push flow along negative cycle
        pushFlowInGraph(residualGraph, negativeCycle, augmentingFlow)
        # Check for another negative cycle using bellman ford modification
        negativeCycle = negativeCycleBelmanFord(residualGraph)

    flowGraph = graphDifference(startingGraph, residualGraph)
    return {"cost": currentCost, "flow": (amountOfFlow-remainingFlow), "flowGraph": flowGraph}
