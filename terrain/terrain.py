import arcade
import pymunk


class Terrain:

    def __init__(self, space):
        self.segment_length = 70

        self.terrain_shapes = []
        self.visuals = arcade.ShapeElementList()

        self.__setup(space)
        self.__setup_draw()

    def __setup(self, space):
        # TODO: Make adjustable
        for i in range(3, 8):
            shape = pymunk.Segment(space.static_body, (self.segment_length * i, 250), (self.segment_length * (i + 1), 250), 0.0)
            shape.friction = 0.2
            space.add(shape)
            self.terrain_shapes.append(shape)

    def __setup_draw(self):
        for line in self.terrain_shapes:
            start_x, start_y = line.a
            end_x, end_y = line.b
            self.visuals.append(arcade.create_line(start_x, start_y, end_x, end_y, arcade.color.BLACK, 2))

    def draw(self):
        self.visuals.draw()

    def update(self, offset):
        print(offset)