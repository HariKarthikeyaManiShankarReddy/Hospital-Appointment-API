import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.base import Base


if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")
elif any(k.startswith("pytest") or k.startswith("pytest_cov") for k in sys.modules):
    # Use a shared in-memory sqlite DB for pytest runs (works with pytest-cov too)
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = "sqlite:///./hospital.db"

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool if DATABASE_URL == "sqlite:///:memory:" else None,
    }
    engine = create_engine(DATABASE_URL, **{k: v for k, v in engine_kwargs.items() if v is not None})
else:
    engine = create_engine(DATABASE_URL)

# re-export Base for consumers importing from app.database
__all__ = ["engine", "SessionLocal", "Base", "DATABASE_URL"]

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
