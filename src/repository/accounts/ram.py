from datetime import datetime
from decimal import Decimal
import uuid

from repository.accounts import base
from repository import exc, schemes


class RAMAccountRepository(base.AccountRepository):
    _accounts: list[schemes.Account]
    _operations: list[schemes.Operation]

    def __init__(self) -> None:
        self._accounts = []
        self._operations = []
        super().__init__()

    def get_account(self, id: uuid.UUID) -> schemes.Account | None:
        for acc in self._accounts:
            if acc.id == id:
                return acc
        return None

    def create_account(self, name: str) -> schemes.Account:
        account = schemes.Account(
            id=self._make_id(),
            name=name,
            created_at=self._get_created_at_date(),
        )
        self._accounts.append(account)
        return account

    def available_accounts(self) -> list[schemes.Account]:
        return self._accounts

    def get_operation(self, id: uuid.UUID) -> schemes.Operation | None:
        for oper in self._operations:
            if oper.id == id:
                return oper
        return None

    def add_operation(
        self, account_id: uuid.UUID, amount: Decimal
    ) -> schemes.Operation:
        operation = schemes.Operation(
            id=self._make_id(),
            account_id=account_id,
            amount=amount,
            created_at=self._get_created_at_date(),
        )
        self._operations.append(operation)
        return operation

    def list_operations(self) -> list[schemes.Operation]:
        return self._operations

    def delete_operation(self, id: uuid.UUID) -> None:
        for idx, oper in enumerate(self._operations):
            if oper.id == id:
                self._operations.pop(idx)
                return None
        raise exc.DoesNotExist()

    def _make_id(self) -> uuid.UUID:
        return uuid.uuid4()

    def _get_created_at_date(self) -> datetime:
        return datetime.now()