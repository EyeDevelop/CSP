import os
import pickle
import random
import string

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random.random import getrandbits

# Garble memory so this isn't in a static place.
a = [0] * random.gauss(10, 5)
ANTI_MEMORY_KEY = getrandbits(32)
del a


class Vault:
    def __init__(self, vault_key: bytes, vault_file: str = "vault.edb", aes_type: int = AES.MODE_EAX):
        """
        A class which generates and stores passwords.
        """

        # Store the main passwords dictionary
        self.passwords = {}

        # Keep track of vault status.
        self.vault_unlocked = False
        self.vault_file = vault_file

        # Set the password requirements.
        self.aes_type = aes_type

        # Store the vault key for ease-of-use.
        self.vault_key = self.__encrypt_password(pad(vault_key, 32))

    @staticmethod
    def __encrypt_password(key: bytes):
        """
        A function that obfuscates the password so it is not stored in memory as plain text.

        :param key: The programs anti-memory reading key.
        :return:
        """

        # Encrypt the password.
        cipher = AES.new(ANTI_MEMORY_KEY, AES.MODE_EAX)
        obfuscated_password, tag = cipher.encrypt_and_digest(key)

        return b";".join([obfuscated_password, tag, cipher.nonce])

    @staticmethod
    def __decrypt_password(key: bytes):
        """
        A function that de-obfuscates the password so it can be used as normal.

        :param key: The programs anti-memory reading key.
        :return:
        """

        # Decrypt the password.
        obfuscated_password, tag, nonce = key.split(b";")
        cipher = AES.new(ANTI_MEMORY_KEY, AES.MODE_EAX, nonce)

        return cipher.decrypt_and_verify(obfuscated_password, tag)

    @staticmethod
    def _generate_password(length: int, complexity_info: str) -> str:
        """
        A function which generates a password.

        :param length: The length of the passwords.
        :param complexity_info: The complexity of the password as a string: "<letter parameter><digit parameter><symbol parameter>". I.e. "311" for the strongest password.

        Letter parameter:
          0 - No letters.
          1 - All lowercase.
          2 - All uppercase.
          3 - Mixed lowercase and uppercase.

        Digit parameter:
          0 - No digits.
          1 - Digits.

        Symbol parameter:
          0 - No symbols
          1 - Symbols.
        :return:
        """

        # Prepare the dataset with options.
        dataset_options = {
            "letter": {
                "0": "",
                "1": string.ascii_lowercase,
                "2": string.ascii_uppercase,
                "3": string.ascii_letters
            },

            "digit": {
                "0": "",
                "1": string.digits
            },

            "symbol": {
                "0": "",
                "1": "!@#$%^&*()-_=+[{}];:|,./<>?"
            }
        }

        # Retrieve the dataset_options.
        letter_complexity, digit_complexity, symbol_complexity = list(complexity_info)

        # Assemble the dataset.
        dataset = dataset_options["letter"][letter_complexity] + dataset_options["digit"][digit_complexity] + dataset_options["symbol"][symbol_complexity]

        # Generate a password.
        password = "".join([random.choice(dataset) for _ in range(length)])

        return password

    def generate_password(self, service_name: str, length: int, complexity_info: str) -> str:
        """
        A function which generates a password, then stores it in the vault.

        :param service_name: The name of the password for Vault purposes.
        :param length: The length of the passwords.
        :param complexity_info: The complexity of the password as a string: "<letter parameter><digit parameter><symbol parameter>". I.e. "311" for the strongest password.

        Letter parameter:
          0 - No letters.
          1 - All lowercase.
          2 - All uppercase.
          3 - Mixed lowercase and uppercase.

        Digit parameter:
          0 - No digits.
          1 - Digits.

        Symbol parameter:
          0 - No symbols
          1 - Symbols.
        :return:
        """

        # Generate the password.
        password = self._generate_password(length, complexity_info)

        # Store the password.
        self.store_password(service_name, password)

        # Return the password.
        return password

    def unlock_vault(self):
        """
        A function which unlocks the vault.

        :return:
        """

        # Don't unlock if the vault is already unlocked.
        if self.vault_unlocked:
            return

        # If the file doesn't exist, the vault is automatically unlocked.
        if not os.path.isfile(self.vault_file):
            self.vault_unlocked = True
            return

        # Open the vault.
        with open(self.vault_file, 'rb') as vault_file:
            nonce, tag, vault_encrypted = [vault_file.read(x) for x in (16, 16, -1)]
            cipher = AES.new(self.__decrypt_password(self.vault_key), self.aes_type, nonce)

            vault_decrypted = cipher.decrypt_and_verify(vault_encrypted, tag)
            self.passwords = pickle.loads(vault_decrypted)

            self.vault_unlocked = True

    def lock_vault(self):
        """
        A function which locks the vault.

        :return:
        """

        # Don't lock if it's already locked.
        if not self.vault_unlocked:
            return

        # Lock the vault and write the data.
        with open(self.vault_file, 'wb') as vault_file:
            cipher = AES.new(self.__decrypt_password(self.vault_key), self.aes_type)

            data, tag = cipher.encrypt_and_digest(pickle.dumps(self.passwords))
            for x in [cipher.nonce, tag, data]:
                vault_file.write(x)

        self.vault_unlocked = False

        # For security, remove all references to the key and data.
        self.passwords = None
        cipher, data, tag = [None] * 3

        del cipher
        del data
        del tag

    def store_password(self, service_name: str, password: str):
        """
        An intermediary function to store password in the dictionary.
        The vault is locked after storing.

        :param service_name: The name of the password.
        :param password: The password to add.
        :return:
        """

        # First unlock the vault.
        self.unlock_vault()
        assert self.vault_unlocked, "Failed to unlock vault."

        # Store the password and lock the vault.
        self.passwords[service_name.lower()] = password
        self.lock_vault()

    def get_password(self, service_name: str):
        """
        An intermediary function to retrieve passwords from the vault.

        :param service_name: The name of the password.
        :return:
        """

        # First unlock the vault.
        self.unlock_vault()
        assert self.vault_unlocked, "Failed to unlock vault."
        assert service_name.lower() in self.passwords, "Password not found in vault."

        # Retrieve the password and lock the vault.
        password = self.passwords[service_name.lower()]
        self.lock_vault()

        return password

    def get_services(self):
        """
        A function to return the keys of the password dictionary for retrieval.

        :return:
        """

        # First unlock the vault.
        self.unlock_vault()
        assert self.vault_unlocked, "Failed to unlock vault."

        # Get the services and lock the vault.
        keys = self.passwords.keys()
        self.lock_vault()

        return keys

    def delete_service(self, service_name: str):
        """
        A function to delete a password from the vault.

        :param service_name: The service to delete.
        :return:
        """

        # First unlock the vault.
        self.unlock_vault()
        assert self.vault_unlocked, "Failed to unlock vault."

        # Delete the service.
        if service_name in self.passwords.keys():
            del self.passwords[service_name]

        # Lock the vault.
        self.lock_vault()
