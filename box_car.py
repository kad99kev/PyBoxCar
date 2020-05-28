import arcade
import pymunk

import math
from car_parts import Chromosome, Chassis, Wheel
from constants import START_POSITION


class BoxCar:

    def __init__(self, space, chromosome=None):
        
        if chromosome is None:
            self.chromosome = Chromosome.generate_inital_chromosome()
        
        position_main = pymunk.Vec2d(START_POSITION)
        vs = self.chromosome.get_vertices()
        self.chassis = Chassis(space, position_main, vs)
        self.wheels = []

        wheel_info = self.chromosome.wheels_info()

        for position, radius, speed in wheel_info:
        
            if position == (-1, -1) or radius == -1 or speed == -1:
                continue

            position = position + position_main
            wheel = Wheel(space, position, radius)
            c = pymunk.constraint.PivotJoint(self.chassis.body, wheel.body, position)
            c.collide_bodies = False
            m = pymunk.SimpleMotor(self.chassis.body, wheel.body, speed)
            space.add(c, m)
            self.wheels.append(wheel)

        self.__setup_draw()

    def __setup_draw(self):            
        # Drawing Wheels
        for wheel in self.wheels:
            wheel.setup_draw()

        # Drawing Chassis
        self.chassis.setup_draw()

    def draw(self):
        for wheel in self.wheels:
            wheel.draw()
        self.chassis.draw()
    
    def update_visuals(self):
        for wheel in self.wheels:
            wheel.update_visuals()
        self.chassis.update_visuals()

    def get_position(self):
        return self.chassis.body.position