#This file contains functions needed to schedule olympic events amongst reporters
#The main functions are focused on finding the minimum reporters required to cover all events, max events coverable and the list of reporters vs events
from minCost import *
from maxflow import *

#Function to remove reverse edges within events
def removeReverseEdgesOfEvents(residualGraph):
    for nodeName in residualGraph.nodes.keys():
        params = nodeName.split(" ")
        if params[0] == "event":
            if params[2] == "end":
                nodeNumber = int(params[1])
                outNodeToRemove = "event " + str(nodeNumber) + " start"
                residualGraph.nodes[nodeName].edgesOut.pop(outNodeToRemove)
    
    return residualGraph

#Function to find the minimum reporters required to cover all events
def minReportersToCoverAllEvents(startingGraph):
    #Pass graph through max flow
    maxFlowOutput1 = edmondsKarps(startingGraph,"start","end")
    residualGraph = maxFlowOutput1["residualGraph"]
    #Edit the residual graph
    residualGraph = removeReverseEdgesOfEvents(residualGraph)
    #Pass the graph through reverse max flow
    maxFlowOutput2 = edmondsKarps(residualGraph,"end","start")
    #Return the flow, flow graph and residual graph
    flowGraph = graphDifference(startingGraph, maxFlowOutput2["residualGraph"])
    return {"flow": maxFlowOutput1["flow"]-maxFlowOutput2["flow"], "flowGraph": flowGraph, "residualGraph": maxFlowOutput2["residualGraph"]}

#Function to find the maximum number of events coverable within given constraints
def maxEventsCoverable(inputModel):
    #Find the maximum flow (or 1000) or number of reporters available
    reportersAvailable = inputModel["inputSet"]["reporterLimit"]
    if reportersAvailable == None:
        reportersAvailable = 1000
    #Find the min cost at which the flow can be achieved
    minCostOutput = capacityScaling(inputModel["graph"],"start","end",reportersAvailable)
    #Return the flow graph of min cost
    return minCostOutput

#Function to provide reporter count, event count and reporter event mapping from a flow
def flowToReporterSchedule(flowGraph,inputModel):
    #TODO: Find the number of reporters as amount of flow
    #TODO: Find the number and list of events by iterating through the node list and checking for flow vs capacity
    #TODO: Find augmenting paths as reporters and the list of events that they cover