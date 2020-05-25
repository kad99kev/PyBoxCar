import arcade
import pymunk

import math
import random
from car_parts import Chromosome, Chassis, Wheel
from constants import MASS, SEED


class TestCar:

    def __init__(self, space, chromosome=None):
        
        vs = [(-20, 25), (19, -34), (-3, 27), (10, 30), (24, -42), (27, -49)]
        self.chassis = Chassis(space, [700//2, 350], sorted(vs))
        
        position_1 = pymunk.Vec2d(-50, -50) + pymunk.Vec2d(700//2, 350)
        radius_1 = 10
        self.wheel_1 = Wheel(space, position_1, radius_1)

        position_2 = pymunk.Vec2d(50, -50) + pymunk.Vec2d(700//2, 350)
        radius_2 = 10
        self.wheel_2 = Wheel(space, position_2, radius_2)


        c1 = pymunk.constraint.PivotJoint(self.chassis.body, self.wheel_1.body, position_1)
        c1.collide_bodies = False
        m1 = pymunk.SimpleMotor(self.chassis.body, self.wheel_1.body, 5)

        c2 = pymunk.constraint.PivotJoint(self.chassis.body, self.wheel_2.body, position_2)
        c2.collide_bodies = False
        m2 = pymunk.SimpleMotor(self.chassis.body, self.wheel_2.body, 5)

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