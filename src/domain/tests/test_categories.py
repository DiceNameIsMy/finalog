import pytest

import repository
import domain


class TestCreateCategory:
    def test_valid(
        _, user_domain: domain.UserDomain, user_repo: repository.UserRepository
    ):
        category = user_domain.create_category("category")
        repo_category = user_repo.get_category(category.id)
        assert repo_category is not None

        assert category.name == repo_category.name
        assert category.user_id == repo_category.user_id

    def test_with_the_same_name_as_existing_one(
        _, user_domain: domain.UserDomain, category: domain.schemes.Category
    ):
        with pytest.raises(domain.exc.InvalidData):
            user_domain.create_category(category.name)


def test_get_categories(
    category: domain.schemes.Category,
    not_belonging_category: domain.schemes.Category,
    user_domain: domain.UserDomain,
):
    categories = user_domain.show_categories()
    assert len(categories) == 1
    assert categories[0].id == category.id
