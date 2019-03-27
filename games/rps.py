from helpers import validate_input


def check_win(first_move: int, second_move: int) -> int:
    """
    A function that checks if a player has one.
    This functions assumes the moves are valid.

    :param first_move: Move of the first player.
    :param second_move: Move of the second player.
    :return: The PlayerID of who won. 0 if draw.
    """
    # Define the win conditions.
    opposites = {
        0: 1,
        1: 2,
        2: 0
    }

    # Get the opposites for both moves.
    first_opposite = opposites[first_move]
    second_opposite = opposites[second_move]

    # Check which player won.
    if second_move == first_opposite:
        # Player 1 won.
        return 1
    elif first_move == second_opposite:
        # Player 2 won.
        return 2
    else:
        # It's a draw.
        return 0


def ask_move(current_player: int) -> int:
    """
    A function which asks the player for a move.
    Returns that move.

    0 = rock
    1 = paper
    2 = scissors

    :param current_player: The PlayerID of the player at turn.
    :return: The move the player made as an integer, if valid, else -1.
    """

    # Get the move.
    move = validate_input(f"{current_player} > ", lambda x: x.lower() in list("rpsq"), err_text="Invalid move.")

    if move == "q":
        print("Thanks for playing!")
        exit(0)

    # Convert the move to an int.
    move_id = "rps".index(move.lower())

    return move_id
