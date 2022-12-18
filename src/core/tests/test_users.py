import uuid
import pytest

import repository
import core


class TestMakeUserDomain:
    def test_valid(
        _,
        user_id: uuid.UUID,
        user_repo: repository.UserRepository,
        account_repo: repository.AccountRepository,
    ):
        user_domain = core.UserDomain.from_id(user_id, user_repo, account_repo)
        assert user_domain.user.id == user_id

    def test_not_existing_id(
        _,
        user_repo: repository.UserRepository,
        account_repo: repository.AccountRepository,
    ):
        not_existing_user_id = uuid.uuid4()
        with pytest.raises(repository.exc.DoesNotExist):
            core.UserDomain.from_id(not_existing_user_id, user_repo, account_repo)
