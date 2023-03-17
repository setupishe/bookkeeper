import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    b = Budget(category=1, summ=100, pk=1)
    assert b.summ == 100
    assert b.category == 1


def test_create_brief():
    b = Budget(1, 100)
    assert b.summ == 100
    assert b.category == 1


def test_can_add_to_repo(repo):
    b = Budget(1, 100)
    pk = repo.add(b)
    assert b.pk == pk


def test_cant_add_negative_summ():
    with pytest.raises(ValueError):
        b = Budget(1, -100)
