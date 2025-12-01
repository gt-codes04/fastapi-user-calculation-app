from passlib.context import CryptContext

# Use PBKDF2-SHA256 instead of bcrypt to avoid backend issues and 72-byte limits
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def hash_password(plain_password: str) -> str:
    """Return a hashed password string."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

