import arcade
import pymunk
import math
from constants import CHASSIS_MASS, CHASSIS_FRICTION, FILTER

class Chassis:
    '''
    The main body of the car.
    '''

    def __init__(self, space, position, vertices):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(position)
        self.vertices = vertices
        self.shape = pymunk.Poly(self.body, self.vertices, radius=1)
        self.shape.friction = CHASSIS_FRICTION
        self.shape.mass = CHASSIS_MASS
        self.shape.filter = pymunk.ShapeFilter(group=FILTER)

        space.add(self.body, self.shape)

        self.visuals = arcade.ShapeElementList()

    def setup_draw(self):
        '''
        Creating the inital shapes to be rendered later by the BoxCar class.
        '''

        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y

        for i in range(len(self.vertices) - 1):
            v = self.vertices[i]
            v_1 = self.vertices[i + 1]
            colour_list = self.__generate_colour_list(v, v_1)
            shape = arcade.create_triangles_filled_with_colors([v, v_1, (0, 0)], colour_list)
            self.visuals.append(shape)
        
        v = self.vertices[0]
        v_1 = self.vertices[-1]
        colour_list = self.__generate_colour_list(v, v_1)
        shape = arcade.create_triangles_filled_with_colors([v, v_1, (0, 0)], colour_list)
        self.visuals.append(shape)

    def update_visuals(self):
        '''
        To update the visuals after every step.
        Called by the parent class.
        '''

        self.visuals.center_x = self.body.position.x
        self.visuals.center_y = self.body.position.y
        self.visuals.angle = math.degrees(self.body.angle)
    
    def draw(self):
        '''
        To render the chassis.
        Called by the parent class.
        '''

        self.visuals.draw()

    def __generate_colour_list(self, v, v_1):
        '''
        Generate a colour for each triangle of the chassis.
        Idea is to have similar vertices to have similar colour.
        Thus indicating that the cars are similar in structure.
        '''

        c_sum = v[0] + v[1] + v_1[0] + v[1]
        return [(v[0] + v_1[0], v[1] + v_1[1], c_sum)]