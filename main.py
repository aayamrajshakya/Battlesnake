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
        "author": "Jack Sparrow ☠️",  # TODO: Your Battlesnake Username
        "color": "#abb1b6",  # TODO: Choose color
        "head": "pirate",  # TODO: Choose head
        "tail": "pirate",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    boardHeight = game_state["board"]["height"]
    boardWidth = game_state["board"]["width"]
    timeout = game_state["game"]["timeout"]
    print(
        "Starting game with %dx%d board and %dms timeout"
        % (boardHeight, boardWidth, timeout)
    )


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# Game terminates when my health is zero
# There are other possible conditions too, like when there's only one snake left, and so on
def game_over(game_state):
    return game_state["you"]["health"] <= 0


# TODO: calculate the evaluation function value for the current state
# the value should be a function of various attributes of the game state
# such as the current number of move options available, length of each snake,
# number of squares controlled, snake health, distance to nearest food etc.

# REFERENCE: https://github.com/han191299/starter-snake-python/tree/main
def evaluation_function(game_state):
    my_snake = game_state["you"]
    my_head = my_snake["body"][0]
    my_health = my_snake["health"]
    my_length = my_snake["length"]
    food = game_state["board"]["food"]
    global opponent_snake_index
    opponent_snake = game_state["board"]["snakes"][opponent_snake_index]  
      
    # Hardcoding Manhattan formula is better than using function
    dist_from_opponent = abs(my_head["x"] - opponent_snake["head"]["x"]) + abs(my_head["y"] - opponent_snake["head"]["y"])

    # Incentivize my snake to stay away from the opponent's
    safety_lvl = 0
    if dist_from_opponent <= 5:
        safety_lvl = 1 if my_length > opponent_snake["length"] else -1
    
    closest_food_dist = float('inf')
    for each_food in food:
        dist_to_food = abs(my_head["x"] - each_food["x"]) + abs(my_head["y"] - each_food["y"])
        if dist_to_food < closest_food_dist:
            closest_food_dist = dist_to_food

    # Weight for each evaluation factor
    length_weight = 1
    safety_weight = 20
    health_weight = 4
    food_dist_weight = -2
    
    return (my_length*length_weight) + (safety_lvl*safety_weight) + (my_health*health_weight) + (closest_food_dist*food_dist_weight)


# simulates what the next state will be after a given move
def get_next_state(game_state, move, is_maximizing_player):
    global opponent_snake_index
    next_game_state = copy.deepcopy(game_state)
    your_snake_index = (
        0 if game_state["board"]["snakes"][0]["id"] == game_state["you"]["id"] else 1
    )
    opponent_snake_index = 1 - your_snake_index

    snake = (
        next_game_state["board"]["snakes"][your_snake_index]
        if is_maximizing_player
        else next_game_state["board"]["snakes"][opponent_snake_index]
    )
    new_head = copy.deepcopy(game_state["you"]["body"][0])
    if move == "up":
        new_head["y"] += 1
    elif move == "down":
        new_head["y"] -= 1
    elif move == "left":
        new_head["x"] -= 1
    elif move == "right":
        new_head["x"] += 1

    snake["health"] -= 1
    snake["head"] = new_head
    snake["body"].insert(0, new_head)
    snake["body"].pop()

    if is_maximizing_player:
        next_game_state["you"]["health"] -= 1
        next_game_state["you"]["head"] = new_head
        next_game_state["you"]["body"].insert(0, new_head)
        next_game_state["you"]["body"].pop()

    for food in next_game_state["board"]["food"]:
        if food == new_head:
            next_game_state["board"]["food"].remove(food)
            snake["health"] = 100
            snake["body"].append(snake["body"][-1])
            snake["length"] += 1
            if is_maximizing_player:
                next_game_state["you"]["health"] = 100
                next_game_state["you"]["body"].append(snake["body"][-1])
                next_game_state["you"]["length"] += 1
            break

    return next_game_state


# REFERENCE: https://github.com/DayneHack/chess-engine/tree/main
# def makeNullMove(board):
#     move = chess.Move.null()
#     board.push(move)

def make_null_move(game_state):
    null_state = copy.deepcopy(game_state)  # copy the state and do nothing to simulate null move
    return null_state
    
    
# TODO: implement the minimax algorithm
# game_state: object that stores the current game state
# depth: remaining depth to be searched
#       depth=0 indicates that this is a leaf node / terminal node
# is_maximizing_player:
#       True if your snake (maximizing player) is taking an action
#       False if the opponent's snake (minimizing player) is taking an action

# REFERENCE: https://www.youtube.com/watch?v=l-hh51ncgDI
# https://algocademy.com/blog/implementing-game-algorithms-minimax-and-alpha-beta-pruning/
def minimax(game_state, depth, alpha, beta, is_maximizing_player, r):
    # hint: you may use the get_next_state function provided above
    if depth == 0 or game_over(game_state):
        return evaluation_function(game_state), None
    
    # Null move pruning: https://github.com/DayneHack/chess-engine/blob/77a265b946b95c58314c3ff95c6ca9adff538490/chess-engine.py#L119
    if not is_maximizing_player and depth >= 3:
        null_state = make_null_move(game_state)
        currEval, _ = -minimax(null_state, depth - r - 1, -beta, -beta + 1, True, r)
        if currEval >= beta:
            return beta, None

    if is_maximizing_player:
        maxEval = float("-inf")
        optimal_move = None
        for possible_move in safe_moves(game_state):
            new_state = get_next_state(game_state, possible_move, True)
            eval, _ = minimax(new_state, depth - 1, alpha, beta, False, r)
            if eval > maxEval:
                maxEval, optimal_move = eval, possible_move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, optimal_move

    else:
        minEval = float("inf")
        optimal_move = None
        for possible_move in safe_moves(game_state):
            new_state = get_next_state(game_state, possible_move, True)
            eval, _ = minimax(new_state, depth - 1, alpha, beta, True, r)
            if eval < minEval:
                minEval, optimal_move = eval, possible_move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, optimal_move


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def safe_moves(game_state: typing.Dict) -> typing.Dict:

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
    board_width = game_state["board"]["width"]      # 11
    board_height = game_state["board"]["height"]    # 11

    if my_head["x"] == 0:
        is_move_safe["left"] = False
        
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    if my_head["y"] == 0:
        is_move_safe["down"] = False
        
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # TODO: Prevent your Battlesnake from colliding with itself
    # index 0 is just head, the rest body starts from index 1
    my_body = game_state["you"]["body"][1:]
    for body in my_body:
        if my_head["x"] == body["x"] and my_head["y"] + 1 == body["y"]:  # Head is below the body
            is_move_safe["up"] = False
            
        if my_head["x"] == body["x"] and my_head["y"] - 1 == body["y"]:  # Head is above the body
            is_move_safe["down"] = False

        if my_head["y"] == body["y"] and my_head["x"] - 1 == body["x"]:  # Head is facing towards the right side
            is_move_safe["left"] = False
            
        if my_head["y"] == body["y"] and my_head["x"] + 1 == body["x"]:  # Head is facing towards the left side
            is_move_safe["right"] = False

    # TODO: Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state["board"]["snakes"]
    for opponent in opponents:
        for body in opponent["body"]:
            if my_head["x"] == body["x"] and my_head["y"] + 1 == body["y"]: # Opponent is above me (same x-axis)
                is_move_safe["up"] = False
                
            if my_head["x"] == body["x"] and my_head["y"] - 1 == body["y"]: # Opponent is below me (same x-axis)
                is_move_safe["down"] = False

            if my_head["y"] == body["y"] and my_head["x"] + 1 == body["x"]: # Opponent is in front of me from right side
                is_move_safe["right"] = False
                
            if my_head["y"] == body["y"] and my_head["x"] - 1 == body["x"]: # Opponent is in front of me from left side
                is_move_safe["left"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    return safe_moves


# TODO: Instead of making a random move, use the minimax algorithm to find the optimal move
# `move` is an innate function of the game, so I separated the 'safe moves' and 'next move' parts
def move(game_state: typing.Dict) -> typing.Dict:
    _, next_move = minimax(game_state, 1, float('-inf'), float('inf'), True, r=2)
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == "--port":
            port = sys.argv[i + 1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
