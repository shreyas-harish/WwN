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
    for eventObject in listOfEvents:
        eventObject.printEvents()

# Function to setup start and end nodes of graph, with required reporter constraint


def setupStartAndEnd(reporterLimit):
    outputGraph = graph()
    outputGraph.addNode("start")
    outputGraph.addNode("start capacity constrained")
    outputGraph.addNode("end")
    capacity = 1000
    if not reporterLimit == None:
        capacity = reporterLimit
    outputGraph.addEdge("start", "start capacity constrained", capacity)

    return outputGraph

# Function to add nodes for a given event and update nodeIDs across nodes and events


def addEventToGraph(listOfEvents, eventNumber, currentGraph):
    # Create node ID names
    startingNodeID = "event " + str(eventNumber) + " start"
    endingNodeID = "event " + str(eventNumber) + " end"
    # Create nodes
    currentGraph.addNode(startingNodeID)
    currentGraph.addNode(endingNodeID)
    # Save node ID references in event
    listOfEvents[eventNumber].startingNodeID = startingNodeID
    listOfEvents[eventNumber].endingNodeID = endingNodeID
    # Identify the relevant sport object and get capacity and cost values
    capacity = listOfEvents[eventNumber].sport.reportersRequired
    cost = -(listOfEvents[eventNumber].sport.priorityLevel/capacity)
    # Add edge between start and end node
    currentGraph.addEdge(startingNodeID, endingNodeID, capacity, cost)
    # Add edge between start point and starting node
    currentGraph.addEdge("start capacity constrained", startingNodeID, 1000)
    # Add edge between ending node and end point
    currentGraph.addEdge(endingNodeID, "end", 1000)

    return {"graph": currentGraph, "event": listOfEvents[eventNumber]}

#Function to check if the timings & venues match, returns direction of edge if any
def checkForEventTimeGap(event1,event2,listOfVenues,distanceMatrix):
    #Identify venue IDs
    venue1ID = listOfVenues.index(event1.venue)
    venue2ID = listOfVenues.index(event2.venue)
    #Identify venue distances
    distance1 = distanceMatrix[venue1ID][venue2ID]
    distance2 = distanceMatrix[venue2ID][venue1ID]
    #Identify direction of match
    match = 0
    if event1.endTime + distance1 + 0.25 <= event2.startTime:
        match = 1
    elif event2.endTime + distance2 + 0.25 <= event1.startTime:
        match = -1
    return match

#Function to iterate through the events added and identify what edges to add
def addEdgesBetweenEvents(listOfEvents,currentGraph,reporterSpecialisation,listOfVenues,distanceMatrix):
    currentEvent = listOfEvents[-1]
    currentEventNumber = len(listOfEvents)-1

    #Iterate through all previous events
    count = 0
    for eventObject in listOfEvents[:-1]:
        match = 1
        #If specialisation is required, check for matching sport
        if reporterSpecialisation:
            if not eventObject.sport.sportName == currentEvent.sport.sportName:
                match = 0
        #Check for timing match
        if not match == 0:
            match = checkForEventTimeGap(eventObject,currentEvent,listOfVenues,distanceMatrix)
        #Add edge between, if need be
        if match == 1:
            startingNodeID = "event " + str(count) + " end"
            endingNodeID = "event " + str(currentEventNumber) + " start"
            currentGraph.addEdge(startingNodeID,endingNodeID,1000)
        elif match == -1:
            startingNodeID = "event " + str(currentEventNumber) + " end"
            endingNodeID = "event " + str(count) + " start"
            currentGraph.addEdge(startingNodeID,endingNodeID,1000)
        count += 1

    return currentGraph

# Function to accept an input set and return a graph modelling the scheduling problem and constraints


def inputToGraph(inputSet):
    # Setup graph and add two start nodes, with joining edge which limits capcity to 1000 or #reporters and one end node
    outputGraph = setupStartAndEnd(inputSet["reporterLimit"])
    # Create a revised list of events, with references to graph added
    listOfEvents = []

    # iterate through all event objects and add nodes + edges appropriately
    count = 0
    for eventObject in inputSet["events"]:
        # Add a start node and an end node + add node ids to the event object + add edges relevant to event
        eventAdditionOutput = addEventToGraph(
            inputSet["events"], count, outputGraph)
        outputGraph = eventAdditionOutput["graph"]
        listOfEvents.append(eventAdditionOutput["event"])
        #Find matches and add appropriate edges
        outputGraph = addEdgesBetweenEvents(listOfEvents,outputGraph,inputSet["reportersSpecialiseBySport"],inputSet["venues"],inputSet["distanceMatrix"])
        count += 1

    # Edit input set
    finalInputSet = {"sports": inputSet["sports"], "venues": inputSet["venues"], "events": listOfEvents, "distanceMatrix": inputSet["distanceMatrix"],
                "reporterLimit": inputSet["reporterLimit"], "reportersSpecialiseBySport": inputSet["reportersSpecialiseBySport"]}
    #Return the final graph and the input set (updated with node IDs in events)
    return {"graph": outputGraph, "inputSet": finalInputSet}
