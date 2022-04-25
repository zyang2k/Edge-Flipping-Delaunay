from incirclefast import *
from triangulation import *
from findCircle import *
from sympy import *
from sympy.geometry import *
import random
import math
import matplotlib.pyplot as plt
import time

def generalPosition(numOfPoints):
  """
  This function generates random points in general positions.
  """
  #Initiate an empty list
  points_in_general = []
  
  # initiate w/ two points
  for h in range(2):
    points_in_general.append(Point(random.randint(-5, 5), random.randint(-5, 5)))
    
  # generate points in general position
  for i in range(numOfPoints-2):
    currentPoint = Point(random.randint(-5, 5), random.randint(-5, 5))
    isColinear = False # set the default of boolean isColinear to False
    for j in points_in_general:
      for k in points_in_general:
        # skip if j and k are the same point
        if (j == k):
          continue
          
        # three points are collinear if and only if the triangle they determine has zero area. If colinearity happens, currentPoint will not be added into the point list    
        sorted_list = sortByAngle([j, k, currentPoint])
        if isLeftTurn(sorted_list[-1],sorted_list[-2],sorted_list[0]) == 0:      
           isColinear = True
           break
    
      if (isColinear == True):
        break
    #only add point that does not bring colinearity to the general position set 
    if (isColinear == False):
      points_in_general.append(currentPoint)
  return points_in_general
  
def isLeftTurn(P1, P2, P3):
  """
  P1, P2, P3: individual point objects arranged ccw
  
  This function returns twice the signed area of the triangle determined by P1, P2, P3. The area is positive if P3 is on the left of P1, P2, negative if P3 is on the right of P1, P2, and zero if the points are collinear.
  """
  return (P2[0] - P1[0]) * (P3[1] - P1[1]) - (P3[0] - P1[0]) * (P2[1] - P1[1])


def getArcCosine(start, test):
  """
  start, test: 2DPoint objects
  
  This function returns the arccosine value between the bottommost point and the test point
  """
  if start == test:
      return -math.inf
  else:
      return math.acos(
          (start[0] - test[0]) / (sqrt((start[0] - test[0])**2 +
                                       (start[1] - test[1])**2)))

def sortByAngle(pointList):
  """
  pointList: a list of points generated randomly
  
  This function sorts the list of points by angles.
  """
  start = getBottomMost(pointList)
  angleDict = {}
  for i in pointList:
      angle = getArcCosine(start, i)
      angleDict[i] = angle

  sortedAngleDict = dict(
      sorted(angleDict.items(),
             key=lambda x: (x[1], (x[0][0]**2 + x[0][1]**2)))
  )  # sort by angle first, when tie, sort by distance

  sortedPointList = list(sortedAngleDict.keys())

  return sortedPointList


def getBottomMost(pointList):
  """
  This function finds the bottom left-most point
  """
  return (sorted(pointList, key=lambda x: (x[1], x[0]))[0])

def findTriangles(triangle_list, diagonal):
  """
  triangle_list: a list of triangles generated by the triangle-splitting algorithm
  diagonal: a diagonal within the triangulated hull
  
  This function returns two lists: 
  quadrilateral_list: a list of quadrilaterals of length 4
  paired_triangle_list: a list of paired triangles (triangles that share the same edge) of length 6
  """
  #initiate the point set
  quadrilateral_list = []
  paired_triangle_list = []
  for triangle in triangle_list:

    #return true if the triangle contains the input diagonal
    if all(point in triangle for point in diagonal):
      paired_triangle_list.append(triangle)
      
      for point in triangle:
        if point not in quadrilateral_list:
          quadrilateral_list.append(point)

  return quadrilateral_list, paired_triangle_list
   
def checkSameDiagonalList(new_diagonal_list, old_diagonal_list):
  """
  This function returns True if Delaunay triangulation is reached
  """
  for new_diag in new_diagonal_list:
    for old_diag in old_diagonal_list:
      # check if new diagonal == old diagonal regardless of orientation
      if new_diag[0] in old_diag and new_diag[1] in old_diag:
        continue
        
      else:
        return False
  
  return True

def diagonalFlip(diagonal_list, triangle_list):
  """
  Flip the diagonal if there's an illegal edge
  """
  #initiate the newer/updated version of diagonal_list 
  new_diagonal_list = []

  # Stop flipping if reached Delaunay
  while checkSameDiagonalList(new_diagonal_list, diagonal_list): 
    #only update diagonal_list to the newer verison when we have a non empty newer version
    if new_diagonal_list != []:
      diagonal_list = new_diagonal_list
    
    new_diagonal_list = []
    circle = None
    for diagonal in diagonal_list:
    #find the points set of two triangles that share the diagonal and turn the set into a list
     
      quadrilateral_list, paired_triangle_list = findTriangles(triangle_list, diagonal)
      

    #make sure the points on the triangle is counter clockwise
      sortedTriangle = sortByAngle(quadrilateral_list[0:3])
    #define checkpoint
      checkpoint = quadrilateral_list[3]
    #Animation for circle
      center, radius = define_circle(sortedTriangle[0],sortedTriangle[1],sortedTriangle[2])
      circle = drawCircle(center,radius)
      time.sleep(1)
      #Since our points are sorted clockwise, the return of incirclefast should be greater than or equal to 0 for a valid Delaunay 
      if incirclefast(sortedTriangle[0],sortedTriangle[1],sortedTriangle[2], checkpoint) >= 0:
        new_diagonal_list.append(diagonal)
        circle.remove()
        fig.canvas.draw()
        continue
      else:
        #flip the diagonal by adding the other two points in the pair of triangle (points that are not in diagonal )
        new_diagonal = [point for point in quadrilateral_list if point not in diagonal]
        new_diagonal_list.append(new_diagonal)
        #Animation for diagonal update
        drawDiagonal(diagonal,"white", thickness = 1.5)
        drawDiagonal(new_diagonal,"#FF995D")
        time.sleep(1)
        circle.remove()
        fig.canvas.draw()
        #update triangulation
        for triangle in paired_triangle_list:
          triangle_list.remove(triangle)
        triangle_list.append([new_diagonal[0],new_diagonal[1],diagonal[0]])
        triangle_list.append([new_diagonal[0],new_diagonal[1],diagonal[1]])

      ax.scatter(xsc, ysc, c="pink", zorder = 2)
  
  return new_diagonal_list



def drawInitGraphStatic(pointSet, diagonal_list,pointsOnHull):
    ax.cla()
    #draw init triangulation
  
    for diagonal in init_diagonal_list:
        xid, yid = zip(*diagonal)
        ax.plot(xid, yid, c = "#9CBCFF", linewidth = 1)


    xh, yh = zip(*pointsOnHull)

    xsc, ysc = zip(*pointSet)
    ax.scatter(xsc, ysc, c="pink", zorder = 2)
    ax.plot(xh, yh, c = "#8BB0FE", linewidth = 1.5)

    fig.canvas.draw()
    fig.canvas.flush_events()


def drawCircle(center,radius):
    """
    This function draws a circle in correspondence to each triangle.
    Show the user whether or not the empty-circle property is satisfied.
    """
    # create circle object and make it show on the top layer
    circle=plt.Circle(center, radius, color='#4BD79B',fill=False, zorder = 3) 
    ax.add_patch(circle)
    fig.canvas.draw()
    fig.canvas.flush_events()
    return circle

def drawDiagonal(diagonal, color, thickness = 1):
    """
    This function draws a diagonal in the animation.
    """
    ax.autoscale(enable=False, axis='both', tight=None)
    plt.autoscale(enable=False, axis='both', tight=None)
    xd,yd = zip(*diagonal)
    ax.plot(xd,yd, c = color, linewidth = thickness)
    fig.canvas.draw()
    fig.canvas.flush_events()




# generate 20 points in general position
test_1 = generalPosition(numOfPoints = 20)

# perform triangle splitting
pointsOnHull, sortedPointList = grahamScan(test_1)
triangle_list, diagonal_list = diagToTriang(pointsOnHull)
init_triangle_list, pointsInHull, init_diagonal_list = splitTriangle(sortedPointList, pointsOnHull, triangle_list, diagonal_list) 


# initialize the figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal', adjustable='box')
plt.show(block=False)
ax.autoscale(enable=False, axis='both', tight=None)

# draw init triangulation
xsc, ysc = zip(*test_1)
drawInitGraphStatic(test_1, init_diagonal_list, pointsOnHull)

time.sleep(1)

# perform Delaunay
new_diagonal_list = diagonalFlip(diagonal_list, triangle_list) 

    
  
  
 
    