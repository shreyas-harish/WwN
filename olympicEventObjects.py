from graphDefs import *
# This file contains definitions for an olympic event and sport

# Definition of a sport
class sport:
    def __init__(self, sportName):
        self.sportName = sportName
        self.reportersRequired = 1
        self.priorityLevel = 1

    # Function to set or change reporters required
    def setReportersRequired(self, reportersRequired):
        self.reportersRequired = reportersRequired

    # Function to set or change priority level
    def setPriorityLevel(self, priorityLevel):
        self.priorityLevel = priorityLevel

    # Function to print a sports object and its values
    def printSport(self):
        print("sport name -> ", self.sportName, end=" | ")
        print("reporters required -> ", self.reportersRequired, end=" | ")
        print("priority level -> ", self.priorityLevel)

# Useful functions to run on groups of sport objects

# Function to print a dict of sports objects


def printDictOfSports(dictOfSports):
    for key in dictOfSports.keys():
        dictOfSports[key].printSport()

# Definition of a event


class event:
    def __init__(self, sport, venue, startTime, endTime):
        self.sport = sport
        self.venue = venue
        self.startTime = startTime
        self.endTime = endTime
        self.startingNodeID = "event start not set"
        self.endingNodeID = "event end not set"

    # Function to set or change starting node ID
    def setStartingNodeID(self, startingNodeID):
        self.startingNodeID = startingNodeID

    # Function to set or change ending node ID
    def setEndingNodeID(self, endingNodeID):
        self.endingNodeID = endingNodeID

    # Function to print an event object and its values
    def printEvent(self):
        print("sport name -> ", self.sport, end=" | ")
        print("venue -> ", self.venue, end=" | ")
        print("start time -> ", self.startTime, end=" | ")
        print("end time -> ", self.endTime)

# Useful functions to run on groups of event objects

# Function to print a list of event objects


def printListOfEvents(listOfEvents):
    for event in listOfEvents:
        event.printEvents()

#Function to setup start and end nodes of graph, with required reporter constraint
def setupStartAndEnd(reporterLimit):
    outputGraph = graph()
    outputGraph.addNode("start")
    outputGraph.addNode("start capacity constrained")
    outputGraph.addNode("end")
    capacity = 1000
    if not reporterLimit == None:
        capacity = reporterLimit
    outputGraph.addEdge("start","start capacity constrained",capacity)

    return outputGraph

#Function to accept an input set and return a graph modelling the scheduling problem and constraints
def inputToGraph(inputSet):
    #Setup graph and add two start nodes, with joining edge which limits capcity to 1000 or #reporters and one end node
    outputGraph = setupStartAndEnd(inputSet["reporterLimit"])

    #TODO: iterate through all event objects and add nodes + edges appropriately
        #TODO: Add a start node and an end node "event <number> start/end"
        #TODO: Add node ids to the event object
        #TODO: Add an edge with appropriate capacity and cost
        #TODO: Add an edge from source, with 1000 capcity, no cost + add an edge to sink with 1000 capacity, no cost
        #TODO: Write a function to iterate through existing nodes, find matches and add appropriate edges

    #TODO: Return the final graph and the input set (updated with node IDs in events)
