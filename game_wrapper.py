from checkers import Checkers

class GameWrapper:
    """
    GAME WRAPPER
    ------------
    This object controles the Checker object to play out checkers.
    It does that with a number of game states, them being:
    [new_game, new_round, waiting_for_move, selection, drag_and_place, click_and_place, end_round, game_over, end_game]

    Using this game states machine, this object determines when each method
    from the Checkers object should be executed. And finally, with that, 
    eventual alterations to the game's functions related to the playability
    (like adding a menu screen or a starting screen) are facilitated.
    """

    def __init__(self, board_shape, initial_arrangement=[]):
        self.running = True
        self.board_shape = board_shape
        self.game_state = self.new_game # initial game state
        self.update(initial_arrangement) # a first update
        self.winner = None

    @property
    def glowing_tiles(self):
        if self.selected_tile!=None:
            glowing_tiles = self.checkers.get_piece_legal_moves(self.selected_tile, concat=True)
        else:
            glowing_tiles = []
        return glowing_tiles

    def take_inputs(self, mouse_did_pressdown, mouse_did_pressup, mouse_tile_pos):
        self.mouse_did_pressdown = mouse_did_pressdown
        self.mouse_did_pressup = mouse_did_pressup
        self.mouse_tile_pos = mouse_tile_pos

    def update(self, *args):
        self.game_state(*args)

    # STATES MACHINE ----------------------------------------------------------------------------------

    def new_game(self, initial_arrangement=None):
        # Starts a new game and game board
        self.checkers = Checkers(self.board_shape, initial_arrangement)
        self.game_state = self.new_round
        self.selected_tile = None
        self.released_tile = None
        self.selected_tile2 = None
        # Prints--------------------------------
        print("STARTING NEW GAME")

    def new_round(self):
        # Initializes the game logic parameter,
        # updates all the legal moves of this round,
        # and starts a new round
        self.selected_tile = None
        self.released_tile = None
        self.selected_tile2 = None
        self.checkers.update_moves()
        self.checkers.advance_round()
        self.game_state = self.waiting_for_move
        # Prints--------------------------------
        if self.checkers.player_turn() == 1:
            print("--> white's turn")
        else:
            print("--> black's turn")

    def waiting_for_move(self):
        # Waits for a mouse button press on top of a movable pice
        if self.mouse_did_pressdown:
            self.selected_tile = self.mouse_tile_pos
            if self.selected_tile in self.checkers.movable_pieces_pos():
                self.game_state = self.selection

    def selection(self):
        # There are two ways to move a piece:
        # either the mouse button press is dragged to the move position,
        # or the mouse button is quickly released, and the move position is clicked afterwards
        if self.mouse_did_pressup:
            self.released_tile = self.mouse_tile_pos
            if self.released_tile == self.selected_tile:
                self.game_state = self.click_and_place
            else:
                self.game_state = self.drag_and_place

    def drag_and_place(self):
        # The mouse button press is dragged to a legal move position
        ended_turn = self.checkers.make_move(self.selected_tile, self.released_tile)
        if ended_turn:
            self.game_state = self.end_round
        else:
            self.released_tile = None
            self.game_state = self.waiting_for_move

    def click_and_place(self):
        # The mouse button is quickly released (released in the same tile), 
        # and the move position is clicked afterwards as a second click
        if self.mouse_did_pressdown:
            self.selected_tile2 = self.mouse_tile_pos
            if self.selected_tile2 == self.selected_tile:
                self.selected_tile = None
                self.released_tile = None
                self.selected_tile2 = None
                self.game_state = self.waiting_for_move
            else:
                if self.checkers.player_in_pos(self.selected_tile2) == self.checkers.player_turn():
                    self.selected_tile = self.selected_tile2
                    self.released_tile = None
                    self.selected_tile2 = None
                    self.game_state = self.selection
                else:
                    ended_turn = self.checkers.make_move(self.selected_tile, self.selected_tile2)
                    if ended_turn:
                        self.game_state = self.end_round
                    else:
                        self.released_tile = None
                        self.game_state = self.waiting_for_move

    def end_round(self):
        # Finishes the round and checks if the game if over
        if not self.checkers.has_legal_moves():
            self.game_state = self.game_over
        else:
            self.game_state = self.new_round

    def game_over(self):
        # Game over state
        self.winner = self.checkers.player_turn()
        if self.checkers.player_turn() == 1:
            print("WHITE WINS")
        else:
            print("BLACK WINS")
        self.game_state = self.end_game

    def end_game(self):
        # This state could have "play again?" button
        #self.running = False
        #self.game_state = self.new_game
        pass

    # DEBUGGING ----------------------------------------------------------------------------------

    def print_debugs(self):
        try:
            if self.prev_game_state != self.game_state:
                # prints only in game_state changes
                print(self.game_state.__name__)
                print(self.checkers.round)
                print("sel: ",self.selected_tile)
                print("rel: ",self.released_tile)
                print("sel2: ",self.selected_tile2)
                print()
            self.prev_game_state = self.game_state
        except:
            self.prev_game_state = ''