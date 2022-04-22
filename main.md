# Final Project

---

## Possiblilities
1. expression trees
2. genetic trees
3. euclidian algorithm (GCF)
4. monoids + sub monoids
5. kruscles algorith
6. Delaunay Triangulation (Voronoi Diagrams)

### Properties of Delaunay triangulation
1. every circumcircle contains only 3 points that are on it's edges

# Useful Links
1. Powerpoint to help explain triangulation
https://i11www.iti.kit.edu/_media/teaching/sommer2018/compgeom/psession3b.pdf

2. A chapter in book describing triangulations with problems and proofs
https://ti.inf.ethz.ch/ew/Lehre/CG13/lecture/Chapter%206.pdf

3. Another chapter with good definitions and pictures 
https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/lect12-delaun-prop.pdf

4. Libraries in matlab that do what we want 
https://www.mathworks.com/help/matlab/ref/voronoi.html
https://www.mathworks.com/help/matlab/ref/delaunaytriangulation.html

5. Youtube explaining everything: https://www.youtube.com/watch?v=ysLCuqcyJZA

6. GitHub Repositories useful to make our code
https://github.com/HakanSeven12/Delaunator-Python
https://github.com/jmespadero/pyDelaunay2D/blob/master/delaunay2D.py

### Potential Algorithm Explanation
1. We consider each point one by one inside the larger "super-triangle". 
2. For every point, we consider all the triangles whose circumcircles contain the point, and call these the "bad triangles".
3. For every triangle in the "bad triangles", we remove from the main mesh any edges that are shared by at least 2 of the "bad triangles" (i.e. we keep only those "bad-triangle-edges" which are unique to a single "bad triangle"). Now, for every edge belonging to a "bad triangle" that was not removed, form a triangle using the edge and the point. 
4. Repeat the above for all points. 
5. When done, remove the vertices of the "super triangle" and all edges incident upon them.

TODO: prove this algorithm works using prperties of delony triangulation
