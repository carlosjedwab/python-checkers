import pygame

class Renderer:
    """
    RENDERER
    ------------
    This object handles the rendering of the game.

    In this implementation, there are only two types of
    rendered object:
    the tiles (varies with 4 colors) and the pieces (varies with 2 colors).

    They are both rendered in various positions to show in screen.
    """

    def __init__(self, screen_shape, board_shape):
        self.board_shape = board_shape
        # Tile square colors
        self.NORMAL_WHITE=(237, 218, 166)
        self.NORMAL_BLACK=(176, 123, 70)
        self.GLOWING_WHITE=(242, 226, 82)
        self.GLOWING_BLACK=(209, 169, 38)

        # Tile square shape
        self.tile_width = int(screen_shape[0]/self.board_shape[0])
        self.tile_height = int(screen_shape[1]/self.board_shape[1])

        # Piece image shape
        self.piece_width = int(self.tile_width * 0.8)
        self.piece_height = int(self.tile_height * 0.8)

        # Player 1 normal piece image
        self.piece1Img = pygame.image.load('assets/piece1.png')
        self.piece1Img = pygame.transform.scale(self.piece1Img, (self.piece_width, self.piece_height))

        # Player 2 normal piece image
        self.piece2Img = pygame.image.load('assets/piece2.png')
        self.piece2Img = pygame.transform.scale(self.piece2Img, (self.piece_width, self.piece_height))

        # Player 1 queen piece image
        self.queen1Img = pygame.image.load('assets/queen1.png')
        self.queen1Img = pygame.transform.scale(self.queen1Img, (self.piece_width, self.piece_height))

        # Player 2 queen piece image
        self.queen2Img = pygame.image.load('assets/queen2.png')
        self.queen2Img = pygame.transform.scale(self.queen2Img, (self.piece_width, self.piece_height))

    def map_tile(self, mouse_pos):
        # This function maps a mouse position to a tile position
        i = int(mouse_pos[0]/self.tile_width)
        j = int(mouse_pos[1]/self.tile_height)
        return (i, j)

    def draw_tile_rect(self, screen, pos, glowing_tiles):
        # render the tile with the collor based in the position and if it is glowing or not
        if (pos[0]+pos[1])%2: # render in a chess board style
            if pos not in glowing_tiles:
                color = self.NORMAL_BLACK
            else:
                color = self.GLOWING_BLACK
        else:
            if pos not in glowing_tiles:
                color = self.NORMAL_WHITE
            else:
                color = self.GLOWING_WHITE
        tile_posx = pos[0]*self.tile_width
        tile_posy = pos[1]*self.tile_height
        pygame.draw.rect(screen, color, (tile_posx, tile_posy, self.tile_width, self.tile_height))

    def draw_piece_img(self, screen, pos, player, rank):
        # renders the piece given the piece's player
        offset = ((self.tile_width-self.piece_width)/2, (self.tile_height-self.piece_height)/2)
        piece_render_pos = (pos[0]*self.tile_width+offset[0], pos[1]*self.tile_height+offset[1])
        if rank == 1:
            if player == 1:
                screen.blit(self.piece1Img, piece_render_pos)
            elif player == 2:
                screen.blit(self.piece2Img, piece_render_pos)
        elif rank == 2:
            if player == 1:
                screen.blit(self.queen1Img, piece_render_pos)
            elif player == 2:
                screen.blit(self.queen2Img, piece_render_pos)

    def render(self, screen, game):
        screen.fill([255,255,255])

        glowing_tiles = game.glowing_tiles
        for i in range(self.board_shape[0]):
            for j in range(self.board_shape[1]):
                pos = (i,j)
                self.draw_tile_rect(screen, pos, glowing_tiles)
                self.draw_piece_img(screen, pos, game.checkers.player_in_pos(pos), game.checkers.rank_in_pos(pos))

        pygame.display.flip()
        pygame.display.update()