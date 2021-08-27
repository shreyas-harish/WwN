import xlrd
import xlwt
import xlsxwriter
import os
import shutil

#Function to read distance matrix and reorder the venue list accordingly
def readDistanceMatrix(inputSet,file='/Users/shreyasharish/Documents/WwN/Venue distances.xls',sheetName="Distances"):
    #Opening the appropriate excel and sheet
    excelWorkbook = xlrd.open_workbook(file)
    distanceSheet = excelWorkbook.sheet_by_name(sheetName)

    #Populate the list of venues in the required order
    listOfVenues = []
    rowNumber = 2
    colNumber = 1
    lastRow = distanceSheet.nrows-1
    while rowNumber <= lastRow:
        listOfVenues.append(distanceSheet.cell_value(rowNumber,colNumber))
        rowNumber += 1

    #Create a distance matrix and populate the same
    distanceMatrix = [[0.0 for i in range(len(listOfVenues))] for j in range(len(listOfVenues))]
    #Populate distance matrix in hour values from minutes
    rowNumberOffset = 2
    colNumberOffset = 2
    for row in range(len(listOfVenues)):
        for col in range(len(listOfVenues)):
            distanceMatrix[row][col] = (float(distanceSheet.cell_value(row+rowNumberOffset,col+colNumberOffset))/60)

    inputSet["venues"] = listOfVenues
    inputSet["distanceMatrix"] = distanceMatrix

    return inputSet


#TODO: Function to read the new distance matrix

#TODO: Function to update dict of sports with new constraints

#TODO: Function to update the number of reporters available

#TODO: Function to update the reporter specialisation flag