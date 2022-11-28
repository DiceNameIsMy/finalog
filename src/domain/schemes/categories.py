from dataclasses import dataclass
import uuid


@dataclass
class Category:
    id: uuid.UUID
    name: str

    user_id: uuid.UUID
