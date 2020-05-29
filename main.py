import arcade
import pymunk
import pymunkoptions
pymunkoptions.options["debug"] = True

from box_car import BoxCar
from test_car import TestCar
from terrain import Terrain
from ga import evolve
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, DT, GRAVITY, NUM_CARS


class MainScreen(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.space.sleep_time_threshold = 1

        self.cars = []
        for _ in range(NUM_CARS):
            self.cars.append(BoxCar(self.space))
        
        # self.test_car = TestCar(self.space, 0)
        
        print(len(self.cars))
        
        self.terrain = Terrain(self.space)
        self.checkpoints = self.terrain.get_checkpoints()

        # self.checkpoint_shape = arcade.ShapeElementList()
        # for checkpoint in self.checkpoints:
        #     shape = arcade.create_ellipse_filled(checkpoint.x, checkpoint.y, 5, 5, arcade.color.RED)
        #     shape = arcade.create_ellipse_outline(checkpoint.x, checkpoint.y, 20, 20, arcade.color.RED)
        #     self.checkpoint_shape.append(shape)

        debug_handler = self.space.add_default_collision_handler()
        debug_handler.begin = self.debug_handler


    def on_draw(self):
        arcade.start_render()

        self.terrain.draw()

        for car in self.cars:
            car.draw()

        # self.test_car.draw()

    def on_update(self, delta_time):
        self.space.step(DT)

        all_dead = True
        for car in self.cars:
            alive = car.update_lifespan(self.checkpoints)
            if alive:
                all_dead = False

        if all_dead:
            self.new_generation()

    def debug_handler(self, arbiter, space, data):
        # print(f'Space: {space}')
        # print(f'Arbiter: {arbiter}')
        # print(f'Data: {data}')

        return True

    def new_generation(self):
        gene_scores = []
        for car in self.cars:
            g_s = car.get_chromosome_and_score()
            gene_scores.append(g_s)
        new_genes = evolve(gene_scores)
        constraints = self.space.constraints
        for c in constraints:
            self.space.remove(c)
        for car in self.cars:
            self.space.remove(car.chassis.body)
            for wheel in car.wheels:
                self.space.remove(wheel.body)
        
        self.cars = []
        for gene in new_genes:
            self.cars.append(BoxCar(self.space, gene))



def main():
    main_screen = MainScreen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_screen.setup()
    arcade.run()

if __name__ == "__main__":
    main()