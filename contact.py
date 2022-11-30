import math

from pygame.math import Vector2

from physics_objects import Circle, PhysicsObject, Polygon, Wall


# Returns a new contact object of the correct subtype
# This function has been done for you.
def generate(a: PhysicsObject, b: PhysicsObject, **kwargs):
    # Check if a's type comes later than b's alphabetically.
    # We will label our collision types in alphabetical order,
    # so the lower one needs to go first.
    if b.contact_type < a.contact_type:
        a, b = b, a
    # This calls the class of the appropriate name based on the two contact types.
    return globals()[f"{a.contact_type}_{b.contact_type}"](a, b, **kwargs)


# Generic contact class, to be overridden by specific scenarios
class Contact:
    def __init__(self, a, b, resolve=False, **kwargs):
        self.a = a
        self.b = b
        self.kwargs = kwargs
        self.update()
        self.resolved = False

        if resolve:
            self.resolve(update=False)

    def update(self):  # virtual function
        self.overlap = 0
        self.normal = Vector2(0, 0)

    def point(self):
        return Vector2(0, 0)

    def collided(self):
        return self.resolved

    def resolve(self, restitution=None, update=True):
        obj_a: PhysicsObject = self.a
        obj_b: PhysicsObject = self.b
        # print(f"                     {obj_b.points = }")

        if update:
            self.update()

        if restitution is None:
            if "restitution" in self.kwargs.keys():
                restitution = self.kwargs["restitution"]
            else:
                restitution = 0

        # resolve overlap
        # print(f"in resolve {self.overlap = }")
        if self.overlap > 0:
            self.resolved = True
            m = 1 / (1 / obj_a.mass + 1 / obj_b.mass)
            obj_a.delta_pos(m / obj_a.mass * self.overlap * self.normal)
            obj_b.delta_pos(-m / obj_b.mass * self.overlap * self.normal)

            # resolve velocity
            point = self.point()
            s_ap = (point - obj_a.pos).rotate(90)
            s_bp = (point - obj_b.pos).rotate(90)
            v_ap = obj_a.vel + obj_a.avel * s_ap
            v_bp = obj_b.vel + obj_b.avel * s_bp
            v = v_ap - v_bp
            n = self.normal
            vn = v.dot(n)

            if vn < 0:
                m = 1 / (
                    1 / obj_a.mass
                    + 1 / obj_b.mass
                    + (s_ap * n) ** 2 / obj_a.momi
                    + (s_bp * n) ** 2 / obj_b.momi
                )
                J = -(1 + restitution) * m * vn

                impulse = J * n
                obj_a.impulse(impulse, point)
                obj_b.impulse(-impulse, point)


# Contact class for two circles
class Circle_Circle(Contact):
    def __init__(self, a, b, **kwargs):
        self.a: Circle = a
        self.b: Circle = b
        super().__init__(a, b, **kwargs)

    def point(self):
        return self.a.pos - self.a.radius * self.normal

    def update(self):  # compute the appropriate values
        r = self.a.pos - self.b.pos
        self.overlap = self.a.radius + self.b.radius - r.magnitude()
        self.normal = Vector2(0, 0)
        if r.magnitude() != 0:
            self.normal = r.normalize()


# Contact class for Circle and a Polygon
class Circle_Polygon(Contact):
    def __init__(self, a, b, **kwargs):
        self.circle: Circle = a
        self.polygon: Polygon = b
        super().__init__(a, b, **kwargs)

    def point(self):
        return Vector2(self.circle.pos - self.circle.radius * self.normal)

    def update(self):
        min_overlap = math.inf

        circle: Circle = self.circle
        polygon: Polygon = self.polygon

        for i, (wall_point, wall_normal) in enumerate(
            zip(polygon.points, polygon.normals)
        ):
            overlap = circle.radius + Vector2(wall_point - circle.pos).dot(wall_normal)

            # if overlap is less than min_overlap
            if overlap < min_overlap:
                # update min_overlap
                min_overlap = overlap
                # save index
                index = i

        self.overlap = min_overlap
        self.normal = polygon.normals[index]

        if 0 < self.overlap < circle.radius:
            # Check if new point is beyond one of the endpoints
            endpoint1 = polygon.points[index]
            endpoint2 = polygon.points[index - 1]
            # if beyond index
            if Vector2(circle.pos - endpoint1).dot(endpoint1 - endpoint2) > 0:
                # set new overlap and normal
                r = Vector2(circle.pos - endpoint1)
                self.overlap = circle.radius - r.magnitude()
                self.normal = r.normalize()
            # elif beyond index-1
            elif Vector2(circle.pos - endpoint2).dot(endpoint2 - endpoint1) > 0:
                # set new overlap and normal
                r = Vector2(circle.pos - endpoint2)
                self.overlap = circle.radius - r.magnitude()
                self.normal = r.normalize()


# Contact class for Circle and a Wall
class Circle_Wall(Contact):
    def __init__(self, a, b, **kwargs):
        self.circle: Circle = a
        self.wall: Wall = b
        super().__init__(a, b, **kwargs)

    def point(self):
        return Vector2(self.circle.pos - self.circle.radius * self.normal)

    def update(self):  # compute the appropriate values
        r = Vector2(self.wall.pos - self.circle.pos)
        self.overlap = self.circle.radius + r.dot(self.wall.normal)
        self.normal = self.wall.normal


class Polygon_Polygon(Contact):
    def __init__(self, a: Polygon, b: Polygon, resolve=False, **kwargs):
        self.a: Polygon = a
        self.b: Polygon = b
        super().__init__(a, b, resolve, **kwargs)

    def point(self):
        return self.pt

    def update(self):
        poly_a = self.a
        poly_b = self.b

        # A OVERLAPPING B
        min_overlap = math.inf
        for i, point in enumerate(poly_b.points):
            start = poly_b.points[i - 1].copy()  # start
            end = point.copy()  # end
            wall = Wall(window=None, start_point=start, end_point=end, reverse=True)
            polywall_a: Polygon_Wall = generate(poly_a, wall)
            if polywall_a.overlap < min_overlap:
                min_overlap = polywall_a.overlap
                norm = polywall_a.normal
                pt = polywall_a.point()

        self.overlap = min_overlap
        self.normal = norm
        self.pt = pt

        # B OVERLAPPING A
        for i, point in enumerate(poly_a.points):
            start = poly_a.points[i - 1].copy()  # start
            end = point.copy()  # end
            wall = Wall(window=None, start_point=start, end_point=end, reverse=True)
            polywall_b: Polygon_Wall = generate(poly_b, wall)
            if polywall_b.overlap < min_overlap:
                min_overlap = polywall_b.overlap
                norm = polywall_b.normal.rotate(180)
                pt = polywall_b.point()

        self.overlap = min_overlap
        self.normal = norm
        self.pt = pt


class Polygon_Wall(Contact):
    def __init__(self, a, b, resolve=False, **kwargs):
        self.poly: Polygon = a
        self.wall: Wall = b
        super().__init__(a, b, resolve, **kwargs)

    def point(self):
        return self.poly.points[self.index]

    def update(self):
        max_overlap = -math.inf

        polygon: Polygon = self.poly
        wall: Wall = self.wall

        for i, point in enumerate(polygon.points):
            overlap = Vector2(wall.pos - point).dot(wall.normal)
            # if overlap is more than max_overlap
            if overlap > max_overlap:
                # update min_overlap
                max_overlap = overlap
                # save index
                index = i

        self.overlap = max_overlap
        self.normal = wall.normal
        self.index = index


# SPECIFICS FOR PROJECT


# BORING
class Wall_Wall(Contact):
    def __init__(self, a, b, **kwargs):
        super().__init__(a, b, **kwargs)
