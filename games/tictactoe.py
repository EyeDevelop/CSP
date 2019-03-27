import typing


class TicTacToe:
    def __init__(self, grid_size: int = 3, players: int = 2, player_symbols: typing.Union[list, tuple] = ('X', 'O')):
        """
        Initialises a Board object for playing the game Tic Tac Toe.
        """

        # Store some basic information.
        self.players = players
        self.current_player = 0
        self.grid_size = grid_size

        # Check if the player symbols is valid.
        if len(player_symbols) >= players:
            player_symbols = player_symbols[:players]
        else:
            raise ValueError("Invalid size for player_symbols")

        self.player_icons = player_symbols
        self.active = True
        self.winner = None

        # Generate a grid.
        self.grid = None
        self.generate_grid()

    def generate_grid(self):
        """
        Makes a grid with grid_size rows and grid_size columns.

        :return:
        """

        # Clear the grid.
        self.grid = []

        # Fill the grid with spaces.
        for row_index in range(self.grid_size):
            row = []
            for column_index in range(self.grid_size):
                row.append(" ")

            self.grid.append(row)

    def get_player_icon(self, player_id: int):
        """
        Returns the player icon.

        :param player_id: The PlayerID of the player.
        :return: The player icon.
        """

        return self.player_icons[player_id]

    def update_player_icon(self, player_id: int, new_symbol: str):
        """
        Updates a player icon.

        :param player_id: The PlayerID of the player.
        :param new_symbol: The new symbol of the player.
        :return:
        """

        self.player_icons[player_id] = new_symbol

    def get_symbol_at(self, move):
        """
        Get the symbol at place move.

        :param move: The move index.
        :return: The symbol.
        """

        # The row that is requested is how many times move fits in the grid.
        # Arrays start at 0, so move has to be decremented first.
        row = (move - 1) // self.grid_size

        # The column changed is the remainder.
        column = (move - 1) % self.grid_size

        # Return the requested symbol.
        return self.grid[row][column]

    def switch_player(self):
        """
        Switches the player around.

        :return:
        """

        # Switch the players around.
        if self.current_player + 1 < self.players:
            self.current_player += 1
        else:
            self.current_player = 0

    def print_grid(self):
        """
        A function that prints the current state of the grid.

        :return:
        """

        for row_index in range(self.grid_size):
            # Print the grid row by row.
            print(" | ".join(map(str, self.grid[row_index])))

    def print_move_grid(self):
        """
        A function that prints the grid with possible moves.

        :return:
        """

        rows_travelled = 0
        for row_index in range(self.grid_size):
            # Print a list of ints from 1 to self.grid_size^2.
            print(" | ".join(map(str, list(range(rows_travelled * self.grid_size + 1, rows_travelled * self.grid_size + self.grid_size + 1)))))
            rows_travelled += 1

    def make_move(self, move: int):
        """
        Updates the grid with the move made.

        :param move: The index of what has changed.

        :return:
        """

        # The row that has changed is how many times move fits in the grid.
        # Arrays start at 0, so move has to be decremented first.
        row_changed = (move - 1) // self.grid_size

        # The column changed is the remainder.
        column_changed = (move - 1) % self.grid_size

        # Update the grid.
        self.grid[row_changed][column_changed] = self.player_icons[self.current_player]

        # Check if someone has won.
        self.active = self.check_win(row_changed, column_changed)

        # Switch the players.
        self.switch_player()

    def check_win(self, row_changed: int, column_changed: int) -> bool:
        """
        Checks if a player has won in all directions.

        :param row_changed: The row that has changed with the move.
        :param column_changed: The column that has changed with the move.

        :return:
        """

        # First check horizontally.
        row = "".join(self.grid[row_changed])

        # If the amount of unique characters of the row is 1, a player has won.
        row_set = set(row)
        if len(row_set) == 1 and " " not in row_set:
            # Set the winner.
            self.winner = self.current_player

            # Game is not active anymore.
            return False

        # Check vertically.
        row = ""
        for row_index in range(len(self.grid)):
            row += self.grid[row_index][column_changed]

        # If the amount of unique characters of the row is 1, a player has won.
        row_set = set(row)
        if len(row_set) == 1 and " " not in row_set:
            # Set the winner.
            self.winner = self.current_player

            # Game is not active anymore.
            return False

        # Check diagonally.
        for direction_index in [0, 1]:
            # Set a starting position and a step size.
            starting_pos = [(0, 0), (0, self.grid_size - 1)][direction_index]
            step_size = [1, -1][direction_index]

            # Set up the loop parameters.
            row = []
            index_offset = 0
            row_index, column_index = starting_pos

            # Loop until end of grid.
            while abs(index_offset) < self.grid_size:
                # Add the item to the row.
                row.append(self.grid[row_index + abs(index_offset)][column_index + index_offset])

                # Increment the index_offset with step_size.
                index_offset += step_size

            # Check the length.
            row = "".join(row)

            row_set = set(row)
            if len(row_set) == 1 and " " not in row_set:
                # Set the winner.
                self.winner = self.current_player

                # Game is not active anymore.
                return False

        # Nobody has won.
        return True

    def check_move_validity(self, move):
        """
        A function to check the validity of a move.

        :param move: The integer of the board place.
        :return:
        """

        # Check the validity of the move.
        if not move.isdigit():
            # Move is not a digit.
            move_valid = False

        elif not (0 <= int(move) - 1 < self.grid_size ** 2):
            # Move is outside the grid range.
            move_valid = False

        elif self.get_symbol_at(int(move)) != " ":
            # Move is taken.
            move_valid = False

        else:
            # Move should be valid.
            move_valid = True

        return move_valid
