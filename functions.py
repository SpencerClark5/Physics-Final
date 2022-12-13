#function to calculate area of a triangle
#A(x1, y1), B(x2,y2), C(x3,y3)
def AreaOfTriangle(x1, y1, x2, y2, x3, y3):

    return abs((x1 * (y2 - y3) + 
                x2 * (y3 - y1) +
                x3 * (y1 - y2))
                / 2.0)


# A function to check whether point P(x, y)
# lies inside the triangle formed by
# A(x1, y1), B(x2, y2) and C(x3, y3)
def IsInsideThreePointArea(x1, y1, x2, y2, x3, y3, x, y):

    # Calculate area of triangle ABC
    A = AreaOfTriangle(x1, y1, x2, y2, x3, y3)
    
    # Calculate area of triangle PBC
    A1 = AreaOfTriangle(x, y, x2, y2, x3, y3)
    
    # Calculate area of triangle PAC
    A2 = AreaOfTriangle(x1, y1, x, y, x3, y3)
    
    # Calculate area of triangle PAB
    A3 = AreaOfTriangle(x1, y1, x2, y2, x, y)
    
    # Check if sum of A1, A2 and A3
    # is same as A
    if(A == A1 + A2 + A3):
        return True
    else:
        return False


# A function to check whether point
# P(x, y) lies inside the rectangle
# formed by A(x1, y1), B(x2, y2),
# C(x3, y3) and D(x4, y4)
def IsInsideOnePointArea(x1, y1, x2, y2, x3, y3, x4, y4, x, y):

    # Calculate area of rectangle ABCD
    A = (AreaOfTriangle(x1, y1, x2, y2, x3, y3) +
        AreaOfTriangle(x1, y1, x4, y4, x3, y3))
    
    # Calculate area of triangle PAB
    A1 = AreaOfTriangle(x, y, x1, y1, x2, y2)
    
    # Calculate area of triangle PBC
    A2 = AreaOfTriangle(x, y, x2, y2, x3, y3)
    
    # Calculate area of triangle PCD
    A3 = AreaOfTriangle(x, y, x3, y3, x4, y4)
    
    # Calculate area of triangle PAD
    A4 = AreaOfTriangle(x, y, x1, y1, x4, y4)
    
    # Check if sum of A1, A2, A3
    # and A4 is same as A
    return (A == A1 + A2 + A3 + A4)