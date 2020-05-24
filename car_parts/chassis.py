import arcade
import pymunk
from constants import MASS

class Chassis:

    def __init__(self, space, position, vertices):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(position)
        self.vertices = vertices
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.mass = MASS

        space.add(self.body, self.shape)

        self.visuals = arcade.ShapeElementList()

    def setup_draw(self, center):
        self.visuals.center_x = center.x
        self.visuals.center_y = center.y

        shape = arcade.create_polygon(self.vertices, arcade.color.AVOCADO)
        self.visuals.append(shape)

    def update_visuals(self):
        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y
    
    def draw(self):
        self.visuals.draw()