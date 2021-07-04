"""Sample engine implementation"""
import sys
from src.game_engine.board import (
    PositionTakenException,
    WrongPlayerException,
    OutsideBoardException,
)
from src.game_engine.engine import Engine

instance = Engine("x")

print("Type location and symbol to play")
while not instance.has_won:
    print(instance.get_board_copy())
    from_usr = input("Type location and symbol to play (example: 0,0,x):\n").split(",")
    if from_usr[0] == "exit":
        sys.exit(0)
    if len(from_usr) < 2:
        print("input error")
        continue
    from_usr[0] = int(from_usr[0])
    from_usr[1] = int(from_usr[1])
    move = {"coordinates": tuple(from_usr[:2]), "symbol": from_usr[2]}
    try:
        instance.make_move(move)
    except PositionTakenException:
        print("position is already taken by another symbol")
    except WrongPlayerException:
        print("Not your turn")
    except OutsideBoardException:
        print("Chosen position is ouside the board")


if instance.winner != "DRAW":
    print(instance.winner + "'s have won")
else:
    print(instance.winner)
