import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size=1000):
        self.size = size
        self.players = [player.Player() for _ in range(size)]
        self.generation = 1
        self.species = []

    def update_live_players(self):
        for player in self.players:
            if player.alive:
                player.look()
                player.think()
                player.draw(config.window)
                player.update(config.ground)

    def natural_selection(self):
        print('Spawning new generation')

        self.speciate()
        self.calculate_fitness()
        self.kill_extinct_species()
        self.kill_stale_species()
        self.sort_species_by_fitness()
        self.next_generation()

    def speciate(self):
        for specie in self.species:
            specie.players = []

        for player in self.players:
            add_to_species = False

            for specie in self.species:
                if specie.similarity(player.brain):
                    specie.add_to_species(player)
                    add_to_species = True
                    break

            if not add_to_species:
                self.species.append(species.Species(player))

    def calculate_fitness(self):
        for player in self.players:
            player.calculate_fitness()
        
        for specie in self.species:
            specie.calculate_average_fitness()

    # Remove species that have no players
    def kill_extinct_species(self):
        species_bin = []

        for specie in self.species:
            if len(specie.players) == 0:
                species_bin.append(specie)
        
        for specie in species_bin:
            self.species.remove(specie)

    # Remove species that haven't improved in 15 generations
    def kill_stale_species(self):
        players_bin = []
        species_bin = []

        for specie in self.species:
            if specie.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(specie)
                    
                    for player in specie.players:
                        players_bin.append(player)
                
                else:
                    specie.staleness = 0
            
        for player in players_bin:
            self.players.remove(player)
        
        for specie in species_bin:
            self.species.remove(specie)


    def sort_species_by_fitness(self):
        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_generation(self):
        children = []

        # Clone the champion of each species
        for specie in self.species:
            children.append(specie.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))

        for specie in self.species:
            for _ in range(children_per_species):
                children.append(specie.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []

        for child in children:
            self.players.append(child)

        self.generation += 1

        print(f'Generation: {self.generation} | Species: {len(self.species)}')

    def extinct(self):
        return all(not player.alive for player in self.players)