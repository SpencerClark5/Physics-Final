from pygame.math import Vector2
import math

# Returns a new contact object of the correct subtype
# This function has been done for you.
def generate(a, b, **kwargs):
    # Check if a's type comes later than b's alphabetically.
    # We will label our collision types in alphabetical order, 
    # so the lower one needs to go first.
    if b.contact_type < a.contact_type:
        a, b = b, a
    # This calls the class of the appropriate name based on the two contact types.
    return globals()[f"{a.contact_type}_{b.contact_type}"](a, b, **kwargs)
    

# Generic contact class, to be overridden by specific scenarios
class Contact():
    def __init__(self, a, b, canJump=False, resolve=False, **kwargs):
        self.a = a
        self.b = b
        self.canJump = canJump
        self.kwargs = kwargs
        self.score = 0
        self.update()
        if resolve:
            self.resolve(update=False)

    def point(self):
        return self.circle.pos - self.circle.radius*self.normal
 
    def update(self):  # virtual function
        self.overlap = 0
        self.normal = Vector2(0, 0)

    def resolve(self, restitution=None, friction=None, update=True):
        a = self.a
        b = self.b
        if update:
            self.update()

        if restitution is None:
            if "restitution" in self.kwargs.keys():
                restitution = self.kwargs["restitution"]
            else:
                restitution = 0

        if friction is None:
            if "friction" in self.kwargs.keys():
                friction = self.kwargs["friction"]
            else:
                friction = 0

        # resolve overlap
        if self.overlap > 0:

            self.resolved = True
            m = 1 / (1 / a.mass + 1 / b.mass)
            a.delta_pos(m / a.mass * self.overlap * self.normal)
            b.delta_pos(-m / b.mass * self.overlap * self.normal)

            # resolve velocity
            r_c = Vector2(a.pos - a.radius * self.normal)
            v_ap = Vector2(a.vel + a.avel * Vector2(r_c - a.pos).rotate(90))
            v_bp = Vector2(b.vel + b.avel * Vector2(r_c - b.pos).rotate(90))
            v = Vector2(v_ap - v_bp)
            vn = v.dot(self.normal)

            if Vector2.dot(v, self.normal) < 0:
                Jn = -(1 + restitution) * m * vn
                # calc tangent and vel
                tangent = self.normal.rotate(90)
                vt = v.dot(tangent)
                vts = math.copysign(1.0, vt)
                # calc tangent impulse to make vel 0
                Jt = -m * vt
                # check if too stronk
                if abs(Jt) > friction * Jn:  # if too stronk
                    # set jt to max
                    Jt = -vts * friction * Jn
                else:  # object stick
                    # prevent creep
                    disp = vt / vn * self.overlap
                    a.delta_pos(m / a.mass * disp * tangent)
                    b.delta_pos(-m / b.mass * disp * tangent)

                impulse = Jn * self.normal + Jt * tangent
                a.impulse(impulse)
                b.impulse(-impulse) 




class Circle_Polygon(Contact):
    def __init__(self, a, b, **kwargs):
        self.circle = a
        self.polygon = b
        super().__init__(a, b, **kwargs)

    def update(self):
        min_overlap = math.inf
        # loop over all sides, find index of minimum overlap
        for i, (wall_point, wall_normal) in enumerate(zip(self.polygon.points, self.polygon.normals)):
            overlap = self.circle.radius + (wall_point - self.circle.pos).dot(wall_normal)
            # if overlap is less than min overlap
            if overlap < min_overlap:
                min_overlap = overlap
                index = i

        self.overlap = min_overlap
        self.normal = self.polygon.normals[index]

        if 0 < self.overlap < self.circle.radius:
            # check if the point is beyond one of the endpoints
            endpoint1 = self.polygon.points[index]
            endpoint2 = self.polygon.points[index-1]

            if (self.circle.pos - endpoint1).dot(endpoint1 - endpoint2) > 0:
                r = self.circle.pos - endpoint1
                self.overlap = self.circle.radius - r.magnitude()
                self.normal = r.normalize()

            elif (self.circle.pos - endpoint2).dot(endpoint2 - endpoint1) > 0:
                r = self.circle.pos - endpoint2
                self.overlap = self.circle.radius - r.magnitude()
                self.normal = r.normalize()



# Contact class for two circles
class Circle_Circle(Contact):
    def __init__(self, a, b, **kwargs):
        self.a = a
        self.b = b
        super().__init__(a, b, **kwargs)

    def update(self):  # compute the appropriate values
        r = self.a.pos - self.b.pos
        self.overlap = self.a.radius + self.b.radius - r.magnitude()
        self.normal = r.normalize()


# Contact class for Circle and a Wall
# Circle is before Wall because it comes before it in the alphabet
class Circle_Wall(Contact):
    def __init__(self, a, b, **kwargs):
        self.circle = a
        self.wall = b
        super().__init__(a, b, **kwargs)


    def update(self):  # compute the appropriate values
        
        self.overlap = self.circle.radius + (self.wall.pos - self.circle.pos).dot(self.wall.normal)
        self.normal = self.wall.normal


# Empty class for Wall - Wall collisions
# The intersection of two infinite walls is not interesting, so skip them
class Wall_Wall(Contact):
    def __init__(self, a, b, **kwargs):
        super().__init__(a, b, **kwargs)

class Polygon_Wall(Contact):
    def __init__(self,a,b, **kwargs):
        super().__init__(a,b,**kwargs)

class Polygon_Polygon(Contact):
    def __init__(self,a,b,**kwargs):
        super().__init__(a,b,**kwargs)


