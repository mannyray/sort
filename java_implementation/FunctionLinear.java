public class FunctionLinear extends Function{

	Matrix A;

	public FunctionLinear(){
	}

        public Matrix next( Matrix x, double time){
		Matrix position = x.getSubmatrix(0,0,2,1);
		Matrix velocity = x.getSubmatrix(2,0,2,1);
		Matrix position_next = Matrix.plus(position,velocity);
		Matrix velocity_next = new Matrix(velocity);
		Matrix result = new Matrix(4,1);
		result.setSubmatrix(0,0,2,1,position_next);
		result.setSubmatrix(2,0,2,1,velocity_next);
		return result;
        }

        public Matrix jacobian(Matrix x, double time){
		Matrix result = new Matrix(4,4);
		result.set(0,0,1);
		result.set(0,2,1);
		result.set(1,1,1);
		result.set(1,3,1);
		result.set(2,2,1);
		result.set(3,3,1);
                return result;
        }
}
