from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Self
from uuid import UUID

import repository as repo


@dataclass
class Operation:
    id: UUID
    amount: Decimal
    created_at: datetime

    @classmethod
    def from_repo(
        cls,
        repo_oper: repo.schemes.Operation,
    ) -> Self:  # type: ignore[valid-type]
        return cls(
            id=repo_oper.id, amount=repo_oper.amount, created_at=repo_oper.created_at
        )
