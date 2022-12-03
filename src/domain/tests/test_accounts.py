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


class TestRenameAccount:
    def test_valid(
        _,
        account: domain.schemes.Account,
        account_domain: domain.AccountDomain,
        account_repo: repository.AccountRepository,
    ):
        new_name = "new_valid_account_name"
        account_domain.set_new_name(new_name)
        repo_account = account_repo.get_account(account.id)
        assert repo_account is not None
        assert repo_account.name == new_name

    def test_name_too_short(
        _,
        account_domain: domain.AccountDomain,
    ):
        short_new_name = ""
        with pytest.raises(domain.exc.InvalidData):
            account_domain.set_new_name(short_new_name)

    def test_name_too_long(_, account_domain: domain.AccountDomain):
        long_new_name = "long_new_name" + ("_" * 256)
        with pytest.raises(domain.exc.InvalidData):
            account_domain.set_new_name(long_new_name)

    def test_account_name_is_used_by_another_user(
        _,
        account: domain.schemes.Account,
        another_account: domain.schemes.Account,
        account_domain: domain.AccountDomain,
        account_repo: repository.AccountRepository,
    ):
        new_name = another_account.name
        account_domain.set_new_name(new_name)
        repo_account = account_repo.get_account(account.id)
        assert repo_account is not None
        assert repo_account.name == new_name

    def test_user_has_account_with_given_name(
        _,
        account: domain.schemes.Account,
        account2: domain.schemes.Account,
        account_domain: domain.AccountDomain,
    ):
        with pytest.raises(domain.exc.InvalidData):
            account_domain.set_new_name(account2.name)

    def test_name_is_same_as_old_one(
        _,
        account: domain.schemes.Account,
        account_domain: domain.AccountDomain,
        account_repo: repository.AccountRepository,
    ):
        account_domain.set_new_name(account.name)
        repo_account = account_repo.get_account(account.id)
        assert repo_account is not None
        assert repo_account.name == account.name
