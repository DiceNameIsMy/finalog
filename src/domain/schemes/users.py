from dataclasses import dataclass
import uuid


import repository


@dataclass
class User:
    id: uuid.UUID
    email: str
    hashed_password: str

    @classmethod
    def from_repo(cls, user: repository.schemes.User) -> "User":
        return cls(id=user.id, email=user.email, hashed_password=user.hashed_password)
