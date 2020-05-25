import arcade
import pymunk
import math
from constants import MASS

class Chassis:

    def __init__(self, space, position, vertices):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(position)
        self.vertices = vertices
        self.shape = pymunk.Poly(self.body, self.vertices, radius=1)
        self.shape.friction = 0.5
        self.shape.mass = MASS

        space.add(self.body, self.shape)

        self.visuals = arcade.ShapeElementList()

    def setup_draw(self):
        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y

        #TODO: Change car visual
        shape = arcade.create_line_loop(self.vertices, arcade.color.AVOCADO)
        self.visuals.append(shape)

    def update_visuals(self):
        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y
        self.visuals.angle = math.degrees(self.body.angle)
    
    def draw(self):
        self.visuals.draw()