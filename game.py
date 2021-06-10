"""Opencv based game"""
import argparse
import queue

import cv2 as cv

from src.game_ai.ai import AI
from src.game_engine.board import OutsideBoardException, PositionTakenException
from src.game_engine.engine import Coordinates, instance
from src.opencv_backend.input import InputSystem
from src.opencv_backend.ui import UI

parser = argparse.ArgumentParser(description="A tictactoe game using opencv as input")
parser.add_argument(
    "--symbol", type=str, help="symbol that player will play as (x,o)", default="x"
)
parser.add_argument(
    "--starting", type=bool, help="should the player start the game?", default=True
)

args = parser.parse_args()
if not args.symbol in ("x", "o"):
    print("Unrecoginsed option: --symbol " + args.symbol)

if args.symbol == "x":
    bot = AI()
else:
    bot = AI("x")

camera = cv.VideoCapture(0)
if not camera.isOpened:
    print("Failed to open camera")
ok, frame = camera.read()
interface = UI(frame)
interface.draw_grid()
in_sys = InputSystem(camera)
in_sys.setup_tracker()


def player_move():
    """Attempts to move, returns whether the move was successful"""
    location = in_sys.check_bounds(interface)
    coords = Coordinates(location[0], location[1], args.symbol)
    try:
        instance.make_move(coords)
    except PositionTakenException:
        print("Position already taken")
        return False
    except OutsideBoardException:
        print("Chosen position is ouside the board (don't know how you did it)")
        return False
    interface.draw_move(coords)
    return True


moves = queue.Queue(2)


def opponent_move():
    """makes a bot move"""
    coords = bot.make_random_move()
    instance.make_move(coords)
    bot.add_move(coords)
    interface.draw_move(coords)


if args.starting:
    moves.put(player_move)
    moves.put(opponent_move)
else:
    moves.put(opponent_move)
    moves.put(player_move)

while not instance.has_won:
    move = moves.get()
    moves.put(move)
    move()
