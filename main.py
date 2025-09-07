import config
import pygame
import game_components
import population

from sys import exit

pygame.init()
clock = pygame.time.Clock()

population = population.Population()

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def generate_pipes():
    config.pipes.append(game_components.Pipes(config.window_width))

def main():
    pipes_spawn_time = 10

    while True:
        # Setup
        quit_game()
        config.window.fill((0, 0, 0))

        # Check if all players are dead
        if population.extinct():
            pass


        # Draw ground
        config.ground.draw(config.window)

        # Draw pipes
        if pipes_spawn_time <= 10:
            generate_pipes()
            pipes_spawn_time = 200

        for pipe in config.pipes:
            pipe.draw(config.window)
            pipe.update()
            if pipe.off_screen:
                config.pipes.remove(pipe)

        pipes_spawn_time -= 1

        # Draw population
        population.update_live_players()

        clock.tick(60)
        pygame.display.flip()

main()        
