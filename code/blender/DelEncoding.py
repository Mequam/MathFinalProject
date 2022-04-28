#This file contains the data structures used in delauny triangulation
import DelTriagUtils as du

class Triangulation:
	def __init__(self,points):
		self.points = points	
		#array of tuples
		#where each element in the
		#tuple corispoinds to 
		#a point idx
		self.triangles = {}
	#adds a new point to the triangulation
	def add_point(self,point):
		pass
class DelTriangulation(Triangulation):
	def __init__(self,points):
		#an array of circomcircles
		#takes a triangle (tuple
		# of point idx) and returns
		# the stored circomcircle
		self.circles = {}	
		super().__init__(points)
	
	#convinience function to get the circum center
	#of our triangles
	def get_circum_circle(self,t):
		(p1,p2,p3) = t
		return du.circumCenter(self.points[p1],
			self.points[p2],
			self.points[p3])
	
	#adds a single triangle to the mesh, no questions asked
	#DOES NOT MAINTAIN DELAUNAY NICENECSS >:[
	def add_triangle(self,t,adjacent_triangles):
		self.triangles[t] = adjacent_triangles
		self.circles[t] = self.get_circum_circle(t)
	
	#deletes a triangle from the mesh
	def remove_triangle(self,t):
		del self.triangles[t]
		del self.circles[t]
			
	#takes a subset of CONNECTED triangles
	def get_boundry(self,innerTriangles):
		ret_val = []
		focusTriangle = innerTriangles[0]
		focusEdge = 0	
		while True:	
			adjacentTriangle = self.triangles[focusTriangle][focusEdge]
			#we have found a triangle outside of the given set
			#store the border edge and triangle
			if adjacentTriangle and adjacentTriangle in innerTriangles:
				focusEdge = (self.triangles[
						adjacentTriangle].index(
							focusTriangle) + 1) % 3
				focusTriangle = adjacentTriangle	
			else:
				ret_val.append([focusTriangle[(focusEdge - 1) % 3],
						focusTriangle[(focusEdge + 1) % 3],
						adjacentTriangle])
				
				focusEdge = (focusEdge + 1) % 3
			
				if ret_val[0][1] == ret_val[-1][0]:
					break
		return ret_val
	#returns true if the point is in the given circle
	def in_circle(self,point,t):
		return du.inCircle(point,self.get_circum_circle(t))

	#adds a point to an existing delany triangulation
	#while maintaining the current configuration
	def add_point(self,point):	
		badTriangles = []	
		for t in self.triangles:
			if self.in_circle(point,t):
				badTriangles.append(t)
		badBoundry = self.get_boundry(badTriangles)
		
		newTriangles = []
		
		#the number of points we have is the new index for
		#the target point
		idx = len(self.points)
		
		new_triangles = []
		for (edge_point0,edge_point1,boundryTriangle) in badBoundry:
			
			focusTriangle = (idx,edge_point0,edge_point1)	
			
			new_triangles.append(focusTriangle)
			
			print(edge_point0,edge_point1,boundryTriangle)	
			
			self.triangles[focusTriangle] = [boundryTriangle,None,None]
		
			if boundryTriangle:	
				boundryBorder = self.triangles[boundryTriangle]
				
				for i in range(0,len(boundryBorder)):
					if boundryBorder[i] and edge_point1 in boundryBorder[i] and edge_point0 in boundryBorder[i]:
						boundryBorder[i] = focusTriangle
				
		new_tri_len = len(new_triangles)
		
		#link the new triangles together
		for i in range(0,new_tri_len):
			self.triangles[new_triangles[i]][1] = new_triangles[(i - 1) % new_tri_len]
			self.triangles[new_triangles[i]][2] = new_triangles[(i + 1) % new_tri_len]
