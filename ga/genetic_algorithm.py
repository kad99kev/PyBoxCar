import random
import math

from constants import NUM_CARS, MUTATION_RATE, SIZE, VERTICES, NUM_WHEELS, WHEEL_SPEED, WHEEL_RADIUS
from .chromosome import Chromosome

def evolve(population):
    normalized_population = _normalize(population)
    new_population = []
    for _ in range(NUM_CARS):
        parent_1 = _pick_one(normalized_population)
        parent_2 = _pick_one(normalized_population)
        new_child = _reproduce(parent_1, parent_2)
        new_population.append(new_child)
    return new_population

def _normalize(population):
    p_sum = 0
    for p in population:
        p_sum += p['score']

    for p in population:
        p['score'] /= p_sum

    return population

def _pick_one(population):
        index = 0
        r = random.random()

        while r > 0:
            r -= population[index]['score']
            index += 1

        index -= 1
        return population[index]['gene']

def _reproduce(parent_1, parent_2):
    child_gene = []
    midpoint = random.randint(0, len(parent_1))
    for i in range(len(parent_1)):
        if i < midpoint:
            child_gene.append(parent_1[i])
        else:
            child_gene.append(parent_2[i])
    child_gene = _mutate(child_gene)
    sort_vert = sorted(child_gene[:VERTICES], key=lambda point: math.atan2(point[1], point[0]))
    child_gene[:VERTICES] = sort_vert
    child = Chromosome(child_gene)
    return child

def _mutate(child_gene):
    for index in range(len(child_gene)):
        if random.random() < MUTATION_RATE:
            gene_type = child_gene[index]
            if isinstance(gene_type, tuple):
                mutation = _generate_new_vertex(child_gene)
            else:
                mutation = _generate_new_wheel(child_gene)
            child_gene[index] = mutation
    return child_gene

def _generate_new_vertex(child_gene):
    x_cor = random.randrange(-SIZE, SIZE)
    y_cor = random.randrange(-SIZE, SIZE)
    new_vertex = (x_cor, y_cor)
    return new_vertex



def _generate_new_wheel(child_gene):
    wheel_index = random.randrange(-1, VERTICES)
    if wheel_index == -1:
        return [(-1, -1), -1, -1]
    wheel_vertex = child_gene[wheel_index]
    wheel_radius = random.randint(1, WHEEL_RADIUS)
    wheel_speed = random.randint(-WHEEL_SPEED, WHEEL_SPEED)
    wheel_gene = [wheel_vertex, wheel_radius, wheel_speed]
    if wheel_gene in child_gene:
        return [(-1, -1), -1, -1]
    return wheel_gene

