import arcade
import pymunk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from box_car import BoxCar
from terrain import Terrain
from ga import evolve
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, DT, GRAVITY, NUM_CARS


class MainScreen(arcade.Window):
    '''
    Main application class.
    '''

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        '''
        Setting up the environment.
        '''
        # Setting up space.
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.space.sleep_time_threshold = 1

        # Creating cars.
        self.cars = []
        for _ in range(NUM_CARS):
            self.cars.append(BoxCar(self.space))
        
        # Setting up terrain and checkpoints.
        self.terrain = Terrain(self.space)
        self.checkpoints = self.terrain.get_checkpoints()

        # Setting up extra UI elements.
        self.goal = arcade.create_line(self.checkpoints[-1].x - 40, self.checkpoints[-1].y, self.checkpoints[-1].x - 40, self.checkpoints[-1].y + 50, arcade.color.GREEN, 2)
        self.generation_number = 1
        self.best_score = 0
        self.plot_history = []
        self.score_history = []
        self.score_list = arcade.ShapeElementList()

    def on_draw(self):
        '''
        Render the screen.
        '''

        arcade.start_render()

        self.goal.draw()

        self.show_status()

        self.terrain.draw()

        for car in self.cars:
            car.draw()

    def on_update(self, delta_time):
        '''
        Update the simulation.
        '''

        self.space.step(DT)

        # To check if all cars in the current generation are alive.

        all_dead = True
        for car in self.cars:
            alive = car.update_lifespan(self.checkpoints)
            if alive:
                all_dead = False
                if self.best_score < car.get_checkpoint_index():
                    self.best_score = car.get_checkpoint_index()

        if all_dead:
            self.new_generation()

    def new_generation(self):
        '''
        Generate a new generation of cars.
        '''

        gene_scores = []
        
        for car in self.cars:
            g_s = car.get_chromosome_and_score()
            gene_scores.append(g_s)
        new_genes = evolve(gene_scores)
        
        constraints = self.space.constraints
        for c in constraints:
            self.space.remove(c)
        for car in self.cars:
            self.space.remove(car.chassis.body, car.chassis.shape)
            for wheel in car.wheels:
                self.space.remove(wheel.body, wheel.shape)
        
        self.cars = []
        for gene in new_genes:
            self.cars.append(BoxCar(self.space, gene))

        self.plot_history.append(self.best_score)
        plt.clf()
        plt.plot(self.plot_history)
        plt.xlabel('Number of Generations')
        plt.ylabel('Best Score per Generation')
        plt.draw()
        plt.show(block=False)

        self.score_history.append({'gen': self.generation_number, 'score': self.best_score})
        self.score_history = sorted(self.score_history, key=lambda x: x['score'], reverse=True)[:25]

        self.best_score = 0
        self.generation_number += 1

    def show_status(self):
        '''
        Show the current generation and history stats.
        '''

        score = f"Current Generation: {self.generation_number}\nBest Car Info | Score: {self.best_score}"
        arcade.draw_text(score, 50, 50, arcade.color.RED, anchor_y='top')

        arcade.draw_text('Top 25 Scores', 1100, 780, arcade.color.DARK_BLUE, anchor_x='center', anchor_y='top')
        
        for i, score in enumerate(self.score_history):
            arcade.draw_text(f"Generation: {score['gen']} | Score: {score['score']}\n", 1120, 760 - i * 30, arcade.color.DARK_ELECTRIC_BLUE, anchor_x='center', anchor_y='top')





def main():
    '''
    Main method.
    '''
    main_screen = MainScreen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_screen.setup()
    arcade.run()

if __name__ == "__main__":
    main()