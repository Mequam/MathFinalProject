import numpy as np
import DelTriagUtils as du

if __name__ == '__main__':
	n1 = np.array([0,-1])
	v1 = np.array([0,20])
	
	n2 = np.array([-1,1])
	v2 = np.array([100,0])
	
	print(du.colParam(n1,v1
			,n2,v2))


	n1 = np.array([0,1])
	n2 = np.array([1,1])
	n3 = np.array([5,10])
	
	print(du.circumCenter(n1,n2,n3))
