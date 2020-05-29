import arcade
import pymunk
import math

from constants import WHEEL_FRICTION, WHEEL_MASS, FILTER

class Wheel:

    def __init__(self, space, position, radius):
        self.radius = radius
        self.mass = WHEEL_MASS
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(self.mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.friction = WHEEL_FRICTION
        self.shape.filter = pymunk.ShapeFilter(group=FILTER)

        space.add(self.body, self.shape)

        self.visuals = arcade.ShapeElementList()

    def setup_draw(self):
        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y

        # Draws the wheel
        shape = arcade.create_ellipse_filled(0, 0, self.radius, self.radius, arcade.color.GRAY)
        self.visuals.append(shape)
        
        # Draws the orientation of wheel
        end = self.body.rotation_vector * self.radius
        shape = arcade.create_line(0, 0, end.x , end.y, arcade.color.BLACK, 2)
        self.visuals.append(shape)

    def update_visuals(self):
        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y
        self.visuals.angle = math.degrees(self.body.angle)

    def draw(self):
        self.visuals.draw()
