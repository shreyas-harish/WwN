# This file contains helper functions to read txt files and store the input in the form of a network/graph.
from graphDefs import *
from olympicEventObjects import *

# Function to process one line of input and add to a given graph


def inputLine(g, l, delimit=" ", inputType="directedArc"):
    if inputType == "directedArc":
        params = l.split(delimit)
        if len(params) == 4:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0], params[1], cost=int(
                params[2]), capacity=int(params[3]))
    elif inputType == "bidirectionalArc":
        params = l.split(delimit)
        if len(params) == 4:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0], params[1], cost=int(
                params[2]), capacity=int(params[3]))
            g.addEdge(params[1], params[0], cost=int(
                params[2]), capacity=int(params[3]))
    elif inputType == "directedEdge":
        params = l.split(delimit)
        if len(params) == 2:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0], params[1])
    elif inputType == "bidirectionalEdge":
        params = l.split(delimit)
        if len(params) == 2:
            g.safeAddNode(params[0])
            g.safeAddNode(params[1])
            g.addEdge(params[0], params[1])
            g.addEdge(params[1], params[0])
    return g

# Function to process one line of input and return an edge


def inputLineEdge(edgeList, l, delimit=" ", inputType="directedArc"):
    if inputType == "directedArc":
        params = l.split(delimit)
        if len(params) == 4:
            ed = edge(params[0], params[1])
            ed.setCost(int(params[2]))
            ed.setCapacity(int(params[3]))
            edgeList.append(ed)
    elif inputType == "bidirectionalArc":
        params = l.split(delimit)
        if len(params) == 4:
            ed = edge(params[0], params[1])
            ed.setCost(int(params[2]))
            ed.setCapacity(int(params[3]))
            edgeList.append(ed)
            ed2 = edge(params[1], params[0])
            ed2.setCost(int(params[2]))
            ed2.setCapacity(int(params[3]))
            edgeList.append(ed2)
    elif inputType == "directedEdge":
        params = l.split(delimit)
        if len(params) == 2:
            ed = edge(params[0], params[1])
            edgeList.append(ed)
    elif inputType == "bidirectionalEdge":
        params = l.split(delimit)
        if len(params) == 2:
            ed = edge(params[0], params[1])
            edgeList.append(ed)
            ed2 = edge(params[1], params[0])
            edgeList.append(ed2)
    return edgeList

# Function to read file and create a graph output


def inputFile(file='/Users/shreyasharish/Documents/WwN/input.txt', delimit=" ", inputType="directedArc"):
    file1 = open(file, 'r')
    Lines = file1.readlines()
    count = 0
    g = graph()
    for lin in Lines:
        g = inputLine(g, lin.strip(), delimit, inputType)
        count += 1
    return g

# Function to read file and create an edge list


def inputFileEdges(file='/Users/shreyasharish/Documents/WwN/input.txt', delimit=" ", inputType="directedArc"):
    file1 = open(file, 'r')
    Lines = file1.readlines()
    count = 0
    edgeList = []
    for lin in Lines:
        edgeList = inputLineEdge(edgeList, lin.strip(), delimit, inputType)
        count += 1
    return edgeList

# Function to process one line of input and return the sport name, venue name, start time and end time


def inputOlympicEventLine(inputLineEvent, delimit=", "):
    params = inputLineEvent.split(delimit)
    sportName = params[0]
    venueName = params[1]

    # Isolate the hour and minute of start and end, and store as a float of the hour
    timeParams = params[2].split(" ")
    startTimeParams = timeParams[1].split(":")
    endTimeParams = timeParams[2].split(":")
    startTime = float(startTimeParams[0]) + (float(startTimeParams[1])/60)
    endTime = float(endTimeParams[0]) + (float(endTimeParams[1])/60)

    # Return dictionary of required values
    return {"sport": sportName, "venue": venueName, "startTime": startTime, "endTime": endTime}

# Function to read file and create a graph output


def inputOlympicEvents(file='/Users/shreyasharish/Documents/WwN/OlympicEvents.txt', delimit=", "):
    file1 = open(file, 'r')
    Lines = file1.readlines()

    dictOfSports = {}
    listOfVenues = []
    listOfEvents = []

    # Read each line of the input
    for lin in Lines:
        # For each line of input, get the sport, venue and timing
        eventDetails = inputOlympicEventLine(lin.strip(), delimit)
        # Add the sport, venue and even to the respective output lists/dicts
        dictOfSports[eventDetails["sport"]] = sport(eventDetails["sport"])
        if not eventDetails["venue"] in listOfVenues:
            listOfVenues.append(eventDetails["venue"])
        listOfEvents.append(event(
            dictOfSports[eventDetails["sport"]], eventDetails["venue"], eventDetails["startTime"], eventDetails["endTime"]))

    inputSet = {"sports": dictOfSports, "venues": listOfVenues, "events": listOfEvents,
                "distanceMatrix": None, "reporterLimit": None, "reportersSpecialiseBySport": False}
    return inputSet
