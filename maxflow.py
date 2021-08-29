# This file contains shortest maximum flow related helper functions through Edmond Karps and Push Relabel implementations
from graphDefs import *
from readInput import *
from bfs import *
from yen import *
from dijkstras import *

# NOTE: In this file all residual graphs have different edge objects for edgeIn one node and edgeOut another node. The functions in this file are built to treat this separated edge style.

# Function to check if a give edge exists or not


def checkForEdge(graphToSearch, startNode, endNode):
    nodeToCheck = graphToSearch.nodes[startNode]
    if endNode in nodeToCheck.edgesOut:
        return True
    else:
        return False

# Function to take a graph and create a full bidirectional residual version of it


def convertToResidualGraph(startingGraph,negativeReverseEdges=False):
    residualGraph = copyGraph(startingGraph)
    # Iterate through all nodes and edges to create reverse edges with 0 capacity if needed
    for nodeID in residualGraph.nodes.keys():
        nodeToUse = residualGraph.nodes[nodeID]
        for edgeToID in nodeToUse.edgesOut.keys():
            if not checkForEdge(residualGraph, edgeToID, nodeID):
                if negativeReverseEdges == True:
                    edgeCost = -nodeToUse.edgesOut[edgeToID].cost
                    residualGraph.addEdge(edgeToID, nodeID,cost=edgeCost)
                else:
                    residualGraph.addEdge(edgeToID, nodeID)
    edgeSeparatedResidualGraph = copyGraph(residualGraph)
    return edgeSeparatedResidualGraph

# Function to crete a copy of a graph, without any zero capacity edges


def removeEmptyEdges(graphToReduce):
    graphCopy = copyGraph(graphToReduce)
    # Iterate through all nodes and edges to remove any empty edges
    for nodeID in graphToReduce.nodes.keys():
        nodeToUse = graphToReduce.nodes[nodeID]
        for edgeToID in nodeToUse.edgesOut.keys():
            if nodeToUse.edgesOut[edgeToID].capacity <= 0:
                graphCopy.delEdge(nodeID, edgeToID)
    return graphCopy

# Function to find max flow in a discovered augmenting path


def criticalFlowInPath(path):
    criticalFlow = None
    nodeToUse = None
    nextNode = None
    if len(path) > 1:
        nodeToUse = path[0]
        nextNode = path[1]
        position = 1
    while not nextNode == None:
        edgeCapacity = nodeToUse.edgesOut[nextNode.nodeID].capacity
        if (criticalFlow == None) or (criticalFlow > edgeCapacity):
            criticalFlow = edgeCapacity
        nodeToUse = nextNode
        position += 1
        if position < len(path):
            nextNode = path[position]
        else:
            return criticalFlow
    return criticalFlow

# Function to set all of the parents to None in a graph


def setParentsToNone(graphToReset):
    for nodeID in graphToReset.nodes.keys():
        graphToReset.nodes[nodeID].parent = None

# Function to run a BFS on a residual graph to find the shortest (#arcs) augmenting path and the flow value of the same


def findAugmentingPath(residualGraph, startNode, endNode):
    breadthFirstReset()
    graphToSearch = removeEmptyEdges(residualGraph)
    if breadthFirstSearch(graphToSearch, startNode, endNode):
        # Convert path found into an array and capture maximum flow through path
        path = pathToArray(graphToSearch, graphToSearch.nodes[endNode])
        flow = criticalFlowInPath(path)
        return {"path": path, "flow": flow}
    return None

# Function to pass flow between 2 nodes while appropriately changing edge capacities


def flow2Nodes(residualGraph, fromNode, toNode, volumeOfFlow):
    node1 = residualGraph.nodes[fromNode]
    node2 = residualGraph.nodes[toNode]
    node1.edgesOut[toNode].capacity -= volumeOfFlow
    node2.edgesIn[fromNode].capacity -= volumeOfFlow
    node2.edgesOut[fromNode].capacity += volumeOfFlow
    node1.edgesIn[toNode].capacity += volumeOfFlow

# Function to take a path and reverse it in a residual graph, returning the changed residual graph


def pushFlowInGraph(graphToFlow, path, volumeOfFlow):
    # NOTE: The node objects in the path can't be directly used because they belong to a graph copy. Thus we only reuse the nodeID
    nodeToUse = None
    nextNode = None
    if len(path) > 1:
        nodeToUse = graphToFlow.nodes[path[0].nodeID]
        nextNode = graphToFlow.nodes[path[1].nodeID]
        position = 1
    while not nextNode == nodeToUse:
        flow2Nodes(graphToFlow, nodeToUse.nodeID,
                   nextNode.nodeID, volumeOfFlow)
        nodeToUse = nextNode
        position += 1
        if position < len(path):
            nextNode = graphToFlow.nodes[path[position].nodeID]

# Function to find the difference between graph1 and graph2 (graph1 node & edges - graph2 edges)


def graphDifference(graph1, graph2):
    graphDiff = copyGraph(graph1)
    # Iterate through all nodes and edges to reduce edge weight or delete edge
    for nodeID in graphDiff.nodes.keys():
        nodeToUse = graphDiff.nodes[nodeID]
        nodeToUse1 = graph1.nodes[nodeID]
        nodeToUse2 = graph2.nodes[nodeID]
        for edgeToID in nodeToUse1.edgesOut.keys():
            edgeDifference = nodeToUse.edgesOut[edgeToID].capacity - \
                nodeToUse2.edgesOut[edgeToID].capacity
            if edgeDifference == 0:
                graphDiff.delEdge(nodeID, edgeToID)
            else:
                nodeToUse.edgesOut[edgeToID].capacity = edgeDifference
                graphDiff.nodes[edgeToID].edgesIn[nodeID].capacity = edgeDifference
    return graphDiff


# Function to find the maximum flow from s to t in a given graph


def edmondsKarps(startingGraph, startNode, endNode,conversionToResidualGraphNeeded=True):
    flow = 0
    # Copy the starting graph to create a residual graph
    if conversionToResidualGraphNeeded:
        residualGraph = convertToResidualGraph(startingGraph)
    else:
        residualGraph = startingGraph
    # While we can find augmenting path using a BFS
    augmentingPath = findAugmentingPath(residualGraph, startNode, endNode)
    while not augmentingPath == None:
        flow += augmentingPath["flow"]
        # Reverse found path in residual graph
        pushFlowInGraph(
            residualGraph, augmentingPath["path"], augmentingPath["flow"])
        # Find next augmenting path
        augmentingPath = findAugmentingPath(residualGraph, startNode, endNode)

    flowGraph = graphDifference(startingGraph, residualGraph)
    return {"flow": flow, "flowGraph": flowGraph, "residualGraph": residualGraph}

# Function to implement reverse dijkstra's to set distance values as distance labels and return the full graph


def reverseDijkstra(g, t):
    heapList = []
    current = g.nodes[t]
    current.setDistance(0)
    current.setCategory(2)
    count = 1
    while not current == None:
        for n in current.edgesIn.keys():
            nod = g.nodes[n]
            newDistance = current.distance+1
            if not nod.category == 2:
                if (nod.distance == None) or (nod.distance > newDistance):
                    nod.setDistance(newDistance)
                    if nod.category == 0:
                        nod.setCategory(1)
                        heapPush(g, heapList, n)
        if len(heapList) > 0:
            current = g.nodes[heapPop(g, heapList)]
            current.setCategory(2)
        else:
            current = None
        count += 1

    for resetNode in g.nodes.keys():
        g.nodes[resetNode].setCategory(0)

    return g


# Function to check if a given edge is admissable or not (checks node distances and edge capacity)
def checkEdgeAdmissability(residualGraph, fromNode, toNode):
    node1 = residualGraph.nodes[fromNode]
    node2 = residualGraph.nodes[toNode]
    if (node1.distance == None) or (node2.distance == None):
        return False
    if node1.distance <= node2.distance:
        return False
    if toNode in node1.edgesOut:
        if node1.edgesOut[toNode].capacity > 0:
            return True
        else:
            return False
    else:
        return False


# Maintain list of active nodes for the push relabel algorithm
activeNodes = []
activeNodeAdmissableDivider = -1

# Function to activate a given node. Checks if already active. Never activate start or end node.


def activateNode(nodeToActivate, startNode, endNode):
    global activeNodes
    global activeNodeAdmissableDivider
    if nodeToActivate in activeNodes:
        if activeNodes.index(nodeToActivate) <= activeNodeAdmissableDivider:
            activeNodeAdmissableDivider -= 1
        activeNodes.remove(nodeToActivate)
    if (not nodeToActivate == startNode) and (not nodeToActivate == endNode):
        activeNodes.append(nodeToActivate)

# Function to de-activate a given node. Checks if already inactive


def deactivateNode(nodeToActivate):
    global activeNodes
    global activeNodeAdmissableDivider
    if nodeToActivate in activeNodes:
        if activeNodes.index(nodeToActivate) <= activeNodeAdmissableDivider:
            activeNodeAdmissableDivider -= 1
        activeNodes.remove(nodeToActivate)

# Function to handle a flow push, including setting nodes as active/inactive and updating excess values. Returns true if some flow is admissable.


def advancedPushFlow(residualGraph, fromNode, toNode, startNode, endNode):
    if not checkEdgeAdmissability(residualGraph, fromNode, toNode):
        return False
    flowAvailable = residualGraph.nodes[fromNode].category
    capacityAvailable = residualGraph.nodes[fromNode].edgesOut[toNode].capacity
    if fromNode == startNode:
        if capacityAvailable > 0:
            flow2Nodes(residualGraph, fromNode, toNode, capacityAvailable)
            activateNode(toNode, startNode, endNode)
            residualGraph.nodes[toNode].category += capacityAvailable
    elif flowAvailable >= capacityAvailable:
        if capacityAvailable > 0:
            flow2Nodes(residualGraph, fromNode, toNode, capacityAvailable)
            activateNode(toNode, startNode, endNode)
            residualGraph.nodes[fromNode].category -= capacityAvailable
            residualGraph.nodes[toNode].category += capacityAvailable
    elif flowAvailable < capacityAvailable:
        if flowAvailable > 0:
            flow2Nodes(residualGraph, fromNode, toNode, flowAvailable)
            activateNode(toNode, startNode, endNode)
            residualGraph.nodes[fromNode].category -= flowAvailable
            residualGraph.nodes[toNode].category += flowAvailable
    if residualGraph.nodes[fromNode].category == 0:
        deactivateNode(fromNode)
    if (toNode == endNode) or (toNode == startNode):
        return False
    return True

# Function to re-label a given node


def relabel(residualGraph, nodeToRelabel):
    minNewLabel = len(residualGraph.nodes)+1
    for toNode in residualGraph.nodes[nodeToRelabel].edgesOut.keys():
        if (residualGraph.nodes[nodeToRelabel].edgesOut[toNode].capacity > 0) and (not residualGraph.nodes[toNode].distance == None):
            newLabel = residualGraph.nodes[toNode].distance + 1
            if minNewLabel > newLabel:
                minNewLabel = newLabel
    residualGraph.nodes[nodeToRelabel].distance = minNewLabel

# Function to implement the push relabel algorithm


def pushRelabel(startingGraph, startNode, endNode):
    # NOTE: Distance holds the reverse distance label for each node and category holds the excess at the node
    # Reset list of active nodes
    global activeNodes
    activeNodes = []
    global activeNodeAdmissableDivider
    activeNodeAdmissableDivider = -1
    # Call a reverse dijkstra's on the original graph to set distances as distance label. Also set start node with special label value.
    distanceLabelGraph = reverseDijkstra(startingGraph, endNode)
    distanceLabelGraph.nodes[startNode].distance = len(distanceLabelGraph.nodes)
    # Create a residual network copy of the original graph
    residualGraph = convertToResidualGraph(distanceLabelGraph)
    # Push maximum flow possible from start node. Activate all nodes which have been pushed to and set their excess values.
    for toNode in residualGraph.nodes[startNode].edgesOut.keys():
        advancedPushFlow(residualGraph, startNode, toNode, startNode, endNode)
    nodeToPushFrom = None
    iterationPosition = 0
    nodeToPushFrom = activeNodes[iterationPosition]
    # While active nodes are not empty, run through them in FIFO manner
    while not nodeToPushFrom == None:
        changeInActiveNodes = False
        activeNodeAdmissableDivider += 1
        # Iterate through all edges from the node and check if the edge is admissable or not
        for toNode in residualGraph.nodes[nodeToPushFrom].edgesOut.keys():
            # Push maximum flow possible through admissable edge. Set the next node to active, update excess values of both nodes.
            thisChangedActiveNodes = advancedPushFlow(residualGraph, nodeToPushFrom, toNode, startNode, endNode)
            changeInActiveNodes = (changeInActiveNodes or thisChangedActiveNodes)
        # Identify next active node to use in FIFO. Check if all active are impossible, then relabel one (in FIFO). Check if active nodes are empty, then end.
        if changeInActiveNodes:
            iterationPosition = -1
        iterationPosition += 1
        if iterationPosition < len(activeNodes):
            nodeToPushFrom = activeNodes[iterationPosition]
        elif len(activeNodes) == 0:
            nodeToPushFrom = None
        else:
            # relabel the first node and restart iteration
            iterationPosition = 0
            nodeToPushFrom = activeNodes[iterationPosition]
            relabel(residualGraph, nodeToPushFrom)

    flow = residualGraph.nodes[endNode].category
    flowGraph = graphDifference(startingGraph, residualGraph)
    return {"flow": flow, "flowGraph": flowGraph, "residualGraph": residualGraph}

#Function to find the next active node o select, given the most recently used node

def nextActiveNode(residualGraph,lastNode):
    global activeNodes
    global activeNodeAdmissableDivider
    lastNode = len(activeNodes)-1
    nodePosition = activeNodeAdmissableDivider + 1
    nextNode = None
    while nodePosition <=lastNode:
        checkNode = activeNodes[nodePosition]
        if (nextNode == None) or (nextNode > int(checkNode)):
            nextNode = int(checkNode)
        nodePosition += 1
        
    if nextNode == None:
        if len(activeNodes) > 0:
            minDistance = None
            nodeToRelabel = None
            for checkNode in activeNodes:
                distance = residualGraph.nodes[checkNode].distance
                if (minDistance == None) or (minDistance > distance):
                    minDistance = distance
                    nodeToRelabel = checkNode
            relabel(residualGraph, nodeToRelabel)
            nextNode = nodeToRelabel

    if not nextNode == None:
        nextNode = str(nextNode)
        deactivateNode(nextNode)
        activeNodes.insert(activeNodeAdmissableDivider+1,nextNode)

    return nextNode

# Function to implement the push relabel algorithm with some heuristics


def pushRelabelHeuristics(startingGraph, startNode, endNode):
    # NOTE: Distance holds the reverse distance label for each node and category holds the excess at the node
    # Reset list of active nodes
    global activeNodes
    activeNodes = []
    global activeNodeAdmissableDivider
    activeNodeAdmissableDivider = -1
    # Call a reverse dijkstra's on the original graph to set distances as distance label. Also set start node with special label value.
    distanceLabelGraph = reverseDijkstra(startingGraph, endNode)
    distanceLabelGraph.nodes[startNode].distance = len(distanceLabelGraph.nodes)
    # Create a residual network copy of the original graph
    residualGraph = convertToResidualGraph(distanceLabelGraph)
    # Push maximum flow possible from start node. Activate all nodes which have been pushed to and set their excess values.
    for toNode in residualGraph.nodes[startNode].edgesOut.keys():
        advancedPushFlow(residualGraph, startNode, toNode, startNode, endNode)
    nodeToPushFrom = None
    iterationPosition = 0
    nodeToPushFrom = nextActiveNode(residualGraph,"-1")
    # While active nodes are not empty, run through them in FIFO manner
    iterationCount = 0
    while not nodeToPushFrom == None:
        changeInActiveNodes = False
        activeNodeAdmissableDivider += 1
        # Iterate through all edges from the node and check if the edge is admissable or not
        for toNode in residualGraph.nodes[nodeToPushFrom].edgesOut.keys():
            # Push maximum flow possible through admissable edge. Set the next node to active, update excess values of both nodes.
            startingExcess = residualGraph.nodes[nodeToPushFrom].category
            thisChangedActiveNodes = advancedPushFlow(residualGraph, nodeToPushFrom, toNode, startNode, endNode)
            finalExcess = residualGraph.nodes[nodeToPushFrom].category
            if finalExcess < startingExcess:
                iterationCount += 1
                print("iteration ",iterationCount,end=", ")
                print("push from ",nodeToPushFrom,end=", ")
                print("push to ",toNode)
            changeInActiveNodes = (changeInActiveNodes or thisChangedActiveNodes)
        # Identify next active node to use by finding the next highest node value or relabeling. Check if active nodes are empty, then end.
        nodeToPushFrom = nextActiveNode(residualGraph,nodeToPushFrom)

    flow = residualGraph.nodes[endNode].category
    flowGraph = graphDifference(startingGraph, residualGraph)
    return {"flow": flow, "flowGraph": flowGraph, "residualGraph": residualGraph}
