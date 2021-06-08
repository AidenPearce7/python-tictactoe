"""Sample engine implementation"""
from src.game_engine.board import (
    PositionTakenException,
    WrongPlayerException,
    OutsideBoardException,
)


from src.game_engine.engine import instance
from src.opencv_backend.ui import draw_grid, draw_x, draw_circle, cv
from src.game_ai.ai import AI

game_AI = AI()

game_started = False
img = cv.imread('red.jpg',0)
draw_grid(img)
while not instance.has_won:
    print(instance.get_board_copy())    
    from_usr = input("Type location and symbol to play (example: 0,0,x):\n").split(",")
    if from_usr[0] == "exit":
        exit(0)
    if len(from_usr) < 2:
        print("input error")
        continue
    from_usr[0] = int(from_usr[0])
    from_usr[1] = int(from_usr[1])
    move = {"coordinates": tuple(from_usr[:2]), "symbol": 'x'}

    drawer = list(move["coordinates"])
    drawer.reverse()
    symbol = move['symbol']
    game_AI.push_move(drawer)

    ai_coordinate = game_AI.check_field()
    ai_move = game_AI.make_move(ai_coordinate, 'o')
    try:
        instance.make_move(move)
        instance.make_move(ai_move)
        ai_coordinate.reverse()
        draw_x(img, drawer)
        draw_circle(img, ai_coordinate)
        cv.imshow('image',img)
        cv.waitKey(400)
    except PositionTakenException:
        print("position is already taken by another symbol")
    except WrongPlayerException:
        print("Not your turn.")
    except OutsideBoardException:
        print("Chosen position is ouside the board")
if instance.winner != "DRAW":
    print(instance.winner + "'s have won")
else:
    print(instance.winner)