from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import uuid

import repository as repo

from core.schemes.operations import Operation


@dataclass
class Account:
    id: UUID
    name: str
    currency: repo.enums.Currency
    base_balance: Decimal
    user_id: uuid.UUID

    created_at: datetime

    @classmethod
    def from_repo(
        cls,
        repo_acc: repo.schemes.Account,
    ) -> "Account":
        return cls(
            id=repo_acc.id,
            name=repo_acc.name,
            currency=repo_acc.currency,
            base_balance=repo_acc.base_balance,
            user_id=repo_acc.user_id,
            created_at=repo_acc.created_at,
        )

    def get_balance(self, all_operations: list[Operation]) -> Decimal:
        balance = self.base_balance
        for oper in all_operations:
            assert oper.account_id == self.id
            balance += oper.amount
        return balance
