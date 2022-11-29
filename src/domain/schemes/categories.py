from dataclasses import dataclass
import uuid

import repository as repo


@dataclass
class Category:
    id: uuid.UUID
    name: str

    user_id: uuid.UUID

    @classmethod
    def from_repo(cls, category: repo.schemes.Category) -> "Category":
        return cls(id=category.id, name=category.name, user_id=category.user_id)
