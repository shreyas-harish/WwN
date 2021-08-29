#NOTE: The packages imported below contain functions written for the WwN course at IIM-A
#NOTE: Some of these functions have been reused for the purpose of this project
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

#Packages which have been written/imported exclusively for this project
from olympicEventObjects import *
from olympicScheduling import *

#Reading all inputs (events schedule, distances, reporters available, other constraints)
inputSet = inputOlympicEvents(file='/Users/shreyasharish/Documents/WwN/OlympicEvents.txt')

#Read constraints
#Create different inputSet versions for:
# 1. no constraints
#Read venue distance matrix and update venue order
inputSet1 = readDistanceMatrix(inputSet,'/Users/shreyasharish/Documents/WwN/Venue distances.xls',"Distances")
# 2. fixed number of reporters
#capture number of reporters available
inputSet2 = readReportersAvailable(inputSet1,'/Users/shreyasharish/Documents/WwN/Venue distances.xls',"Constraints")
# 3. 2+ number of reporters required
#Iterate through and capture number of reporters required sport
inputSet3 = readReportersRequired(inputSet2,'/Users/shreyasharish/Documents/WwN/Venue distances.xls',"Constraints")
# 4. 2+3+ event priority
#Iterate through and capture priority by sport
inputSet4 = readPriorityLevels(inputSet3,'/Users/shreyasharish/Documents/WwN/Venue distances.xls',"Constraints")
# 5. 2+3+4+ reporter specialisation flag
#Set reporter specialisation flag
inputSet5 = readReporterSpecialisation(inputSet4,'/Users/shreyasharish/Documents/WwN/Venue distances.xls',"Constraints")
# 6. 2+3+4+5+ updated distance matrix
#Read updated distance matrix
inputSet6 = readDistanceMatrix(inputSet5,'/Users/shreyasharish/Documents/WwN/Venue distances.xls',"Updated Distances")

#Modelling the problem in the form of a graph
#Setup required graphs (different graphs for each set of constraints)
model1 = inputToGraph(inputSet1)
model2 = inputToGraph(inputSet2)
model3 = inputToGraph(inputSet3)
model4 = inputToGraph(inputSet4)
model5 = inputToGraph(inputSet5)
model6 = inputToGraph(inputSet6)

#Finding the minimum number of reports required to cover all events and the maximum events coverable with the given reporters
#Find minimum reporters required if there are no constraints
# 1. no constraints
print("Case 1 - No constraints")
minReportersProblem(model1)
#Find maximum events coverable with given number of reporters
print("Case 2 - Limited reporters available")
maxEventsProblem(model2)
#Find minimum reporters required and maximum events coverable with given number of reporters and number of reporters required per event
print("Case 3 - Multiple reporters required per event + limited reporters")
maxEventsProblem(model3)
#Find maximum events coverable with given number of reporters and number of reporters required per event and event priority
print("Case 4 - sport priority + multiple reporters per event + limited reporters")
maxEventsProblem(model4)
#Find minimum reporters required and maximum events coverable with given number of reporters and number of reporters required per event and event priority and reporter specialisation by event
print("Case 5 - reporter specialisation + sport priority + multiple reporters per event + limited reporters")
maxEventsProblem(model5)
#Find minimum reporters required and maximum events coverable with updated distances and above event+reporter requirements
print("Case 6 - all constraints with updated distances")
maxEventsProblem(model6)