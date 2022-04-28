#this file contains utilities for performing Deaulany Triangulation
#on a set of points

import numpy as np

#returns the radius and then point 
#of a circumcenter
def circumCenter(pa,pb,pc):
	v3 = ((pa+pb)/2)
	v2 = ((pa+pc)/2)
	vmat = np.hstack((v3,v2))
	print(vmat)

#returns the parametric time of line
#collision between two lines represented 
#in parametric notation
def colParam(n1,v1,n2,v2):
	#we need column vectors to work
	#with numpys linalg systems
	val = (v2-v1).reshape(-1,1)

	col_n1 = n1.reshape(-1,1)
	col_n2 = n2.reshape(-1,1)
	
	return np.transpose(
		np.linalg.solve(np.hstack((col_n1,
					-col_n2)),
					val)
		)[0]
