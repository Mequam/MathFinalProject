#This file contains the data structures used in delauny triangulation
#
class Triangulation:
	def __init__(self,points):
		self.points = points	
		#array of tuples
		#where each element in the
		#tuple corispoinds to 
		#a point idx
		self.triangles = {}
		#an array of circomcircles
		#takes a triangle (tuple
		# of point idx) and returns
		# the stored circomcircle
		self.circles = {}
	#adds a new point to the triangulation
	def addPoint(self,point):
		pass
