# This file contains definitions for graphs/networks and sub-elements, such as nodes and edges

# Definition of an edge
class edge:
    # Initialization function requires a start and end node. All other parameters take default values to begin with
    def __init__(self, startNode, endNode):
        self.startNode = startNode
        self.endNode = endNode
        self.capacity = 0
        self.cost = 0
        self.utilization = 0
        self.category = 0

    # Function to set or change capacity
    def setCapacity(self, capacity):
        self.capacity = capacity

    # Function to set or change cost
    def setCost(self, cost):
        self.cost = cost

    # Function to set or change utilization
    def setUtilization(self, utilization):
        self.utilization = utilization

    # Function to set or change category
    def setCategory(self, category):
        self.category = category

    # Function to print edge
    def printEdge(self):
        print(self.startNode, "->", self.endNode, ", cap ", self.capacity,
              ", cost ", self.cost, ", util ", self.utilization)

    # Function to print edge in a simpler (succinct) manner
    def printEdgeSimple(self):
        print(self.startNode, "->", self.endNode)


class node:
    # Initialization function requires a nodeID. All other parameters take default values to begin with
    def __init__(self, nodeID):
        self.nodeID = nodeID
        self.category = 0
        self.distance = None
        self.parent = None
        self.edgesIn = {}
        self.edgesOut = {}

    # Function to set or change category
    def setCategory(self, category):
        self.category = category

    # Function to set or change distance
    def setDistance(self, distance):
        self.distance = distance

    # Function to set or change parent
    def setParent(self, parent):
        self.parent = parent

    # Function to add/overwrite inward edge
    def addEdgeIn(self, edgeIn):
        self.edgesIn[edgeIn.startNode] = edgeIn

    # Function to delete inward edge
    def delEdgeIn(self, edgeIn):
        if edgeIn.startNode in self.edgesIn.keys():
            self.edgesIn.pop(edgeIn.startNode)

    # Function to add/overwrite outward edge
    def addEdgeOut(self, edgeOut):
        self.edgesOut[edgeOut.endNode] = edgeOut

    # Function to delete outward edge
    def delEdgeOut(self, edgeOut):
        if edgeOut.endNode in self.edgesOut.keys():
            self.edgesOut.pop(edgeOut.endNode)

    # Function to print node
    def printNode(self):
        print(self.nodeID)


class graph:
    # Initialization function creates an empty dictionary of nodes, with empty source and target variables
    def __init__(self):
        self.nodes = {}
        self.sourceID = None
        self.targetID = None

    # Function to add/overwrite a node
    def addNode(self, addNode):
        self.nodes[addNode] = node(addNode)

    # Function to add a node only if node already doesn't exist
    def safeAddNode(self, addNode):
        if not addNode in self.nodes.keys():
            self.nodes[addNode] = node(addNode)

    # Function to add/overwrite an edge
    def addEdge(self, startNode, endNode, capacity=0, cost=0, utilization=0, category=0, bidirectional=False):
        # Create nodes if missing
        if not startNode in self.nodes.keys():
            self.nodes[startNode] = node(startNode)
        if not endNode in self.nodes.keys():
            self.nodes[endNode] = node(endNode)
        # Create edges and add edges to nodes
        edgeToAdd = edge(startNode, endNode)
        edgeToAdd.setCapacity(capacity)
        edgeToAdd.setCost(cost)
        edgeToAdd.setUtilization(utilization)
        edgeToAdd.setCategory(category)
        self.nodes[startNode].addEdgeOut(edgeToAdd)
        self.nodes[endNode].addEdgeIn(edgeToAdd)
        # For bidirectional edge, create reverse edge and add to nodes
        if bidirectional:
            edgeToAdd = edge(endNode, startNode)
            edgeToAdd.setCapacity(capacity)
            edgeToAdd.setCost(cost)
            edgeToAdd.setUtilization(utilization)
            edgeToAdd.setCategory(category)
            self.nodes[startNode].addEdgeOut(edgeToAdd)
            self.nodes[endNode].addEdgeOut(edgeToAdd)
            self.nodes[startNode].addEdgeIn(edgeToAdd)

    # Function to delete an edge
    def delEdge(self, startNode, endNode, bidirectional=False):
        edgeToDelete = edge(startNode, endNode)
        if startNode in self.nodes.keys():
            self.nodes[startNode].delEdgeOut(edgeToDelete)
        if endNode in self.nodes.keys():
            self.nodes[endNode].delEdgeIn(edgeToDelete)
        if bidirectional:
            edgeToDelete = edge(endNode, startNode)
            if startNode in self.nodes.keys():
                self.nodes[startNode].delEdgeIn(edgeToDelete)
            if endNode in self.nodes.keys():
                self.nodes[endNode].delEdgeOut(edgeToDelete)

    # Function to delete a node
    def delNode(self, remNode):
        # Delete all of the nodes edges from adjacent nodes
        if remNode in self.nodes.keys():
            for ed in self.nodes[remNode].edgesIn:
                if ed in self.nodes.keys():
                    self.nodes[ed].delEdgeOut(edge(ed, remNode))
            for ed in self.nodes[remNode].edgesOut:
                if ed in self.nodes.keys():
                    self.nodes[ed].delEdgeIn(edge(remNode, ed))

        # Delete node itself (and all edges in and out that it holds)
        self.nodes.pop(remNode)

    # Function to print each node in the graph, with all of its incoming & outgoing edges
    def printGraph(self):
        for no in self.nodes:
            nod = self.nodes[no]
            print("Node",end=" ")
            nod.printNode()
            print("Edges In")
            for ed in nod.edgesIn.values():
                ed.printEdge()
            print("Edges Out")
            for ed in nod.edgesOut.values():
                ed.printEdge()

    # Function to print the graph in a simpler (almost edge list) manner
    def printGraphSimple(self):
        for no in self.nodes:
            nod = self.nodes[no]
            nod.printNode()
            for ed in nod.edgesOut.values():
                ed.printEdgeSimple()

    # Function to clear parents across all nodes
    def clearParents(self):
        for no in self.nodes:
            self.nodes[no].parent = None

    # Function to clear category across all nodes
    def clearCategory(self):
        for no in self.nodes:
            self.nodes[no].category = 0

    # Function to print from a given node, upwards through parents
    def printThroughParent(self, no):
        nod = self.nodes[no]
        nod.printNode()
        if not nod.parent == None:
            self.printThroughParent(nod.parent)
