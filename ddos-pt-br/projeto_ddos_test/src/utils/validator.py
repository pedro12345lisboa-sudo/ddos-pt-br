"""Validacao de destinos para testes locais e autorizados."""
from ipaddress import ip_address
from urllib.parse import urlparse


def validate_target(value: str) -> str:
    """Retorna uma URL HTTP(S) valida e rejeita credenciais embutidas."""
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("O destino deve ser uma URL HTTP(S) com hostname.")
    if parsed.username or parsed.password:
        raise ValueError("Credenciais embutidas na URL nao sao permitidas.")
    return value.rstrip("/")


def is_loopback_host(hostname: str) -> bool:
    """Indica se o hostname e localhost ou um endereco de loopback."""
    normalized = hostname.lower().strip("[]")
    if normalized in {"localhost", "localhost.localdomain"}:
        return True
    try:
        return ip_address(normalized).is_loopback
    except ValueError:
        return False
