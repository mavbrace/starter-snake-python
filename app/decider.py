"""
BATTLESNAKE: deciding on a MOVE
"""
import json
import random

SHOUT = "HISS"

DIRECTIONS = ["up", "down", "left", "right"]
SHOUTS = ["oh no", "cool!", "aha"]

DIR_VECTORS = {
    "up" : (0, -1),
    "down" : (0, 1),
    "left" : (-1, 0),
    "right" : (1, 0)
}

DIR_OPPOSITES = {
    "up" : "down",
    "down" : "up",
    "left" : "right",
    "right" : "left"
}

class Decider:

    def __init__(self):
        #===[ SET UP ]===#
        self.game_id = "tbd"
        self.board_height = 0
        self.board_width = 0
        self.max_health = 0
        #===[ UPDATED EACH TURN ]===#
        self.turn = 0
        self.you = None
        self.board = None
        self.last_move = ""
        #===[ CALCULATED INFO ]===#
        self.move_values = {
        "up" : 0,
        "down" : 0,
        "left" : 0,
        "right" : 0
        }

    def InitialBoard(self, board):
        self.game_id = board["game"]["id"]
        self.board_width = board["board"]["width"]
        self.board_height = board["board"]["height"]
        self.max_health = board["you"]["health"]

    # get the dictionary
    def UpdateBoard(self, board):
        self.turn = board["turn"]
        self.board = board["board"]
        self.you = board["you"]

    def ChooseAShout(self):
        return "oh no"

    #=====[ DECIDE ON A MOVE ]=====#
    def DecideOnMove(self):
        self._PrepChoices()
        move = self._MakeAChoice()
        self.last_move = move
        return move

    def _PrepChoices(self):
        # initialize to 100. All directions seem fine. We're fine. Everything's good.
        for key in self.move_values.keys():
            self.move_values[key] = 100
        # we super don't want to just reverse on ourselves...
        if self.last_move != "":
            self.move_values[DIR_OPPOSITES[self.last_move]] = -1
        # assign some values!!! yayyyyyy
        for key in self.move_values.keys():
            # don't run into walls! That's an instant lose, so also worth -1
            self._AddValue(key, self._walls(key))

    def _walls(self, dir):
        snake_head_coords = self.you["body"][0] #this is a dictionary
        potential_new_pos = (snake_head_coords['x'] + DIR_VECTORS[dir][0],
                            snake_head_coords['y'] + DIR_VECTORS[dir][1])
        if potential_new_pos[0] < 0 or potential_new_pos[0] >= self.board_width:
            print("WALL FOUND: " + dir + ". Potential X Pos was: " + str(potential_new_pos[0]))
            return -1
        if potential_new_pos[1] < 0 or potential_new_pos[1] >= self.board_height:
            print("WALL FOUND: " + dir + ". Potential Y Pos was: " + str(potential_new_pos[1]))
            return -1
        # CLEAR!
        else: return 100


    def _AddValue(self, key, value_to_add):
        # nothing can make a -1 move better! :O
        if self.move_values[key] == -1: return
        # TODO: do this properly :)
        self.move_values[key] = value_to_add


    # If there is one value that is above all others, that is the move chosen.
    # If there are multiple equal best values, we choose (randomly) between them.
    def _MakeAChoice(self):
        multiple_best_choices = []
        best_choice = ""
        best_value = 0
        for key in self.move_values.keys():
            if self.move_values[key] > best_value:
                best_choice = key
                best_value = self.move_values[key]
        for key in self.move_values.keys():
            if self.move_values[key] == best_value:
                multiple_best_choices.append(key)
        if len(multiple_best_choices) > 0:
            best_choice = random.choice(multiple_best_choices)
        if best_choice == "":
            print("====> WARNING: Failed to make a valid move choice! Something went wrong, or there were no good choices.")
        return best_choice
