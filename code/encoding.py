#this file contains classes used to draw shapes with the turtle library
#intended to be used with the vector library
import vector as v
import math as m

class Path():
	def __init__(self,points,t):
		self.points = points
		self.t = t
	def draw(self):
		self.t.penup()
		self.t.goto(self.points[0].cords[0],
				self.points[0].cords[1])
		for i in range(1,len(self.points)):
			self.t.pendown()
			self.t.goto(self.points[i].cords[0],
					self.points[i].cords[1])	
class CubePath(Path):
	def __init__(self,startPoint,dim,t):
		self.t = t
		self.points = []
		self.dim = dim
		self.points.append(startPoint)
	def draw(self):
		self.points = [self.points[0]]
		self.points = CubePath.genBinPath(self.points,self.dim)		
		super().draw()

	@staticmethod	
	def getTranslation(pointCount):
		match pointCount:
			case 1:
				return v.Vector([100,0])
			case 2:
				return v.Vector([0,100])
			case 4:
				return v.Vector([m.cos(m.pi/4)*80,m.sin(m.pi/4)*80])
			case _:
				return v.Vector([m.cos(pointCount)*80,m.sin(pointCount)*80])	
	@staticmethod
	def genBinPath(points,dim):
		while len(points) < 2**dim:	
			rev_arr = [p.copy() for p in points[::-1]] 
			translation = CubePath.getTranslation(len(points))
			for i in range(0,len(rev_arr)):
				rev_arr[i] = rev_arr[i] + translation	

			points = points + rev_arr
		return points
		
class Loop(Path):
	def __init__(self,points,t):
		super().__init__(points,t)
	def draw(self):
		super().draw()
		self.t.pendown()
		self.t.goto(self.points[0].cords[0],
			self.points[0].cords[1])
#a loop with 3 points
class Triangle(Loop):
	def __init__(self,points,t):
		if len(points) != 3:
			raise Exception("Triangles have 3 points dum dum")
		super().__init__(points,t)
