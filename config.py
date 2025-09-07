import pygame
import game_components

window_height = 720
window_width = 550

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird - Genetic Alogrithm")

ground = game_components.Ground(window_width)
pipes = []
