from board import Board

class Checkers:
    """
    CHECKERS
    --------
    This object controles the Board object to interface this
    implementation of the game of checkers. This means it doesn't
    play out the game, but it provides the methods to do so.

    While the Board object is in charge of the actual board
    components, the Checkers object mannages the 'non physical'
    aspects of checkers, like the round count and rules like the
    forcefull captures.
    """

    def __init__(self, board_shape, initial_arrangement=[]):
        self.board = Board(board_shape, initial_arrangement)    # the game's board
        self.round = 0  # the round/turn number
        self.mid_move_piece = None  # an overwrite to the available movable pieces, necessary for moves with +1 captures

    def piece_in_pos(self, pos):
        # returns the piece object given a tile position
        return self.board.tiles[pos]

    def player_in_pos(self, pos):
        # return the player number of a piece given a tile position
        return self.piece_in_pos(pos).player

    def rank_in_pos(self, pos):
        # return the rank number of a piece given a tile position
        return self.piece_in_pos(pos).rank

    def player_turn(self):
        # returns white's turn for odd rounds, and black's turn for even rounds
        if self.round % 2 == 1:
            return 1
        else:
            return 2

    def turn_oponent(self):
        # returns white as oponent for odd rounds, and black as oponent for even rounds
        if self.round % 2 == 0:
            return 1
        else:
            return 2

    def movable_pieces_pos(self):
        # returns the pieces that can be moved by a player in the round, that is,
        # the pieces of the player with the turn
        if self.mid_move_piece != None: # obligatory capture continuation 
            return self.mid_move_piece

        movable_pos = []
        for i in range(self.board.tiles.shape[0]):
            for j in range(self.board.tiles.shape[1]):
                if self.player_in_pos((i,j)) == self.player_turn():
                    movable_pos.append((i,j))
        return movable_pos

    def update_moves(self):
        # find and stores (inside the piece object) the moves for every piece
        self.board.compute_all_moves()

    def has_legal_moves(self):
        # returns if a certain player has any moves at all (moves with and without capture together)
        has_legal_no_capture_moves, has_legal_capture_moves = self.board.has_legal_moves(self.turn_oponent())
        return has_legal_no_capture_moves or has_legal_capture_moves

    def is_capture_obligatory(self):
        # returns if there are any moves with capture to do,
        # (if there is, it is obligatory to make one of them)
        _, has_legal_capture_moves = self.board.has_legal_moves(self.player_turn())
        return has_legal_capture_moves

    def get_piece_legal_moves(self, selected_pos, concat=False):
        # returns the legal moves a given piece can make,
        # (can return the moves with and without capture separately or as one single concatenated list)
        if selected_pos in self.movable_pieces_pos(): # the piece can't have legal moves if it can't be moved
            piece = self.piece_in_pos(selected_pos)
            if self.is_capture_obligatory(): # there aren't any legal moves without captures if the capture is obligatory
                legal_no_capture_moves = []
            else:
                legal_no_capture_moves = piece.no_capture_moves
            legal_capture_moves = piece.capture_moves # but the moves with captures have no restrictions
        else:
            legal_no_capture_moves = []
            legal_capture_moves = []

        if concat:
            return legal_no_capture_moves + legal_capture_moves
        else:
            return legal_no_capture_moves, legal_capture_moves

    def promote_if_needed(self, piece, piece_pos):
        if piece_pos[1] == self.board.oponents_homeline(piece.player) and piece.rank == 1:
            piece.rank = 2

    def make_move(self, selected_pos, released_pos):
        # executes a move of a piece having the game rules in mind
        # in case the move is illegal or not finished (has another step continuation),
        # then this function returns False
        legal_piece_no_capture_moves, legal_piece_capture_moves = self.get_piece_legal_moves(selected_pos)
        piece = self.piece_in_pos(selected_pos)
        if released_pos in legal_piece_capture_moves: # is it a legal move with capture?
            captured_piece_pos = piece.get_captured_piece_pos(released_pos)
            self.board.move_piece(selected_pos, released_pos, captured_piece_pos) # then make the move
            self.board.compute_all_moves()
            _, next_legal_piece_capture_moves = self.get_piece_legal_moves(released_pos)
            if next_legal_piece_capture_moves != []: # and is there any capture continuations?
                self.mid_move_piece = [released_pos] # if so, ask for a move continuation
                return False
            else:
                self.mid_move_piece = None # if not, don't ask for a move continuation
                self.promote_if_needed(piece, released_pos) # and promote piece if needed
                return True
        elif released_pos in legal_piece_no_capture_moves: # is it a legal move without capture?
            self.board.move_piece(selected_pos, released_pos) # then make the move
            self.mid_move_piece = None # and don't ask for a move continuation
            self.promote_if_needed(piece, released_pos) # and promote piece if needed
            return True
        else:
            return False

    def advance_round(self):
        # advances the round by 1
        self.round += 1