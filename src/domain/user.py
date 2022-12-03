import uuid

from repository import enums, AccountRepository, UserRepository
from repository import exc as repo_exc

from domain import schemes, exc


class UserDomain:
    def __init__(
        self,
        user: schemes.User,
        user_repository: UserRepository,
        account_repository: AccountRepository,
    ) -> None:
        self.user = user
        self.user_repository = user_repository
        self.account_repository = account_repository

    @classmethod
    def from_id(
        cls,
        id: uuid.UUID,
        user_repository: UserRepository,
        account_repository: AccountRepository,
    ) -> "UserDomain":
        repo_user = user_repository.get_user(id)
        if repo_user is None:
            raise repo_exc.DoesNotExist()

        user = schemes.User.from_repo(repo_user)
        return cls(user, user_repository, account_repository)

    def create_account(self, name: str, currency: enums.Currency) -> schemes.Account:
        try:
            account = self.account_repository.create_account(
                name, currency, self.user.id
            )
        except repo_exc.InvalidData as e:
            raise exc.InvalidData(e.detail)

        return schemes.Account.from_repo(account)

    def get_accounts(self) -> list[schemes.Account]:
        accounts = self.account_repository.list_accounts(self.user.id)
        return [schemes.Account.from_repo(acc) for acc in accounts]

    def create_category(self, name: str) -> schemes.Category:
        try:
            category = self.user_repository.create_category(name, self.user.id)
        except repo_exc.InvalidData as e:
            raise exc.InvalidData(e.code)

        return schemes.Category.from_repo(category)

    def get_category(self, id: uuid.UUID) -> schemes.Category:
        category = self.user_repository.get_category(id)
        if category is None:
            raise exc.DoesNotExist()
        if category.user_id != self.user.id:
            raise exc.DoesNotExist()

        return schemes.Category.from_repo(category)

    def show_categories(self) -> list[schemes.Category]:
        available_categories = self.user_repository.list_categories(
            user_id=self.user.id
        )
        return [
            schemes.Category.from_repo(category) for category in available_categories
        ]
