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

    def find_moves(self):
        # Returns the indices of tiles in the current player's supply that can be legally played this turn
        moves = []
        left_end = self.snake[0][0]
        right_end = self.snake[-1][1]

        if self.curr_player == "player":
            for i, tile in enumerate(self.player):
                if left_end in tile:
                    moves.append((i + 1) * -1)
                if right_end in tile:
                    moves.append(i + 1)

        else:
            for i, tile in enumerate(self.computer):
                # The player's list of pieces starts with one, so add one to the tile index before appending it to moves list
                if left_end in tile:
                    # If the tile can be played on the left side of the snake, make tile number negative
                    moves.append((i + 1) * -1)
                if right_end in tile:
                    moves.append(i + 1)

        return moves

    def player_turn(self):
        action = ""
        possible_moves = self.find_moves()

        while action == "":
            try:
                action = int(input())
            except ValueError:
                print("Invalid input. Please try again.")

        while action not in possible_moves and action != 0:
            if abs(action) > len(self.player):
                print("Invalid input. Please try again.")
            else:
                print("Illegal move. Please try again")
            action = int(input())

        if action < 0:
            action = abs(action)
            curr_tile = self.player.pop(action - 1)

            if curr_tile[1] == self.snake[0][0]:
                self.snake.insert(0, curr_tile)

            else:
                self.snake.insert(0, curr_tile[::-1])

        elif action > 0:
            curr_tile = self.player.pop(action - 1)

            if curr_tile[0] == self.snake[-1][1]:
                self.snake.append(curr_tile)

            else:
                self.snake.append(curr_tile[::-1])

        else:
            # If the user inputs 0, remove a random tile from the stock and add it to their supply (if stock isn't empty)
            if self.stock:
                curr_tile = randint(0, len(self.stock) - 1)
                self.player.append(self.stock.pop(curr_tile))

        self.curr_player = "computer"

    def computer_turn(self):
        input()

        possible_moves = self.find_moves()

        if possible_moves:
            action = possible_moves[randint(0, len(possible_moves) - 1)]

            if action < 0:
                action = abs(action)
                curr_tile = self.computer.pop(action - 1)

                if curr_tile[1] == self.snake[0][0]:
                    self.snake.insert(0, curr_tile)

                else:
                    self.snake.insert(0, curr_tile[::-1])

            elif action > 0:
                curr_tile = self.computer.pop(action - 1)

                if curr_tile[0] == self.snake[-1][1]:
                    self.snake.append(curr_tile)

                else:
                    self.snake.append(curr_tile[::-1])

        else:
            if self.stock:
                curr_tile = randint(0, len(self.stock) - 1)
                self.computer.append(self.stock.pop(curr_tile))

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
