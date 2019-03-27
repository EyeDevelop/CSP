import os

from util.passgen import Vault
from helpers import validate_input


def new_vault() -> Vault:
    """
    Generate a new vault.

    :return:
    """

    print("No existing vault detected.")
    print("To create a new password, create a password below.")
    vault_key = validate_input("Password for new vault: ", lambda x: 8 <= len(x) <= 32 and x.isprintable(), err_text="It needs to be at least 8 characters, max 32. (no weird characters).\n")

    # Make a new vault object.
    vault = Vault(vault_key.encode("utf-8"))

    # Remove vault key from memory for security.
    del vault_key

    return vault


def existing_vault() -> Vault:
    """
    Open an existing vault.

    :return:
    """

    print("Found an existing vault.")
    print("Please input the password for that vault.")
    vault_key = validate_input(": ", lambda x: 8 <= len(x) <= 32 and x.isprintable(), err_text="Has to be at least 8 characters long, max 32. No weird characters.\n")

    # Key is provided for existing vault. Try to open it.
    vault = Vault(vault_key.encode("utf-8"))
    try:
        vault.unlock_vault()
        vault.lock_vault()
    except ValueError:
        print("\nInvalid vault key provided.")
        exit(0)

    # Remove vault key from memory for security.
    del vault_key

    return vault


def get_vault() -> Vault:
    """
    Try to retrieve an existing vault.

    :return:
    """

    if os.path.isfile("vault.edb"):
        return existing_vault()
    else:
        return new_vault()


def main():
    print("Welcome to the Password Vault!")

    # Gather input.
    vault = get_vault()

    print()
    print("\nLogged into the vault.")

    # Run the menu.
    menu = True
    while menu:
        print("\nPlease choose what you want to do.")
        print("1: Store a new password.")
        print("2: Generate a new password.")
        print("3: Retrieve a password.")
        print("4: Delete a password.")
        print("5: Show the list of saved services.\n")
        print("0: Exit and lock the vault.\n")

        option = int(validate_input("> ", lambda x: 0 <= int(x) <= 5))

        # Exit.
        if option == 0:
            print("\nLocking vault...")
            vault.lock_vault()

            print("Thanks for using EyeDevelop's Vault!")
            menu = False

        # Store a password.
        elif option == 1:
            service = validate_input("Please enter the service name: ", lambda x: x.isprintable())
            password = validate_input("Please enter the password: ", lambda x: len(x) > 0)

            vault.store_password(service, password)

            print("Saved!")

        # Generate a password.
        elif option == 2:
            service = validate_input("Please enter the service name: ", lambda x: x.isprintable())
            length = int(validate_input("Enter the length of the password: ", lambda x: x.isnumeric()))

            print("\n\nIt's time to choose complexity.")
            print("Complexity is built of three numbers. The letter complexity, number complexity and symbol complexity.")
            print("\nFirst up is letter complexity.")
            print("0 = No letters, 1 = Only lowercase, 2 = Only uppercase, 3 = Mixed case.")
            letter_complexity = validate_input("> ", lambda x: 0 <= int(x) <= 3)

            print("\nNow the number complexity.")
            print("0 = No digits, 1 = Use digits.")
            digit_complexity = validate_input("> ", lambda x: 0 <= int(x) <= 1)

            print("\nFinally, the symbol complexity.")
            print("0 = No symbols, 1 = Use symbols.")
            symbol_complexity = validate_input("> ", lambda x: 0 <= int(x) <= 1)

            complexity = letter_complexity + digit_complexity + symbol_complexity

            password = vault.generate_password(service, length, complexity)
            print("Your generated password:", password)
            print("\nAlso stored in vault.")

        # Retrieve password for service.
        elif option == 3:
            service = validate_input("Please enter the service name: ", lambda x: x.isprintable())

            if service in vault.get_services():
                print("Your password for {}: {}".format(service, vault.get_password(service)))
            else:
                print("That service is not stored in the vault.")

        # Delete service.
        elif option == 4:
            service = validate_input("Please enter the service name: ", lambda x: x.isprintable())

            vault.delete_service(service)

            print("Deleted {}.".format(service))

        # Print services.
        elif option == 5:
            services = vault.get_services()

            print("Your services ({}):\n".format(len(services)))
            for service in services:
                print(service)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
