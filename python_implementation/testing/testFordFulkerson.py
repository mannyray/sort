import sys
sys.path.insert(0,'..')
import FordFulkerson

#https://www-m9.ma.tum.de/graph-algorithms/flow-ford-fulkerson/index_en.html
graphAlg = FordFulkerson.GraphAlgorithm( 5 )
graphAlg.addEdge( 0, 1, 2 )
graphAlg.addEdge( 0, 2, 4 )
graphAlg.addEdge( 1, 2, 3 )
graphAlg.addEdge( 1, 3, 1 )
graphAlg.addEdge( 2, 4, 2 )
graphAlg.addEdge( 2, 3, 5 )
graphAlg.addEdge( 3, 4, 7 )

maxFlow, residualGraph = graphAlg.EdmondsKarp(0,4)

assert maxFlow == 6

#https://www.programiz.com/dsa/ford-fulkerson-algorithm
graphAlg2 = FordFulkerson.GraphAlgorithm( 6 )
graphAlg2.addEdge( 0, 1, 8 )
graphAlg2.addEdge( 0, 2, 3 )
graphAlg2.addEdge( 1, 3, 9 )
graphAlg2.addEdge( 3, 2, 7 )
graphAlg2.addEdge( 2, 4, 4 )
graphAlg2.addEdge( 3, 5, 2 )
graphAlg2.addEdge( 4, 5, 5 )

maxFlow, residualGraph = graphAlg2.EdmondsKarp(0,5)

assert maxFlow == 6


#https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/07DemoFordFulkerson.pdf
graphAlg3 = FordFulkerson.GraphAlgorithm( 6 )
graphAlg3.addEdge( 0, 4, 10 )
graphAlg3.addEdge( 0, 1, 10 )
graphAlg3.addEdge( 1, 2, 9 )
graphAlg3.addEdge( 4, 1, 2 )
graphAlg3.addEdge( 4, 5, 4 )
graphAlg3.addEdge( 4, 2, 8 )
graphAlg3.addEdge( 2, 5, 6 )
graphAlg3.addEdge( 2, 3, 10 )
graphAlg3.addEdge( 5, 3, 10 )


maxFlow, residualGraph = graphAlg3.EdmondsKarp(0,3)

assert maxFlow == 19

