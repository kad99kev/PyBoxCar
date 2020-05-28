import arcade
import pymunk

import math
import random
from car_parts import Chromosome, Chassis, Wheel
from constants import START_POSITION, SEED


class TestCar:

    def __init__(self, space, chromosome=None):
        
        main_position = pymunk.Vec2d(START_POSITION)
        vs = [(-25, 10), (25, 25), (25, 0), (25, -25), (-25, -10), (-25, 0)]

        self.chassis = Chassis(space, main_position, vs)
        
        position_1 = pymunk.Vec2d(25, -25) + main_position
        radius_1 = 10
        self.wheel_1 = Wheel(space, position_1, radius_1)

        position_2 = pymunk.Vec2d(25, 25) + main_position
        radius_2 = 10
        self.wheel_2 = Wheel(space, position_2, radius_2)


        c1 = pymunk.constraint.PivotJoint(self.chassis.body, self.wheel_1.body, position_1)
        c1.collide_bodies = False
        m1 = pymunk.SimpleMotor(self.chassis.body, self.wheel_1.body, 25)

        c2 = pymunk.constraint.PivotJoint(self.chassis.body, self.wheel_2.body, position_2)
        c2.collide_bodies = False
        m2 = pymunk.SimpleMotor(self.chassis.body, self.wheel_2.body, -25)

        space.add(c1, m1, c2, m2)

        self.__setup_draw()

    def __setup_draw(self):            
        # Drawing Wheels
        self.wheel_1.setup_draw()
        self.wheel_2.setup_draw()

        # Drawing Chassis
        self.chassis.setup_draw()

    def draw(self):
        self.wheel_1.draw()
        self.wheel_2.draw()
        self.chassis.draw()
    
    def update_visuals(self):
        self.wheel_1.update_visuals()
        self.wheel_2.update_visuals()
        self.chassis.update_visuals()

    def update(self):
        pass

    @staticmethod
    def generate_inital_chromosome(num_vertices, max_range):
        genes = []

        random.seed(SEED)
        for _ in range(num_vertices):
            x_cor = random.randrange(-max_range, max_range)
            y_cor = random.randrange(-max_range, max_range)
            genes.append(((x_cor, y_cor)))
        wheel1_vertex = random.randrange(-1, len(genes))
        wheel1_radius = random.randint(0, 50)
        
        wheel2_vertex = random.randrange(-1, len(genes))
        wheel2_radius = random.randint(0, 50)
        genes.extend([wheel1_vertex, wheel1_radius, wheel2_vertex, wheel2_radius])
        
        chromosome = Chromosome(genes)

        return chromosome