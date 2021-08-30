import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.*;

public class hungarian{
	class IntPair{
		final int x;
		final int y;
		IntPair(int x, int y) {this.x=x;this.y=y;}
	}

	class Pair{
		final int x;
		final double y;
		Pair(int x, double y) {this.x=x;this.y=y;}
	}

	public class Selection{
		final String ID;
		final int jobNum;
		final double jobCost;
		Selection(String ID, int jobNum, double jobCost){ this.ID=ID;this.jobNum=jobNum;this.jobCost=jobCost;}
	}


	public boolean contains(int [] arr, int item){
		for(int i=0; i<arr.length; i++){
			if(arr[i]==item){
				return  true;
			}
		}
		return false;
	}
	
	public List<Selection> hungarianAlgorithm( int candidateCount, String[] candidateIDs, double [][] candidateOptions){
		double [][] candidateOptionsCopy = new double[candidateCount][candidateCount];

		if(candidateCount != candidateIDs.length){
			throw new RuntimeException("hungarianAlgorithm expects candidateCount to match candidateIDs length");
		}
		if(candidateCount != candidateOptions.length){
			throw new RuntimeException("hungarianAlgorithm expects candidateCount to match candidateOptions length");
		}
		for(int i=0; i<candidateOptions.length; i++){
			if(candidateCount != candidateOptions[i].length){
				throw new RuntimeException("hungarianAlgorithm expects candidateCount["+i+"] to match candidateOptions length");
			}
		}

		for(int i=0; i<candidateCount; i++){
			for(int j=0; j<candidateCount; j++){
				candidateOptionsCopy[i][j] = candidateOptions[i][j];
			}
		}

		if(candidateCount==0){
			return new ArrayList<Selection>(); 
		}

		for(int rowIndex=0; rowIndex<candidateCount; rowIndex++){
			double minRow = candidateOptions[rowIndex][0];
			for(int colIndex=0; colIndex<candidateCount; colIndex++){
				if(minRow>candidateOptions[rowIndex][colIndex]){
					minRow = candidateOptions[rowIndex][colIndex];
				}
			}
			for(int colIndex=0; colIndex<candidateCount; colIndex++){
				candidateOptions[rowIndex][colIndex] = candidateOptions[rowIndex][colIndex] - minRow;
			}
		}
		for(int colIndex=0; colIndex<candidateCount; colIndex++){
			double minColumn = candidateOptions[0][colIndex];
			for(int rowIndex=0; rowIndex<candidateCount; rowIndex++){
				if(minColumn>candidateOptions[rowIndex][colIndex]){
					minColumn = candidateOptions[rowIndex][colIndex];
				}
			}
			for(int rowIndex=0; rowIndex<candidateCount; rowIndex++){
				candidateOptions[rowIndex][colIndex] = candidateOptions[rowIndex][colIndex] - minColumn;
			}
		}


		int counter = 0;

		while(true){
			counter = counter + 1;
			if(counter > 100){
				break;
			}
			
			int [][] res = coverZeros(candidateOptions);	
			int [] rowCover = res[0];
			int [] colCover = res[1];
			if(rowCover.length + colCover.length < candidateCount){
				double minimumElement = Double.MAX_VALUE;
				for(int row=0; row<candidateCount; row++){
					for(int col=0; col<candidateCount; col++){
						if(!contains(rowCover,row) && !contains(colCover,col)){
							if(minimumElement == Double.MAX_VALUE){
								minimumElement = candidateOptions[row][col];
							}
							else if(minimumElement > candidateOptions[row][col]){
								minimumElement = candidateOptions[row][col];
							}
						}
					}
				}


				for(int row=0; row<candidateCount; row++){
					if(contains(rowCover,row)){
						continue;
					}
					for(int col=0; col<candidateOptions[row].length; col++){
						candidateOptions[row][col] = candidateOptions[row][col] - minimumElement;
					}
				}

				for(int col=0; col<candidateCount; col++){
					if(!contains(colCover,col+candidateCount)){
						continue;
					}
					for(int row=0; row<candidateCount; row++){
						candidateOptions[row][col] = candidateOptions[row][col] + minimumElement;
					}
				}

			}
			else{
				List<IntPair> result = selectOptimalRange(candidateOptions);
				Map<String,Pair> mMap = new HashMap<String,Pair>();
				for(int i=0; i<result.size(); i++){
					mMap.put(candidateIDs[result.get(i).x], new Pair(result.get(i).y,candidateOptionsCopy[result.get(i).x][result.get(i).y]));	
				}

				List<Selection> output = new ArrayList<Selection>();
				for(int i=0; i<result.size(); i++){
					String ID = candidateIDs[i];
					Selection s = new Selection(ID,mMap.get(ID).x,mMap.get(ID).y);
					output.add(s);
				}
				return output;
			}
		}	
		return null;
	}

	public List<IntPair> selectOptimalRange( double [][]matrix){
		if(matrix.length==1){
			if(matrix[0][0] == 0){
				List<IntPair> res = new ArrayList<IntPair>();
				res.add(new IntPair(0,0));
				return res;
			}
			else{
				return null;
			}
		}
		else{
			for(int row=0;row<matrix.length;row++){
				if(matrix[row][0] == 0){
					IntPair zeroIndex = new IntPair(row,0);
					double [][] subMatrix = new double[matrix.length-1][matrix.length-1];
					for(int i=0; i<matrix.length; i++){
						if(i == row){
							continue;
						}
						for(int j=0; j<matrix.length-1;j++){
							if(i > row){
								subMatrix[i-1][j] = matrix[i][j+1];
							}
							else{
								subMatrix[i][j] = matrix[i][j+1];
							}
						}
					}


					List<IntPair> res = selectOptimalRange(subMatrix);
					if(res != null){
						for(int i=0; i<res.size(); i++){
							int rowIndex = -1;
							if(res.get(i).x < row){
								rowIndex = res.get(i).x;
							}
							else{
								rowIndex = res.get(i).x + 1;
							}
							int colIndex = res.get(i).y + 1;
							IntPair newPair = new IntPair(rowIndex,colIndex);
							res.set(i,newPair);
						}
						res.add(zeroIndex);
						//System.out.println(zeroIndex.x+" "+zeroIndex.y);
						return res;
					}
				}
			}
		}
		return null;
	}	

		
	public int[][] coverZeros(double[][] matrix){

		List<Integer> cover = new ArrayList<>();
		int rowCount = matrix.length;
		for(int row=0; row<rowCount; row++){
			if(matrix[row].length != rowCount){
				throw new RuntimeException("coverZeros expects square matrix");
			}
		}
			
		int nodeCount = rowCount*2;
		int [] nodes = new int[rowCount*2];
		for(int i=0; i<nodeCount; i++){
			nodes[i] = nodeCount;
		}

		//create biparite graph, (+2) add source/sink node for ford fulkerson
		fordfulkerson F = new fordfulkerson(nodeCount+2);
		for(int rowNode=0; rowNode<rowCount; rowNode++){
			for(int columnNode=rowCount; columnNode<nodeCount; columnNode++){
				if(matrix[rowNode][columnNode-rowCount]==0){
					F.addEdge(rowNode,columnNode,1,0);
				}
			}
		}

		//connect source to all row nodes
		int sourceNode = nodeCount;
		for(int rowNode=0; rowNode<rowCount; rowNode++){
			F.addEdge(sourceNode,rowNode,1,0);
		}

		//connect sink to all column nodes
		int sinkNode = nodeCount + 1;
		for(int columnNode=rowCount; columnNode<nodeCount; columnNode++){
			F.addEdge(columnNode,sinkNode,1,0);
		}
		
		int [][] graph = F.EdmondsKarp(sourceNode,sinkNode);


		List<IntPair> maximumMatchingEdgeList = new ArrayList<>();
		for(int rowNode=0; rowNode<rowCount; rowNode++){
			for(int columnNode=rowCount; columnNode<nodeCount; columnNode++){
				if(graph[rowNode][columnNode] == 1){
					maximumMatchingEdgeList.add( new IntPair(rowNode,columnNode) );
				}
			}
		}

		List<Integer> verticesPartOfMaximumMatching = new ArrayList<>();
		for(int edge=0; edge<maximumMatchingEdgeList.size(); edge++){
			verticesPartOfMaximumMatching.add(maximumMatchingEdgeList.get(edge).x);
			verticesPartOfMaximumMatching.add(maximumMatchingEdgeList.get(edge).y);
		}


		if( verticesPartOfMaximumMatching.size() == nodeCount){
			for(int row=0; row<rowCount; row++){
				cover.add(row);
			}
		}
		else{
			boolean unmarkedVisited[] = new boolean[nodeCount];
			for(int i=0; i<nodeCount; i++){
				unmarkedVisited[i] = false;
			}

			for(int node=0; node<nodeCount; node++){
				if(!verticesPartOfMaximumMatching.contains(node)){
					if(unmarkedVisited[node] == true){
						continue;
					}
					List<Integer> unmarked = new ArrayList<>();
					unmarked.add(node);
					while(unmarked.size() > 0){
						int currentUnmarked = unmarked.remove(0);
						if(unmarkedVisited[currentUnmarked] == false){
							unmarkedVisited[currentUnmarked] = true;
						}else{
							continue;
						}

						List<Integer> matchedNeighboursOfCurrent = new ArrayList<>();
						if(currentUnmarked < rowCount){
							for(int col=0; col<matrix[currentUnmarked].length; col++){
								if(matrix[currentUnmarked][col] == 0 && verticesPartOfMaximumMatching.contains(rowCount+col)){
									matchedNeighboursOfCurrent.add(rowCount+col);
								}
							}	
						}
						else{
							for(int row=0; row<rowCount; row++){
								if(matrix[row][currentUnmarked-rowCount] == 0 && verticesPartOfMaximumMatching.contains(row)){
									matchedNeighboursOfCurrent.add(row);
								}
							}
						}

						for(int i=0; i<matchedNeighboursOfCurrent.size(); i++){
							int matched = matchedNeighboursOfCurrent.get(i);
							if(!cover.contains(matched)){
								cover.add(matched);
							}
						}
					}
				}
			}


			for(int i=0; i<verticesPartOfMaximumMatching.size(); i++){
				int vertex = verticesPartOfMaximumMatching.get(i);
				if(!cover.contains(vertex)){
					//for edge in maximumMatchingEdgeList
					for(int j=0;j<maximumMatchingEdgeList.size();j++){
						if(maximumMatchingEdgeList.get(j).x == vertex){
							if(!cover.contains(maximumMatchingEdgeList.get(j).y)){
								cover.add(vertex);
								break;
							}
						}
						else if(maximumMatchingEdgeList.get(j).y == vertex){
							if(!cover.contains(maximumMatchingEdgeList.get(j).x)){
								cover.add(vertex);
								break;
							}
						}
					}
				}
			}

		}


		List<Integer> rowsToCover = new ArrayList<>();
		List<Integer> colsToCover = new ArrayList<>();
		for(int i=0;i<cover.size();i++){
			int node = cover.get(i);
			if(node<rowCount){
				rowsToCover.add(node);
			}
			else{
				colsToCover.add(node);
			}
		}

		int[][] output = new int[2][];
		int [] output_1 = new int[rowsToCover.size()];
		for(int i=0; i<output_1.length; i++){
			output_1[i] = rowsToCover.get(i);			
		}
		output[0] = output_1;

		int [] output_2 = new int[colsToCover.size()];
		for(int i=0; i<output_2.length; i++){
			output_2[i] = colsToCover.get(i) - rowCount;			
		}
		output[1] = output_2;
		return output;
	}
}
