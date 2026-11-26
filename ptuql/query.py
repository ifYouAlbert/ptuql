from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .table import ColumnValue


class QueryOperator(StrEnum):
    Equal = '='
    NotEqual = '!='
    Greater = '>'
    Less = '<'


@dataclass
class Query:
    column_name: str
    operator: QueryOperator
    value: ColumnValue
