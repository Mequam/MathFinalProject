#this file contains classes used to draw shapes with the turtle library
#intended to be used with the vector library
import vector as v
import math as m
import numpy as np
from math import sqrt

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
		
		
		
		
#Things That will make project go boom and well hopefully		
class Delaunay2D:
    """Class to compute a Delaunay triangulation in 2D
    ref: http://en.wikipedia.org/wiki/Bowyer-Watson_algorithm
    ref: http://www.geom.uiuc.edu/~samuelp/del_project.html
    """

    def __init__(self, center=(0, 0), radius=9999):
        """ This function simply creates a frame that will contain our triangulation honestly 
        Both center and readius optional of the frame is optional
        """
        center = np.asarray(center)
        # Create coordinates for the corners of the frame
        self.coords = [center+radius*np.array((-1, -1)),
                       center+radius*np.array((+1, -1)),
                       center+radius*np.array((+1, +1)),
                       center+radius*np.array((-1, +1))]

        # Two dictionaries used to contain our triangles and their circumcircles
        self.triangles = {}
        self.circles = {}

        # Create two  triangles for the frame just as a starter 
        T1 = (0, 1, 3)
        T2 = (2, 3, 1)
        self.triangles[T1] = [T2, None, None]
        self.triangles[T2] = [T1, None, None]

        # Compute circumcenters for each triangle located within our frame
        for t in self.triangles:
            self.circles[t] = self.generateCircumcenter(t)

    def generateCircumcenter(self, tri):
        """Compute a circumcenter for a given triangle will be useful for determining if a triangle is considered bad or not
        Uses an extension of the method described here:
        http://www.ics.uci.edu/~eppstein/junkyard/circumcenter.html
        """
        pts = np.asarray([self.coords[v] for v in tri]) #for every coordinate in our triangle convert this into an array containing those coordinates
        pts2 = np.dot(pts, pts.T)   #will multiply our two arrays using dot product 
        matrix1 = np.bmat([[2 * pts2, [[1],       #generates a matrix with the following inputs used to solve linear equation getting center point
                                 [1],
                                 [1]]],
                      [[[1, 1, 1, 0]]]])       

        matrix2 = np.hstack((np.sum(pts * pts, axis=1), [1])) #stacks an array column wise which will generate a matrix as well containing multiplication of our points
        linerEquationAnswer = np.linalg.solve(matrix1, matrix2)   #soves our linear equation of created by our two matrix 
        barycentCoordinate = linerEquationAnswer[:-1] #creates a barycentric coordinate variable used to calculate our circumcenter with multiplication
        center = np.dot(barycentCoordinate, pts)    # our center of our circle is the dot product of our barycentric coordiante and out enterd points array

        radius = np.sum(np.square(pts[0] - center))  # gives squared distance of radius of our circle
        return (center, radius)

    def inCircle(self, tri, p):
        """checks to see if the enterd point p is contained in our circumcenter of our triangle"""
        center, radius = self.circles[tri]
        return np.sum(np.square(center - p)) <= radius #check to see if the sum of the center minus our entered ponint squared is <= our radius teeling us if in circle ot not


    def addPoint(self, p):
        """Will add a point to our current triangulation, and ensure it maintains delaunay triangulation using Bowyer-Watson algorithm."""
        p = np.asarray(p)   #takes our entered point and makes it an array
        idx = len(self.coords)  #our index is the length of our coordinates arry
        self.coords.append(p)  #append our entered point to our coordinates

        # Search the triangle(s) whose circumcircle contains p
        deleteableTriangles = [] #creates a bad triangle array used to store triangles that dont follow triangulation rules
        for T in self.triangles:
            if self.inCircle(T, p):         #for every triangle see if entered p is in that triangle if so push it to bad triangle array
                deleteableTriangles.append(T)

        # Find the  boundary  of the bad triangles
        boundary = []
        # Choose a "random" triangle and edge
        T = deleteableTriangles[0]
        edge = 0
        # get the opposite triangle of this edge
        while True:
            # Check if edge of triangle T is on the boundary or if opposite triangle of this edge is external to the list
            oppositeTriangle = self.triangles[T][edge] #set the oposite triangle of our chosen T and its edge connected to it
            if oppositeTriangle not in deleteableTriangles: #if our opposite triangle is a bad triangle then insert that edge and triangle into our boundry array to search for bad triangels
                # Insert edge and external triangle into boundary list
                boundary.append((T[(edge+1) % 3], T[(edge-1) % 3], oppositeTriangle))

                # Move to next edge in the current triangle
                edge = (edge + 1) % 3

                # Check if boundary is a closed loop
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                # If the triangle is not closed loop , Move to next edge in opposite triangle
                edge = (self.triangles[oppositeTriangle].index(T) + 1) % 3 #set new edge to check for bad triangle
                T = oppositeTriangle  #our new triangle is now our opposite triangle repeat above steps

        # Deletes triangles and circles that are considered bad by being in circumcenter of another triangle
        for T in deleteableTriangles:
            del self.triangles[T]
            del self.circles[T]

        # Now we must retriangulate the hole left by the removal of the other bad triangles
        new_triangles = []  #initializes new triangle array
        for (e0, e1, oppositeTriangle) in boundary:   #for edges and opposite triangle in our boundary array do the following
            # Create a new triangle 
            T = (idx, e0, e1)

            # Store circumcenter and circumradius of the triangle we just created
            self.circles[T] = self.generateCircumcenter(T) 

            # Set opposite triangle of the edge as neighbour of our current triangle
            self.triangles[T] = [oppositeTriangle, None, None]

            # Try to set T as neighbour of the opposite triangle
            if oppositeTriangle:
                # search the neighbour of oppositeTriangle that use the entered edge
                for i, neigh in enumerate(self.triangles[oppositeTriangle]):
                    if neigh:
                        if e1 in neigh and e0 in neigh:
                            # change link to use our newly created triangle
                            self.triangles[oppositeTriangle][i] = T

            # Add triangle to our array
            new_triangles.append(T)

        # Link the new triangles each another
        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangles[T][1] = new_triangles[(i+1) % N]   
            self.triangles[T][2] = new_triangles[(i-1) % N]   

    def printTrinagles(self):
        """Displays an array of triangles in our tirangulation"""
        return [(a-4, b-4, c-4)
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]

    def printCircles(self):
        """Export the circumcircles as a list of (center, radius)
        """
        # Remember to compute circumcircles if not done before
        # for t in self.triangles:
        #     self.circles[t] = self.circumcenter(t)

        # Filter out triangles with any vertex not in frame
        # Do sqrt of radius before of return
        return [(self.circles[(a, b, c)][0], sqrt(self.circles[(a, b, c)][1]))
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]

    def printDelaunayTriangulation(self):
        """Prints the set of coordinates as well as triangles."""
        coord = self.coords[4:]

        # Filter out triangles with any vertex not in frame
        tris = [(a-4, b-4, c-4)
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]
        return coord, tris
