#This file contains helper functions to read txt files and store the input in the form of a network/graph.
from graphDefs import *

file1 = open('/Users/shreyasharish/Documents/WwN/input.txt','r')
Lines = file1.readlines()
for lin in Lines:
    print(lin.strip())