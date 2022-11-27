import pytest
import uuid
from decimal import Decimal

import repository
import domain


def test_show_empty_operations(account_domain: domain.AccountDomain):
    available_operations = account_domain.show_operations()
    assert len(available_operations) == 0


def test_show_operations(
    account_domain: domain.AccountDomain,
    operation: domain.schemes.Operation,
):
    available_operations = account_domain.show_operations()
    assert len(available_operations) == 1


def test_get_operation(
    account_domain: domain.AccountDomain,
    operation: domain.schemes.Operation,
):
    operation_from_domain = account_domain.get_operation(operation.id)
    assert operation_from_domain.amount == operation.amount
    assert operation_from_domain.created_at == operation.created_at


def test_get_not_existing_operation(account_domain: domain.AccountDomain):
    operation_id = uuid.uuid4()
    with pytest.raises(domain.exc.DoesNotExist):
        account_domain.get_operation(operation_id)


def test_remove_operation(
    account_domain: domain.AccountDomain,
    operation: domain.schemes.Operation,
    account_repo: repository.AccountRepository,
):
    account_domain.remove_operation(operation.id)

    deleted_opertaion = account_repo.get_operation(operation.id)
    assert deleted_opertaion is None


def test_remove_not_existing_operation(account_domain: domain.AccountDomain):
    operation_id = uuid.uuid4()
    with pytest.raises(domain.exc.DoesNotExist):
        account_domain.remove_operation(operation_id)


def test_add_operation(
    account_domain: domain.AccountDomain,
    account_repo: repository.AccountRepository,
):
    amount = Decimal("1.00")
    opertaion = account_domain.add_operation(amount)

    assert opertaion.amount == amount

    repo_operation = account_repo.get_operation(opertaion.id)
    assert repo_operation is not None
    assert repo_operation.amount == opertaion.amount
    assert repo_operation.created_at == opertaion.created_at
