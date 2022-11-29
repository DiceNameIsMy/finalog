from abc import ABC, abstractmethod
import uuid
from repository import schemes


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, email: str, hashed_password: str) -> schemes.User:
        pass

    @abstractmethod
    def get_user(self, id: uuid.UUID) -> schemes.User | None:
        pass

    @abstractmethod
    def create_category(self, name: str, user_id: uuid.UUID) -> schemes.Category:
        pass

    @abstractmethod
    def get_category(self, id: uuid.UUID) -> schemes.Category | None:
        pass

    @abstractmethod
    def list_categories(
        self, user_id: uuid.UUID | None = None
    ) -> list[schemes.Category]:
        pass
