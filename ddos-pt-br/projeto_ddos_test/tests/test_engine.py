import pytest

from src.utils.validator import is_loopback_host, validate_target


def test_validate_target_accepts_http_url() -> None:
    assert validate_target("http://127.0.0.1:8080/") == "http://127.0.0.1:8080"


def test_validate_target_rejects_credentials() -> None:
    with pytest.raises(ValueError):
        validate_target("http://user:pass@127.0.0.1:8080")


def test_loopback_detection() -> None:
    assert is_loopback_host("127.0.0.1")
    assert is_loopback_host("localhost")
    assert not is_loopback_host("example.com")
