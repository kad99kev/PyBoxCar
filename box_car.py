import arcade
import pymunk

import math
from car_parts import Chromosome, Chassis, Wheel
from constants import START_POSITION, SIZE


class BoxCar:

    def __init__(self, space, chromosome=None):

        self.lifespan = 1000
        self.is_alive = True
        self.check_index = 0
        
        if chromosome is None:
            self.chromosome = Chromosome.generate_inital_chromosome()
        
        position_main = pymunk.Vec2d(START_POSITION)
        vs = self.chromosome.get_vertices()
        self.chassis = Chassis(space, position_main, vs)
        self.position = self.chassis.body.position

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
        self.__update_visuals()
        if self.is_alive:
            for wheel in self.wheels:
                wheel.draw()
            self.chassis.draw()
    
    def __update_visuals(self):
        if self.is_alive:
            for wheel in self.wheels:
                wheel.update_visuals()
            self.chassis.update_visuals()       

    def get_position(self):
        return self.position

    def update_lifespan(self, checkpoints):
        if self.is_alive:
            car_position = self.chassis.body.position
            check_position = checkpoints[self.check_index]

            if checkpoints[self.check_index] == checkpoints[-1]:
                self.is_alive = False
            
            if abs(check_position - car_position).length < SIZE and self.is_alive:
                self.check_index += 1
                self.lifespan += 10
            
            self.lifespan -= 1
            if self.lifespan < 0 and self.is_alive:
                self.is_alive = False
                self.__set_bodies_to_sleep()
            
            print(self.lifespan, self.is_alive, self.check_index)

        return self.is_alive

    def get_chromosome_and_score(self):
        return self.chromosome.get_genes(), self.check_index + self.lifespan

    def __set_bodies_to_sleep(self):
        if not self.chassis.body.is_sleeping:
            self.chassis.body.sleep()
        
        for wheel in self.wheels:
            if not wheel.body.is_sleeping:
                wheel.body.sleep()
