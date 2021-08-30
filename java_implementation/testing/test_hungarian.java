import java.util.List;

public class test_hungarian {
	public static void main(String[] args) {
		hungarian H = new hungarian();
		int candidateCount = 7;
		String[] candidateIDs = { "1","2","3","4","5","6","7" };
		double [][] candidateOptions = {{98,85,47,9,4,48, 23},{11,71,95,3,77,51,56},{32,62,11,86,79,32,82},{30,8,14,74,11,96,20},{57,92,86,22,45,75,66},{60,80,8,6,62,91,95},{12,55,72,3,45,77,9}};
		List<hungarian.Selection> result = H.hungarianAlgorithm( candidateCount, candidateIDs, candidateOptions);
		for(int i=0; i<result.size(); i++){
			System.out.println(result.get(i).ID + " " + result.get(i).jobNum + " " + result.get(i).jobCost );
		}

		int candidateCount2 = 10;
		String []candidateIDs2 = { "1","2","3","4","5","6","7","8","9","10" };
		double [][] candidateOptions2 = {{87,46,17,61,95,76,64,72,89,88},{30,49,43,72,6,8,81,35,11,56},{37,10,84,75,87,78,57,58,65,65},{60,53,49,39,16,55,29,97,69,1},{40,40,34,97,76,60,98,59,55,96},{10,96,65,85,4,44,7,61,27,62},{37,61,97,51,49,80,46,12,25,25},{62,28,94,13,18,70,80,23,58,13},{94,16,50,97,1,41,23,11,17,11},{61,95,80,63,83,61,35,77,13,39}};

		List<hungarian.Selection> result2 = H.hungarianAlgorithm( candidateCount2, candidateIDs2, candidateOptions2);
		for(int i=0; i<result2.size(); i++){
			System.out.println(result2.get(i).ID + " " + result2.get(i).jobNum + " " + result2.get(i).jobCost );
		}


		int candidateCount3 = 3;
		String []candidateIDs3 = {"1","2","3"};
		double [][] candidateOptions3 = {{40,72,72},{85,13,83},{35,39,33}};
		List<hungarian.Selection> result3 = H.hungarianAlgorithm( candidateCount3, candidateIDs3, candidateOptions3);
		for(int i=0; i<result3.size(); i++){
			System.out.println(result3.get(i).ID + " " + result3.get(i).jobNum + " " + result3.get(i).jobCost );
		}


	}
}

