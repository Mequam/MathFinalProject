from encoding import Delaunay2D
import numpy as np

# Create a random set of points
seeds = np.random.random((10, 2))

# Create Delaunay Triangulation and insert points one by one
dt = Delaunay2D()
for s in seeds:
    dt.addPoint(s)


# Dump points and triangles to console
print("Input points:\n", seeds)
print ("Delaunay triangles:\n", dt.printTrinagles())
