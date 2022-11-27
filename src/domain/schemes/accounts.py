from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID

import repository as repo


@dataclass
class Account:
    id: UUID
    name: str
    created_at: datetime

    @classmethod
    def from_repo(
        cls,
        repo_acc: repo.schemes.Account,
    ) -> Self:  # type: ignore[valid-type]
        return cls(id=repo_acc.id, name=repo_acc.name, created_at=repo_acc.created_at)
