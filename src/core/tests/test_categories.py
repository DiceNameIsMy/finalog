import uuid
import pytest

import repository
import core


class TestCreateCategory:
    def test_valid(
        _, user_domain: core.UserDomain, user_repo: repository.UserRepository
    ):
        category = user_domain.create_category("category")
        repo_category = user_repo.get_category(category.id)
        assert repo_category is not None

        assert category.name == repo_category.name
        assert category.user_id == repo_category.user_id

    def test_with_the_same_name_as_existing_one(
        _, user_domain: core.UserDomain, category: core.schemes.Category
    ):
        with pytest.raises(core.exc.InvalidData):
            user_domain.create_category(category.name)


def test_get_categories(
    category: core.schemes.Category,
    not_belonging_category: core.schemes.Category,
    user_domain: core.UserDomain,
):
    categories = user_domain.show_categories()
    assert len(categories) == 1
    assert categories[0].id == category.id


class TestGetCategory:
    def test_valid(_, user_domain: core.UserDomain, category: core.schemes.Category):
        ctgr = user_domain.get_category(category.id)
        assert ctgr.id == category.id
        assert ctgr.name == category.name
        assert ctgr.user_id == category.user_id

    def test_does_not_exist(_, user_domain: core.UserDomain):
        fake_id = uuid.uuid4()
        with pytest.raises(core.exc.DoesNotExist):
            user_domain.get_category(fake_id)

    def test_does_not_have_access(
        _,
        user_domain: core.UserDomain,
        not_belonging_category: core.schemes.Category,
    ):
        with pytest.raises(core.exc.DoesNotExist):
            user_domain.get_category(not_belonging_category.id)
