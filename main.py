import pygame
from game_wrapper import GameWrapper
from renderer import Renderer

pygame.init()

# Game screen
screen_shape = (800, 720)
screen = pygame.display.set_mode(screen_shape)

# Screen title and icon
pygame.display.set_caption("Jogo de Damas")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Game loop objects
board_shape = (8,8)
game = GameWrapper(board_shape) # game state machine
renderer = Renderer(screen_shape, board_shape) # render objects

# GAME LOOP
running = True
while running:
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse_did_pressdown = (event.type == pygame.MOUSEBUTTONDOWN)
        mouse_did_pressup = (event.type == pygame.MOUSEBUTTONUP)
        mouse_tile_pos = renderer.map_tile(pygame.mouse.get_pos())
            
    # GAME STATES 
    game.take_inputs(mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos)
    game.update()
    #game.print_debugs()
    if game.running == False:
        running = False

    # RENDERING   
    renderer.render(screen, game)