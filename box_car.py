import arcade
import pymunk

import math
import random
from car_parts import Chromosome, Chassis, Wheel
from constants import MASS, SEED


class BoxCar:

    def __init__(self, space, chromosome=None):
        
        if chromosome is None:
            self.chromosome = BoxCar.generate_inital_chromosome(6, 50)
        
        vs = self.chromosome.get_vertices()
        self.chassis = Chassis(space, [700//2, 350], vs)

        w_info_1, w_info_2 = self.chromosome.wheels_info()
        genes = self.chromosome.get_genes()
        
        position_1 = genes[w_info_1[0]] + pymunk.Vec2d(700//2, 350)
        radius_1 = w_info_1[1]
        self.wheel_1 = Wheel(space, position_1, radius_1)

        position_2 = genes[w_info_2[0]] + pymunk.Vec2d(700//2, 350)
        radius_2 = w_info_2[1]
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

    def get_position(self):
        return self.chassis.body.position

    @staticmethod
    def generate_inital_chromosome(num_vertices, max_range):
        genes = []

        random.seed(SEED)
        for _ in range(num_vertices):
            x_cor = random.randrange(-max_range, max_range)
            y_cor = random.randrange(-max_range, max_range)
            genes.append(((x_cor, y_cor)))
        wheel1_vertex = random.randrange(-1, len(genes))
        wheel1_radius = random.randint(0, 10)
        
        wheel2_vertex = random.randrange(-1, len(genes))
        wheel2_radius = random.randint(0, 10)
        genes.extend([wheel1_vertex, wheel1_radius, wheel2_vertex, wheel2_radius])
        
        chromosome = Chromosome(genes)

        return chromosome