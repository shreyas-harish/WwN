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

    # Function to set or change starting node ID
    def setStartingNodeID(self, startingNodeID):
        self.startingNodeID = startingNodeID

    # Function to set or change ending node ID
    def setEndingNodeID(self, endingNodeID):
        self.endingNodeID = endingNodeID

# Useful functions to run on groups of event objects

# TODO: Function to print a dict of event objects
