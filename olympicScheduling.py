# This file contains functions needed to schedule olympic events amongst reporters
# The main functions are focused on finding the minimum reporters required to cover all events, max events coverable and the list of reporters vs events
from minCost import *
from maxflow import *
from bfs import *

# Function to remove reverse edges within events


def removeReverseEdgesOfEvents(residualGraph):
    for nodeName in residualGraph.nodes.keys():
        params = nodeName.split(" ")
        if params[0] == "event":
            if params[2] == "end":
                nodeNumber = int(params[1])
                outNodeToRemove = "event " + str(nodeNumber) + " start"
                residualGraph.nodes[nodeName].edgesOut.pop(outNodeToRemove)

    return residualGraph

# Function to find the minimum reporters required to cover all events


def minReportersToCoverAllEvents(startingGraph):
    # Pass graph through max flow
    maxFlowOutput1 = edmondsKarps(startingGraph, "start", "end")
    residualGraph = maxFlowOutput1["residualGraph"]
    # Edit the residual graph
    residualGraph = removeReverseEdgesOfEvents(residualGraph)
    # Pass the graph through reverse max flow
    maxFlowOutput2 = edmondsKarps(residualGraph, "end", "start",False)
    # Return the flow, flow graph and residual graph
    flowGraph = graphDifference(startingGraph, maxFlowOutput2["residualGraph"])
    return {"flow": maxFlowOutput1["flow"]-maxFlowOutput2["flow"], "flowGraph": flowGraph, "residualGraph": maxFlowOutput2["residualGraph"]}

# Function to find the maximum number of events coverable within given constraints


def maxEventsCoverable(inputModel):
    # Find the maximum flow (or 1000) or number of reporters available
    reportersAvailable = inputModel["inputSet"]["reporterLimit"]
    if reportersAvailable == None:
        reportersAvailable = 1000
    # Find the min cost at which the flow can be achieved
    minCostOutput = capacityScaling(
        inputModel["graph"], "start", "end", reportersAvailable)
    # Return the flow graph of min cost
    return minCostOutput

# Function to check if and how much flow is present between 2 nodes in a graph


def flowPresentBetweenNodes(graphToCheck, startNode, endNode):
    flow = 0
    if (startNode in graphToCheck.nodes.keys()) and (endNode in graphToCheck.nodes.keys()):
        if endNode in graphToCheck.nodes[startNode].edgesOut.keys():
            flow = graphToCheck.nodes[startNode].edgesOut[endNode].capacity

    return flow

# Function to count the number of events which have been covered


def numberOfEventsCovered(baseGraph, flowGraph):
    eventCoveredCount = 0.0
    for nodeName in baseGraph.nodes.keys():
        params = nodeName.split(" ")
        if params[0] == "event":
            if params[2] == "start":
                nodeNumber = int(params[1])
                outNodeToCheck = "event " + str(nodeNumber) + " end"
                reportersRequired = baseGraph.nodes[nodeName].edgesOut[outNodeToCheck].capacity
                reportersAttended = flowPresentBetweenNodes(
                    flowGraph, nodeName, outNodeToCheck)
                eventCoveredCount += (reportersAttended/reportersRequired)

    return eventCoveredCount

# Function to traceback parents, reduce capacity by 1 and return a list of events visited by 1 reporter


def traceEventsOfAugmentingPath(flowGraph, endNode):
    listOfEvents = []
    currentNode = endNode
    while not flowGraph.nodes[currentNode].parent == None:
        # If it's a relevant event, add it to the list
        params = currentNode.split(" ")
        if params[0] == "event":
            if params[2] == "end":
                nodeNumber = int(params[1])
                listOfEvents.insert(0, nodeNumber)
        # Reduce the capacity by 1
        nextNode = flowGraph.nodes[currentNode].parent
        flowGraph.nodes[nextNode].edgesOut[currentNode].capacity -= 1
        currentNode = nextNode

    return {"events": listOfEvents, "graph": flowGraph}

# Function to find the list of events covered by reporter


def reporterWiseScheduleOfEvents(flowGraph, startNode, endNode):
    augmentingPathsRemain = True
    listOfReporterSchedules = []
    while augmentingPathsRemain:
        breadthFirstReset()
        if breadthFirstSearch(flowGraph, startNode, endNode):
            augmentingPathOutput = traceEventsOfAugmentingPath(
                flowGraph, endNode)
            flowGraph = removeEmptyEdges(augmentingPathOutput["graph"])
            listOfReporterSchedules.append(augmentingPathOutput["events"])
        else:
            augmentingPathsRemain = False

    return listOfReporterSchedules

# Function to provide reporter count, event count and reporter event mapping from a flow


def flowToReporterSchedule(flowInput, inputModel):
    # Find the number of reporters as amount of flow
    flowGraph = flowInput["flowGraph"]
    numberOfReporters = flowInput["flow"]
    # Find the number of events by iterating through the node list and checking for flow vs capacity
    baseGraph = inputModel["graph"]
    eventCoverageCount = numberOfEventsCovered(baseGraph, flowGraph)
    # Find augmenting paths as reporters and the list of events that they cover
    reporterSchedule = reporterWiseScheduleOfEvents(flowGraph, "start", "end")

    return {"numberOfReporters": numberOfReporters, "numberOfEventsCovered": eventCoverageCount, "reporterSchedule": reporterSchedule}

# Function to print the output of a flow analysis neatly in terminal


def printFlowAnalysis(flowAnalysis, inputModel):
    print("Number of Reporters -", end=" ")
    print(flowAnalysis["numberOfReporters"])
    print("Number of Events Covered -", end=" ")
    print(flowAnalysis["numberOfEventsCovered"], end=" / ")
    print(len(inputModel["inputSet"]["events"]))
    count = 1
    for reporter in flowAnalysis["reporterSchedule"]:
        print("Reporter ", count, end=" - ")
        for eventNumber in reporter:
            print("event ", eventNumber, end=", ")
        print("")
        count += 1

# Function to find the minimum reporters required in a given model and output appropriately


def minReportersProblem(inputModel):
    print("______________________________________________________________")
    print("Q) Min reporters required to cover all events")
    minReportersOutput = minReportersToCoverAllEvents(inputModel["graph"])
    flowAnalysis = flowToReporterSchedule(minReportersOutput, inputModel)
    printFlowAnalysis(flowAnalysis, inputModel)
    print("______________________________________________________________")

# Function to find the maximum events coverable in a given model and output appropriately


def maxEventsProblem(inputModel):
    print("______________________________________________________________")
    print("Q) Max events coverable within a given set of constraints")
    maxEventsOutput = maxEventsCoverable(inputModel)
    flowAnalysis = flowToReporterSchedule(maxEventsOutput, inputModel)
    printFlowAnalysis(flowAnalysis, inputModel)
    print("______________________________________________________________")
