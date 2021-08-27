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
