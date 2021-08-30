class Measurement{
	public double x;
	public double y;
	public Matrix position;
	public double percentage;
	public String objectType;
	public double width;
	public double height;
	
	public Measurement(double x, double y, double width, double height, String objectType, double percentage){
		this.x = x;
		this.y = y;
		this.position = Matrix.zero(2,1);
		this.position.set(0,0,x);
		this.position.set(1,0,y);
		this.width = width;
		this.height = height;
		this.objectType = objectType;
		this.percentage = percentage;
	}
}
