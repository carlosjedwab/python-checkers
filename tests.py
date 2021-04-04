import pygame
from game_wrapper import GameWrapper
from renderer import Renderer
from board import empty_tiles, tile_is_empty
from piece import Piece

# ----------------------------------------------------------------------------------- Tests utils

def update_game(game, renderer, mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos):    
    # GAME STATES 
    game.take_inputs(mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos)
    game.update()
    #game.print_debugs()
    if game.running == False:
        running = False

    # RENDERING   
    renderer.render(screen, game)

def press_at(game, renderer, pos):
    # press in the piece at pos
    mouse_did_pressdown = True
    mouse_did_pressup = False
    mouse_tile_pos = pos
    for _ in range(5):
        update_game(game, renderer, mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos)

def unpress_at(game, renderer, pos):
    # unpress in the piece at pos
    mouse_did_pressdown = False
    mouse_did_pressup = True
    mouse_tile_pos = pos
    for _ in range(5):
        update_game(game, renderer, mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos)

def wait(game, renderer, pos, n=200):
    # wait a few iterations (mostly for visible test purposes)
    mouse_did_pressdown = False
    mouse_did_pressup = False
    mouse_tile_pos = pos
    for _ in range(n):
        update_game(game, renderer, mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos)

def make_move(game, renderer, from_pos, to_pos):
    # make a move from a position to another
    # click in the piece at from_pos
    press_at(game, renderer, from_pos)
    unpress_at(game, renderer, from_pos)
    wait(game, renderer, from_pos)
    # make the move to to_pos
    press_at(game, renderer, to_pos)
    unpress_at(game, renderer, to_pos)
    wait(game, renderer, to_pos)

# ----------------------------------------------------------------------------------- Tests initiation

pygame.init()

# Game screen
screen_shape = (800, 720)
screen = pygame.display.set_mode(screen_shape)

# Screen title and icon
pygame.display.set_caption("Jogo de Damas - testes")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# ----------------------------------------------------------------------------------- Tests cases

def move_test_case():
    # Tests if two game moves work

    # Game loop objects
    board_shape = (8,8)

    game = GameWrapper(board_shape) # game state machine
    renderer = Renderer(screen_shape, board_shape) # render objects

    # GAME LOOP

    # make the white move from (0,5) -> (1,4)
    make_move(game, renderer, (0,5), (1,4))
    # assert the piece was moved correctly
    assert(tile_is_empty(game.checkers.piece_in_pos((0,5))))
    assert(game.checkers.board.has_piece_in(pos=(1,4), player=1))
    # make the black move from (1,2) -> (0,3)
    make_move(game, renderer, (1,2), (0,3))
    # assert the piece was moved correctly
    assert(tile_is_empty(game.checkers.piece_in_pos((1,2))))
    assert(game.checkers.board.has_piece_in(pos=(0,3), player=2))

def capture_test_case():
    # Tests if a rank1 capture works

    # Game loop objects
    board_shape = (8,8)

    # initial tiles
    initial_tiles = empty_tiles(board_shape)
    initial_tiles[3, 4] = Piece(player=1)
    initial_tiles[5, 2] = Piece(player=2)

    game = GameWrapper(board_shape, initial_tiles) # game state machine
    renderer = Renderer(screen_shape, board_shape) # render objects

    # GAME LOOP

    # make the white move from (3,4) -> (4,3)
    make_move(game, renderer, (3,4), (4,3))
    # assert the capture is obligatory
    assert(game.checkers.is_capture_obligatory() == True)
    # make the capture
    make_move(game, renderer, (5,2), (3,4))
    # assert the piece was captured correctly
    assert(tile_is_empty(game.checkers.piece_in_pos((5,2))))
    assert(tile_is_empty(game.checkers.piece_in_pos((4,3))))
    assert(game.checkers.board.has_piece_in(pos=(3,4), player=2))

def capture_continuation_test_case():
    # Tests if a rank1 capture works

    # Game loop objects
    board_shape = (8,8)

    # initial tiles
    initial_tiles = empty_tiles(board_shape)
    initial_tiles[7, 2] = Piece(player=1)
    initial_tiles[6, 1] = Piece(player=2)
    initial_tiles[4, 1] = Piece(player=2)

    game = GameWrapper(board_shape, initial_tiles) # game state machine
    renderer = Renderer(screen_shape, board_shape) # render objects

    # GAME LOOP

    # make the capture
    make_move(game, renderer, (7,2), (5,0))
    # assert the capture is obligatory
    assert(game.checkers.is_capture_obligatory() == True)
    # assert there is a capture continuation
    assert(game.checkers.mid_move_piece != None)
    # make the capture continuation
    make_move(game, renderer, (5,0), (3,2))
    # assert the two pieces were captured correctly
    assert(tile_is_empty(game.checkers.piece_in_pos((7,2))))
    assert(tile_is_empty(game.checkers.piece_in_pos((6,1))))
    assert(tile_is_empty(game.checkers.piece_in_pos((5,0))))
    assert(tile_is_empty(game.checkers.piece_in_pos((4,1))))
    assert(game.checkers.board.has_piece_in(pos=(3,2), player=1))
    # assert also that the piece was NOT promoted in the continuation
    assert(game.checkers.piece_in_pos((7,0)).rank==1)
    

def complex_test_case():
    # Test if a promotion, a queen capture, a queen capture continuation and a game winner works

    # Game loop objects
    board_shape = (8,8)

    # initial tiles
    initial_tiles = empty_tiles(board_shape)
    initial_tiles[6, 1] = Piece(player=1)
    initial_tiles[4, 3] = Piece(player=2)
    initial_tiles[3, 4] = Piece(player=2)

    game = GameWrapper(board_shape, initial_tiles) # game state machine
    renderer = Renderer(screen_shape, board_shape) # render objects

    # GAME LOOP

    # make the white move from (6,1) -> (7,0)
    make_move(game, renderer, (6,1), (7,0))
    # assert the piece was promoted
    assert(game.checkers.piece_in_pos((7,0)).rank==2)
    # make the black move from (3,4) -> (2,5)
    make_move(game, renderer, (3,4), (2,5))
    # assert the piece was moved correctly
    assert(tile_is_empty(game.checkers.piece_in_pos((3,4))))
    assert(game.checkers.board.has_piece_in(pos=(2,5), player=2))
    # assert the capture is obligatory
    assert(game.checkers.is_capture_obligatory() == True)
    # make the capture
    make_move(game, renderer, (7,0), (3,4))
    # assert there is a capture continuation
    assert(game.checkers.mid_move_piece != None)
    # make the capture
    make_move(game, renderer, (3,4), (0,7))
    # assert white (player 1) won
    assert(game.winner == 1)

# ----------------------------------------------------------------------------------- Tests executions    

move_test_case()
capture_test_case()
capture_continuation_test_case()
complex_test_case()