from decimal import Decimal
import pytest
import uuid

import repository
import core


class TestMakeAccountDomain:
    def test_valid(
        _, account_id: uuid.UUID, account_repo: repository.AccountRepository
    ):
        core.AccountDomain.from_id(account_id, account_repo)

    def test_with_invalid_id(_, account_repo: repository.AccountRepository):
        account_id = uuid.uuid4()
        with pytest.raises(core.exc.DoesNotExist):
            core.AccountDomain.from_id(account_id, account_repo)


class TestCreateAccount:
    def test_valid(
        _, user_domain: core.UserDomain, account_repo: repository.AccountRepository
    ):
        domain_account = user_domain.create_account(
            "new_account", repository.enums.Currency.USD, Decimal(0)
        )
        repo_account = account_repo.get_account(domain_account.id)
        assert repo_account is not None

        assert repo_account.user_id == user_domain.user.id
        assert repo_account.name == "new_account"
        assert repo_account.currency == repository.enums.Currency.USD
        assert repo_account.base_balance == Decimal(0)

    def test_already_have_account_with_given_name(
        _,
        account: core.schemes.Account,
        user_domain: core.UserDomain,
    ):
        with pytest.raises(core.exc.InvalidData):
            user_domain.create_account(
                account.name, repository.enums.Currency.USD, Decimal(0)
            )


def test_get_available_accounts(
    user_domain: core.UserDomain,
    account: core.schemes.Account,
    another_account: core.schemes.Account,
):
    accounts = user_domain.get_accounts()
    assert len(accounts) == 1


class TestRenameAccount:
    def test_valid(
        _,
        account: core.schemes.Account,
        account_domain: core.AccountDomain,
        account_repo: repository.AccountRepository,
    ):
        new_name = "new_valid_account_name"
        account_domain.set_new_name(new_name)
        repo_account = account_repo.get_account(account.id)
        assert repo_account is not None
        assert repo_account.name == new_name

    def test_name_too_short(
        _,
        account_domain: core.AccountDomain,
    ):
        short_new_name = ""
        with pytest.raises(core.exc.InvalidData):
            account_domain.set_new_name(short_new_name)

    def test_name_too_long(_, account_domain: core.AccountDomain):
        long_new_name = "long_new_name" + ("_" * 256)
        with pytest.raises(core.exc.InvalidData):
            account_domain.set_new_name(long_new_name)

    def test_account_name_is_used_by_another_user(
        _,
        account: core.schemes.Account,
        another_account: core.schemes.Account,
        account_domain: core.AccountDomain,
        account_repo: repository.AccountRepository,
    ):
        new_name = another_account.name
        account_domain.set_new_name(new_name)
        repo_account = account_repo.get_account(account.id)
        assert repo_account is not None
        assert repo_account.name == new_name

    def test_user_has_account_with_given_name(
        _,
        account: core.schemes.Account,
        account2: core.schemes.Account,
        account_domain: core.AccountDomain,
    ):
        with pytest.raises(core.exc.InvalidData):
            account_domain.set_new_name(account2.name)

    def test_name_is_same_as_old_one(
        _,
        account: core.schemes.Account,
        account_domain: core.AccountDomain,
        account_repo: repository.AccountRepository,
    ):
        account_domain.set_new_name(account.name)
        repo_account = account_repo.get_account(account.id)
        assert repo_account is not None
        assert repo_account.name == account.name
