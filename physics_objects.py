from __future__ import annotations

import math

import pygame
from pygame import Surface
from pygame.math import Vector2, Vector3


class PhysicsObject:
    def __init__(
        self,
        pos: list | tuple | Vector2,
        vel: list | tuple | Vector2 = (0, 0),
        mass: float = 1,
        angle: float = 0,
        avel: float = 0,
        momi: float = math.inf,
        isBeanbag: bool = False,
        contact_type: str = "None",
    ):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.mass = mass
        self.angle = angle
        self.avel = avel
        self.momi = momi
        self.isBeanbag = isBeanbag
        self.contact_type = contact_type
        self.clear_force()

    def set_pos(self, pos: list | tuple | Vector2):
        self.pos = Vector2(pos)

    def set_contact_type(self, type: str):
        self.contact_type = type

    def get_contact_type(self) -> str:
        return self.contact_type

    def clear_force(self):
        self.force = Vector2(0, 0)
        self.torque = 0

    def add_force(self, force: Vector2):
        self.force += force

    def add_torque(self, torque: float):
        self.torque += torque

    def update(self, delta_t: float):
        # update velocity using the current force
        self.vel += (self.force / self.mass) * delta_t
        # update position using the newly updated velocity
        self.pos += self.vel * delta_t
        # update angular velocity
        self.avel += (self.torque / self.momi) * delta_t
        # update the angle of rotation
        self.angle += self.avel * delta_t

    def delta_pos(self, delta: list | tuple | Vector2):
        self.pos += Vector2(delta)

    def impulse(
        self, impulse: list | tuple | Vector2, point: list | tuple | Vector2 = None
    ):
        imp = Vector2(impulse)
        self.vel += imp / self.mass
        if point is not None:
            s = Vector2(point) - self.pos
            self.avel += Vector2.cross(s, imp) / self.momi

    def draw(self) -> None:
        ...


class Circle(PhysicsObject):
    def __init__(
        self,
        window: Surface,
        radius: float = 100,
        color: list | tuple | Vector3 = (255, 0, 0),
        width: int = 0,
        contact_type: str = "Circle",
        **kwargs,
    ):
        self.window = window
        self.radius = radius
        self.color = Vector3(color)
        self.width = width

        super().__init__(contact_type=contact_type, **kwargs)

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.pos, self.radius, self.width)


class Polygon(PhysicsObject):
    def __init__(
        self,
        window: Surface,
        local_points: list[list | tuple | Vector2] = [],
        color: list | tuple | Vector3 = (255, 0, 0),
        width: int = 0,
        contact_type: str = "Polygon",
        **kwargs,
    ):
        self.window = window
        self.color = Vector3(color)
        self.width = width
        super().__init__(contact_type=contact_type, **kwargs)

        self.local_points = [Vector2(point) for point in local_points]

        self.local_normals = [
            Vector2(point - self.local_points[i - 1]).normalize().rotate(90)
            for i, point in enumerate(self.local_points)
        ]

        self.points = self.local_points.copy()
        self.normals = self.local_normals.copy()
        self.update_polygon()

    def get_local_points(self):
        return self.local_points

    def update_polygon(self):
        for i, point in enumerate(self.local_points):
            self.points[i] = self.pos + point.rotate_rad(self.angle)
            self.normals[i] = self.local_normals[i].rotate_rad(self.angle)

    def update(self, dt: float):
        super().update(dt)
        self.update_polygon()

    def delta_pos(self, delta: list | tuple | Vector2):
        super().delta_pos(delta)
        self.update_polygon()

    def draw(self):
        pygame.draw.polygon(
            surface=self.window, color=self.color, points=self.points, width=self.width
        )
        # for point, normal in zip(self.points, self.normals):
        #     pygame.draw.line(self.window, self.color, point, point + 50 * normal)


class Wall(PhysicsObject):
    def __init__(
        self,
        window: Surface,
        start_point: list | tuple | Vector2,
        end_point: list | tuple | Vector2,
        reverse: bool = False,
        color: list | tuple | Vector3 = (255, 255, 255),
        width: int = 1,
        contact_type: str = "Wall",
    ):
        self.window = window
        self.start = Vector2(start_point)
        self.end = Vector2(end_point)
        self.color = Vector3(color)
        self.width = width
        self.pos = (self.start + self.end) / 2
        self.reverse = reverse
        super().__init__(pos=self.pos, contact_type=contact_type, mass=math.inf)
        self.update_wall()

    def update_wall(self):
        self.normal = (self.end - self.start).normalize().rotate(90)
        if self.reverse:
            self.normal.rotate(180)

    def draw(self):
        pygame.draw.line(self.window, self.color, self.start, self.end, self.width)


class UniformCircle(Circle):
    def __init__(self, window: Surface, radius: float, density: float = 1, **kwargs):
        # calculate mass and moment of inertia
        r2 = radius ** 2
        mass = math.pi * r2 * density
        momi = 0.5 * mass * r2
        super().__init__(window=window, radius=radius, mass=mass, momi=momi, **kwargs)


class UniformPolygon(Polygon):
    def __init__(
        self,
        window: Surface,
        density: float = 1,
        local_points: list[list | tuple | Vector2] = [],
        pos: list[list | tuple | Vector2] = (0, 0),
        angle: float = 0,
        shift: bool = True,
        **kwargs,
    ):
        # Calculate mass, moment of inertia, and center of mass
        total_mass: float = 0
        total_momi: float = 0
        com_num: Vector2 = Vector2(0, 0)
        # by looping over all "triangles" of the polygon
        for i in range(len(local_points)):
            r1 = Vector2(local_points[i - 1])
            r2 = Vector2(local_points[i])
            # triangle mass
            tmass: float = density * (0.5 * Vector2.cross(r2, r1))

            # triangle moment of inertia
            tmomi: float = (tmass / 6) * (
                r1.magnitude_squared() + r2.magnitude_squared() + r1.dot(r2)
            )

            # triangle center of mass
            tcom: Vector2 = (1 / 3) * (r1 + r2)

            # add to total mass
            total_mass += tmass
            # add to total moment of inertia
            total_momi += tmomi
            # add to center of mass numerator
            com_num += tmass * tcom

        # calculate total center of mass by dividing numerator by denominator (total mass)
        com: Vector2 = com_num / total_mass

        if shift:
            # Shift loca_points by com
            for i in range(len(local_points)):
                local_points[i] -= com
            # shift pos
            pos += com
            # Use parallel axis theorem to correct the moment of inertia
            total_momi -= total_mass * com.magnitude_squared()

        # Then call super().__init__() with those correct values
        super().__init__(
            window,
            mass=total_mass,
            momi=total_momi,
            local_points=local_points,
            pos=pos,
            angle=angle,
            **kwargs,
        )


