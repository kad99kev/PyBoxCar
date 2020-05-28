# MainScreen
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 800
SCREEN_TITLE = "BoxCar"

# Space
DT = 1 / 120.0
GRAVITY = (0, -980)

# Terrain
TERRAIN_FRICTION = 1

# BoxCar
START_POSITION = (100, SCREEN_HEIGHT - 100)
SEED = 3

# Genes
SIZE = 40
VERTICES = 6
NUM_WHEELS = 4 # Keep the number of wheels less than the vertices, else you'll get buggy behaviour!
WHEEL_SPEED = 20
WHEEL_RADIUS = 8

# Chassis
CHASSIS_FRICTION = 0.
CHASSIS_MASS = 50

# Wheel
WHEEL_FRICTION = 1
WHEEL_MASS = 10


# Seed 0 both wheels same position
# Seed 1 one wheel deactivates
# Seed 3 okay