import arcade
import pymunk
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TERRAIN_FRICTION, SEED, SIZE

class Terrain:

    def __init__(self, space):
        self.segment_length = 30

        self.terrain_shapes = []
        self.visuals = arcade.ShapeElementList()

        self.checkpoints = self.__setup(space)
        self.__setup_draw()

    def __setup(self, space):

        checkpoints = []
        correction = pymunk.Vec2d(0, SIZE)

        random.seed(SEED)
        
        # First level
        current_height = SCREEN_HEIGHT - 150
        previous_height = current_height
        for i in range(30):
            y = random.randint(-5, 5)
            current_height += y
            
            start_pos = pymunk.Vec2d(self.segment_length * i, previous_height)
            end_pos = pymunk.Vec2d(self.segment_length * (i + 1), current_height)
            shape = pymunk.Segment(space.static_body, start_pos, end_pos, 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            
            previous_height = current_height

            if i > 3:
                checkpoints.append((start_pos + end_pos + correction) / 2)

        # Second level
        current_height -= 150
        previous_height = current_height
        for i in range(33, 3, -1):
            y = random.randint(-5, 5)
            current_height += y

            start_pos = pymunk.Vec2d(self.segment_length * i, current_height)
            end_pos = pymunk.Vec2d(self.segment_length * (i + 1), previous_height)
            shape = pymunk.Segment(space.static_body, start_pos, end_pos, 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            
            previous_height = current_height

            if i < 31:
                checkpoints.append((start_pos + end_pos + correction) / 2)

        
        # Third level
        current_height -= 150
        previous_height = current_height
        for i in range(30):
            y = random.randint(-5, 5)
            current_height += y
            
            start_pos = pymunk.Vec2d(self.segment_length * i, previous_height)
            end_pos = pymunk.Vec2d(self.segment_length * (i + 1), current_height)
            shape = pymunk.Segment(space.static_body, start_pos, end_pos, 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            
            previous_height = current_height

            if i > 3:
                checkpoints.append((start_pos + end_pos + correction) / 2)

        # Fourth level
        current_height -= 150
        previous_height = current_height
        for i in range(33, 3, -1):
            y = random.randint(-5, 5)
            current_height += y

            start_pos = pymunk.Vec2d(self.segment_length * i, current_height)
            end_pos = pymunk.Vec2d(self.segment_length * (i + 1), previous_height)
            shape = pymunk.Segment(space.static_body, start_pos, end_pos, 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            
            previous_height = current_height

            if i < 31:
                checkpoints.append((start_pos + end_pos + correction) / 2)

        # Final floor
        current_height -= 150
        previous_height = current_height
        for i in range(34):
            y = random.randint(-5, 5)
            current_height += y
            
            start_pos = pymunk.Vec2d(self.segment_length * i, previous_height)
            end_pos = pymunk.Vec2d(self.segment_length * (i + 1), current_height)
            shape = pymunk.Segment(space.static_body, start_pos, end_pos, 0.0)
            shape.friction = TERRAIN_FRICTION
            space.add(shape)
            self.terrain_shapes.append(shape)
            
            previous_height = current_height

            if i > 3:
                checkpoints.append((start_pos + end_pos + correction) / 2)

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

        return checkpoints


    def __setup_draw(self):
        self.visuals.center_x = 0
        self.visuals.center_y = 0
        for line in self.terrain_shapes:
            start_x, start_y = line.a
            end_x, end_y = line.b
            self.visuals.append(arcade.create_line(start_x, start_y, end_x, end_y, arcade.color.BLACK, 2))

    def draw(self):
        self.visuals.draw()

    def get_checkpoints(self):
        return self.checkpoints