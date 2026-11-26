import taskq


def test_package_imports():
    assert taskq.__version__ == "0.2.0"