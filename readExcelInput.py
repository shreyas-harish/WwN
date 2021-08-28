import xlrd
import xlwt
import xlsxwriter
import os
import shutil
from olympicEventObjects import *

# Function to read distance matrix and reorder the venue list accordingly


def readDistanceMatrix(inputSet, file='/Users/shreyasharish/Documents/WwN/Venue distances.xls', sheetName="Distances"):
    # Opening the appropriate excel and sheet
    excelWorkbook = xlrd.open_workbook(file)
    distanceSheet = excelWorkbook.sheet_by_name(sheetName)

    # Populate the list of venues in the required order
    listOfVenues = []
    rowNumber = 2
    colNumber = 1
    lastRow = distanceSheet.nrows-1
    while rowNumber <= lastRow:
        listOfVenues.append(distanceSheet.cell_value(rowNumber, colNumber))
        rowNumber += 1

    # Create a distance matrix and populate the same
    distanceMatrix = [
        [0.0 for i in range(len(listOfVenues))] for j in range(len(listOfVenues))]
    # Populate distance matrix in hour values from minutes
    rowNumberOffset = 2
    colNumberOffset = 2
    for row in range(len(listOfVenues)):
        for col in range(len(listOfVenues)):
            distanceMatrix[row][col] = (float(distanceSheet.cell_value(
                row+rowNumberOffset, col+colNumberOffset))/60)

    # Edit input set and return
    return {"sports": inputSet["sports"], "venues": listOfVenues, "events": inputSet["events"],
            "distanceMatrix": distanceMatrix, "reporterLimit": inputSet["reporterLimit"], "reportersSpecialiseBySport": inputSet["reportersSpecialiseBySport"]}

# Function to update the number of reporters available


def readReportersAvailable(inputSet, file='/Users/shreyasharish/Documents/WwN/Venue distances.xls', sheetName="Constraints"):
    # Opening the appropriate excel and sheet
    excelWorkbook = xlrd.open_workbook(file)
    constraintsSheet = excelWorkbook.sheet_by_name(sheetName)

    # Get reporter limit
    reporterLimit = constraintsSheet.cell_value(0, 1)
    if reporterLimit == "None":
        reporterLimit = None
    else:
        reporterLimit = int(reporterLimit)

    # Edit input set and return
    return {"sports": inputSet["sports"], "venues": inputSet["venues"], "events": inputSet["events"],
            "distanceMatrix": inputSet["distanceMatrix"], "reporterLimit": reporterLimit, "reportersSpecialiseBySport": inputSet["reportersSpecialiseBySport"]}

# Function to update the dict of sports with new number of reporters required by sport


def readReportersRequired(inputSet, file='/Users/shreyasharish/Documents/WwN/Venue distances.xls', sheetName="Constraints"):
    # Opening the appropriate excel and sheet
    excelWorkbook = xlrd.open_workbook(file)
    constraintsSheet = excelWorkbook.sheet_by_name(sheetName)

    # Get reporters required and create new sport object for each
    dictOfSports = {}
    rowNumber = 5
    colNumber = 0
    colNumberOffset = 1
    lastRow = constraintsSheet.nrows-1
    while rowNumber <= lastRow:
        sportName = constraintsSheet.cell_value(rowNumber, colNumber)
        reportersRequired = int(constraintsSheet.cell_value(
            rowNumber, colNumber+colNumberOffset))
        dictOfSports[sportName] = sport(sportName)
        dictOfSports[sportName].setReportersRequired(reportersRequired)
        dictOfSports[sportName].setPriorityLevel(
            inputSet["sports"][sportName].priorityLevel)
        rowNumber += 1

    #Update sports objects inside event objects
    listOfEvents = []
    for eventObject in inputSet["events"]:
        newEventObject = event(dictOfSports[eventObject.sport.sportName],eventObject.venue,eventObject.startTime,eventObject.endTime)
        listOfEvents.append(newEventObject)

    # Edit input set and return
    return {"sports": dictOfSports, "venues": inputSet["venues"], "events": listOfEvents,
            "distanceMatrix": inputSet["distanceMatrix"], "reporterLimit": inputSet["reporterLimit"], "reportersSpecialiseBySport": inputSet["reportersSpecialiseBySport"]}

# Function to update the dict of sports with new priority level by sport


def readPriorityLevels(inputSet, file='/Users/shreyasharish/Documents/WwN/Venue distances.xls', sheetName="Constraints"):
    # Opening the appropriate excel and sheet
    excelWorkbook = xlrd.open_workbook(file)
    constraintsSheet = excelWorkbook.sheet_by_name(sheetName)

    # Get priority level and create new sport object for each
    dictOfSports = {}
    rowNumber = 5
    colNumber = 0
    colNumberOffset = 2
    lastRow = constraintsSheet.nrows-1
    while rowNumber <= lastRow:
        sportName = constraintsSheet.cell_value(rowNumber, colNumber)
        priorityLevel = int(constraintsSheet.cell_value(
            rowNumber, colNumber+colNumberOffset))
        dictOfSports[sportName] = sport(sportName)
        dictOfSports[sportName].setReportersRequired(
            inputSet["sports"][sportName].reportersRequired)
        dictOfSports[sportName].setPriorityLevel(priorityLevel)
        rowNumber += 1

    #Update sports objects inside event objects
    listOfEvents = []
    for eventObject in inputSet["events"]:
        newEventObject = event(dictOfSports[eventObject.sport.sportName],eventObject.venue,eventObject.startTime,eventObject.endTime)
        listOfEvents.append(newEventObject)

    # Edit input set and return
    return {"sports": dictOfSports, "venues": inputSet["venues"], "events": listOfEvents,
            "distanceMatrix": inputSet["distanceMatrix"], "reporterLimit": inputSet["reporterLimit"], "reportersSpecialiseBySport": inputSet["reportersSpecialiseBySport"]}


# Function to update the reporter specialisation flag


def readReporterSpecialisation(inputSet, file='/Users/shreyasharish/Documents/WwN/Venue distances.xls', sheetName="Constraints"):
    # Opening the appropriate excel and sheet
    excelWorkbook = xlrd.open_workbook(file)
    constraintsSheet = excelWorkbook.sheet_by_name(sheetName)

    # Get reporter specialisation
    reporterSpecialisation = constraintsSheet.cell_value(2, 1)
    if reporterSpecialisation == "No":
        reporterSpecialisation = False
    elif reporterSpecialisation == "Yes":
        reporterSpecialisation = True

    # Edit input set and return
    return {"sports": inputSet["sports"], "venues": inputSet["venues"], "events": inputSet["events"],
            "distanceMatrix": inputSet["distanceMatrix"], "reporterLimit": inputSet["reporterLimit"], "reportersSpecialiseBySport": reporterSpecialisation}