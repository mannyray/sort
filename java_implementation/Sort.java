import java.util.ArrayList;
import java.util.*; 
import java.util.Collections;

class Sort{
	Map<String,ArrayList<TrackedObject>> trackedObjectsByType;
	Matrix processNoise;
	Matrix sensorNoise;
	Matrix processNoiseSqrt;
	Matrix sensorNoiseSqrt;
	Matrix measurementMatrix;
	double minimum_IOU;
	double threshold;
	int totalCandidateCount;
	double newShapeWeight;
	Function predictFunction;
	Function predictFunctionDefault = new FunctionLinear();
	Matrix initialCovariance;
	Matrix initialVelocity;

	public Sort(Matrix sensorNoise, Matrix processNoise, Function f, double minimumIOU, double newShapeWeight, double threshold, Matrix initialVelocity, Matrix initialCovariance){
		this.trackedObjectsByType = new HashMap<String,ArrayList<TrackedObject> >();
		this.processNoise = new Matrix(processNoise);
		this.sensorNoise = new Matrix(sensorNoise);
		this.processNoiseSqrt = new Matrix(processNoise);
		this.sensorNoiseSqrt = new Matrix(sensorNoise);
		this.measurementMatrix = Matrix.zero(2,4);
		this.measurementMatrix.set(0,0,1);
		this.measurementMatrix.set(1,1,1);
		this.minimum_IOU = minimumIOU;
		this.threshold = threshold;
		this.totalCandidateCount = 0;
		this.newShapeWeight = newShapeWeight;

		if(f==null){
			this.predictFunction = this.predictFunctionDefault;
		}
		else{
			this.predictFunction =  f;
		}

		this.initialCovariance = new Matrix(initialCovariance);
		this.initialVelocity = new Matrix(initialVelocity);
	}

	public void set_minimumIOU(double IOU){
		this.minimum_IOU = IOU;
	}

	public void set_threshold(double threshold){
		this.threshold = threshold;
	}

	public void set_sensorNoise(Matrix sensorNoise){
		this.sensorNoise = new Matrix(sensorNoise);
		this.sensorNoiseSqrt = new Matrix(sensorNoise);
	}

	public Matrix get_sensorNoise(){
		return new Matrix(this.sensorNoise);
	}

	public void set_processNoise(Matrix processNoise){
		this.processNoise = new Matrix(processNoise);
		this.processNoiseSqrt = new Matrix(processNoise);
	}

	public Matrix get_processNoise(){
		return new Matrix(this.processNoise);
	}

	public void set_predictFunction(Function f){
		this.predictFunction = f;
	}

	public void set_newShapeWeight(double weight){
		this.newShapeWeight = weight;
	}


	public TrackedObject[] getTracked(){
		int totalCount = 0;
		Iterator <String> it = trackedObjectsByType.keySet().iterator();	
		while(it.hasNext()){
			String key = it.next();
			totalCount += trackedObjectsByType.get(key).size();

		}
		TrackedObject[] result = new TrackedObject[totalCount];

		it = trackedObjectsByType.keySet().iterator();	
		int counter = 0;
		while(it.hasNext()){
			String key = it.next();
			for(int i=0; i<this.trackedObjectsByType.get(key).size(); i++){
				result[counter++] = this.trackedObjectsByType.get(key).get(i);
			}
		}
		return result;
	}


	public void predictPhase(double time){
		Iterator <String> it = trackedObjectsByType.keySet().iterator();	
		while(it.hasNext()){
			String key = it.next();
			for(int i=0; i<trackedObjectsByType.get(key).size(); i++){
				
				double time_since_last_predict = time - trackedObjectsByType.get(key).get(i).last_predict;

				if(time_since_last_predict > 0){
					Matrix state = new Matrix(4,1); 
					state.set(0,0,trackedObjectsByType.get(key).get(i).position.get(0,0));
					state.set(1,0,trackedObjectsByType.get(key).get(i).position.get(1,0));
					state.set(2,0,trackedObjectsByType.get(key).get(i).velocity.get(0,0)*time_since_last_predict);
					state.set(3,0,trackedObjectsByType.get(key).get(i).velocity.get(1,0)*time_since_last_predict);

					Matrix[] results = KalmanFilter.predictPhase( this.predictFunction, time, this.trackedObjectsByType.get(key).get(i).velocity_covariance_sqrt, state, this.processNoiseSqrt );

					Matrix estimate = results[0];
					Matrix covariance_sqrt = results[1];



					this.trackedObjectsByType.get(key).get(i).velocity = Matrix.scalarMultiply(1.0/(time_since_last_predict),estimate.getSubmatrix(2,0,2,1));
					this.trackedObjectsByType.get(key).get(i).velocity_covariance_sqrt = covariance_sqrt;
					this.trackedObjectsByType.get(key).get(i).position = estimate.getSubmatrix(0,0,2,1);
					this.trackedObjectsByType.get(key).get(i).last_predict = time;
				}
			}
		}
	}

	public void updatePhase( Measurement[] measurements, double time ){
		Map<String,ArrayList<Measurement>> measurementsByType = new HashMap<String,ArrayList<Measurement>>();
		for(int i=0; i<measurements.length; i++){
			if(!measurementsByType.containsKey( measurements[i].objectType )){
				measurementsByType.put(measurements[i].objectType, new ArrayList<Measurement>());
			}
			measurementsByType.get(measurements[i].objectType).add(measurements[i]);
		}

		Iterator <String>it = measurementsByType.keySet().iterator();	
		while(it.hasNext()){
			String key = it.next();
			if(!this.trackedObjectsByType.containsKey(key)){
				this.trackedObjectsByType.put(key, new ArrayList<TrackedObject>());
			}
			this.updatePhaseByObject(measurementsByType.get(key),time,key);
		}

		//find objects that are too old
		it = this.trackedObjectsByType.keySet().iterator();	
		while(it.hasNext()){
			String key = it.next();
			ArrayList<Integer> indexToPop = new ArrayList<Integer>();
			for(int i=0; i<this.trackedObjectsByType.get(key).size(); i++){
				if(this.threshold < (time-this.trackedObjectsByType.get(key).get(i).last_update)){
					indexToPop.add(i);
				}
			}
			Collections.sort(indexToPop);
			int deletedSoFar = 0;
			for(int i=0; i<indexToPop.size(); i++){
				this.trackedObjectsByType.get(key).remove(indexToPop.get(i)-deletedSoFar);
				deletedSoFar++;
			}
		}
	}

	public void updatePhaseByObject(ArrayList<Measurement> measurements, double time, String key){
		//identify new objects
		for(int i=0; i<measurements.size(); i++){
			if(this.trackedObjectsByType.get(key).size() == 0){
				this.totalCandidateCount = this.totalCandidateCount + 1;
				this.trackedObjectsByType.get(key).add(new TrackedObject(measurements.get(i).position,measurements.get(i).width,measurements.get(i).height,this.initialVelocity,this.initialCovariance,time,"id-"+this.totalCandidateCount,measurements.get(i).objectType));
				continue;
			}
			ArrayList<Double> IOUTrackedObjectsToMeasurement = new ArrayList<Double>();
			double maxIOU = 0;
			for( int k=0; k<this.trackedObjectsByType.get(key).size(); k++){
				double iou = Intersection.IOU(measurements.get(i).x,measurements.get(i).y,measurements.get(i).width,measurements.get(i).height,
					this.trackedObjectsByType.get(key).get(k).position.get(0,0),this.trackedObjectsByType.get(key).get(k).position.get(1,0),
					this.trackedObjectsByType.get(key).get(k).width,this.trackedObjectsByType.get(key).get(k).height);
				IOUTrackedObjectsToMeasurement.add(iou);
				maxIOU = Math.max(maxIOU,iou);
			}
			if(maxIOU < this.minimum_IOU){
				this.totalCandidateCount = this.totalCandidateCount + 1;
				this.trackedObjectsByType.get(key).add(new TrackedObject(measurements.get(i).position,measurements.get(i).width,measurements.get(i).height,this.initialVelocity,this.initialCovariance,time,"id-"+this.totalCandidateCount,measurements.get(i).objectType));
			}
		}

		double local_minimum_IOU = this.minimum_IOU;
		while(true){
			if(local_minimum_IOU > 1){
				break;
			}
			if( measurements.size() > this.trackedObjectsByType.get(key).size()){
				local_minimum_IOU += 0.1;
				for(int i=0; i<measurements.size(); i++){
					ArrayList<Double> IOUTrackedObjectsToMeasurement = new ArrayList<Double>();
					double maxIOU = 0;
					for(int k=0; k<this.trackedObjectsByType.get(key).size(); k++){
						double iou = Intersection.IOU(measurements.get(i).x,measurements.get(i).y,measurements.get(i).width,measurements.get(i).height,
							this.trackedObjectsByType.get(key).get(k).position.get(0,0),this.trackedObjectsByType.get(key).get(k).position.get(1,0),
							this.trackedObjectsByType.get(key).get(k).width,this.trackedObjectsByType.get(key).get(k).height);
						IOUTrackedObjectsToMeasurement.add(iou);
						maxIOU =Math.max(maxIOU,iou);
					}
					if(maxIOU < this.minimum_IOU){
						this.totalCandidateCount = this.totalCandidateCount + 1;
						this.trackedObjectsByType.get(key).add(new TrackedObject(measurements.get(i).position,measurements.get(i).width,measurements.get(i).height,this.initialVelocity,this.initialCovariance,time,"id-"+this.totalCandidateCount,measurements.get(i).objectType));
					}
				}
			}
			else{
				break;
			}
		}

		int localCandidateCount = this.trackedObjectsByType.get(key).size();
		ArrayList<String> candidateIDs = new ArrayList<String>();

		for(int k=0; k<this.trackedObjectsByType.get(key).size(); k++){
			candidateIDs.add(this.trackedObjectsByType.get(key).get(k).name); 
		}

		ArrayList<ArrayList<Double>> candidateOptions = new ArrayList<ArrayList<Double>>();
		double maxCandidate = 0;
		for(int k=0; k<this.trackedObjectsByType.get(key).size(); k++){
			ArrayList<Double> optionsForKthObject = new ArrayList<Double>();
			for(int i=0; i<measurements.size(); i++){
				double iou = Intersection.IOU(measurements.get(i).x,measurements.get(i).y,measurements.get(i).width,measurements.get(i).height,
					this.trackedObjectsByType.get(key).get(k).position.get(0,0),this.trackedObjectsByType.get(key).get(k).position.get(1,0),
					this.trackedObjectsByType.get(key).get(k).width,this.trackedObjectsByType.get(key).get(k).height);
				optionsForKthObject.add(iou);
				maxCandidate = Math.max(maxCandidate,iou);
			}
			candidateOptions.add(optionsForKthObject);
		}

		int dummyCount = 0;
		if(measurements.size() > this.trackedObjectsByType.get(key).size()){
			dummyCount = measurements.size() - this.trackedObjectsByType.get(key).size();
			for(int i=0; i<dummyCount; i++){
				ArrayList<Double> optionsForDummyObject = new ArrayList<Double>();
				for(int k=0; k<measurements.size(); k++){
					optionsForDummyObject.add(0.0);
				}
				candidateOptions.add(optionsForDummyObject);
				candidateIDs.add("dummy"+i);
			}
		}
		
		localCandidateCount += dummyCount;

		
		for(int k=0; k<this.trackedObjectsByType.get(key).size(); k++){
			for(int i=0; i<measurements.size(); i++){
				candidateOptions.get(k).set(i,maxCandidate - candidateOptions.get(k).get(i));
			}
		}


		int extraCount = 0;
		if(localCandidateCount > measurements.size()){
			extraCount = localCandidateCount - measurements.size();
			for(int row=0; row<localCandidateCount; row++){
				for(int i=0; i<extraCount; i++){
					candidateOptions.get(row).add(maxCandidate+1);
				}
			}
		}

		double [][] options = new double[localCandidateCount][localCandidateCount];
		String [] IDs = new String[localCandidateCount];
		for(int i=0; i<localCandidateCount; i++){
			for(int j=0; j<localCandidateCount; j++){
				options[i][j] = candidateOptions.get(i).get(j);
			}
			IDs[i] = candidateIDs.get(i);
		}

		hungarian solver = new hungarian();
		List<hungarian.Selection> selection = solver.hungarianAlgorithm(localCandidateCount,IDs,options);
		if(selection == null){
			return;
		}

		for(int i=0; i<selection.size()-dummyCount;i++){
			if(selection.get(i).jobNum >= measurements.size()){
				continue;
			}


			Matrix state = Matrix.zero(4,1);
			state.setSubmatrix(0,0,2,1,this.trackedObjectsByType.get(key).get(i).position);
			state.setSubmatrix(2,0,2,1,this.trackedObjectsByType.get(key).get(i).velocity);
			Matrix measurement = new Matrix(measurements.get(selection.get(i).jobNum).position);

			Matrix [] result = KalmanFilter.updatePhase( this.sensorNoiseSqrt, this.trackedObjectsByType.get(key).get(i).velocity_covariance_sqrt,
				this.measurementMatrix,state,measurement);

			Matrix estimate = new Matrix(result[0]);
			Matrix covariance_sqrt = new Matrix(result[1]);

			this.trackedObjectsByType.get(key).get(i).position = estimate.getSubmatrix(0,0,2,1);
			this.trackedObjectsByType.get(key).get(i).velocity = estimate.getSubmatrix(2,0,2,1);
			this.trackedObjectsByType.get(key).get(i).velocity_covariance_sqrt = new Matrix(covariance_sqrt);

			this.trackedObjectsByType.get(key).get(i).width = (this.trackedObjectsByType.get(key).get(i).width)*(1.0-this.newShapeWeight) + (measurements.get(selection.get(i).jobNum).width*this.newShapeWeight);
			this.trackedObjectsByType.get(key).get(i).height = (this.trackedObjectsByType.get(key).get(i).height)*(1.0-this.newShapeWeight) + (measurements.get(selection.get(i).jobNum).height*this.newShapeWeight);
			this.trackedObjectsByType.get(key).get(i).last_update = time;
			this.trackedObjectsByType.get(key).get(i).last_predict = time;
		}
	}
}
