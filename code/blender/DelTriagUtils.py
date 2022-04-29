#this file contains utilities for performing Deaulany Triangulation
#on a set of points
import numpy as np

def inCircle(p,circle,give = 0.1):
	(center,radius) = circle
	# print("distance: " + str(np.linalg.norm(center - p) - give ))
	# print("radius: " + str(radius))
	return np.linalg.norm(center - p) - give < radius

#returns the radius and then point 
#of a circumcenter
def circumCenter(pa,pb,pc):
	badn1 = (pb-pa)
	badn2 = (pc-pa)
		
	n1 = np.array([-badn1[1],badn1[0]])
	n2 = np.array([-badn2[1],badn2[0]])

	v1 = ((pa+pb)/2)
	v2 = ((pa+pc)/2)
	
	center = colParam(n1,v1,n2,v2)[0]*n1+v1
	return (center,np.linalg.norm(center - pa))

#returns the point where parametric lines collide
def colPoint(n1,v1,n2,v2):
	(t1,t2) = colParam(n1,v1,n2,v2)
	return n1*t1 + v1

#returns the parametric time of line
#collision between two lines represented 
#in parametric notation
def colParam(n1,v1,n2,v2):
	#we need column vectors to work
	#with numpys linalg systems
	val = (v2-v1).reshape(-1,1)

	col_n1 = n1.reshape(-1,1)
	col_n2 = n2.reshape(-1,1)
	
	# print("\n\ntest print ughghadjdjdjdjdfjdf\n")
	# print(n1, v1, n2, v2)
	# print(col_n1)
	# print("\n\n")
	return np.transpose(
		np.linalg.solve(np.hstack((col_n1,
					-col_n2)),
					val)
		)[0]
