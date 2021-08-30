class Intersection{
	public static double[] intersectionCompute( double box1_x, double box1_y, double box1_width, double box1_height, double box2_x, double box2_y, double box2_width, double box2_height){
		double leftX = Math.max(box1_x,box2_x);
		double rightX = Math.min(box1_x+box1_width,box2_x+box2_width);
		double topY = Math.max(box1_y,box2_y);
		double bottomY = Math.min(box1_y+box1_height,box2_y+box2_height);

		if(leftX<rightX && topY < bottomY){
			double[] result = new double[4];
			result[0] = leftX;
			result[1] = topY;
			result[2] = rightX - leftX;
			result[3] = bottomY - topY;
			return result;
		}
		else{
			return null;
		}
	}

	public static double IOU( double box1_x, double box1_y, double box1_width, double box1_height, double box2_x, double box2_y, double box2_width, double box2_height){
		double [] intersection = intersectionCompute( box1_x, box1_y, box1_width, box1_height, box2_x, box2_y, box2_width, box2_height);
		if(intersection == null){
			return 0;
		}

		double intersectionArea = intersection[2]*intersection[3];
		double box1_area = box1_width*box1_height;
		double box2_area = box2_width*box2_height;

		double iou = intersectionArea/(box1_area+box2_area-intersectionArea);
		return iou;
	}
}
