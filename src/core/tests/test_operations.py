from datetime import datetime, timedelta
import pytest
import uuid
from decimal import Decimal

import repository
import core
import utils


class TestShowOperations:
    def test_empty(_, account_domain: core.AccountDomain):
        available_operations = account_domain.show_operations(
            account_domain.account.created_at, utils.dt.tz_aware_current_dt()
        )
        assert len(available_operations) == 0

    def test_valid(
        _, account_domain: core.AccountDomain, operation: core.schemes.Operation
    ):
        available_operations = account_domain.show_operations(
            account_domain.account.created_at, utils.dt.tz_aware_current_dt()
        )
        assert len(available_operations) == 1

        result_operation = available_operations[0]
        assert result_operation.id == operation.id
        assert result_operation.amount == operation.amount
        assert result_operation.category_id == operation.category_id

    def test_excluding_date_range(
        _, account_domain: core.AccountDomain, operation: core.schemes.Operation
    ):
        date_from = utils.dt.tz_aware_dt(datetime.utcnow() + timedelta(days=1))
        date_to = utils.dt.tz_aware_dt(datetime.utcnow() + timedelta(days=2))
        available_operations = account_domain.show_operations(date_from, date_to)
        assert len(available_operations) == 0

    def test_date_to_is_before_date_from(_, account_domain: core.AccountDomain):
        date_to = utils.dt.tz_aware_dt(datetime.utcnow() - timedelta(days=1))
        with pytest.raises(core.exc.InvalidData):
            account_domain.show_operations(utils.dt.tz_aware_current_dt(), date_to)


def test_get_operation(
    account_domain: core.AccountDomain,
    operation: core.schemes.Operation,
):
    operation_from_domain = account_domain.get_operation(operation.id)
    assert operation_from_domain.amount == operation.amount
    assert operation_from_domain.created_at == operation.created_at


def test_get_not_existing_operation(account_domain: core.AccountDomain):
    operation_id = uuid.uuid4()
    with pytest.raises(core.exc.DoesNotExist):
        account_domain.get_operation(operation_id)


def test_remove_operation(
    account_domain: core.AccountDomain,
    operation: core.schemes.Operation,
    account_repo: repository.AccountRepository,
):
    account_domain.remove_operation(operation.id)

    deleted_opertaion = account_repo.get_operation(operation.id)
    assert deleted_opertaion is None


def test_remove_not_existing_operation(account_domain: core.AccountDomain):
    operation_id = uuid.uuid4()
    with pytest.raises(core.exc.DoesNotExist):
        account_domain.remove_operation(operation_id)


def test_add_operation(
    account_domain: core.AccountDomain,
    account_repo: repository.AccountRepository,
    category: core.schemes.Category,
):
    amount = Decimal("1.00")
    opertaion = account_domain.add_operation(amount, category)

    assert opertaion.amount == amount

    repo_operation = account_repo.get_operation(opertaion.id)
    assert repo_operation is not None
    assert repo_operation.amount == opertaion.amount
    assert repo_operation.category_id == category.id
    assert repo_operation.created_at == opertaion.created_at


def test_add_operation_to_not_belonging_account(
    account_domain: core.AccountDomain,
    account_repo: repository.AccountRepository,
    not_belonging_category: core.schemes.Category,
):
    amount = Decimal("1.00")
    with pytest.raises(core.exc.InvalidData):
        account_domain.add_operation(amount, not_belonging_category)


class TestBalance:
    def test_empty(
        _, account: core.schemes.Account, account_domain: core.AccountDomain
    ):
        balance = account_domain.get_balance()
        assert balance == account.base_balance

    def test_valid(
        _,
        account: core.schemes.Account,
        account_domain: core.AccountDomain,
        operation: core.schemes.Operation,
        operation2: core.schemes.Operation,
    ):
        balance = account_domain.get_balance()
        assert balance == (account.base_balance + operation.amount + operation2.amount)

    def test_negative(
        _,
        account: core.schemes.Account,
        account_domain: core.AccountDomain,
        negative_operation: core.schemes.Operation,
    ):
        balance = account_domain.get_balance()
        assert balance == (account.base_balance + negative_operation.amount)
