import random
import math

from constants import NUM_CARS, MUTATION_RATE, SIZE, VERTICES, WHEEL_SPEED, WHEEL_RADIUS
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
    midpoint = random.randint(0, VERTICES)
    for i, p_zip in enumerate(zip(parent_1, parent_2)):
        p_1, p_2 = p_zip
        if i < midpoint:
            child_gene.append(list(p_1))
        else:
            child_gene.append(list(p_2))
    child_gene = _mutate(child_gene)
    child_gene = sorted(child_gene, key=lambda point: math.atan2(point[0][1], point[0][0]))
    child = Chromosome(child_gene)
    return child

def _mutate(child_gene):
    # child_gene = []
    for i in range(len(child_gene)):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5:
                new_vertex = _generate_new_vertex()
                child_gene[i][0] = new_vertex
            else:
                new_wheel = _generate_new_wheel()
                child_gene[i][1] = new_wheel
    return child_gene

def _generate_new_vertex():
    x_cor = random.randrange(-SIZE, SIZE)
    y_cor = random.randrange(-SIZE, SIZE)
    new_vertex = (x_cor, y_cor)
    return new_vertex

def _generate_new_wheel():
    wheel_index = random.randrange(-1, VERTICES)
    if wheel_index == -1:
        return [-1, -1]
    wheel_radius = random.randint(5, WHEEL_RADIUS)
    wheel_speed = random.randint(-WHEEL_SPEED, WHEEL_SPEED)
    return [wheel_radius, wheel_speed]