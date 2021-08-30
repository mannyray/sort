import java.io.File;  // Import the File class
import java.util.ArrayList;
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files

public class test{
        public static void main(String[] args) {
		ArrayList<Measurement[]> totalArr = new ArrayList<Measurement[]>();
		try{
			File myObj = new File("testing/example1_measurements.txt");
			Scanner myReader = new Scanner(myObj);
			ArrayList<Measurement> arr = new ArrayList<Measurement>();
			boolean firstTime = true;
			while(myReader.hasNextLine()){
				String data = myReader.nextLine();
				String[] strings = data.split(" ");
				if(strings[0].equals("frame")){
					if(firstTime){
						firstTime = false;
					}else{
						Measurement[] tmp = new Measurement[arr.size()];			
						for(int i=0; i<arr.size(); i++){
							tmp[i] = arr.get(i);
						}
						totalArr.add(tmp);
					}
					arr = new ArrayList<Measurement>();
				}
				else{
					Measurement m = new Measurement(Double.valueOf(strings[1]),Double.valueOf(strings[2]),Double.valueOf(strings[3]),Double.valueOf(strings[4]),strings[5],0);
					arr.add(m);
				}
			}
			myReader.close();
		} catch(FileNotFoundException e){
			System.out.println("An error occurred.");
			e.printStackTrace();
		}


		ArrayList<Measurement[]> totalArrTracked = new ArrayList<Measurement[]>();
		ArrayList<ArrayList<String>> totalArrTrackedID = new ArrayList<ArrayList<String>>();
		try{
			File myObj = new File("testing/example1_actual_tracked.txt");
			Scanner myReader = new Scanner(myObj);
			ArrayList<Measurement> arr = new ArrayList<Measurement>();
			ArrayList<String> arr_str = new ArrayList<String>();
			boolean firstTime = true;
			while(myReader.hasNextLine()){
				String data = myReader.nextLine();
				String[] strings = data.split(" ");
				if(strings[0].equals("frame")){
					if(firstTime){
						firstTime = false;
					}else{
						Measurement[] tmp = new Measurement[arr.size()];
						for(int i=0; i<arr.size(); i++){
							tmp[i] = arr.get(i);
						}
						totalArrTracked.add(tmp);
						totalArrTrackedID.add(arr_str);
					}
					arr = new ArrayList<Measurement>();
					arr_str = new ArrayList<String>();
				}
				else{
					Measurement m = new Measurement(Double.valueOf(strings[1]),Double.valueOf(strings[2]),Double.valueOf(strings[3]),Double.valueOf(strings[4]),strings[5],0);
					arr.add(m);
					arr_str.add(strings[6]);
				}
			}
			myReader.close();
		} catch(FileNotFoundException e){
			System.out.println("An error occurred.");
			e.printStackTrace();
		}

		
		Matrix sensorNoise = Matrix.identity(2,2);
		Matrix processNoise = Matrix.identity(4,4);
		Function f = (Function) null;
		double minimumIOU = 0.001;
		double newShapeWeight = 0.1;
		double threshold = 4;
		Matrix initialVelocity = Matrix.zero(2,1);
		Matrix initialCovariance = Matrix.identity(4,4);

		Sort s = new Sort(sensorNoise,processNoise,f,minimumIOU,newShapeWeight,threshold,initialVelocity,initialCovariance);
		for(int frame=0; frame<totalArr.size(); frame++){
			s.predictPhase(frame);
			s.updatePhase(totalArr.get(frame),(double)frame);
			TrackedObject[] tmp = s.getTracked();
			for(int i=0; i<tmp.length; i++){
				boolean match = false;
				for(int j=0; j <totalArrTrackedID.get(frame).size(); j++){
					if(tmp[i].name.equals(totalArrTrackedID.get(frame).get(j))){
						match = true;
						if (Math.abs(tmp[i].position.get(0,0) - totalArrTracked.get(frame)[j].position.get(0,0)) > 0.01){
							System.out.println("Difference too big");
							System.out.println(Math.abs(tmp[i].position.get(0,0) - totalArrTracked.get(frame)[j].position.get(0,0)));
						}
						if(Math.abs(tmp[i].position.get(1,0) - totalArrTracked.get(frame)[j].position.get(1,0)) > 0.01){
							System.out.println("Difference too big");
						}
					}
				}
				if(!match){
					System.out.println("No match");
				}
			}
		}
	}
}
