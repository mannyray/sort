//import fordfulkerson.fordfulkerson;

public class test_fordfulkerson {
	public static void main(String[] args) { 
		fordfulkerson F = new fordfulkerson(5);
		F.addEdge(0,1,2,0);
		F.addEdge(0,2,4,0);
		F.addEdge(1,2,3,0);
		F.addEdge(1,3,1,0);
		F.addEdge(2,4,2,0);
		F.addEdge(2,3,5,0);
		F.addEdge(3,4,7,0);
		int res1[][] = F.EdmondsKarp(0,4);
		for(int i=0; i<5; i++){
			for(int j=0; j<5; j++){
				System.out.print(res1[i][j]+" ");
			}System.out.println();
		}
		System.out.println(F.getFlow());

		fordfulkerson F2 = new fordfulkerson(6);
		F2.addEdge( 0, 1, 8, 0); 
		F2.addEdge( 0, 2, 3, 0);
		F2.addEdge( 1, 3, 9, 0);
		F2.addEdge( 3, 2, 7, 0);
		F2.addEdge( 2, 4, 4, 0);
		F2.addEdge( 3, 5, 2, 0);
		F2.addEdge( 4, 5, 5, 0);
		int res2[][] = F2.EdmondsKarp(0,5);
		for(int i=0; i<6; i++){
			for(int j=0; j<6; j++){
				System.out.print(res2[i][j]+" ");
			}System.out.println();
		}
		System.out.println(F2.getFlow());


		fordfulkerson F3 = new fordfulkerson(6);
		F3.addEdge( 0, 4, 10, 0);
		F3.addEdge( 0, 1, 10, 0); 
		F3.addEdge( 1, 2, 9, 0); 
		F3.addEdge( 4, 1, 2, 0);
		F3.addEdge( 4, 5, 4, 0); 
		F3.addEdge( 4, 2, 8, 0);
		F3.addEdge( 2, 5, 6, 0);
		F3.addEdge( 2, 3, 10, 0); 
		F3.addEdge( 5, 3, 10, 0); 
		int res3[][] = F3.EdmondsKarp(0,3);
		for(int i=0; i<6; i++){
			for(int j=0; j<6; j++){
				System.out.print(res3[i][j]+" ");
			}System.out.println();
		}
		System.out.println(F3.getFlow());
	}
}
