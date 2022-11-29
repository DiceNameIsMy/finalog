from datetime import datetime
from decimal import Decimal
from typing import Self
import uuid

from repository.accounts.base import AccountRepository
from repository import exc as repo_exc
import utils

from domain import exc, schemes


class AccountDomain:
    def __init__(self, account: schemes.Account, repository: AccountRepository) -> None:
        self.account = account
        self.repository = repository

    @classmethod
    def from_id(
        cls,
        id: uuid.UUID,
        repository: AccountRepository,
    ) -> Self:  # type: ignore[valid-type]
        """
        Create domain instance from account ID

        :raises: DoesNotExist: Account with given ID does not exist
        """
        repo_account = repository.get_account(id)
        if repo_account is None:
            raise exc.DoesNotExist()
        account = schemes.Account.from_repo(repo_account)
        return cls(account=account, repository=repository)

    def add_operation(self, amount: Decimal) -> schemes.Operation:
        repo_operation = self.repository.add_operation(self.account.id, amount)
        return schemes.Operation.from_repo(repo_operation)

    def show_operations(
        self, date_from: datetime, date_to: datetime
    ) -> list[schemes.Operation]:
        if date_from > date_to:
            raise exc.InvalidData(
                "`date_to` parameter should be bigger than `date_from`"
            )

        repo_operations = self.repository.list_operations(date_from, date_to)
        return [schemes.Operation.from_repo(oper) for oper in repo_operations]

    def get_balance(self) -> Decimal:
        repo_opertaions = self.repository.list_operations(
            self.account.created_at, utils.dt.tz_aware_current_dt()
        )
        balance = sum([oper.amount for oper in repo_opertaions], start=Decimal("0.00"))
        return balance

    def remove_operation(self, id: uuid.UUID) -> None:
        try:
            self.repository.delete_operation(id=id)
        except repo_exc.DoesNotExist:
            raise exc.DoesNotExist()

    def get_operation(self, id: uuid.UUID) -> schemes.Operation:
        repo_operation = self.repository.get_operation(id=id)
        if repo_operation is None:
            raise exc.DoesNotExist()

        return schemes.Operation.from_repo(repo_operation)
