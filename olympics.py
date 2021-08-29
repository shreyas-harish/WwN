# NOTE: The packages imported below contain functions written for the WwN course at IIM-A
# NOTE: Some of these functions have been reused for the purpose of this project
from readExcelInput import readDistanceMatrix, readPriorityLevels, readReporterSpecialisation, readReportersAvailable, readReportersRequired
from graphDefs import *
from readInput import *
from bfs import *
from dfs import *
from bf import *
from dijkstras import *
from floydWarshall import *
from yen import *
from astar import *
from maxflow import *
from minCost import *

# Packages which have been written/imported exclusively for this project
from olympicEventObjects import *
from olympicScheduling import *


# Function to handle all inputs required for olympic scheduling
def inputScheduleAndConstraint():
    # Reading all inputs (events schedule, distances, reporters available, other constraints)
    inputSet = inputOlympicEvents(
        file='/Users/shreyasharish/Documents/WwN/OlympicEvents.txt')

    # Read constraints
    # Create different inputSet versions for:
    # 1. no constraints
    # Read venue distance matrix and update venue order
    inputSet1 = readDistanceMatrix(
        inputSet, '/Users/shreyasharish/Documents/WwN/Venue distances.xls', "Distances")
    # 2. fixed number of reporters
    # capture number of reporters available
    inputSet2 = readReportersAvailable(
        inputSet1, '/Users/shreyasharish/Documents/WwN/Venue distances.xls', "Constraints")
    # 3. 2+ number of reporters required
    # Iterate through and capture number of reporters required sport
    inputSet3 = readReportersRequired(
        inputSet2, '/Users/shreyasharish/Documents/WwN/Venue distances.xls', "Constraints")
    # 4. 2+3+ event priority
    # Iterate through and capture priority by sport
    inputSet4 = readPriorityLevels(
        inputSet3, '/Users/shreyasharish/Documents/WwN/Venue distances.xls', "Constraints")
    # 5. 2+3+4+ reporter specialisation flag
    # Set reporter specialisation flag
    inputSet5 = readReporterSpecialisation(
        inputSet4, '/Users/shreyasharish/Documents/WwN/Venue distances.xls', "Constraints")
    # 6. 2+3+4+5+ updated distance matrix
    # Read updated distance matrix
    inputSet6 = readDistanceMatrix(
        inputSet5, '/Users/shreyasharish/Documents/WwN/Venue distances.xls', "Updated Distances")

    return {"inputSet1": inputSet1, "inputSet2": inputSet2, "inputSet3": inputSet3, "inputSet4": inputSet4, "inputSet5": inputSet5, "inputSet6": inputSet6}

# Function to handle all inputs required for olympic scheduling


def modelInputsAsGraph(inputSets):
    # Modelling the problem in the form of a graph
    # Setup required graphs (different graphs for each set of constraints)
    model1 = inputToGraph(inputSets["inputSet1"])
    model2 = inputToGraph(inputSets["inputSet2"])
    model3 = inputToGraph(inputSets["inputSet3"])
    model4 = inputToGraph(inputSets["inputSet4"])
    model5 = inputToGraph(inputSets["inputSet5"])
    model6 = inputToGraph(inputSets["inputSet6"])

    return {"model1": model1, "model2": model2, "model3": model3, "model4": model4, "model5": model5, "model6": model6}

# Function to complete scheduling and print results


def scheduleOlympicReporters(models):
    # Finding the minimum number of reports required to cover all events and the maximum events coverable with the given reporters
    # Find minimum reporters required if there are no constraints
    # 1. no constraints
    print("Case 1 - No constraints")
    minReportersProblem(models["model1"])
    # Find maximum events coverable with given number of reporters
    print("Case 2 - Limited reporters available")
    maxEventsProblem(models["model2"])
    # Find minimum reporters required and maximum events coverable with given number of reporters and number of reporters required per event
    print("Case 3 - Multiple reporters required per event + limited reporters")
    maxEventsProblem(models["model3"])
    # Find maximum events coverable with given number of reporters and number of reporters required per event and event priority
    print("Case 4 - sport priority + multiple reporters per event + limited reporters")
    maxEventsProblem(models["model4"])
    # Find minimum reporters required and maximum events coverable with given number of reporters and number of reporters required per event and event priority and reporter specialisation by event
    print("Case 5 - reporter specialisation + sport priority + multiple reporters per event + limited reporters")
    maxEventsProblem(models["model5"])
    # Find minimum reporters required and maximum events coverable with updated distances and above event+reporter requirements
    print("Case 6 - all constraints with updated distances")
    maxEventsProblem(models["model6"])


inputSets = inputScheduleAndConstraint()
models = modelInputsAsGraph(inputSets)
scheduleOlympicReporters(models)
