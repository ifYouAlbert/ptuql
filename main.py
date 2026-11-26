from pprint import pprint

from ptuql import PtuQL
from ptuql.query import Query, QueryOperator
from ptuql.table import Column, DataType, Literals

if __name__ == "__main__":
    pql = PtuQL([
        Column("id", DataType.PrimaryKey),
        Column("date year", DataType.Number),
        Column("name", DataType.String),
        Column("age", DataType.Number),
        Column("company", DataType.String),
    ])

    pql.insert_list([
        [Literals.Auto, 2023, "Ivan L.", 16, "sno_is"],
        [Literals.Auto, 2023, "Ivan L.", 16, "spo journal"],
        [Literals.Auto, 2023, "Albert", 16, "spo journal"],
        [Literals.Auto, 2024, "Albert", 17, "HellHounds"],
        [Literals.Auto, 2025, "Fedor", 18, "Ai Docs"],
        [Literals.Auto, 2025, "Ivan L.", 18, "Ai Docs"],
        [Literals.Auto, 2025, "Albert", 17, "Storyloom"],
        [Literals.Auto, 2025, "Fedor", 18, "Storyloom"],
        [Literals.Auto, 2025, "J. Jordan", 19, "Edge inc."],
        [Literals.Auto, 2025, "Albert", 18, "Edge inc."],
        [Literals.Auto, 2026, "Ivan L.", 19, "Quantum Safe Systems co."],
        [Literals.Auto, 2026, "Albert", 18, "Quantum Safe Systems co."],
        [Literals.Auto, 2026, "Fedor", 19, "SPO ENTERPRICE LLC"],
        [Literals.Auto, 2026, "Nikas", 19, "SPO ENTERPRICE LLC"],
        [Literals.Auto, 2026, "Ivan L.", 19, "SPO ENTERPRICE LLC"],
        [Literals.Auto, 2026, "Albert", 19, "SPO ENTERPRICE LLC"],
    ])

    cols = pql.table.columns
    get_costs = pql._get_methods_costs

    print()
    print("HashTable:")
    pprint(get_costs(cols[2], QueryOperator.Equal, "J. Jordan"))

    print()
    print("BST:")
    pprint(get_costs(cols[0], QueryOperator.Greater, 12))

    print()
    print("SeqScan:")
    pprint(get_costs(cols[1], QueryOperator.Greater, 2024))

    print()
    print("select:")
    pprint(pql.select(Query("company", QueryOperator.Equal, "SPO ENTERPRICE LLC")))
