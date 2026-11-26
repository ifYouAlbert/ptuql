from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from ..table import ColumnValue
from crypto_yayca import CryptoYayca


@dataclass
class HashEntry:
    key: ColumnValue
    row_ids: list[int] = field(default_factory=list)


class HashTable:
    def __init__(self, bucket_count: int = 16) -> None:
        if bucket_count <= 0:
            raise ValueError("Bucket count must be > 0")

        self.bucket_count: Final[int] = bucket_count
        self.buckets: list[list[HashEntry]] = [[] for _ in range(bucket_count)]

    def insert(self, value: ColumnValue, row_id: int) -> None:
        bucket = self._get_bucket(value)

        for entry in bucket:
            if entry.key == value:
                entry.row_ids.append(row_id)
                return

        bucket.append(HashEntry(value, [row_id]))

    def search(self, value: ColumnValue) -> list[int]:
        bucket = self._get_bucket(value)

        for entry in bucket:
            if entry.key == value:
                return entry.row_ids.copy()

        return []

    def _get_bucket_index(self, value: ColumnValue) -> int:
        # return hash(value) % self.bucket_count
        return CryptoYayca.strongest_db_hash(value, self.bucket_count)

    def _get_bucket(self, value: ColumnValue) -> list[HashEntry]:
        return self.buckets[self._get_bucket_index(value)]


if __name__ == "__main__":
    def main():
        from pprint import pprint

        table = HashTable(bucket_count=5)

        table.insert(18, 0)
        table.insert(23, 1)
        table.insert(21, 2)
        table.insert(18, 3)

        assert table.search(18) == [0, 3]
        assert table.search(23) == [1]
        assert table.search(21) == [2]
        assert table.search(99) == []

        print("buckets: ")
        pprint(table.buckets)

    main()
