from __future__ import annotations

from enum import StrEnum, Enum
from typing import NamedTuple, Final, Any


class IndexMethod(StrEnum):
    HashTable = "HashTable"
    BST = "BST"
    SeqScan = "SeqScan"


class DataTypeValue(NamedTuple):
    id: int
    name: str
    types: tuple[type, ...]
    index_methods: tuple[IndexMethod, ...]
    is_support_auto: bool = False


class DataType(Enum):
    Number = DataTypeValue(
        1,
        "Number",
        (int, float),
        (IndexMethod.HashTable, IndexMethod.BST)
    )
    String = DataTypeValue(
        2,
        "String",
        (str,),
        (IndexMethod.HashTable, IndexMethod.BST)
    )
    PrimaryKey = DataTypeValue(
        3,
        "PrimaryKey",
        (int,),
        (IndexMethod.HashTable, IndexMethod.BST),
        True
    )

    @property
    def types(self): return self.value.types
    @property
    def is_support_auto(self): return self.value.is_support_auto
    @property
    def index_methods(self): return self.value.index_methods


class Literals(StrEnum):
    Auto = "Auto"


class Column(NamedTuple):
    name: str
    data_type: DataType


type ColumnValue = Any


class Table:
    primary_key_index: Final[int] = 0

    def __init__(self, columns: list[Column]) -> None:
        if len(columns) < 1 or columns[self.primary_key_index].data_type != DataType.PrimaryKey:
            raise ValueError

        self.columns: Final[list[Column]] = columns
        self.columns_index: Final[dict[str, int]] = {f.name: f_i for f_i, f in enumerate(self.columns)}
        self.rows: list[list[ColumnValue]] = []

        self.stats: dict[str, dict[ColumnValue, int]] = {
            col.name: {} for col in self.columns
        }

    def add(self, values: list[ColumnValue]) -> int:
        self._check(values)
        new_id: int = len(self.rows)

        row: list[ColumnValue] = []
        for value, column in zip(values, self.columns):
            if value is Literals.Auto:
                if column.data_type == DataType.PrimaryKey:
                    row_el = new_id
                else:
                    raise ValueError
            else:
                row_el = value
            row.append(row_el)

        self.rows.append(row)

        for column, value in zip(self.columns, row):
            stats = self.stats[column.name]
            stats[value] = stats.get(value, 0) + 1

        return new_id

    def get(self, row_id: int) -> list[ColumnValue]:
        if 0 <= row_id < len(self.rows):
            return self.rows[row_id]
        raise IndexError(f'Row id {row_id} is out of range')

    def get_col_value(self, row_id: int, col_name: str) -> ColumnValue:
        row = self.get(row_id)
        self._check_column(col_name)
        return row[self.columns_index[col_name]]

    def get_col_by_name(self, col_name: str) -> Column:
        self._check_column(col_name)
        return self.columns[self.columns_index[col_name]]

    def _check(self, values: list[ColumnValue]):
        if len(self.columns) != len(values):
            raise ValueError(f'Number of columns does not match number of values')
        for value, column in zip(values, self.columns):
            if value is Literals.Auto and column.data_type.is_support_auto:
                continue
            if not isinstance(value, column.data_type.types):
                raise ValueError(f'Column {column.name} is not of type {column.data_type.types}')

    def _check_column(self, col_name: str):
        if col_name not in self.columns_index:
            raise ValueError(f'Column {col_name} is not in table')


if __name__ == '__main__':
    def main():
        f0 = Column("id", DataType.PrimaryKey)
        f1 = Column("name", DataType.String)
        f2 = Column("age", DataType.Number)

        t = Table([f0, f1, f2])
        print(t.add([Literals.Auto, "Ivan", 19]))
        print(t.add([Literals.Auto, "Andrew", 19]))

        print(t.get(0))
        print(t.get_col_value(0, "age"))
        print(t.get_col_value(1, "name"))
    main()
