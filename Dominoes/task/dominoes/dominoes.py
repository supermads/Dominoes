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
        self.computer = self.tiles[:7]
        self.player = self.tiles[7:14]
        self.stock = self.tiles[14:]

    def find_starter(self):
        snakes = [[6,6], [5,5], [4,4], [3,3], [2,2], [1,1], [0,0]]

        for snake in snakes:
            if snake in self.computer:
                self.computer.remove(snake)
                return snake, "player"
            elif snake in self.player:
                self.player.remove(snake)
                return snake, "computer"

        return None, None

    def main(self):
        self.distribute_dominoes()
        snake, start_player = self.find_starter()

        # If starting piece can't be determined, reshuffle and redistribute tiles
        while not start_player:
            self.distribute_dominoes()
            snake, start_player = self.find_starter()

        print("=" * 70)
        print(f"Stock size: {len(self.stock)}")
        print(f"Computer pieces: {len(self.computer)}\n")
        print(snake)

        print("\nYour pieces:")
        for i, tile in enumerate(self.player):
            print(f"{i + 1}:{tile}")

        if start_player == "computer":
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        else:
            print("\nStatus: It's your turn to make a move. Enter your command.")


Dominoes().main()






