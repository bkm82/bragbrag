import pytest
from bragbrag.main import example_add


def test_example_add():
    expected = 5
    actual = example_add(3, 2)
    assert (actual == expected)


if __name__ == "__main__":
    pytest.main()
