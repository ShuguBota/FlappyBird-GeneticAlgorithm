import random
import pygame
import config

class Player:
    def __init__(self):
        # Brid
        self.x, self.y = 50, 200

        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)

        self.velocity = 0
        self.flap = False
        self.alive = True

        # AI
        self.decission = None

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

    # AI related functions
    def think(self):
        self.decission = random.uniform(0, 1)

        if self.decission > 0.8:
            self.bird_flap()