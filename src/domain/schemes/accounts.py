from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID
import uuid

import repository as repo


@dataclass
class Account:
    id: UUID
    name: str
    currency: repo.enums.Currency
    user_id: uuid.UUID

    created_at: datetime

    @classmethod
    def from_repo(
        cls,
        repo_acc: repo.schemes.Account,
    ) -> Self:  # type: ignore[valid-type]
        return cls(
            id=repo_acc.id,
            name=repo_acc.name,
            currency=repo_acc.currency,
            user_id=repo_acc.user_id,
            created_at=repo_acc.created_at,
        )
