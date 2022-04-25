from sympy import *
from sympy.geometry import *
import random
import math
import matplotlib.pyplot as plt

def isLeftTurn(P1, P2, P3):
  """
P1, P2, P3: individual point objects arranged ccw
This function returns twice the signed area of the triangle determined by P1, P2, P3. The area is positive if P3 is on the left of P1, P2, negative if P3 is on the right of P1, P2, and zero if the points are collinear.
  """
  return (P2[0] - P1[0]) * (P3[1] - P1[1]) - (P3[0] - P1[0]) * (P2[1] - P1[1])


def getArcCosine(start, test):
  """
  This function returns the arccosine value between the bottommost point and the test point
  start, test: 2DPoint object
  """
  if start == test:
      return -math.inf
  else:
      return math.acos(
          (start[0] - test[0]) / (sqrt((start[0] - test[0])**2 +
                                       (start[1] - test[1])**2)))

def sortByAngle(pointList):
  """
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
def grahamScan(pointList):
  """
  This function computes the convex hull and returns points on hull and a sorted point list sorted by arccosine
  pointList: a list of points generated in general position
  Start a loop from the bottommost point, visiting points in the order of PointsToVisit
  """
  sortedPointList = sortByAngle(pointList)
  pointsOnHull = []

  for x in sortedPointList:
      pointsOnHull.append(x)
      
      while len(pointsOnHull) > 2 and isLeftTurn(
              pointsOnHull[-3], pointsOnHull[-2], pointsOnHull[-1])>=0:
          pointsOnHull.pop(-2)

  pointsOnHull.append(sortedPointList[0])

  return pointsOnHull, sortedPointList


def isInTriangle(P1, P2, P3, test): 
  """
  P1, P2, P3: individual point objects ccw
  test: an individual point object of the remainder polygon
  This function returns True if the test point is inside the triangle(P1, P2, P3)
  """
  left_list = [isLeftTurn(P1, P2, test) >= 0, isLeftTurn(P2, P3, test) >= 0, isLeftTurn(P3, P1, test) >= 0] 
  if (left_list[0] and left_list[1] and left_list[2]) == True:
    return True
  else:
    return False 

    
# Triangulate the hull via modified graham scan
def diagToTriang(pointsOnHull):
  """
  Perform triangulation based on the priciples of graham scan
  Connect vertices with the bottom most point on the hull
  Returns a list of triangles (list of 3 points) and a list of diagonals (list of 2 points)
  pointsOnHull: a list of points on the convex hull
  """
  triangle_list = []
  diagonal_list = []
  for i in range(1, len(pointsOnHull)-2):
    triangle_list.append([pointsOnHull[0], pointsOnHull[i], pointsOnHull[i+1]])
    diagonal_list.append([pointsOnHull[0], pointsOnHull[i+1]])
    
  return triangle_list, diagonal_list[:-1]


def splitTriangle(sortedPointList, pointsOnHull, triangle_list, diagonal_list):
  """
  Performs the split triangle algorithm
  sortedPointList: a list of points generated in general position sorted by arccosines
  pointsOnHull: a list of points on the convex hull
  triangle_list: a list of triangles created by triangulation of the hull
  diagonal_list: a list of diagonals created by triangulation of the hull
  """
  points_in_hull = [x for x in sortedPointList if x not in pointsOnHull]
  
  for p in points_in_hull:
    for t in range(len(triangle_list)):
      if isInTriangle(triangle_list[t][2], triangle_list[t][1],triangle_list[t][0], p):
        break
      else:
        continue
    triangle_list.append([p, triangle_list[t][0], triangle_list[t][1]])
    triangle_list.append([p, triangle_list[t][1], triangle_list[t][2]])
    triangle_list.append([p, triangle_list[t][2], triangle_list[t][0]])
    
 
    diagonal_list.append([p, triangle_list[t][0]])
    diagonal_list.append([p, triangle_list[t][1]])
    diagonal_list.append([p, triangle_list[t][2]])
    del triangle_list[t]
    
  return triangle_list, points_in_hull, diagonal_list
