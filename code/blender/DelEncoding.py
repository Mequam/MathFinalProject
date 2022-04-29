#This file contains the data structures used in delauny triangulation
import numpy as np
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
	
	def pointFightDecorator(comparison):
		def most_compared(self):	
			if len(self.points) == 0:
				return None
			most = self.points[0]
			for p in self.points:
				if comparison([0],most):
					left_most = p
		return most_compared
	
	@pointFightDecorator
	def left_most_point(p1,most):
		return p1[0] < most[0]
	@pointFightDecorator
	def right_most_point(p1,most):
		return p1[0] > most[0]
	
	@pointFightDecorator
	def top_most_point(p1,most):
		return p1[1] > most[1]
	
	@pointFightDecorator
	def bottom_most_point(p1,most):
		return p1[1] < most[1]

			
	
class DelTriangulation(Triangulation):
	def __init__(self,points):
		#these are points that we use to ensure we
		#have a poper triangulation to start with
		self.ghostPoints = [np.array([1,0]),
			np.array([0,1]),
			np.array([-1,0])]	

		
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
	
	def remove_triangle_reference(self,t):
		self.remove_triangle(t)
		
		#remove any reference to the triangle
		for tl in self.triangles:
			for j in range(0,3):
				if t == self.triangles[tl][j]:
					self.triangles[tl][j] = None
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
	#clears all data
	def clear_data():
		self.triangles = {}
		self.circles = {}
		self.points = []
	#only clears triangulated data
	def clear_triangulation():
		self.triangles = {}
		self.circles = {}
	#hail mary that resets and re-triangulates the whole mesh
	def triangulate_self(self,points,safty_offset = 256):
		
		self.clear_data()
	
		#specifically copy over a reference of the elements in the gp array
		#not just the array itself	
		for g in self.ghostPoints:
			self.points.append(g)
		
		lm = self.left_most_point()
		rm = self.right_most_point()
		tm = self.top_most_point()
		bm = self.bottom_most_point()
	
		#make the ghost points cover the entire 	
		ghostPoints[0] = (rm[0] + safty_offset ,bm[1] - safty_offset)
		ghostPoints[1] = (lm[0] - safty_offset, bm[1] - safty_offset)
		ghostPoinst[2] = ((rm[0]+lm[0])/2,tm[1] + safty_offset)
	
		self.triangles[(0,1,2)] = [None,None,None]
		self.circles[(0,1,2)] = self.get_circum_circle((0,1,2))
		
		#add all of the points to the mesh
		for point in points:
			self.add_point(point)
		
		#remove the ghost triangle any connections relating to it
		#its circles AND its triangle
		for t in self.triangles:
			for j in range(0,3):
				if t[j] in [0,1,2]:
					#PURGE THE EVIL TRIANGLE *^*
					self.remove_triangle_reference(t)
		
		for i in range(0,len(ghostPoinst)):
			self.points.remove(0)

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
		
		self.points.append(point)
		#evil triangles go to del >:[
		for evilTriangle in badTriangles:
			self.remove_triangle(evilTriangle)

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
			self.circles[new_triangles[i]] = self.get_circum_circle(new_triangles[i])
		print("new triangles")
		for tri in new_triangles:
			print(tri)
			for adj in self.triangles[tri]:
				print('\t',adj)
