import numpy as np
from piece import Piece

def empty_tile():
    # Empty tiles are represented by player0 pieces
    return Piece(player=0)

def tile_is_empty(piece):
    # Empty tiles are represented by player0 pieces
    return (piece.player==0)

def empty_tiles(board_shape):
    tiles = np.array([[empty_tile()]*board_shape[1]]*board_shape[0], dtype=Piece.__class__)
    return tiles

class Board:
    """
    BOARD
    -----
    This object controles the Piece objects to represent the
    physical interactions one would have with a real checkers Board.
    That is, it notes the pieces positions in its tiles, 
    and allows for their movement. It also provides the methods
    to analyze if a given move is possible or not.

    Observation: the Board does not consider rules such as 
    the forcefull captures or players turn, but only more 
    'physical' rules like certifying the move ends up in a free tile.
    """

    def __init__(self, board_shape, initial_arrangement=[]):
        if initial_arrangement == []:
            tiles = empty_tiles(board_shape)
            for i in range(tiles.shape[0]): # initialize the pieces positions
            #for i in range(2): # initialize the pieces positions with less pieces for tests
                if i%2 == 0:
                    tiles[i, 1] = Piece(player=2)
                    tiles[i, -1] = Piece(player=1)
                    tiles[i, -3] = Piece(player=1)
                else:
                    tiles[i, 0] = Piece(player=2)
                    tiles[i, 2] = Piece(player=2)
                    tiles[i, -2] = Piece(player=1)
        else:
            tiles = initial_arrangement

        self.tiles = tiles  # a matrix that maps a Piece with a tile position

    def is_in_bounds(self, pos):
        # returns if the pos is inside the board
        return (pos[0]<self.tiles.shape[0] and pos[0]>=0 and pos[1]<self.tiles.shape[1] and pos[1]>=0)

    def has_piece_in(self, pos, player):
        # returns if the given position has a piece of a given player
        return (self.is_in_bounds(pos) and self.tiles[pos].player == player)

    def is_free_in(self, pos):
        # returns if the given position doesn't have any piece of player1 or player2
        return (self.is_in_bounds(pos) and tile_is_empty(self.tiles[pos]))

    def is_free_in(self, pos):
        # returns if the given position doesn't have any piece of player1 or player2
        return (self.is_in_bounds(pos) and tile_is_empty(self.tiles[pos]))

    def oponents_homeline(self, player):
        # returns if the line value of the oponet's home line
        if player == 1:
            return 0
        elif player == 2:
            return self.tiles.shape[1]-1

    def try_no_capture_given_dist(self, piece, piece_pos, di, dj, dist):
        # analyzes if a piece can make a move without capture if it moves in the direction (di,dj)
        # by a number of 'dist' of tiles.
        # It returns where it would end up in
        new_piece_position = (piece_pos[0]+di*dist, piece_pos[1]+dj*dist)
        if self.is_free_in(new_piece_position):
            return new_piece_position
        return None

    def compute_no_captures_in_direction(self, piece, piece_pos, di, dj):
        # given the direction (di,dj), for all distances of the piece to a 
        # not free tile (a tile outside the board, that is already occupied or that is
        # outside the piece's range), we can store the move as a move without capture
        dist_to_obstacle = 1
        if dj in piece.no_capture_directions: # if the direction is valid
            while dist_to_obstacle <= piece.distance_range(np.max([self.tiles.shape])): # for the dists in the piece's range
                new_piece_pos = self.try_no_capture_given_dist(piece, piece_pos, di, dj, dist_to_obstacle)
            
                if (new_piece_pos is not None): # if found no obstacle, append move and continue loop
                    piece.no_capture_moves.append(new_piece_pos)
                else: # if found some obstacle, we've reached the limit
                    break
                dist_to_obstacle += 1
        return dist_to_obstacle

    def try_capture_given_dist(self, piece, piece_pos, di, dj, dist_to_enemy, dist_after_enemy):
        # analyzes if a piece can make a move with capture if it captures a piece in the direction (di,dj)
        # and by a distance of tiles 'dist_to_enemy'; and also ends up in the direction (di,dj) by a
        # distance of 'dist_after_enemy'.
        # It returns where it would end up in and the captured piece position
        new_piece_pos = (piece_pos[0]+di*dist_to_enemy+di*dist_after_enemy,piece_pos[1]+dj*dist_to_enemy+dj*dist_after_enemy)
        if self.is_free_in(new_piece_pos):
            return new_piece_pos
        return None

    def compute_captures_in_direction(self, piece, piece_pos, di, dj, dist_to_obstacle):
        # given the direction (di,dj) and the distance to an obstacle, if the obstacle is an
        # enemy piece, for all distances after the capture of the piece to a 
        # not free tile (a tile outside the board, that is already occupied or that is
        # outside the piece's range of capture), we can store the move as a move with capture
        dist_after_obstacle = 1
        obstacle_pos = (piece_pos[0]+di*dist_to_obstacle, piece_pos[1]+dj*dist_to_obstacle)
        enemy_player = piece.oponent_player
        if self.has_piece_in(obstacle_pos, enemy_player):
            if dj in piece.capture_directions: # if the direction is valid
                while dist_after_obstacle <= piece.distance_range(np.max([self.tiles.shape])): # for the dists in the piece's range
                    new_piece_pos = self.try_capture_given_dist(piece, piece_pos, di, dj, dist_to_obstacle, dist_after_obstacle)
                
                    if (new_piece_pos is not None): # if found no obstacle after enemy, append move and continue loop
                        piece.capture_moves.append(new_piece_pos)
                        piece.captured_capture_moves.append(obstacle_pos)
                    else: # if found some obstacle, we've reached the limit
                        break
                    dist_after_obstacle += 1

    def compute_piece_moves(self, piece, piece_pos):
        # finds and stores the piece's moves, checking in every direction
        for di in [1, -1]: # for all directions
            for dj in [1, -1]:
                dist_to_obstacle = self.compute_no_captures_in_direction(piece, piece_pos, di, dj)
                if dist_to_obstacle <= piece.distance_range(np.max([self.tiles.shape])): # condition of distance TO enemy in captures
                    self.compute_captures_in_direction(piece, piece_pos, di, dj, dist_to_obstacle)                   

    def compute_all_moves(self):
        # find and stores (inside the piece object) the moves for every piece
        for i in range(self.tiles.shape[0]):
            for j in range(self.tiles.shape[1]):
                piece = self.tiles[(i,j)]
                if not tile_is_empty(piece):
                    piece.no_capture_moves, piece.capture_moves, piece.captured_capture_moves = [],[],[]
                    self.compute_piece_moves(piece, (i,j))

    def has_legal_moves(self, player):
        # returns if a certain player has any moves (moves with and without capture, separately)
        has_legal_capture_moves = False
        has_legal_no_capture_moves = False
        for i in range(self.tiles.shape[0]):
            for j in range(self.tiles.shape[1]):
                piece = self.tiles[(i,j)]
                if not tile_is_empty(piece) and piece.player == player:
                    has_legal_capture_moves = has_legal_capture_moves or piece.has_legal_capture_moves()
                    has_legal_no_capture_moves = has_legal_no_capture_moves or piece.has_legal_no_capture_moves()
        return has_legal_no_capture_moves, has_legal_capture_moves

    def move_piece(self, old_pos, new_pos, captured_pos=None):
        # executes a move of a piece from the old position to a new one 
        # and captures the piece in the specified position (if there is one)
        piece = self.tiles[old_pos]
        self.tiles[old_pos] = empty_tile()
        self.tiles[new_pos] = piece
        if captured_pos != None:
            self.tiles[captured_pos] = empty_tile()