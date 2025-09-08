import random
import pygame
import config
import brain

class Player:
    def __init__(self):
        # Brid
        self.x, self.y = 50, 200

        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)

        self.velocity = 0
        self.flap = False
        self.alive = True

        self.lifespan = 0

        # AI
        self.decission = None
        self.vision = [0.5, 1, 0.5] # Position of the player relative to the pipes
        self.fitness = 0
        self.inputs = 3

        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        # Making the color go brr
        self.color = tuple((c + 3) % 255 for c in self.color)

        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    
    def sky_collision(self):
        return bool(self.rect.y < 30)
    
    def pipe_collision(self):
        for pipe in config.pipes:
            return pygame.Rect.colliderect(self.rect, pipe.top_rect) or pygame.Rect.colliderect(self.rect, pipe.bottom_rect)
    
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.velocity += 0.25
            self.rect.y += self.velocity
            if self.velocity > 5:
                self.velocity = 5
            # Lifespan
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.velocity = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.velocity = -5
            self.flap = True
        
        if self.velocity >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        # Pipes are in order already so we can just return the first one that hasn't been passed yet
        for pipe in config.pipes:
            if not pipe.passed:
                return pipe
            
    def look(self):
        if config.pipes:
            # Line to the top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center, (self.rect.center[0], config.pipes[0].top_rect.bottom))

            # line to the mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center, (config.pipes[0].x, self.rect.center[1]))

            # Line to the bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center, (self.rect.center[0], config.pipes[0].bottom_rect.top))

    # AI related functions
    def think(self):
        self.decission = self.brain.feed_forward(self.vision)

        if self.decission > 0.73: # TODO: Understand why the heck when it was 0.8 it didn't work
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()

        return clone