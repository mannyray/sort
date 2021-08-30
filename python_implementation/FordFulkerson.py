import collections

#algorithm from https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm

class GraphAlgorithm:

    def __init__(self,edgeCount):
        self.edgeCount = edgeCount
        self.residualGraph = []
        for i in range(0,self.edgeCount):
            self.residualGraph.append( [0]*edgeCount)

        self.capacityGraph = []
        for i in range(0,self.edgeCount):
            self.capacityGraph.append( [0]*edgeCount)

    # assuming directed edge from node1 -> node2 with capacity _capacity_
    # and flow _flow_
    def addEdge(self,node1,node2,capacity,flow = 0):
        self.residualGraph[node1][node2] = capacity #- flow
        self.residualGraph[node2][node1] = flow

        # in directed graph, helps keep track of which direction is the capacity
        self.capacityGraph[node1][node2] = capacity

    # return boolean based on if it is possible to reach
    # node _finish_ if starting at node _finish_. Algorithm used 
    # is breadth first search (bfs). If boolean returned, then 
    # second value returned is a parent array
    def breadthFirstSearch(self,adjacencyMatrix,start,finish):
        visited = [False] * self.edgeCount
        path = [-1]*self.edgeCount

        queue = collections.deque()

        queue.append(start)
        visited[start] = True

        while queue:
            currentNode = queue.popleft()

            #find all neighbours of currentNode and add them to queue
            for potentialNeighbour in range(0,self.edgeCount): 
                if adjacencyMatrix[currentNode][potentialNeighbour] > 0 and visited[potentialNeighbour] == False:
                    visited[potentialNeighbour] = True 
                    queue.append(potentialNeighbour)
                    path[potentialNeighbour] = currentNode 

        return visited[finish],path

    def EdmondsKarp(self,source,sink):    
        adjacencyMatrixCopy = []
        for i in range(0,self.edgeCount):
            adjacencyMatrixCopy.append([0]*self.edgeCount)
        for i in range(0,self.edgeCount):
            for j in range(0,self.edgeCount):
                adjacencyMatrixCopy[i][j] = self.residualGraph[i][j]
        flow = 0

        while True:

            canReachSink, parentArray = self.breadthFirstSearch(adjacencyMatrixCopy,source,sink)
            if canReachSink == False:
                break

            path_flow = float("Inf")
            currentNode = sink
            while currentNode != source:
                path_flow = min( path_flow, adjacencyMatrixCopy[parentArray[currentNode]][currentNode] )
                currentNode = parentArray[currentNode]

            flow = flow + path_flow

            currentNode = sink
            while currentNode != source:
                adjacencyMatrixCopy[parentArray[currentNode]][currentNode] = adjacencyMatrixCopy[parentArray[currentNode]][currentNode] - path_flow
                adjacencyMatrixCopy[currentNode][parentArray[currentNode]] = adjacencyMatrixCopy[currentNode][parentArray[currentNode]] + path_flow
                currentNode = parentArray[currentNode]

        # compute the flow graph:
        flowGraph = []
        for i in range(0,self.edgeCount):
            flowGraph.append([0]*self.edgeCount)
        
        for i in range(0,self.edgeCount):
            for j in range(0,self.edgeCount):
                if self.capacityGraph[i][j] > 0: 
                    flowGraph[i][j] = adjacencyMatrixCopy[j][i] 

        return flow,flowGraph
