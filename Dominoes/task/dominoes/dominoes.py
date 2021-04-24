from itertools import combinations_with_replacement
from random import shuffle, randint


class Dominoes:
    def __init__(self):
        self.tiles = list(map(list, combinations_with_replacement(range(0, 7), 2)))
        self.computer = []
        self.player = []
        self.stock = []
        self.snake = []
        self.curr_player = ""
        self.matching_ends = 0

    def distribute_dominoes(self):
        # Shuffle tiles and distribute 7 pieces each to computer and player
        shuffle(self.tiles)
        self.computer = self.tiles[:7]
        self.player = self.tiles[7:14]
        self.stock = self.tiles[14:]

    def find_starters(self):
        doubles = [[6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1], [0, 0]]

        for start_tile in doubles:
            if start_tile in self.computer:
                self.computer.remove(start_tile)
                self.curr_player = "player"
                return start_tile
            elif start_tile in self.player:
                self.player.remove(start_tile)
                self.curr_player = "computer"
                return start_tile

        return None, None

    def set_up(self):
        self.distribute_dominoes()
        start_tile = self.find_starters()
        start_player = self.curr_player
        self.snake.append(start_tile)

        # If starting piece can't be determined, reshuffle and redistribute tiles
        while not start_player:
            self.distribute_dominoes()
            start_tile = self.find_starters()
            self.snake.append(start_tile)

    def print_status(self):
        print("=" * 70)
        print(f"Stock size: {len(self.stock)}")
        print(f"Computer pieces: {len(self.computer)}\n")

        if len(self.snake) > 4:
            print(f"{self.snake[0]}{self.snake[1]}{self.snake[2]}...{self.snake[-3]}{self.snake[-2]}{self.snake[-1]}")
        else:
            print(*self.snake)

        print("\nYour pieces:")
        for i, tile in enumerate(self.player):
            print(f"{i + 1}:{tile}")

        if self.curr_player == "computer":
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        else:
            print("\nStatus: It's your turn to make a move. Enter your command.")

    def player_turn(self):
        action = ""
        move_made = False

        while action == "":
            try:
                action = int(input())
            except ValueError:
                print("Invalid input. Please try again.")

        if action == 0:
            # If the user inputs 0, remove a random tile from the stock and add it to their supply
            curr_tile = randint(0, len(self.stock) - 1)
            self.player.append(self.stock.pop(curr_tile))
            move_made = True

        while not move_made:
            if action < 0:
                try:
                    # If the user inputs a negative number, make it positive
                    # Add the corresponding tile from the player's supply to the left side of the snake
                    action = abs(action)
                    curr_tile = self.player.pop(action - 1)
                    self.snake.insert(0, curr_tile)
                    move_made = True

                    if curr_tile[1] == self.snake[1][0]:
                        self.matching_ends += 1
                    
                except IndexError:
                    print("Invalid input. Please try again.")
                    action = int(input())
                    
            else:
                # If action is positive and within range of available tiles, add corresponding tile to the right side of the snake
                try:
                    curr_tile = self.player.pop(action - 1)
                    self.snake.append(curr_tile)
                    move_made = True

                    if curr_tile[0] == self.snake[-2][1]:
                        self.matching_ends += 1

                except IndexError:
                    print("Invalid input. Please try again.")
                    action = int(input())

        self.curr_player = "computer"

    def computer_turn(self):
        input()

        supply_size = len(self.computer)
        action = randint(-supply_size, supply_size)

        if action < 0:
            action = abs(action)

            # Subtract 1 from action because supply_size is 1 larger than the max index of the supply
            curr_tile = self.computer.pop(action - 1)
            self.snake.append(curr_tile)

            if curr_tile[1] == self.snake[1][0]:
                self.matching_ends += 1

        else:
            curr_tile = self.computer.pop(action - 1)
            self.snake.append(curr_tile)

            if curr_tile[0] == self.snake[-2][1]:
                self.matching_ends += 1

        self.curr_player = "player"

    def find_winner(self):
        if self.matching_ends > 7:
            return "draw"
        elif not self.computer:
            return "computer"
        elif not self.player:
            return "player"
        else:
            return ""

    def play(self):
        winner = ""

        while not winner:
            self.print_status()

            if self.curr_player == "computer":
                self.computer_turn()
            else:
                self.player_turn()

            winner = self.find_winner()

        self.print_status()

        message = "Status: The game is over. "

        if winner == "draw":
            print(message + "It's a draw!")

        elif winner == "computer":
            print(message + "The computer won!")

        else:
            print(message + "You won!")


game = Dominoes()
game.set_up()
game.play()
