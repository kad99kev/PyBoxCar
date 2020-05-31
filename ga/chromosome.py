import random
import math

from constants import SIZE, VERTICES, WHEEL_SPEED, WHEEL_RADIUS

class Chromosome:
    '''
    The Chromosome class.
    Contains genes.
    It is associated with the BoxCar class.
    '''

    def __init__(self, genes):
        self.genes = genes
    
    def get_vertices(self):
        '''
        Returns the vertices information present in the genes.
        '''

        return [g[0] for g in self.genes]
    
    def get_genes(self):
        '''
        Returns the genes.
        '''

        return self.genes

    @classmethod
    def generate_inital_chromosome(cls):
        '''
        Generates an inital chromosome for the first generation based on randomness.
        '''

        genes = []

        for _ in range(VERTICES):
            # Generates a random vertex.
            x_cor = random.randrange(-SIZE, SIZE)
            y_cor = random.randrange(-SIZE, SIZE)
            # Choosing a vertex for the wheel.
            wheel_index = random.randrange(-1, VERTICES)
            if wheel_index == -1:
                wheel_info = [-1, -1]
            else:
                wheel_radius = random.randint(5, WHEEL_RADIUS)
                wheel_speed = random.randint(-WHEEL_SPEED, WHEEL_SPEED)
                wheel_info = [wheel_radius, wheel_speed]
            genes.append([(x_cor, y_cor), wheel_info])
        
        # Sorting the co-ordinates for smooth drawing.
        genes = sorted(genes, key=lambda point: math.atan2(point[0][1], point[0][0]))

        return cls(genes)