import random

class AI:
    def __init__(self, used_coordinate = []):
        self.used_coordinate = used_coordinate
    
    def make_random_move(self):
        # Make random list with random x,y coordinate
        random_field_x = random.randint(0, 2)
        random_field_y = random.randint(0, 2)
        field = [random_field_x, random_field_y]
        return field
    
    def check_field(self):
        # check if AI move is avaiable. If not generate another random number
        random_field = self.make_random_move()
        while random_field in self.used_coordinate :
            random_field = self.make_random_move()
        self.used_coordinate.append(random_field)
        print(self.used_coordinate)
       
        return random_field

    def push_move(self, move):
        # Push player move to array
        self.used_coordinate.append(move) 
    def make_move(self, coordinate, symbol = 'o'):
        # Here you can decide if AI is X or O. By default it is "O"
        return {"coordinates": tuple(coordinate), 'symbol': symbol}
        










