import random
import math

from constants import SIZE, VERTICES, WHEEL_SPEED, WHEEL_RADIUS

class Chromosome:

    def __init__(self, genes):
        self.genes = genes
        self.score = 0
        self.fitness = 0

    def update_score(self):
        self.score += 0
    
    def get_vertices(self):
        return [g[0] for g in self.genes]
    
    def get_genes(self):
        return self.genes

    @classmethod
    def generate_inital_chromosome(cls):
        genes = []

        for _ in range(VERTICES):
            x_cor = random.randrange(-SIZE, SIZE)
            y_cor = random.randrange(-SIZE, SIZE)
            wheel_index = random.randrange(-1, VERTICES)
            if wheel_index == -1:
                wheel_info = [-1, -1]
            else:
                wheel_radius = random.randint(5, WHEEL_RADIUS)
                wheel_speed = random.randint(-WHEEL_SPEED, WHEEL_SPEED)
                wheel_info = [wheel_radius, wheel_speed]
            genes.append([(x_cor, y_cor), wheel_info])
        
        genes = sorted(genes, key=lambda point: math.atan2(point[0][1], point[0][0]))

        return cls(genes)