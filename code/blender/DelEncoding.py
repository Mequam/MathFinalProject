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
		def most_compared(self,points):	
			if len(points) == 0:
				return None
			most = points[0]
			for p in points:
				if comparison(p,most):
					most = p
			return most
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

	def get_bounding_box(self,points,box_margin=0):
		top = self.top_most_point(points)
		left = self.left_most_point(points)
		right = self.right_most_point(points)
		bottom = self.bottom_most_point(points)
	
		#top left
		#bottom left
		#top right
		#bottom right
		return [np.array([left[0]-box_margin,top[1]+box_margin]),
			np.array([left[0]-box_margin,bottom[0]-box_margin]),	
			np.array([right[0]+box_margin,top[0]+box_margin]),
			np.array([right[0]+box_margin,bottom[0]-box_margin])]
	
	def get_bounding_triangle(self,points,box_margin=10,height=10):
		box = self.get_bounding_box(points,box_margin)
	
		#draw a point above the triangle from the bounding box
		triangle_top = (box[0]+box[2])/2
		triangle_top[1] += height
	
		#the center of the triangle from the bounding box	
		triangle_bottom_center = (box[1]+box[3])/2
		triangle_bottom_center[1] -= height

		#aim at the points of the top of the bounding box
		top_aim_left = box[0]-triangle_top
		top_aim_right = box[2]-triangle_top
	
		#check collision with the bottom line of the triangle	
		triangle_left = du.colPoint(top_aim_left,triangle_top,
						np.array([-1,0]),triangle_bottom_center)
		triangle_right = du.colPoint(top_aim_right,triangle_top,
						np.array([1,0]),triangle_bottom_center)
		
		return (triangle_top,triangle_left,triangle_right)
		
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
		# # # print("circum center triangulation")
		(p1,p2,p3) = t
		# # # print(self.points[p1],self.points[p2],self.points[p3])
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
		# # # print(self.triangles)
		if t in self.triangles.keys():
			del self.triangles[t]
		if t in self.circles.keys():
			del self.circles[t]
	
	def remove_triangle_reference(self,t):
		#remove any reference to the triangle
		for tl in self.triangles:
			for j in range(0,3):
				if t == self.triangles[tl][j]:
					self.triangles[tl][j] = None
		
	#takes a subset of CONNECTED triangles
	def get_boundry(self,innerTriangles):
		print('entering boundry code')

		if len(innerTriangles) == 0:
			return []
	
		ret_val = []	
		focusTriangle = innerTriangles[0]
		
		focusEdge = 0
		
		while True:
			print(ret_val)
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
			
				if len(ret_val) >= 3 and ((ret_val[0][1] == ret_val[-1][0] and ret_val[0][0] == ret_val[-1][1]) or (ret_val[0][0] == ret_val[-1][0] and ret_val[0][1] == ret_val[-1][1])):
					break
			#input('(ENTER)> ')
		print('leaving boundry')
		return ret_val
	#returns true if the point is in the given circle
	def in_circle(self,point,t):
		return du.inCircle(point,self.get_circum_circle(t))
	#clears all data
	def clear_data(self):
		self.triangles = {}
		self.circles = {}
		self.points = []
	#only clears triangulated data
	def clear_triangulation(self):
		self.triangles = {}
		self.circles = {}
	#hail mary that resets and re-triangulates the whole mesh
	def triangulate_self(self,points,safty_offset = 10):
		
		# # # print("using points " + str(points))
		self.clear_data()
		# # # print(self.points)
		# # print(self.triangles)
		# # print(self.circles)

		
		boundingTriangle = self.get_bounding_triangle(points,safty_offset)
		#make the ghost points cover the entire 	
		
		self.ghostPoints[0] = boundingTriangle[0]
		self.ghostPoints[1] = boundingTriangle[1]
		self.ghostPoints[2] = boundingTriangle[2]
		
		print('displaying ghost points')
		print('- '*10)
		for g in self.ghostPoints:
			print(g)
		print('- '*10)

		#specifically copy over a reference of the elements in the gp array
		#not just the array itself	
		for g in self.ghostPoints:
			self.points.append(g)
		
		# # print("points ")
		for i in self.points:
			print(i)

		self.add_triangle((0,1,2),[None,None,None])
		
		# # print("adding a point")
		
		#add all of the points to the mesh
		for point in points:
			self.add_point(point)
		
		#remove the ghost triangle any connections relating to it
		#its circles AND its triangle
		arr_ref = []
		for t in self.triangles:
			for j in range(0,3):
				if t[j] in [0,1,2]:
					##PURGE THE EVIL TRIANGLE *^*
					arr_ref.append(t)
					self.remove_triangle_reference(t)
		for t in arr_ref:
			self.remove_triangle(t)
		#
		for i in range(0,len(self.ghostPoints)):
			self.points.pop(0)
		
		dict_ref = {}
		for (a,b,c) in self.triangles:
			## print("tuple:", (a,b,c))
			# print("reindexed tuple:", (a-3,b-3,c-3))
			# print("i:", [((i,i,i) if i else None) for i in self.triangles[(a,b,c)]])
			# print("self tris:", self.triangles[(a,b,c)])
			dict_ref[(a-3,b-3,c-3)] = [((i[0]-3,i[1]-3,i[2]-3) if i else None) for i in self.triangles[(a,b,c)]]
		self.triangles = dict_ref
	#adds a point to an existing delany triangulation
	#while maintaining the current configuration
	def add_point(self,point):
		# print("ADDING POINT ", point)
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
			
			# # print(edge_point0,edge_point1,boundryTriangle)	
			
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
		# # print("new triangles")
		# for tri in new_triangles:
		# 	# # print(tri)
		# 	for adj in self.triangles[tri]:
				# # print('\t',adj)
