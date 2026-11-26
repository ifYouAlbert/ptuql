import warnings


class CryptoYayca:
    """Written by Yaroslave in PTU"""

    @staticmethod
    def hash_password(password: str, salt: str, hash_size: int) -> int:
        message = password + salt
        shift = max(hash_size // len(message), 1)

        # print(f"shift {password} - {hash_size}: {shift}")

        num = 0
        for char in message:
            # print(f"Processing: {char}")
            ord_char = ord(char)
            bin_num = bin(ord_char)[2:]
            # print(f"{bin_num = }")
            # len_bin = len(bin_num)
            # print(f"len: {len_bin}")
            # print(f"{bin(num << 5)}")
            # print(f"биннам до {bin(num)}")
            num = num << shift | ord_char
            # print(f"биннам после {bin(num)}")
            # print(f"password: {num}")
            # print()
        return num

    @staticmethod
    def strongest_db_hash(key: int | str, table_size: int) -> int:
        h = 5381
        for char in str(key):
            h = ((h << 5) + h) + ord(char)
        return h % table_size

    @staticmethod
    @warnings.deprecated("This hash is very simple and should not be used in an ENTERPRISE. "
                         "Use the CryptoYayca.strongest_db_hash")
    def simple_db_hash(key: str, table_size: int) -> int:
        return hash(key) % table_size
