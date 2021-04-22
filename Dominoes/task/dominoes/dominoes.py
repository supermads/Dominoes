from itertools import combinations_with_replacement
from random import shuffle


class Dominoes:
    def __init__(self):
        self.tiles = list(map(list,combinations_with_replacement(range(0,7), 2)))
        self.computer = []
        self.player = []
        self.stock = []

    def distribute_dominoes(self):
        # Shuffle tiles and distribute 7 pieces each to computer and player
        shuffle(self.tiles)
        self.computer = [self.tiles[i] for i in range(7)]
        self.player = [self.tiles[i] for i in range(7, 14)]
        self.stock = [self.tiles[i] for i in range(14, 28)]

    def find_starter(self):
        snakes = [[6,6], [5,5], [4,4], [3,3], [2,2], [1,1], [0,0]]

        for i in range(7):
            curr_snake = snakes[i]
            if curr_snake in self.computer:
                self.computer.remove(curr_snake)
                return curr_snake, "player"
            elif curr_snake in self.player:
                self.player.remove(curr_snake)
                return curr_snake, "computer"

        return None, None

    def main(self):
        self.distribute_dominoes()
        snake, start_player = self.find_starter()

        # If starting piece can't be determined, reshuffle and redistribute tiles
        while not start_player:
            print("next loop")
            self.distribute_dominoes()
            print(self.computer)
            snake, start_player = self.find_starter()

        print(f"Stock pieces: {self.stock}")
        print(f"Computer pieces: {self.computer}")
        print(f"Player pieces: {self.player}")
        print(f"Domino snake: {[snake]}")
        print(f"Status: {start_player}")


Dominoes().main()






