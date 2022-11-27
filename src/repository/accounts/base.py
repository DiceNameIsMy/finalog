from abc import ABC, abstractmethod
import uuid
from decimal import Decimal

from repository import schemes


class AccountRepository(ABC):
    @abstractmethod
    def get_account(self, id: uuid.UUID) -> schemes.Account | None:
        pass

    @abstractmethod
    def available_accounts(self) -> list[schemes.Account]:
        pass

    @abstractmethod
    def create_account(self, name: str) -> schemes.Account:
        pass

    #

    @abstractmethod
    def get_operation(self, id: uuid.UUID) -> schemes.Operation | None:
        pass

    @abstractmethod
    def add_operation(
        self, account_id: uuid.UUID, amount: Decimal
    ) -> schemes.Operation:
        pass

    @abstractmethod
    def list_operations(self) -> list[schemes.Operation]:
        pass

    @abstractmethod
    def delete_operation(self, id: uuid.UUID) -> None:
        pass
