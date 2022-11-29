import pytest
import uuid

import repository
import domain


class TestMakeAccountDomain:
    def test_valid(
        _, account_id: uuid.UUID, account_repo: repository.AccountRepository
    ):
        domain.AccountDomain.from_id(account_id, account_repo)

    def test_with_invalid_id(_, account_repo: repository.AccountRepository):
        account_id = uuid.uuid4()
        with pytest.raises(domain.exc.DoesNotExist):
            domain.AccountDomain.from_id(account_id, account_repo)


class TestCreateAccount:
    def test_valid(_, user_domain: domain.UserDomain):
        account = user_domain.create_account(
            "new_account", repository.enums.Currency.USD
        )
        assert account.user_id == user_domain.user.id

    def test_already_have_account_with_given_name(
        _,
        account: domain.schemes.Account,
        user_domain: domain.UserDomain,
    ):
        with pytest.raises(domain.exc.InvalidData):
            user_domain.create_account(account.name, repository.enums.Currency.USD)


def test_get_available_accounts(
    user_domain: domain.UserDomain,
    account: domain.schemes.Account,
    another_account: domain.schemes.Account,
):
    accounts = user_domain.get_accounts()
    assert len(accounts) == 1
