import base64
import hashlib
import hmac
import secrets

_HASH_PREFIX = "pbkdf2_sha256"
_DEFAULT_ITERATIONS = 120_000


def hash_password(password: str, iterations: int = _DEFAULT_ITERATIONS) -> str:
    """Gera hash de senha em formato compatível com validação posterior."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password inválida")

    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{_HASH_PREFIX}${iterations}${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def verify_password(password: str, stored_password: str) -> bool:
    """
    Verifica senha com suporte a dois formatos:
    1) hash PBKDF2 salvo no formato `pbkdf2_sha256$...`
    2) legado em texto puro (compatibilidade temporária)
    """
    if not isinstance(password, str) or not isinstance(stored_password, str) or not stored_password:
        return False

    if stored_password.startswith(f"{_HASH_PREFIX}$"):
        try:
            _, iterations, salt_b64, digest_b64 = stored_password.split("$", 3)
            salt = base64.urlsafe_b64decode(salt_b64.encode("utf-8"))
            expected_digest = base64.urlsafe_b64decode(digest_b64.encode("utf-8"))
            current_digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
            return hmac.compare_digest(current_digest, expected_digest)
        except Exception:
            return False

    return hmac.compare_digest(password, stored_password)


def is_hashed_password(value: str) -> bool:
    return isinstance(value, str) and value.startswith(f"{_HASH_PREFIX}$")
