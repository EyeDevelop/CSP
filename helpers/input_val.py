def validate_input(input_str: str, val_func, err_text: str = "That is not valid.", print_err: bool = True) -> str:
    """
    A helper-function to validate input.

    :param input_str: The string used when asking for input.
    :param val_func: The validation function with one argument, that checks if input is valid.
    :param err_text: The error text displayed when print_err is True.
    :param print_err: Whether to print an error on invalid input.
    :return: The string with valid data.
    """

    # Create a placeholder value.
    val = None

    # Keep looping while the value is invalid.
    while val is None:
        # Ask for a new value.
        val = input(input_str)

        # Check its validity.
        data_is_valid = False
        try:
            data_is_valid = val_func(val)
        except:
            val = None

        if not data_is_valid:
            # Print if requested.
            if print_err:
                print(err_text)

            # Value is not valid. Set to None.
            val = None

    # Return correct value.
    return val
