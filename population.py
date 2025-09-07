import config
import player

class Population:
    def __init__(self, size=10):
        self.size = size
        self.players = [player.Player() for _ in range(size)]

    def update_live_players(self):
        for player in self.players:
            if player.alive:
                player.think()
                player.draw(config.window)
                player.update(config.ground)

    def extinct(self):
        return all(not player.alive for player in self.players)