import operator
import random

class Species:
    def __init__(self, player):
        self.players = [player]
        self.average_fitness = 0
        self.threshold = 1.2 # Decission of what players will be added to the species
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone()
        self.champion = player.clone()
        self.staleness = 0

    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)

        return similarity < self.threshold
    
    @staticmethod
    def weight_difference(brain_1, brain_2):
        total_weight_difference = 0

        for i in range(0, len(brain_1.connections)):
            for j in range(0, len(brain_2.connections)):
                if i == j:
                    total_weight_difference += abs(brain_1.connections[i].weight - brain_2.connections[j].weight)

        return total_weight_difference
    
    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)

        if self.players[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0

        for player in self.players:
            total_fitness += player.fitness

        self.average_fitness = total_fitness / len(self.players) if len(self.players) > 0 else 0

    def offspring(self):
        # Exclude index 0 because it's the champion which is already set
        baby = self.players[random.randint(1, len(self.players)) - 1].clone() 
        baby.brain.mutate()

        return baby




