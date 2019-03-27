from games.tictactoe import TicTacToe
from helpers import validate_input


def main(board_obj: TicTacToe):
    """
    The main function to play a game of Tic Tac Toe.
    
    :param board_obj: The Board object to run the game on.
    :return: 
    """

    print("Welcome to Tic Tac Toe.")
    print("Possible moves are:")
    board_obj.print_move_grid()

    while board_obj.active:
        # Print a newline.
        print()

        # Get the move the player made.
        move = input(f"{board_obj.get_player_icon(board_obj.current_player)} > ")

        # Check the validity of the move.
        while not board_obj.check_move_validity(move):
            print("Invalid move.")
            move = input(f"{board_obj.get_player_icon(board_obj.current_player)} > ")

        # Convert the move to an int.
        move = int(move)

        # Make the move.
        board_obj.make_move(move)

        # Notify the player of the new board.
        board_obj.print_grid()

    # Print the winner.
    print("\nThe game ended!")
    print(f"Player {board_obj.get_player_icon(board_obj.winner)} won!")


if __name__ == '__main__':
    try:
        # Ask the user for parameters.
        grid_size = int(validate_input("Size of the grid: ", lambda x: x.isnumeric()))
        amount_of_players = int(validate_input("Amount of players: ", lambda x: x.isnumeric()))
        player_symbols = validate_input("Enter the symbols for the players, separated by space.\n", lambda x: len(x.split()) >= amount_of_players).split()[:amount_of_players]
        player_symbols = [x[:1] for x in player_symbols]  # Only use the first character of each symbol.

        # Create the Board class
        board = TicTacToe(grid_size=grid_size, players=amount_of_players, player_symbols=player_symbols)

        # Run the main function.
        main(board)

    except KeyboardInterrupt:
        print("\n\nThanks for playing.")
        exit(0)
