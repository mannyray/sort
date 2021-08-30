# SORT Python implementation

## About the code in this directory

This directory contains the Python implementation of the Simple Online Realtime Tracking (SORT) algorithm.

The algorithm was tested in the `example` directory for performance and accuracy.

The SORT algorithm consitsts of a few key components
 - Kalman Filter
 - Hungarian algorithm 
 - Ford Fulkerson  

The KalmanFilter is sourced from [here](https://github.com/mannyray/kalmanfilter) while Ford Fulkerson and Hungarian algorithm were developed based on wikipedia articles and tested in `testing` directory for accuracy.

In the `example` directory, the README provides a good introduction on uses cases, limitations and simulations of the algorithm.

## How to get started with the code


### 1. Import the code 

First import the code:

```
import sort
```

### 2. Define the tracker object

Next define the tracker object. There are many ways of doing this:


If you want to get started quick then run:

```
tracker = sort.tracker()
```

A lot of the algorithm's parameters are set by default in the object's contructor (as seen in `sort.py`):

```python
def __init__(self,sensorNoise=np.array([[1,0],[0,1]]),processNoise=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]),predictFunction=None,predictFunctionJacobian=None,minimumIOU=0.001,newShapeWeight=1.0/10.0,threshold=4,initialVelocity=np.array([[0,0]]).transpose(),initialCovariance=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])):
```

You can specify all of the parmaters or some of them like:

```python
tracker = sort.tracker(sensorNoise=np.array([[2,0],[0,2]]))
```

Alternatively, you can set certain parameters via method:

```python
tracker = sort.tracker()
tracker.set_sensorNoise(np.array([[2,0],[0,2]]))
```

Let us review the parameters:

 - `sensorNoise` is a Kalman Filter paramater and should be a two by two matrix since we are tracking objects in a two dimensional plane (x and y coordinates).  The higher the `sensorNoise` then the more noisy we assume our measurements (less accurately represent the true location of object being detected).
 - `processNoise` is a Kalman Filter paramter and should be a four by four matrix where first two rows/columns are for position x,y and last two row/matrices are for the velocities of x,y. The higher the `processNoise` then the more noisy we assume our model of motion is.
 - `predictFunction` is a Kalman Filter parameter that describes the expected motion of our objects being tracked. The default model is good for many cases and just assumes that the estimate's position is updated based on current velocity and velocity stays static.
 - `predictFunctionJacobian` is a Kalman Filter parameter that is the Jacobian of `predictFunction`
 - `minimumIOU` - is a SORT parameter and determines the minimum Intersection over Union value for an detected object to be considered new. Float between 0 and 1.
 - `newShapeWeight` - is a SORT parameter float between 0 and 1 to describe how quickly the estimate adjusts to changes in width/height of bounding box of a tracked object.
 - `threshold` - is a SORT parameter and describes how long we keep tracking an object without new updating measurements. A positive float.
 - `initialVelocity` is a Kalman Filter parmater and describes the initial assumed velocity for a new object. A two by one matrix.
 - `initialCovariance` is a Kalman Filter parameter and describes the initial covariance. It is a measurement of uncertainty of a tracked object's position and velocity. Like `processNoise`, the first two rows/columns are for x,y position and last two row/columns are for velocity. A four by four matrix.


For exploring these parameters in detail please see the `example` directory.

### 3. Process measurements

Your object detecting code will for every frame output an array of boxes. Each box bounds a detected object in the frame. Each box has an x,y coordinate and a width and height. For each of these boxes you will need to convert this to an object compatabile with the tracker code:

```
x = #x coordinate of top left coordinate of detection box
y = #y coordinate of top left coordinate of detection box
width = #width of detection box
height = #height of detection box
measurement = sort.measurement(x,y,width,height)
```

Put all of your measurements into an array:

```
measurement_arr = []
....
measurement_arr.append(measurement)
```

### 4. Run predict/update phase


For those familiar, the Kalman filter has two phases which are repeated over and over as incoming measurements come in. The `updatePhase` is responsible for combining new measurements into the tracked objects while the `predictPhase` is responsible for updating the tracked objects based on elapsed time and assumed model of motion. 


```python
while(true):#keep running for all frames
	new_frame = #extract a frame from video feed
	detect_objects = machine_learning_object_detecting_model(new_frame)
	measurements_arr = #convert the output format of detect_objects to an array of measurements objects as discussed in previous point
	time = #current time

	tracker.predictPhase(time)
	tracker.updatePhase(measurements_arr,time)
```


### 5. Analyse the tracked objects


You will want to draw your tracked objects or log their locations. To retrieve the locations:

```
results = tracker.getTracked()
```

where the `results` is an array of `sort.trackedObject` with main properties:

```
position
velocity
name
objectType
width
height
```

With `name` being the tracked object ID, position is x,y of top left corner.

