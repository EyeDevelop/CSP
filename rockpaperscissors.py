from games.rps import check_win, ask_move


def main():
    """
    The main function executed.
    """

    # Welcome the player.
    print("Welcome to Tic Tac Toe.")
    print("The game shows which player is playing.")
    print("Input moves as r (rock), p (paper) or s (scissors).")
    print("Enter q to stop playing.")
    print()

    # Setup variables for the loop.
    playing = True
    current_player = 1

    while playing:
        # Let the first player make a move.
        first_move = ask_move(current_player)

        # Switch the player at turn.
        current_player = 2

        # Let the second player make a move.
        second_move = ask_move(current_player)

        # Get the result.
        winning_player = check_win(first_move, second_move)
        if winning_player != 0:
            # Somebody won.
            print(f"Player {winning_player} won!")
        else:
            # It's a draw.
            print("A draw has met your fate. You shall battle again.")

        # Reset variables for a rematch.
        current_player = 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks for playing!")
        exit(0)
