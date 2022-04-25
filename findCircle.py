# Code retrived from https://stackoverflow.com/questions/28910718/give-3-points-and-a-plot-circle

import math

def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
  
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = math.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return (cx, cy), radius