import arcade
import pymunk

import math
import random
from car_parts import Chromosome, Chassis, Wheel
from constants import START_POSITION, SIZE


class TestCar:

    def __init__(self, space, num):

        self.lifespan = 1000
        self.is_alive = True
        self.check_index = 0
        
        main_position = pymunk.Vec2d(START_POSITION)
        vs = [(-25 + num, 10), (25, 25 + num), (25 + num, 0), (25, -25 + num), (-25 + num, -10), (-25, 0 + num)]

        self.chassis = Chassis(space, main_position, vs)
        self.position = self.chassis.body.position
        
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
        self.__update_visuals()
        self.wheel_1.draw()
        self.wheel_2.draw()
        self.chassis.draw()
    
    def __update_visuals(self):
        self.wheel_1.update_visuals()
        self.wheel_2.update_visuals()
        self.chassis.update_visuals()

    def update_lifespan(self, checkpoints):
        car_position = self.chassis.body.position
        check_position = checkpoints[self.check_index]
        print(car_position, check_position)
        print(abs(check_position - car_position).length)

        if checkpoints[self.check_index] == checkpoints[-1]:
            self.is_alive = False
        
        if abs(check_position - car_position).length < SIZE and self.is_alive:
            self.check_index += 1
            self.lifespan += 100
        
        self.lifespan -= 1
        if self.lifespan < 0 and self.is_alive:
            self.is_alive = False
        
        print(self.lifespan, self.is_alive, self.check_index)

        return self.is_alive


