#NOTE: The packages imported below contain functions written for the WwN course at IIM-A
#NOTE: Some of these functions have been reused for the purpose of this project
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

#Reading all inputs (events schedule, distances, reporters available, other constraints)
inputSet = inputOlympicEvents(file='/Users/shreyasharish/Documents/WwN/OlympicEvents.txt')
#TODO: Read venue distance matrix

#Read constraints
    #TODO: capture number of reporters available
    #TODO: Iterate through and capture number of reporters required and priority by event type
    #TODO: Set reporter specialisation flag
    #TODO: Read the updated distance matrix

#Modelling the problem in the form of a graph
#TODO: Setup required graphs (different graphs for each set of constraints)
#TODO: Create multiple versions of 3 olympic lists + constraints and from each group create 1 graph

#Finding the minimum number of reports required to cover all events and the maximum events coverable with the given reporters
#Find minimum reporters required if there are no constraints
#TODO: Print set of constraints being used
#TODO: Call function to find min reporters required for a given graph (print the list of events against each reporter)
#Find maximum events coverable with given number of reporters
#TODO: Print set of constraints being used
#TODO: If browniePoints flag is on, call function to find list of coverable events with above constraints
#Find minimum reporters required and maximum events coverable with given number of reporters and number of reporters required per event
#TODO: Print set of constraints being used
#TODO: Call function to find min reporters required for a given graph (print the list of events against each reporter)
#TODO: If browniePoints flag is on, call function to find list of coverable events with above constraints
#Find maximum events coverable with given number of reporters and number of reporters required per event and event priority
#TODO: Print set of constraints being used
#TODO: If browniePoints flag is on, call function to find list of coverable events with above constraints
#Find minimum reporters required and maximum events coverable with given number of reporters and number of reporters required per event and event priority and reporter specialisation by event
#TODO: Print set of constraints being used
#TODO: Call function to find min reporters required for a given graph (print the list of events against each reporter)
#TODO: If browniePoints flag is on, call function to find list of coverable events with above constraints
#Find minimum reporters required and maximum events coverable with updated distances and above event+reporter requirements
#TODO: Print set of constraints being used
#TODO: Call function to find min reporters required for a given graph (print the list of events against each reporter)
#TODO: If browniePoints flag is on, call function to find list of coverable events with above constraints