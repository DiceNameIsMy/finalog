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
