from ..table import Table, Column, ColumnValue
from ..query import QueryOperator


class SeqScanner:
    def __init__(self, table: Table):
        self.table = table

    def get(self, col_name: str, op: QueryOperator, value: ColumnValue) -> list[int]:
        col_index = self.table.columns_index[col_name]
        result: list[int] = []

        for row_id, row in enumerate(self.table.rows):
            if self._compare(row[col_index], op, value):
                result.append(row_id)

        return result

    @staticmethod
    def _compare(left: ColumnValue, op: QueryOperator, right: ColumnValue) -> bool:
        match op:
            case QueryOperator.Equal:
                return left == right
            case QueryOperator.NotEqual:
                return left != right
            case QueryOperator.Greater:
                return left > right
            case QueryOperator.Less:
                return left < right
            case _:
                raise ValueError(f"Unsupported operator: {op}")


if __name__ == "__main__":
    def main():
        from pprint import pprint
        from table import Table, DataType, Literals
        from random import randint
        idk = randint(19, 20)

        t = Table([
            Column("id", DataType.PrimaryKey),
            Column("name", DataType.String),
            Column("age", DataType.Number),
            Column("company", DataType.String),
        ])
        seq = SeqScanner(t)

        def get_rows(rows_ids: list[int]) -> list[list[ColumnValue]]:
            return [t.get(row_id) for row_id in rows_ids]

        t.add([Literals.Auto, "J. Jordan", 19, "Edge inc."])
        t.add([Literals.Auto, "Ivan L.", idk, "Quantum Safe Systems co."])
        t.add([Literals.Auto, "Albert Shturnev", 19, "SPO ENTERPRISE LLC"])

        sep = ['='*50]

        pprint(
            get_rows(
                seq.get("company", QueryOperator.Equal, "Edge inc.")
            ) + sep +
            get_rows(
                seq.get("name", QueryOperator.Equal, "Ivan L.")
            ) + sep +
            get_rows(
                seq.get("age", QueryOperator.Greater, 18)
            )
        )

    main()
