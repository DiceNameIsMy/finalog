from dataclasses import dataclass
import uuid


@dataclass
class User:
    id: uuid.UUID
    email: str
    hashed_password: str
