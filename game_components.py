import pygame
import random

class Ground:
    ground_level = 500

    def __init__(self, window_width):
        self.x, self.y = 0, self.ground_level
        self.rect = pygame.Rect(self.x, self.y, window_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    width = 15
    opening = 100

    def __init__(self, window_height):
        self.x = window_height

        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.botttom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(window, (255, 255, 255), self.bottom_rect)

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(window, (255, 255, 255), self.top_rect)

    def update(self):
        self.x -= 1

        # Check if the pipe has been passed by the bird
        if self.x + Pipes.width <= 50:
            self.passed = True

        # Check if the pipe is off the screen
        if self.x  <= -self.width:
            self.off_screen = True