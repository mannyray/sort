import java.util.Queue; 
import java.util.LinkedList;

public class fordfulkerson{

	int noParent = -1;
	int flow = 0;
	int edgeCount = 0;
	int [][] residualGraph = null;
	int [][] capacityGraph = null;

	public fordfulkerson(int edgeCount){
		this.edgeCount = edgeCount;
		this.residualGraph = new int[edgeCount][];
		this.capacityGraph = new int[edgeCount][];
		for( int i = 0; i < edgeCount; i++ ){
			int [] arr = new int[edgeCount];
			int [] arr2 = new int[edgeCount];
			for( int j = 0; j < edgeCount; j++ ){
				arr[j] = 0;
				arr2[j] = 0;
			}
			this.residualGraph[i] = arr;
			this.capacityGraph[i] = arr2;
		}

	}

	public int getFlow(){
		return this.flow;
	}

	public void addEdge(int node1, int node2, int capacity, int flow){
		this.residualGraph[node1][node2] = capacity - flow;
		this.residualGraph[node2][node1] = flow;
		this.capacityGraph[node1][node2] = capacity;

	}

	public int [] breadthFirstSearch(int[][] residualGraph,int startNode){

		boolean[] visited = new boolean[this.edgeCount];
		int[] path = new int[this.edgeCount];
		for( int i = 0; i < this.edgeCount; i++ ){
			visited[i] = false;
			path[i] = this.noParent;
		}

		Queue<Integer> q = new LinkedList<Integer>();
		q.add(startNode);

		while(q.size() > 0){
			int currentNode = q.remove();
			for(int i = 0; i < this.edgeCount; i++){
				if( residualGraph[currentNode][i] > 0 && visited[i] == false){
					visited[i] = true;
					q.add(i);
					path[i] = currentNode;
				}
			}
		}
		return path;
	}

	public int[][] EdmondsKarp( int source, int sink ){
		
		int [][] residualGraphCopy = new int[edgeCount][];
		for( int i = 0; i < edgeCount; i++ ){
			int [] arr = new int[edgeCount];
			for( int j = 0; j < edgeCount; j++ ){
				arr[j] = this.residualGraph[i][j];
			}
			residualGraphCopy[i] = arr;
		}

		int flow = 0;
		
		while(true){
			int [] path = this.breadthFirstSearch( residualGraphCopy, source);
			boolean canReachSink = path[sink] != this.noParent;

			if(canReachSink == false){
				break;
			}
			
			int path_flow = Integer.MAX_VALUE;
			int currentNode = sink;

			while( currentNode != source){
				path_flow = Math.min(path_flow,residualGraphCopy[path[currentNode]][currentNode]);
				currentNode = path[currentNode];
			}

			flow = flow + path_flow;
			
			currentNode = sink;
			while( currentNode != source ){
				residualGraphCopy[path[currentNode]][currentNode] = residualGraphCopy[path[currentNode]][currentNode] - path_flow;
				residualGraphCopy[currentNode][path[currentNode]] = residualGraphCopy[currentNode][path[currentNode]] + path_flow;
				currentNode = path[currentNode];
			}
		}


		int [][] flowGraph = new int[edgeCount][];
		for( int i = 0; i < edgeCount; i++ ){
			int [] arr = new int[edgeCount];
			for( int j = 0; j < edgeCount; j++ ){
				arr[j] = 0;
			}
			flowGraph[i] = arr;
		}

		
		for(int i = 0; i < this.edgeCount; i++){
			for(int j = 0; j < this.edgeCount; j++){
				if( this.capacityGraph[i][j] > 0 ){
					flowGraph[i][j] = residualGraphCopy[j][i];
				}
			}
		}

		this.flow = flow;
		return flowGraph;

	}
}
