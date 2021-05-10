from itertools import combinations_with_replacement
from random import shuffle, randint
from collections import Counter


class Dominoes:
    def __init__(self):
        self.tiles = list(map(list, combinations_with_replacement(range(0, 7), 2)))
        self.computer = []
        self.player = []
        self.stock = []
        self.snake = []
        self.curr_player = ""
        self.freq_dict = Counter({i: 0 for i in range(7)})

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
                self.freq_dict[start_tile[0]] = self.freq_dict[start_tile[0]] + 2
                return start_tile

            elif start_tile in self.player:
                self.player.remove(start_tile)
                self.curr_player = "computer"
                self.freq_dict[start_tile[0]] = self.freq_dict[start_tile[0]] + 2
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

        if len(self.snake) > 6:
            print(f"{self.snake[0]}{self.snake[1]}{self.snake[2]}...{self.snake[-3]}{self.snake[-2]}{self.snake[-1]}")
        else:
            print(*self.snake)

        print("\nYour pieces:")
        for i, tile in enumerate(self.player):
            print(f"{i + 1}:{tile}")

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

    def update_freq_dict(self, num1, num2):
        self.freq_dict[num1] = self.freq_dict[num1] + 1
        self.freq_dict[num2] = self.freq_dict[num2] + 1

    def player_turn(self):
        action = ""
        possible_moves = self.find_moves()

        print("\nStatus: It's your turn to make a move. Enter your command.")

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

            self.update_freq_dict(curr_tile[0], curr_tile[1])

        elif action > 0:
            curr_tile = self.player.pop(action - 1)

            if curr_tile[0] == self.snake[-1][1]:
                self.snake.append(curr_tile)

            else:
                self.snake.append(curr_tile[::-1])

            self.update_freq_dict(curr_tile[0], curr_tile[1])

        else:
            # If the user inputs 0, remove a random tile from the stock and add it to their supply (if stock isn't empty)
            if self.stock:
                curr_tile = randint(0, len(self.stock) - 1)
                self.player.append(self.stock.pop(curr_tile))

        self.curr_player = "computer"

    def create_comp_freq_dict(self):
        # Create a frequency dictionary for computer tiles then combine it with the snake frequency dictionary
        comp_dict = {}
        comp_and_snake_tiles = []

        for tile in self.computer:
            comp_and_snake_tiles.append(tile[0])
            comp_and_snake_tiles.append(tile[1])

        for i in range(7):
            comp_dict[i] = comp_and_snake_tiles.count(i)

        return Counter(comp_dict) + self.freq_dict

    def ai_computer_turn(self):
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        input()

        freq_dict = self.create_comp_freq_dict()

        scores = []
        for tile in self.computer:
            scores.append(freq_dict[tile[0]] + freq_dict[tile[1]])
        # Make the score indexes match the tile numbers used in list returned by find_moves
        scores.insert(0, 0)

        move_found = False
        possible_moves = self.find_moves()

        if possible_moves:
            while not move_found and scores.count(0) != len(self.computer):
                max_tile = scores.index(max(scores))

                if max_tile in possible_moves:
                    move_found = True
                    curr_tile = self.computer.pop(max_tile - 1)

                    if curr_tile[0] == self.snake[-1][1]:
                        self.snake.append(curr_tile)

                    else:
                        self.snake.append(curr_tile[::-1])

                    self.update_freq_dict(curr_tile[0], curr_tile[1])

                elif max_tile * -1 in possible_moves:
                    move_found = True
                    curr_tile = self.computer.pop(max_tile - 1)

                    if curr_tile[1] == self.snake[0][0]:
                        self.snake.insert(0, curr_tile)

                    else:
                        self.snake.insert(0, curr_tile[::-1])

                    self.update_freq_dict(curr_tile[0], curr_tile[1])

                scores[max_tile] = 0

        else:
            if self.stock:
                curr_tile = randint(0, len(self.stock) - 1)
                self.computer.append(self.stock.pop(curr_tile))

        self.curr_player = "player"

    def find_winner(self):
        snake_head = self.snake[0][0]

        if not self.computer:
            return "computer"

        elif not self.player:
            return "player"

        # A draw occurs if the number at the head and tail of the snake match and that number is in the snake 8 times
        elif snake_head == self.snake[-1][1] and self.freq_dict[snake_head] >= 8:
            return "draw"

        else:
            return ""

    def play(self):
        winner = ""

        while not winner:
            self.print_status()

            if self.curr_player == "computer":
                self.ai_computer_turn()
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
