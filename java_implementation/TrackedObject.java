class TrackedObject{
	public Matrix position;
	public Matrix velocity;
	public Matrix velocity_covariance;
	public Matrix velocity_covariance_sqrt;
	public double last_update;
	public String name;
	public String objectType;
	public double last_predict;
	public double width;
	public double height;

	public TrackedObject(Matrix position, double width, double height, Matrix velocity, Matrix velocity_covariance, double time, String name, String objectType){
		this.position = new Matrix(position);
		this.width = width;
		this.height = height;
		this.velocity = new Matrix(velocity);
		this.velocity_covariance = new Matrix(velocity_covariance);
		this.velocity_covariance_sqrt = new Matrix(velocity_covariance);
		this.last_update = time;
		this.last_predict = time;
		this.name = name;
		this.objectType = objectType;
	}
}
