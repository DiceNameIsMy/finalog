from abc import ABC, abstractmethod
from datetime import datetime
import uuid
from decimal import Decimal

from repository import schemes, enums


class AccountRepository(ABC):
    @abstractmethod
    def get_account(self, id: uuid.UUID) -> schemes.Account | None:
        pass

    @abstractmethod
    def list_accounts(self, user_id: uuid.UUID) -> list[schemes.Account]:
        pass

    @abstractmethod
    def create_account(
        self,
        name: str,
        currency: enums.Currency,
        base_balance: Decimal,
        user_id: uuid.UUID,
    ) -> schemes.Account:
        pass

    @abstractmethod
    def update_account(
        self,
        id: uuid.UUID,
        name: str | None = None,
        currency: enums.Currency | None = None,
    ) -> schemes.Account:
        """
        raises: InvalidData
        """

    #

    @abstractmethod
    def get_operation(self, id: uuid.UUID) -> schemes.Operation | None:
        pass

    @abstractmethod
    def add_operation(
        self, account_id: uuid.UUID, amount: Decimal, category_id: uuid.UUID
    ) -> schemes.Operation:
        pass

    @abstractmethod
    def list_operations(
        self, date_from: datetime, date_to: datetime
    ) -> list[schemes.Operation]:
        pass

    @abstractmethod
    def delete_operation(self, id: uuid.UUID) -> None:
        pass
