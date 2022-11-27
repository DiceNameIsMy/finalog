import uuid
from decimal import Decimal

import pytest

import repository
import domain


@pytest.fixture()
def account_repo() -> repository.AccountRepository:
    return repository.RAMAccountRepository()


@pytest.fixture()
def account_id(account_repo: repository.AccountRepository) -> uuid.UUID:
    account = account_repo.create_account("test_account")
    return account.id


@pytest.fixture()
def account_domain(
    account_id: uuid.UUID, account_repo: repository.AccountRepository
) -> domain.AccountDomain:
    return domain.AccountDomain.from_id(account_id, account_repo)


@pytest.fixture()
def operation(
    account_id: uuid.UUID, account_repo: repository.AccountRepository
) -> domain.schemes.Operation:
    amount = Decimal("1.99")
    operation = account_repo.add_operation(account_id, amount)
    return domain.schemes.Operation.from_repo(operation)
