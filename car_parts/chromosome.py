import random
import math

from constants import SEED, SIZE, VERTICES, NUM_WHEELS, WHEEL_SPEED, WHEEL_RADIUS

class Chromosome:

    def __init__(self, genes):
        self.genes = genes
        self.score = 0
        self.fitness = 0

        self.wheel_genes = []
        for i in range(NUM_WHEELS, 0, -1):
            self.wheel_genes.append(self.genes[-i])

    def update_score(self):
        self.score += 0
    
    def get_vertices(self):
        return self.genes[:6]

    def wheels_info(self):
        return tuple(self.wheel_genes)
    
    def get_genes(self):
        return self.genes

    @classmethod
    def generate_inital_chromosome(cls):
        genes = []

        random.seed(SEED)
        for _ in range(VERTICES):
            x_cor = random.randrange(-SIZE, SIZE)
            y_cor = random.randrange(-SIZE, SIZE)
            genes.append(((x_cor, y_cor)))
        
        genes = sorted(genes, key=lambda point: math.atan2(point[1], point[0]))
        wheel_genes = []
        wheel_indices = []
        for _ in range(NUM_WHEELS):
            wheel_index = random.randrange(-1, len(genes))
            if wheel_index == -1 or wheel_index in wheel_indices:
                wheel_genes.extend([[(-1, -1), -1, -1]])
                continue
            wheel_indices.append(wheel_index)
            wheel_vertex = genes[wheel_index]
            wheel_radius = random.randint(0, WHEEL_RADIUS)
            wheel_speed = random.randint(-WHEEL_SPEED, WHEEL_SPEED)
            wheel_genes.extend([[wheel_vertex, wheel_radius, wheel_speed]])

        genes.extend(wheel_genes)
        
        
        print(f'Genes Generated: {genes}')

        return cls(genes)