# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import sys
import copy


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Jack Sparrow",  # TODO: Your Battlesnake Username
        "color": "#abb1b6",  # TODO: Choose color
        "head": "pirate",  # TODO: Choose head
        "tail": "pirate",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    boardHeight = game_state['board']['height']
    boardWidth = game_state['board']['width']
    timeout = game_state['game']['timeout']
    print('Starting game with %dx%d board and %dms timeout' % (boardHeight, boardWidth, timeout))


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# TODO: calculate the evaluation function value for the current state
# the value should be a function of various attributes of the game state
# such as the current number of move options available, length of each snake,
# number of squares controlled, snake health, distance to nearest food etc.
def evaluation_function(game_state):
    return 0

# simulates what the next state will be after a given move
def get_next_state(game_state, move, is_maximizing_player):
    next_game_state = copy.deepcopy(game_state)
    your_snake_index = 0 if game_state['board']['snakes'][0]['id'] == game_state['you']['id'] else 1
    opponent_snake_index = 1 - your_snake_index

    snake = next_game_state['board']['snakes'][your_snake_index] if is_maximizing_player \
            else next_game_state['board']['snakes'][opponent_snake_index]
    new_head = copy.deepcopy(game_state['you']['body'][0])
    if move == "up":
        new_head["y"] += 1
    elif move == "down":
        new_head["y"] -= 1
    elif move == "left":
        new_head["x"] -= 1
    elif move == "right":
        new_head["x"] += 1
    
    snake['health'] -= 1
    snake['head'] = new_head
    snake['body'].insert(0, new_head)
    snake['body'].pop()

    if is_maximizing_player:
        next_game_state['you']['health'] -= 1
        next_game_state['you']['head'] = new_head
        next_game_state['you']['body'].insert(0, new_head)
        next_game_state['you']['body'].pop()

    for food in next_game_state['board']['food']:
        if food == new_head:
            next_game_state['board']['food'].remove(food)
            snake['health'] = 100
            snake['body'].append(snake['body'][-1])
            snake['length'] += 1
            if is_maximizing_player:
                next_game_state['you']['health'] = 100
                next_game_state['you']['body'].append(snake['body'][-1])
                next_game_state['you']['length'] += 1
            break

    return next_game_state

# TODO: implement the minimax algorithm
# game_state: object that stores the current game state
# depth: remaining depth to be searched
#       depth=0 indicates that this is a leaf node / terminal node
# is_maximizing_player:
#       True if your snake (maximizing player) is taking an action
#       False if the opponent's snake (minimizing player) is taking an action
def minimax(game_state, depth, is_maximizing_player):
    # hint: you may use the get_next_state function provided above
    pass

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    # TODO: Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Instead of making a random move, use the minimax algorithm to find the optimal move

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
