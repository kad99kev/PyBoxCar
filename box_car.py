import arcade
import pymunk

import math
import random
from car_parts import Chromosome, Chassis, Wheel
from constants import MASS, SEED


class BoxCar:

    def __init__(self, space, chromosome=None):
        
        if chromosome is None:
            self.chromosome = BoxCar.generate_inital_chromosome(6, 200)
        
        vs = self.chromosome.get_vertices()
        self.chassis = Chassis(space, [700//2, 500//2], vs)

        w_info_1, w_info_2 = self.chromosome.wheels_info()
        genes = self.chromosome.get_genes()
        
        position_1 = genes[w_info_1[0]]
        radius_1 = w_info_1[1]
        self.wheel_1 = Wheel(space, position_1, radius_1)

        position_2 = genes[w_info_2[0]]
        radius_2 = w_info_2[1]
        self.wheel_2 = Wheel(space, position_2, radius_2)


        pymunk.constraint.PivotJoint(self.chassis.body, self.wheel_1.body, position_1, (0, 0))
        pymunk.SimpleMotor(self.chassis.body, self.wheel_1.body, 5)

        pymunk.constraint.PivotJoint(self.chassis.body, self.wheel_2.body, position_2, (0, 0))
        pymunk.SimpleMotor(self.chassis.body, self.wheel_2.body, 5)

        self.__setup_draw()

    def __setup_draw(self):
        center = self.chassis.body.position
            
        # Drawing Wheels
        self.wheel_1.setup_draw(center)
        self.wheel_2.setup_draw(center)

        # Drawing Chassis
        self.chassis.setup_draw(center)

    def draw(self):
        self.wheel_1.draw()
        self.wheel_2.draw()
        self.chassis.draw()
    
    def update_visuals(self):
        center = self.chassis.body.position
        self.wheel_1.update_visuals(center)
        self.wheel_2.update_visuals(center)
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