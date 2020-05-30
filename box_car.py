import arcade
import pymunk

import math
from ga import Chromosome
from car_parts import Chassis, Wheel
from constants import START_POSITION, SIZE


class BoxCar:
    '''
    The BoxCar class.
    It contains chassis and wheels.
    It is characterised based on the chromosome it received.
    '''

    def __init__(self, space, chromosome=None):

        self.lifespan = 1000
        self.is_alive = True
        self.checkpoint_index = 0
        
        # Generate the chromosome for the car.
        self.chromosome = chromosome
        if self.chromosome is None:
            self.chromosome = Chromosome.generate_inital_chromosome()
        
        # Create a chassis.
        position_main = pymunk.Vec2d(START_POSITION)
        vs = self.chromosome.get_vertices()
        self.chassis = Chassis(space, position_main, vs)
        self.position = self.chassis.body.position

        # Create the wheels.
        self.wheels = []
        genes = self.chromosome.get_genes()
        for position, [radius, speed] in genes:
        
            if radius == -1 or speed == -1:
                continue

            position = pymunk.Vec2d(position) + position_main
            wheel = Wheel(space, position, radius)
            c = pymunk.constraint.PivotJoint(self.chassis.body, wheel.body, position)
            c.collide_bodies = False
            m = pymunk.SimpleMotor(self.chassis.body, wheel.body, speed)
            space.add(c, m)
            self.wheels.append(wheel)

        self.__setup_draw()

    def __setup_draw(self):  
        '''
        Setting up the inital body of the chassis and wheels to be rendered.
        '''      

        # Drawing Wheels
        for wheel in self.wheels:
            wheel.setup_draw()

        # Drawing Chassis
        self.chassis.setup_draw()

    def draw(self):
        '''
        To render on screen.
        '''

        self.__update_visuals()
        if self.is_alive:
            for wheel in self.wheels:
                wheel.draw()
            self.chassis.draw()
    
    def __update_visuals(self):
        '''
        To update the visuals after every step.
        '''

        if self.is_alive:
            for wheel in self.wheels:
                wheel.update_visuals()
            self.chassis.update_visuals()       

    def get_position(self):
        '''
        Returns the current position of the car.
        '''

        return self.position

    def update_lifespan(self, checkpoints):
        '''
        Updates the lifespan based on the checkpoints crossed.
        
        Returns the status of the car.
        '''

        if self.is_alive:
            car_position = self.chassis.body.position
            check_position = checkpoints[self.checkpoint_index]

            if checkpoints[self.checkpoint_index] == checkpoints[-1]:
                self.is_alive = False
            
            if abs(check_position - car_position).length < SIZE and self.is_alive:
                self.checkpoint_index += 1
                self.lifespan += 10
            
            self.lifespan -= 1
            if self.lifespan <= 0 and self.is_alive:
                self.is_alive = False
                self.__set_bodies_to_sleep()
            
        return self.is_alive

    def get_chromosome_and_score(self):
        '''
        Returns a dictionary of the genes and the score of the car.
        '''
        
        return {'gene': self.chromosome.get_genes(), 'score': self.checkpoint_index + self.lifespan + 2}

    def get_checkpoint_index(self):
        '''
        Returns the current checkpoint index of the car.
        '''

        return self.checkpoint_index
    
    def __set_bodies_to_sleep(self):
        '''
        Sets the bodies and shapes to sleep to prevent extra computations during simulations.
        '''

        if not self.chassis.body.is_sleeping:
            self.chassis.body.sleep()
        
        for wheel in self.wheels:
            if not wheel.body.is_sleeping:
                wheel.body.sleep()
