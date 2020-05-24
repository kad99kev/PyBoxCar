import arcade
import pymunk

class Wheel:

    def __init__(self, space, position, radius):
        self.radius = radius
        self.mass = 10 # TODO: Adjust and make constant
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)

        space.add(self.body, self.shape)

        self.visuals = arcade.ShapeElementList()

    def setup_draw(self, center):
        self.visuals.center_x = center.x
        self.visuals.center_y = center.y

        # Draws the wheel
        w_pos_x = self.body.position.x
        w_pos_y = self.body.position.y
        print(w_pos_x, w_pos_y)
        shape = arcade.create_ellipse_filled(w_pos_x, w_pos_y, self.radius, self.radius, arcade.color.GRAY)
        self.visuals.append(shape)
        
        # Draws the orientation of wheel
        end = self.body.position + self.body.rotation_vector * self.radius
        shape = arcade.create_line(w_pos_x, w_pos_y, end.x , end.y, arcade.color.BLACK, 2)
        self.visuals.append(shape)

    def update_visuals(self, center):
        self.visuals.center_x = center.x
        self.visuals.center_y = center.y
        self.visuals.angle = self.body.angle

    def draw(self):
        self.visuals.draw()
