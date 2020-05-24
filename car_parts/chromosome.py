class Chromosome:

    def __init__(self, genes):
        self.genes = genes
        self.score = 0
        self.fitness = 0

    def update_score(self):
        self.score += 0
    
    def get_vertices(self):
        return self.genes[:6]

    def wheels_info(self):
        return self.genes[-4:-2], self.genes[-2:]
    
    def get_genes(self):
        return self.genes