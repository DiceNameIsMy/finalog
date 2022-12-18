from datetime import datetime
from decimal import Decimal
import uuid

from repository.accounts import base
from repository import exc, schemes, enums
import utils


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

    def create_account(
        self,
        name: str,
        currency: enums.Currency,
        base_balance: Decimal,
        user_id: uuid.UUID,
    ) -> schemes.Account:
        for accnt in self._accounts:
            if accnt.user_id == user_id and accnt.name == name:
                raise exc.InvalidData(
                    detail="User already have an account with given name",
                    code="already_exists",
                )

        account = schemes.Account(
            id=self._make_id(),
            name=name,
            currency=currency,
            base_balance=base_balance,
            user_id=user_id,
            created_at=self._get_created_at_date(),
        )
        self._accounts.append(account)
        return account

    def list_accounts(self, user_id: uuid.UUID) -> list[schemes.Account]:
        return list(filter(lambda accnt: accnt.user_id == user_id, self._accounts))

    def update_account(
        self,
        id: uuid.UUID,
        name: str | None = None,
        currency: enums.Currency | None = None,
    ) -> schemes.Account:
        account = self.get_account(id)
        if account is None:
            raise exc.DoesNotExist()
        if name is not None:
            for acc in self._accounts:
                if (
                    acc.id != account.id
                    and acc.user_id == account.user_id
                    and acc.name == name
                ):
                    raise exc.InvalidData(
                        detail="User Already has account with given name",
                        code="name_is_taken",
                    )
            account.name = name

        if currency is not None:
            account.currency = currency

        return account

    def get_operation(self, id: uuid.UUID) -> schemes.Operation | None:
        for oper in self._operations:
            if oper.id == id:
                return oper
        return None

    def add_operation(
        self, account_id: uuid.UUID, amount: Decimal, category_id: uuid.UUID
    ) -> schemes.Operation:
        operation = schemes.Operation(
            id=self._make_id(),
            account_id=account_id,
            amount=amount,
            category_id=category_id,
            created_at=self._get_created_at_date(),
        )
        self._operations.append(operation)
        return operation

    def list_operations(
        self, date_from: datetime, date_to: datetime
    ) -> list[schemes.Operation]:
        operations_in_range: list[schemes.Operation] = []
        for oper in self._operations:
            if oper.created_at >= date_from and oper.created_at <= date_to:
                operations_in_range.append(oper)

        return operations_in_range

    def delete_operation(self, id: uuid.UUID) -> None:
        for idx, oper in enumerate(self._operations):
            if oper.id == id:
                self._operations.pop(idx)
                return None
        raise exc.DoesNotExist()

    def _make_id(self) -> uuid.UUID:
        return uuid.uuid4()

    def _get_created_at_date(self) -> datetime:
        return utils.dt.tz_aware_current_dt()
