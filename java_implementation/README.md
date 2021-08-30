# SORT Java implementation

## About the code in this directory

This code is a translation of the Python code in this repository. The Python code was developed first as staging ground for developing the Java implementation since the Python has more built in Matrix libraries and initially I had no Java implementation of Kalman Filter (which I coded up later [here](https://github.com/mannyray/KalmanFilter/tree/master/java_implementation)).

This code was tested in an Android Java TensorFlow application (see [here](https://szonov.com/programming/2021/03/28/prototype/)).

### Testing matching with Python code

Testing of code matching between Java and Python implementation was done. In directory `python_implementation/example`, run 

```
python example7.py
python example1.py
```

which generates

```	
python_implementation/example/output_text/example1_actual_tracked.txt
python_implementation/example/output_text/example1_measurements.txt
python_implementation/example/output_text/example7_actual_tracked.txt
python_implementation/example/output_text/example7_measurements.txt
```

where `_actual_tracked.txt` is the computation of the tracker based on the measurements in `_measurements.txt`.

`cd` into `java_implementation/` and run `test.java` by

```
javac *.java
java test
```

## How to get started with the code

### 1. Import the Code

First import the code. You need to have all the java files in this directory in your project folder (except `test.java`).

### 2. Define the tracker object

```java
Matrix sensorNoise = Matrix.identity(2,2);
Matrix processNoise = Matrix.identity(4,4);
Function f = (Function) null;//by specifying null, you will use default function
double minimumIOU = 0.001;
double newShapeWeight = 0.1;
double threshold = 4;
Matrix initialVelocity = Matrix.zero(2,1);
Matrix initialCovariance = Matrix.identity(4,4);

Sort tracker = new Sort(sensorNoise,processNoise,f,minimumIOU,newShapeWeight,threshold,initialVelocity,initialCovariance);
```

### 3. Process measurements

```java
double x = //
double y = //
double width = //
double height = //
Measurement m = new Measurement(x,y,width,height,"",0);
```


Put all of your measurements into an array:

```
ArrayList<Measurement> measurements_arr  = new ArrayList<Measurement>();
...
measurements_arr.add(m);
```

### 4. Run predict/update phase


```java
while(true){//keep running for all frames
        new_frame = //extract a frame from video feed
        detect_objects = machine_learning_object_detecting_model(new_frame)
        measurements_arr = //convert the output format of detect_objects to an array of measurements objects as discussed in previous point
        double time = //current time

        tracker.predictPhase(time)
        tracker.updatePhase(measurements_arr,time)
}
```

### 5. Analyse the tracked objects

```
TrackedObject[] results = s.getTracked();
```

where each `TrackedObject` has properties:

```
position
width
height
velocity
name
objectType
```

