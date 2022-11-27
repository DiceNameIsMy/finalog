from enum import Enum


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    KZT = "KZT"
    CZK = "CZK"

    def __str__(self) -> str:
        return self.value
