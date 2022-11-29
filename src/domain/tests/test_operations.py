from datetime import datetime, timedelta
import pytest
import uuid
from decimal import Decimal

import repository
import domain
import utils


class TestShowOperations:
    def test_empty(_, account_domain: domain.AccountDomain):
        available_operations = account_domain.show_operations(
            account_domain.account.created_at, utils.dt.tz_aware_current_dt()
        )
        assert len(available_operations) == 0

    def test_valid(
        _, account_domain: domain.AccountDomain, operation: domain.schemes.Operation
    ):
        available_operations = account_domain.show_operations(
            account_domain.account.created_at, utils.dt.tz_aware_current_dt()
        )
        assert len(available_operations) == 1

    def test_excluding_date_range(
        _, account_domain: domain.AccountDomain, operation: domain.schemes.Operation
    ):
        date_from = utils.dt.tz_aware_dt(datetime.utcnow() + timedelta(days=1))
        date_to = utils.dt.tz_aware_dt(datetime.utcnow() + timedelta(days=2))
        available_operations = account_domain.show_operations(date_from, date_to)
        assert len(available_operations) == 0

    def test_date_to_is_before_date_from(_, account_domain: domain.AccountDomain):
        date_to = utils.dt.tz_aware_dt(datetime.utcnow() - timedelta(days=1))
        with pytest.raises(domain.exc.InvalidData):
            account_domain.show_operations(utils.dt.tz_aware_current_dt(), date_to)


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


class TestBalance:
    def test_empty(_, account_domain: domain.AccountDomain):
        balance = account_domain.get_balance()
        assert balance == Decimal("0.00")

    def test_valid(
        _,
        account_domain: domain.AccountDomain,
        operation: domain.schemes.Operation,
        operation2: domain.schemes.Operation,
    ):
        balance = account_domain.get_balance()
        assert balance == sum((operation.amount, operation2.amount), Decimal("0.00"))

    def test_negative(
        _,
        account_domain: domain.AccountDomain,
        negative_operation: domain.schemes.Operation,
    ):
        balance = account_domain.get_balance()
        assert balance < Decimal("0.00")
        assert balance == negative_operation.amount
