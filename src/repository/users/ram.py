import uuid

from repository.users import base
from repository import schemes, exc
import utils


class RAMUserRepository(base.UserRepository):
    _users: list[schemes.User]
    _categories: list[schemes.Category]

    def __init__(self) -> None:
        self._users = []
        self._categories = []
        super().__init__()

    def create_user(self, email: str, hashed_password: str) -> schemes.User:
        new_user = schemes.User(
            id=utils.ram.make_id(), email=email, hashed_password=hashed_password
        )
        for user in self._users:
            if email == user.email:
                raise exc.InvalidData(
                    detail="Email is already used by another user", code="email_taken"
                )

        self._users.append(new_user)
        return new_user

    def get_user(self, id: uuid.UUID) -> schemes.User | None:
        for user in self._users:
            if user.id == id:
                return user
        return None

    def create_category(self, name: str, user_id: uuid.UUID) -> schemes.Category:
        category = schemes.Category(id=utils.ram.make_id(), name=name, user_id=user_id)
        for ctgr in self._categories:
            if ctgr.user_id == user_id and ctgr.name == name:
                raise exc.InvalidData(
                    detail="User already has category with given name",
                    code="already_exists",
                )

        self._categories.append(category)
        return category

    def get_category(self, id: uuid.UUID) -> schemes.Category | None:
        for category in self._categories:
            if id == category.id:
                return category
        return None

    def list_categories(
        self, user_id: uuid.UUID | None = None
    ) -> list[schemes.Category]:
        if user_id is None:
            return self._categories

        return list(filter(lambda ctgr: ctgr.user_id == user_id, self._categories))
