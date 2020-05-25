import arcade
import pymunk
import pymunkoptions
pymunkoptions.options["debug"] = True

from test_car import TestCar
from box_car import BoxCar
from terrain import Terrain
from constants import (SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, DT, GRAVITY, RIGHT_VIEWPORT_MARGIN)


class MainScreen(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Used to keep track of our scrolling
        self.view_left = 0

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        # self.car = TestCar(self.space)
        self.car = BoxCar(self.space)
        self.terrain = Terrain(self.space)

        print(self.space.bodies)
        print(self.space.shapes)
        print(self.space.constraints)

        debug_handler = self.space.add_default_collision_handler()
        debug_handler.begin = self.debug_handler

    def on_draw(self):
        arcade.start_render()

        self.terrain.draw()

        self.car.update_visuals()

        self.car.draw()

    def on_update(self, delta_time):
        self.space.step(DT)

        self.terrain.update(self.view_left)

        self.manage_scrolling()

    def manage_scrolling(self):
        # --- Manage Scrolling ---

        # Track if we need to change the viewport
        changed = False

        car_position = self.car.get_position()

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if car_position.x > right_boundary:
            self.view_left += car_position.x - right_boundary
            changed = True

        if changed:
            print(self.get_viewport())
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, 0, SCREEN_HEIGHT)

    def debug_handler(self, arbiter, space, data):
        print(f'Arbiter: {arbiter.shapes}')
        print(f'Space: {space}')
        print(f'Data: {data}')

        return True



def main():
    main_screen = MainScreen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_screen.setup()
    arcade.run()

if __name__ == "__main__":
    main()