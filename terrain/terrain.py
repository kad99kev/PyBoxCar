import arcade
import pymunk
# import noise
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TERRAIN_FRICTION, SEED

class Terrain:

    def __init__(self, space):
        self.segment_length = 30

        self.terrain_shapes = []
        self.visuals = arcade.ShapeElementList()

        self.__setup(space)
        self.__setup_draw()

    def __setup(self, space):
        random.seed(SEED)
        # First level
        current_height = SCREEN_HEIGHT - 150
        previous_height = current_height
        for i in range(15 * 2):
            y = random.randint(-5, 5)
            current_height += y
            shape = pymunk.Segment(space.static_body, (self.segment_length * i, previous_height), (self.segment_length * (i + 1), current_height), 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            previous_height = current_height

        # Second level
        current_height -= 150
        previous_height = current_height
        for i in range(17 * 2, 3, -1):
            y = random.randint(-5, 5)
            current_height += y
            shape = pymunk.Segment(space.static_body, (self.segment_length * i, current_height), (self.segment_length * (i + 1), previous_height), 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            previous_height = current_height
        
        # Third level
        current_height -= 150
        previous_height = current_height
        for i in range(15 * 2):
            y = random.randint(-5, 5)
            current_height += y
            shape = pymunk.Segment(space.static_body, (self.segment_length * i, previous_height), (self.segment_length * (i + 1), current_height), 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            previous_height = current_height

        # Fourth level
        current_height -= 150
        previous_height = current_height
        for i in range(17 * 2, 3, -1):
            y = random.randint(-5, 5)
            current_height += y
            shape = pymunk.Segment(space.static_body, (self.segment_length * i, current_height), (self.segment_length * (i + 1), previous_height), 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            previous_height = current_height

        # Overall bounding box
        # (0, 0) to (0, height)
        shape = pymunk.Segment(space.static_body, (0, 0), (0, SCREEN_HEIGHT), 0.0)
        shape.friction = TERRAIN_FRICTION
        space.add(shape)
        self.terrain_shapes.append(shape)
        # (0, height) to (width, height)
        shape = pymunk.Segment(space.static_body, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 0.0)
        shape.friction = TERRAIN_FRICTION
        space.add(shape)
        self.terrain_shapes.append(shape)
        # (width, height) to (width, 0)
        shape = pymunk.Segment(space.static_body, (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0), 0.0)
        shape.friction = TERRAIN_FRICTION
        space.add(shape)
        self.terrain_shapes.append(shape)
        # (width, 0) to (0, 0)
        shape = pymunk.Segment(space.static_body, (0, 10), (SCREEN_WIDTH, 10), 0.0)
        shape.friction = TERRAIN_FRICTION
        space.add(shape)
        self.terrain_shapes.append(shape)

    def __get_y(self, x, x_min, x_max):
        scaled_x = self.__map(x, x_min, x_max, 0, 1)
        y = noise.pnoise1(scaled_x)
        scaled_y = self.__map(y, 0, 1, -10, 10)
        return scaled_y

    def __map(self, value, curr_min, curr_max, new_min, new_max):
        curr_span = curr_max - curr_min
        new_span = new_max - new_min
        scaled = float(value - curr_min) / curr_span
        return new_min + (scaled * new_span)

    def __setup_draw(self):
        self.visuals.center_x = 0
        self.visuals.center_y = 0
        for line in self.terrain_shapes:
            start_x, start_y = line.a
            end_x, end_y = line.b
            self.visuals.append(arcade.create_line(start_x, start_y, end_x, end_y, arcade.color.BLACK, 2))

    def draw(self):
        self.visuals.draw()