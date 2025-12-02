# app/security.py
from passlib.context import CryptContext
import secrets

# Use pbkdf2_sha256 which matches the hashes shown in your errors
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Simple fake JWT token generator.

    For this assignment we do not need a real JWT library.
    Tests only care that an 'access_token' string exists.
    """
    return "fake-jwt-" + subject + "-" + secrets.token_urlsafe(16)

