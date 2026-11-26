from __future__ import annotations

from dataclasses import dataclass, field

from ..table import ColumnValue
from ..query import QueryOperator


@dataclass
class BSTNode:
    key: ColumnValue
    row_ids: list[int] = field(default_factory=list)
    left: BSTNode | None = None
    right: BSTNode | None = None


class BST:
    def __init__(self) -> None:
        self.root: BSTNode | None = None

    def insert(self, value: ColumnValue, row_id: int) -> None:
        self.root = self._insert(self.root, value, row_id)

    def search(self, op: QueryOperator, value: ColumnValue) -> list[int]:
        result: list[int] = []
        self._search(self.root, op, value, result)
        return result

    def get_height(self) -> int:
        return self._get_height(self.root)

    def _insert(self, node: BSTNode | None, value: ColumnValue, row_id: int) -> BSTNode:
        if node is None:
            return BSTNode(value, [row_id])

        if value < node.key:
            node.left = self._insert(node.left, value, row_id)
        elif value > node.key:
            node.right = self._insert(node.right, value, row_id)
        else:
            node.row_ids.append(row_id)

        return node

    def _search(self, node: BSTNode | None, op: QueryOperator, value: ColumnValue, result: list[int]) -> None:
        if node is None:
            return

        match op:
            case QueryOperator.Equal:
                if value < node.key:
                    self._search(node.left, op, value, result)
                elif value > node.key:
                    self._search(node.right, op, value, result)
                else:
                    result.extend(node.row_ids)

            case QueryOperator.NotEqual:
                self._search(node.left, op, value, result)

                if node.key != value:
                    result.extend(node.row_ids)

                self._search(node.right, op, value, result)

            case QueryOperator.Greater:
                if node.key > value:
                    self._search(node.left, op, value, result)
                    result.extend(node.row_ids)

                self._search(node.right, op, value, result)

            case QueryOperator.Less:
                self._search(node.left, op, value, result)

                if node.key < value:
                    result.extend(node.row_ids)
                    self._search(node.right, op, value, result)

            case _:
                raise ValueError(f"Unsupported operator: {op}")

    def _get_height(self, node: BSTNode | None) -> int:
        if node is None:
            return 0

        return 1 + max(
            self._get_height(node.left),
            self._get_height(node.right)
        )


if __name__ == "__main__":
    def main():
        from pprint import pprint

        bst = BST()

        bst.insert(21, 0)
        bst.insert(18, 1)
        bst.insert(25, 2)
        bst.insert(17, 3)
        bst.insert(18, 4)
        bst.insert(30, 5)

        assert bst.search(QueryOperator.Equal, 18) == [1, 4]
        assert bst.search(QueryOperator.Equal, 99) == []
        assert bst.search(QueryOperator.Greater, 21) == [2, 5]
        assert bst.search(QueryOperator.Less, 21) == [3, 1, 4]
        assert bst.search(QueryOperator.NotEqual, 21) == [3, 1, 4, 2, 5]

        assert bst.get_height() == 3

        pprint(bst.search(QueryOperator.NotEqual, 0))

    main()
