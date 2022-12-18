from datetime import datetime
from decimal import Decimal
import uuid

from repository.accounts.base import AccountRepository
from repository import exc as repo_exc
import utils

from core import exc, schemes


class AccountDomain:
    def __init__(self, account: schemes.Account, repository: AccountRepository) -> None:
        self.account = account
        self.repository = repository

    @classmethod
    def from_id(
        cls,
        id: uuid.UUID,
        repository: AccountRepository,
    ) -> "AccountDomain":
        """
        Create domain instance from account ID

        :raises: DoesNotExist: Account with given ID does not exist
        """
        repo_account = repository.get_account(id)
        if repo_account is None:
            raise exc.DoesNotExist()
        account = schemes.Account.from_repo(repo_account)
        return cls(account=account, repository=repository)

    def set_new_name(self, new_name: str) -> schemes.Account:
        if len(new_name) == 0:
            raise exc.InvalidData()
        if len(new_name) >= 32:
            raise exc.InvalidData()
        try:
            account = self.repository.update_account(self.account.id, name=new_name)
        except repo_exc.InvalidData:
            raise exc.InvalidData()
        self.account = schemes.Account.from_repo(account)
        return self.account

    def add_operation(
        self, amount: Decimal, category: schemes.Category
    ) -> schemes.Operation:
        if not category.belong_to_user(self.account.user_id):
            raise exc.InvalidData("given category does not belong to account")
        repo_operation = self.repository.add_operation(
            self.account.id, amount, category.id
        )
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

    def get_balance(self) -> Decimal:
        repo_opertaions = self.repository.list_operations(
            self.account.created_at, utils.dt.tz_aware_current_dt()
        )
        operations = [schemes.Operation.from_repo(oper) for oper in repo_opertaions]
        balance = self.account.get_balance(operations)
        return balance
