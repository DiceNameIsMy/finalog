import uuid
from decimal import Decimal

import pytest

import repository
import domain


@pytest.fixture()
def user_repo() -> repository.UserRepository:
    return repository.RAMUserRepository()


@pytest.fixture()
def user_id(user_repo: repository.UserRepository) -> uuid.UUID:
    user = user_repo.create_user(
        email="test_email@email.com", hashed_password="insecure_password"
    )
    return user.id


@pytest.fixture()
def another_user_id(user_repo: repository.UserRepository) -> uuid.UUID:
    another_user = user_repo.create_user(
        email="test_email2@email.com", hashed_password="insecure_password"
    )
    return another_user.id


@pytest.fixture()
def user_domain(
    user_id: uuid.UUID,
    user_repo: repository.UserRepository,
    account_repo: repository.AccountRepository,
) -> domain.UserDomain:
    return domain.UserDomain.from_id(user_id, user_repo, account_repo)


@pytest.fixture()
def account_repo() -> repository.AccountRepository:
    return repository.RAMAccountRepository()


@pytest.fixture()
def account(
    user_id: uuid.UUID, account_repo: repository.AccountRepository
) -> domain.schemes.Account:
    account = account_repo.create_account(
        "test_account", repository.enums.Currency.USD, Decimal(0), user_id
    )
    return domain.schemes.Account.from_repo(account)


@pytest.fixture()
def account_id(account: domain.schemes.Account) -> uuid.UUID:
    return account.id


@pytest.fixture()
def account2(
    user_id: uuid.UUID, account_repo: repository.AccountRepository
) -> domain.schemes.Account:
    account = account_repo.create_account(
        "test_account2", repository.enums.Currency.CZK, Decimal("0.50"), user_id
    )
    return domain.schemes.Account.from_repo(account)


@pytest.fixture()
def another_account(
    another_user_id: uuid.UUID, account_repo: repository.AccountRepository
) -> domain.schemes.Account:
    account = account_repo.create_account(
        "test_another_account",
        repository.enums.Currency.USD,
        Decimal(0),
        another_user_id,
    )
    return domain.schemes.Account.from_repo(account)


@pytest.fixture()
def account_domain(
    account_id: uuid.UUID, account_repo: repository.AccountRepository
) -> domain.AccountDomain:
    return domain.AccountDomain.from_id(account_id, account_repo)


@pytest.fixture()
def category(
    user_id: uuid.UUID, user_repo: repository.UserRepository
) -> domain.schemes.Category:
    category = user_repo.create_category("test_category", user_id)
    return domain.schemes.Category.from_repo(category)


@pytest.fixture()
def category_id(category: domain.schemes.Category) -> uuid.UUID:
    return category.id


@pytest.fixture()
def not_belonging_category(
    another_user_id: uuid.UUID, user_repo: repository.UserRepository
) -> domain.schemes.Category:
    category = user_repo.create_category("test_category2", another_user_id)
    return domain.schemes.Category.from_repo(category)


@pytest.fixture()
def operation(
    account_id: uuid.UUID,
    account_repo: repository.AccountRepository,
    category_id: uuid.UUID,
) -> domain.schemes.Operation:
    amount = Decimal("1.99")
    operation = account_repo.add_operation(account_id, amount, category_id)
    return domain.schemes.Operation.from_repo(operation)


@pytest.fixture()
def operation2(
    account_id: uuid.UUID,
    account_repo: repository.AccountRepository,
    category_id: uuid.UUID,
) -> domain.schemes.Operation:
    amount = Decimal("10.00")
    operation = account_repo.add_operation(account_id, amount, category_id)
    return domain.schemes.Operation.from_repo(operation)


@pytest.fixture()
def negative_operation(
    account_id: uuid.UUID,
    account_repo: repository.AccountRepository,
    category_id: uuid.UUID,
) -> domain.schemes.Operation:
    amount = Decimal("-10.00")
    operation = account_repo.add_operation(account_id, amount, category_id)
    return domain.schemes.Operation.from_repo(operation)
