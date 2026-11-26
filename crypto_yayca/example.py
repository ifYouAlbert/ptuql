from crypto_yayca import CryptoYayca


def main():
    messages: list[str] = [
        "😂😂4сиксевен Z",
        "l;kswegtkl;fdsgkjl;zklgj;;kljo",
        "гойданасамск массоно пидидитральный узел развития трахтенберга habiby diddi allax",
        "2a46-m5",
        "ZPT-98",
        "Сьешь ещё этих мягких французских булок, да выпей чаю"
    ]

    def hash_password(name, _) -> int:
        return CryptoYayca.hash_password(name, "salt", 170)

    for message in messages:
        print(f"{message} (len={len(message)})")
        for hash_func in (
                hash_password,
                CryptoYayca.strongest_db_hash,
                CryptoYayca.simple_db_hash,
        ):
            hash_value = hash_func(message, 1000)
            print(f"\t* {hash_func.__name__:<20} | {hex(hash_value)} -> {hash_value}")
        print()


if __name__ == "__main__":
    main()
