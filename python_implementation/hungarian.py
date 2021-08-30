import copy
import FordFulkerson

#assignments = hungarianAlgorithm(candidateCount,candidateIDs,candidateOptions):
#INPUT:
#   candidateCount -> the amount of candidates
#   candidateIDs -> array of length candidates where each entry
#       is a unique identifier representing a candidate
#   candidateOptions -> an array of length candidateCount where
#       entry i are the options for candidate candidateIDs[i]. Each entry
#       is an entry of length candidateCount -> candidateOptions is a
#       square matrix with candidateCount rows.
#
#OUTPUT:
#   assignments: an array of length candidateCount where each entry i is a
#   triplet (ID_i,column,cost) where ID_i == candidateIDs[i]
#   where the job assigned to ID_i has cost == candidateOptions[i][column]
def hungarianAlgorithm( candidateCount, candidateIDs, candidateOptions ):

    candidateOptionsCopy = copy.deepcopy(candidateOptions)
    
    #check input is valid
    assert (candidateCount == len(candidateIDs)), "candidateCount does not match length of candidateIDs"
    assert (candidateCount == len(candidateOptions)), "candidateCount does not match length of candidateOptions"

    if candidateCount==0:
        return []
    
    for i in range(0,len(candidateOptions)):
        assert ( candidateCount == len(candidateOptions[i])), str(i) + " of candidateOption is not of proper length " + str(candidateCount) + " " + str(len(candidateOptions[i]))


    #for each row of the matrix, find the smallest element and subtract it from every element in its row
    for rowIndex in range(0,candidateCount):
        minRow = min(candidateOptions[rowIndex])
        for columnIndex in range(0,candidateCount):
            candidateOptions[rowIndex][columnIndex] = candidateOptions[rowIndex][columnIndex] - minRow

    #for each column of the matrix, find the smallest element and subtract it from every element in the column
    for columnIndex in range(0,candidateCount):
        minColumn = candidateOptions[0][columnIndex]
        for rowIndex in range(0,candidateCount):
            minColumn = min(minColumn, candidateOptions[rowIndex][columnIndex])
        for rowIndex in range(0,candidateCount):
            candidateOptions[rowIndex][columnIndex] = candidateOptions[rowIndex][columnIndex] - minColumn

    counter = 0
    while True:

        counter = counter + 1
        #in case while loop has been running for too long
        if counter > 100:
            break

        minimumElement = None
        #cover all zeros in the matrix using minimum number of horizontal and vertical lines
        #rowCover are the row indices of the vertical lines and colCover are the column
        #indices of the horizontal lines
        rowCover, colCover = coverZeros(candidateOptions)

        #test for optimality, if len(rowCover) + len(colCover) equals candidateCount then we are done algorithm
        if len(rowCover) + len(colCover) < candidateCount:

            #determine the smallest entry not covered by any lines (from rowCover/colCover) and
            #subtract from each uncovered row/column
            for row in range(0,candidateCount):
                for col in range(0,len(candidateOptions[row])):
                    if row not in rowCover and (col) not in colCover:
                        if minimumElement == None:
                            minimumElement = candidateOptions[row][col]
                        else:
                            minimumElement = min(minimumElement,candidateOptions[row][col])

            for row in range(0,candidateCount):
                if row in rowCover:
                    continue
                for col in range(0,len(candidateOptions[row])):
                    candidateOptions[row][col] = candidateOptions[row][col] - minimumElement

            
            for col in range(0,candidateCount):
                if (col+candidateCount) not in colCover:
                    continue
                for row in range(0,candidateCount):
                    candidateOptions[row][col] = candidateOptions[row][col] + minimumElement

        else:
            result =  selectOptimalRange(candidateOptions)     
            IDMatch = {  }
            for i in range(0,len(result)):
                IDMatch[ (candidateIDs[result[i][0]]) ] = (result[i][1],candidateOptionsCopy[result[i][0]][result[i][1]] )

            #sort according to input of candidateIDs
            output = []
            for ID in candidateIDs:
                output.append( (ID, IDMatch[ID][0], IDMatch[ID][1]) )
            return output


#Assumption:
#For a square matrix for which X,Y = coverZeros( matrix )
#is such that len(X) + len(Y) = rowCount
#
#OUTPUT
#selectOptimalRange returns an array of (row,col) matrix coordinates
#of length rowCount where ith coordinate (row_i,col_i) is such that
#matrix[row_i][col_i] == 0 and for j != i, row_i != row_j and col_i != col_j
#This algorithm is recursive.
def selectOptimalRange( matrix ):
    #base case: Matrix is 1X1
    if len(matrix) == 1:
        if matrix[0][0] == 0:
            return [(0,0)]
        else:
            return None
    else:
        #based on our assumption, it is the case that the first column
        #has at least one zero. We iterate through the first column
        #and each time we encounter a zero at location matrix[row][0]
        #we create a submatrix with column at index 0 removed and
        #row at index _row_ removed (because of _j != i, row_i != row_j and col_i != col_j_).
        #We then recurse on the submatrix using selectOptimalRange. If the recursion on
        #submatrix tmp returns None, then this means that our choice of _row_ in for loop
        #is wrong as we cannot return what the OUTPUT of selectOptimalRange should
        #be.
        for row in range(0,len(matrix[0])):
            if matrix[row][0] == 0:
                
                zeroIndex = (row,0)

                tmp = copy.deepcopy(matrix)
                tmp.pop(row)
                for i in range(0,len(tmp)):
                    tmp[i].pop(0)

                res = selectOptimalRange( tmp )
                if res != None:
                    for i in range(0,len(res)):
                        if res[i][0] < row:
                            rowIndex = res[i][0]
                        else:
                            rowIndex = res[i][0] + 1
                        colIndex = res[i][1] + 1
                        res[i] = (rowIndex, colIndex)
                    res.append(zeroIndex)
                    return res
    return None
        
#For a given square matrix where some entries are zero and the rest non zero, 
#coverZeros returns a list of row indexes X and a list of column indexes Y
#such that if one crosses out all the rows specified in X and all columns in Y, then all the
#zeros in the matrix will be crossed out. len(X) + len(Y) is minimal
#X,Y = coverZeros( matrix )
def coverZeros( matrix ):

    #check that matrix is a square matrix
    rowCount = len(matrix)
    for row in range(0,rowCount):
        assert( rowCount == len(matrix[row]) ), "coverZeros: not a square matrix"

    # To solve this problem, we will translate it to another equivalent problem.
    # Consider the minimum vertex cover problem. A vertex cover is a set of vertices
    # in a graph such that for every edge e = (u,v) at least one of u/v is in the vertex
    # cover set S. Minimum vertex cover is a vertex cover such that the cardinality of S
    # is as small as possible ( |S| is minimized ).
    #
    # Consider the 3X3 matrix D looks like
    #     X 0 X
    # D = 0 0 0
    #     X X 0
    # where 'X' is a non zero number. Consider we label the rows and columns as such:
    #     c1  c2  c3
    # r1   X   0   X
    # r2   0   0   0
    # r3   X   X   0
    #
    # Next, consider constructing a graph where the vertices are the labels
    # (r1,r2,r3,c1,c2,c3) and the edges are between column and row labels
    #  where D[row_label][col_label] is equal to zero 
    #
    # The adjacency matrix of the resultant graph would look like:
    #     r1  r2  r3  c1  c2  c3
    # r1   0   0   0   0   1   0
    # r2   0   0   0   1   1   1
    # r3   0   0   0   0   0   1
    # c1   0   1   0   0   0   0
    # c2   1   1   0   0   0   0
    # c3   0   1   1   0   0   0
    #
    # The problem of covering all the zeros is equivalent to finding a vertex cover.
    # Every edge in the graph will be of the form (rN,cM) and represents a zero in the 
    # original graph D. Due to the definition a vertex cover, at least one of rN or cM will be
    # in the vertex cover. If we cross out all the rN rows in D (that are part of the vertex cover)
    # and all the cN columns in D (that are part of the vertex cover) then all of the zeros
    # will be crossed out.
    #
    # It remains to show that 
    # X,Y = coverZeros( matrix ) where len(X) + len(Y) is minimized
    # is equal to cardinality vertex cover (|S|)
    # len(X) + len(Y) = |S| 
    #
    # For full soundness one needs to prove that
    # Assume len(X) + len(Y) = F is minimal and F < |S| is not possible
    # Assume len(X) + len(Y) = F is minimal and F > |S| is not possible
    # Only possibility is that len(X) + len(Y) = |S|
    # This will not be done here.
    #
    # Now let us do another equivalence. The graph constructed above is
    # is bipartite graph with one set being (r1,r2,r3,...) and the other
    # (c1,c2,c3,...)
    # Due to Konig's theorem [1], there is an equivalence between minimum vertex cover
    # and maximum matching problem. Maximum matching can be viewed as a maximum flow
    # problem [2] and can be solved using the Ford Fulkerson algorithm.
    #
    # Our implementation here will solve the max flow for the bipartite graph
    # (r1,r2,r3,...),(c1,c2,c3,...). The output of the max flow algorithm is
    # the scalar value of the max flow, but also the resultant residual graph.
    # We can use the residual graph to find all edges between rN to cM to make the
    # maximum matching result. After we will convert the maximum matching to
    # minimum vertex cover which will give us X,Y for X,Y = coverZeros( matrix ).
    #
    # [1] https://en.wikipedia.org/wiki/K%C5%91nig%27s_theorem_(graph_theory)
    # [2] https://en.wikipedia.org/wiki/Maximum_cardinality_matching

    nodes = []
    nodeCount = rowCount*2
    for node in range(0,nodeCount):
        nodes.append(node)    

    # create biparite graph, (+2) add source/sink node for ford fulkerson
    graphAlg = FordFulkerson.GraphAlgorithm(nodeCount + 2)
    for rowNode in range(0,rowCount):
        for columnNode in range(rowCount,nodeCount):
            if matrix[rowNode][columnNode-rowCount] == 0:
                graphAlg.addEdge(rowNode,columnNode,1)

    # connect source to all row nodes
    sourceNode = nodeCount
    for rowNode in range(0,rowCount):
        graphAlg.addEdge(sourceNode,rowNode,1)

    # connect sink to all column nodes
    sinkNode = nodeCount + 1
    for columnNode in range(rowCount,nodeCount):
        graphAlg.addEdge(columnNode,sinkNode,1)

    maxFlow, residualGraph = graphAlg.EdmondsKarp(sourceNode,sinkNode)

    # get maximum matching from residual graph
    # all the edges with flow from the rN nodes flowing to the cM nodes
    maximumMatchingEdgeList = []
    for rowNode in range(0,rowCount):
        for columnNode in range(rowCount,nodeCount):
            if residualGraph[rowNode][columnNode] == 1:
                # since only one edge with volume 1 flowing from sourceNode
                # to rowNode, this condition will only be hit once
                maximumMatchingEdgeList.append( (rowNode,columnNode) )

    # get all the vertices from the edges that are part of maximum matching
    verticesPartOfMaximumMatching = []
    for edge in range(0,len(maximumMatchingEdgeList)):
        verticesPartOfMaximumMatching.append(maximumMatchingEdgeList[edge][0])
        verticesPartOfMaximumMatching.append(maximumMatchingEdgeList[edge][1])

    #convert to minimum cover
    cover = []
    if len(verticesPartOfMaximumMatching) == nodeCount:
        # easy case where every edge is part of maximum matching
        # which means we need every row  
        for row in range(0,rowCount):
            cover.append(row)
    else:
        # Due to Konig's theorem, there is an equivalence between maximum matching and minimum cover set.
        # We will discuss transforming maximum matching to minimum cover.
        #
        # By definition of minimum cover, for each edge (u,v) in maximum matching at least
        # one of the u or v _has_ to be in the minimum cover S. In order to decide which 
        # of u or v we include in the minimum cover S, we focus on all the vertices that 
        # are _not_ part of the maximum matching. We go through each vertex that is _not_ part of
        # of an edge in maximum matching (not in verticesPartOfMaximumMatching) - we call such vertex -> P.
        #
        # By definition of cover set, all edges in graph must have at least one vertex part
        # of the minimum vertex cover set S. Therefore, vertex P must be connected to a vertex 
        # that is part of vertex cover set -> vertex Q. Let Q be all vertices thare are adjacent of
        # P _and_ part of maximum matching (in verticesPartOfMaximumMatching).
        # 
        # Going through all possible P -> all the Qs will define the cover set. This section explains
        # the logic below.

        unmarkedVisited = [False]*nodeCount
        for node in range(0,nodeCount):

            if node not in verticesPartOfMaximumMatching:#P vertex
                if unmarkedVisited[node] == True:
                    continue

                unmarked = [node]
                while len(unmarked) > 0:
                    currentUnmarked = unmarked.pop()
                    if unmarkedVisited[currentUnmarked] == False:
                        unmarkedVisited[currentUnmarked] = True
                    else:
                        continue
                    matchedNeighboursOfCurrent = []

                    # find all Q vertex
                    if currentUnmarked < rowCount:#(r1,r2,r3,...) - row node
                        for col in range(0,len(matrix[currentUnmarked])):
                            if matrix[currentUnmarked][col] == 0 and (rowCount+col) in verticesPartOfMaximumMatching:
                                matchedNeighboursOfCurrent.append(rowCount + col)
                    else:#(c1,c2,c3,...) - column node
                        for row in range(0,rowCount):
                            if matrix[row][currentUnmarked-rowCount] == 0 and (row) in verticesPartOfMaximumMatching:
                                matchedNeighboursOfCurrent.append(row)

                    
                    for matched in matchedNeighboursOfCurrent:
                        if matched not in cover:
                            cover.append(matched)

        # Cover the scenario where there are vertices that have no adjacent vertices of type P.
        for vertex in verticesPartOfMaximumMatching:
            if vertex not in cover:
                for edge in maximumMatchingEdgeList:
                    if edge[0] == vertex:
                        if edge[1] not in cover:
                            cover.append(vertex)
                            break
                    elif edge[1] == vertex:
                        if edge[0] not in cover:
                            cover.append(vertex)
                            break

    #convert minimum cover to match the coverZeros output format
    rowsToCover = []
    colsToCover = []
    for node in cover:
        if node < rowCount:
            rowsToCover.append(node)
        else:
            colsToCover.append(node-rowCount)
    return rowsToCover, colsToCover
