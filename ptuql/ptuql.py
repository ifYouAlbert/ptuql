from __future__ import annotations

import math
from typing import Final

from .table import Column, Table, ColumnValue, IndexMethod
from .methods.hash_table import HashTable
from .methods.bst import BST
from .methods.seq import SeqScanner
from .query import QueryOperator, Query


class PtuQL:
    method_operators: Final[dict[IndexMethod, tuple[QueryOperator, ...]]] = {
        IndexMethod.HashTable: (
            QueryOperator.Equal,
        ),
        IndexMethod.BST: (
            QueryOperator.Equal,
            QueryOperator.NotEqual,
            QueryOperator.Greater,
            QueryOperator.Less,
        ),
        IndexMethod.SeqScan: tuple(QueryOperator),
    }

    def __init__(self, columns: list[Column]) -> None:
        self.table: Table = Table(columns)

        self.hash_indexes: Final[dict[str, HashTable]] = {}
        self.bst_indexes: Final[dict[str, BST]] = {}
        self.seq_scanner: Final[SeqScanner] = SeqScanner(self.table)

        for col in columns:
            methods = col.data_type.index_methods

            if IndexMethod.HashTable in methods:
                self.hash_indexes[col.name] = HashTable()
            if IndexMethod.BST in methods:
                self.bst_indexes[col.name] = BST()

    def select(self, query: Query) -> list[list[ColumnValue]]:
        col = self.table.get_col_by_name(query.column_name)

        if not isinstance(query.value, col.data_type.types):
            raise ValueError(f"Invalid value type for column {col.name}")

        method = self._get_index_method(col, query.operator, query.value)

        match method:
            case IndexMethod.SeqScan:
                row_ids = self.seq_scanner.get(col.name, query.operator, query.value)
            case IndexMethod.HashTable:
                row_ids = self.hash_indexes[col.name].search(query.value)
            case IndexMethod.BST:
                row_ids = self.bst_indexes[col.name].search(query.operator, query.value)
            case _:
                raise ValueError(f"Unsupported method: {method}")

        return [self.table.get(row_id) for row_id in row_ids]

    def insert(self, values: list[ColumnValue]) -> int:
        row_id = self.table.add(values)
        row = self.table.get(row_id)

        for col, value in zip(self.table.columns, row):
            if col.name in self.hash_indexes:
                self.hash_indexes[col.name].insert(value, row_id)

            if col.name in self.bst_indexes:
                self.bst_indexes[col.name].insert(value, row_id)

        return row_id

    def insert_list(self, values: list[list[ColumnValue]]) -> list[int]:
        return [self.insert(v) for v in values]

    def _get_index_method(self, col: Column, op: QueryOperator, value: ColumnValue) -> IndexMethod:
        costs = self._get_methods_costs(col, op, value)
        return min(costs, key=costs.__getitem__)

    def _get_methods_costs(self, col: Column, op: QueryOperator, value: ColumnValue) -> dict[IndexMethod, float]:
        n = len(self.table.rows)

        costs: dict[IndexMethod, float] = {
            IndexMethod.SeqScan: n,
        }

        if n == 0:
            return costs

        m = self._get_operator_matches(col.name, op, value)

        for method in col.data_type.index_methods:
            if op not in self.method_operators[method]:
                continue

            match method:
                case IndexMethod.HashTable:
                    if col.name in self.hash_indexes:
                        costs[method] = 1 + 4 * m

                case IndexMethod.BST:
                    if col.name in self.bst_indexes:
                        h = math.ceil(math.log2(n + 1))
                        costs[method] = h + 4 * m

        return costs

    def _get_operator_matches(self, col_name: str, op: QueryOperator, value: ColumnValue) -> int:
        stats = self.table.stats[col_name]

        match op:
            case QueryOperator.Equal:
                return stats.get(value, 0)
            case QueryOperator.NotEqual:
                return len(self.table.rows) - stats.get(value, 0)
            case QueryOperator.Greater:
                return sum(
                    count for key, count in stats.items()
                    if key > value
                )
            case QueryOperator.Less:
                return sum(
                    count for key, count in stats.items()
                    if key < value
                )
            case _:
                raise ValueError(f"Unsupported operator: {op}")
