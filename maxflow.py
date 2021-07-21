# This file contains shortest path algorithm related helper functions through dijkstra's implementation
from graphDefs import *
from readInput import *
from bfs import *
from yen import *

# Function to check if a give edge exists or not


def checkForEdge(graphToSearch, startNode, endNode):
    nodeToCheck = graphToSearch.nodes[startNode]
    if endNode in nodeToCheck.edgesOut:
        return True
    else:
        return False

# Function to take a graph and create a full bidirectional residual version of it


def convertToResidualGraph(startingGraph):
    residualGraph = copyGraph(startingGraph)
    # Iterate through all nodes and edges to create reverse edges with 0 capacity if needed
    for nodeID in residualGraph.nodes.keys():
        nodeToUse = residualGraph.nodes[nodeID]
        for edgeToID in nodeToUse.edgesOut.keys():
            if not checkForEdge(residualGraph, edgeToID, nodeID):
                residualGraph.addEdge(edgeToID, nodeID)
    return residualGraph

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
        nodeToUse.edgesOut[nextNode.nodeID].capacity -= volumeOfFlow
        nextNode.edgesIn[nodeToUse.nodeID].capacity -= volumeOfFlow
        nextNode.edgesOut[nodeToUse.nodeID].capacity += volumeOfFlow
        nodeToUse.edgesIn[nextNode.nodeID].capacity += volumeOfFlow
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
            edgeDifference = nodeToUse.edgesOut[edgeToID].capacity - nodeToUse2.edgesOut[edgeToID].capacity
            if edgeDifference == 0:
                graphDiff.delEdge(nodeID, edgeToID)
            else:
                nodeToUse.edgesOut[edgeToID].capacity = edgeDifference
                graphDiff.nodes[edgeToID].edgesIn[nodeID].capacity = edgeDifference
    return graphDiff


# Function to find the maximum flow from s to t in a given graph


def edmondsKarps(startingGraph, startNode, endNode):
    flow = 0
    # Copy the starting graph to create a residual graph
    residualGraph = convertToResidualGraph(startingGraph)
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
    return {"flow": flow, "flowGraph": flowGraph}
