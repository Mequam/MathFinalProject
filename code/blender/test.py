import numpy as np
import DelTriagUtils as du
import DelEncoding as de

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

	testPointSet = [np.array([0,1]),
			np.array([-0.8660253882,-0.5]),
			np.array([0.8660253882,-0.5]),
			np.array([-0.43301269,0.25]),
			np.array([0,-0.5]),
			np.array([0.43301269,0.25])]
	delTriag = de.DelTriangulation([p*1 for p in testPointSet])
	print("circumcircle")
	print(delTriag.get_circum_circle((0,1,2)))	
	print('- '*10)

	left = (1,4,3)
	top = (0,3,5)
	right = (2,4,5)
	center = (5,3,4) #bottom of the triforce
	
	delTriag.add_triangle(top,[center,None,None])
	delTriag.add_triangle(right,[center,None,None])
	delTriag.add_triangle(left,[center,None,None])
	delTriag.add_triangle(center,[left,right,top])
	
	print("boundry")
	print("center")
	print(delTriag.get_boundry([center]))
	print("right")
	print(delTriag.get_boundry([right]))
	print("left")
	print(delTriag.get_boundry([left]))
	print("top")
	print(delTriag.get_boundry([top]))
	
	print('- ' * 10)
	print("testing add point")
	
	delTriag.add_point(np.array([0,0]))
