import arcade
import pymunk
import pymunkoptions
pymunkoptions.options["debug"] = True

from box_car import BoxCar
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, DT, GRAVITY


class MainScreen(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.car = BoxCar(self.space)

    def on_draw(self):
        arcade.start_render()

        self.car.update_visuals()

        self.car.draw()

    def on_update(self, delta_time):
        self.space.step(DT)



def main():
    main_screen = MainScreen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_screen.setup()
    arcade.run()

if __name__ == "__main__":
    main()