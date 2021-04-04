class Piece:
    """
    PIECE
    --------
    This object controles represents the piece one would have 
    in a real checkers game. It is defined by the piece's 
    player (or team or color), rank (normal piece or queen),
    and the pieces possible moves.

    The piece's possible moves is represented by three lists:
        - no_capture_moves, which stores the possible positions for a 
          move withou a capture
        - capture_moves and captured_capture_moves, which stores the
          possible final piece positions and captured piece positions,
          respectively, for moves with a capture.
    """

    def __init__(self, player, rank = 1):
        self.player = player                # player/team/color number (player0 is like an empty piece)
        self.rank = rank                    # rank1 is normal piece, rank2 is a queen
        self.no_capture_moves = []          # lists of positions to move to without a piece being captured
        self.capture_moves = []             # lists of positions to move to with a piece being captured
        self.captured_capture_moves = []    # lists of positions of the captured piece relative to the self.capture_moves list

    @property
    def oponent_player(self):
        # returns the number of the oponent player
        if self.player == 1:
            return 2
        elif self.player == 2:
            return 1
    @property
    def no_capture_directions(self):
        # returns the vertical directions that the piece advances for a move without capture
        # (can only move forward in rank1, and both directions in rank2)
        if self.rank == 1:
            if self.player == 1:
                return [-1]
            elif self.player == 2:
                return [1]
        elif self.rank == 2:
            return [1,-1]

    @property
    def capture_directions(self):
        # returns the vertical directions that the piece advances for a move with capture
        # (can capture moving to both directions)
        return [1,-1]

    def distance_range(self, max_possible_value):
        # returns the distances that the piece advances for any move
        if self.rank == 1:
            return 1
        elif self.rank == 2:
            return max_possible_value

    def has_legal_capture_moves(self):
        # returns if the piece has any possible moves with a capture
        return (self.capture_moves)!=[]

    def has_legal_no_capture_moves(self):
        # returns if the piece has any possible moves without a capture
        return (self.no_capture_moves)!=[]

    def get_captured_piece_pos(self, final_pos):
        # given a move position, returns the captured oponent piece position
        if final_pos in self.capture_moves:
            for i in range(len(self.capture_moves)):
                if self.capture_moves[i] == final_pos:
                    break
            return self.captured_capture_moves[i]
        else:
            return None