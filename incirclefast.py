# Code from Johnathan Shewchuck’s incirclefast predicate: https://www.cs.cmu.edu/afs/cs/project/quake/public/code/predicates.c.

def incirclefast(pa, pb, pc, pd):
  """
  Return a positive value if the point pd lies inside the circle passing through pa, pb, and pc; 
  Return a negative value if it lies outside; 
  Return zero if the four points are cocircular.
  The points pa, pb, and pc must be in counterclockwise   order, or the sign of the result will be reversed.    
  """
  adx = pa[0] - pd[0]
  ady = pa[1] - pd[1]
  bdx = pb[0] - pd[0]
  bdy = pb[1] - pd[1]
  cdx = pc[0] - pd[0]
  cdy = pc[1] - pd[1]

  abdet = adx * bdy - bdx * ady
  bcdet = bdx * cdy - cdx * bdy
  cadet = cdx * ady - adx * cdy
  alift = adx * adx + ady * ady
  blift = bdx * bdx + bdy * bdy
  clift = cdx * cdx + cdy * cdy

  return alift * bcdet + blift * cadet + clift * abdet