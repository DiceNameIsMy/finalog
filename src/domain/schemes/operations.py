from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import uuid

import repository as repo


@dataclass
class Operation:
    id: UUID
    amount: Decimal
    category_id: uuid.UUID
    created_at: datetime

    @classmethod
    def from_repo(
        cls,
        repo_oper: repo.schemes.Operation,
    ) -> "Operation":
        return cls(
            id=repo_oper.id,
            amount=repo_oper.amount,
            category_id=repo_oper.category_id,
            created_at=repo_oper.created_at,
        )
