#this file is an implimentation of a vector class
class Vector():
	def __init__(self,points):
		self.cords = points
	def scaled(self,n):
		ret_val = self.copy()
		ret_val.cords = [n * x for x in ret_val.cords]
		return ret_val

	def __str__(self):
		return str(self.cords)
	def copy(self):
		return Vector(self.cords)
	def dim(self):
		return len(self.cords)
	def __sub__(self,v):
		return (-v)+(self)
	def __neg__(self):
		return Vector([-i for i in self.cords])
	def __add__(self,v):
		x = self.dim()
		ret_val = self.cords
		adder = v.cords
		
		#in the event we incorectly 
		#initilized
		if x > v.dim():
			x = v.dim()
			ret_val = v.cords.copy()
			adder = self.cords
		else:
			#actually make a copy
			ret_val = self.cords.copy()			
		for i in range(0,x):
			ret_val[i] += adder[i]
		return Vector(ret_val)	
		
