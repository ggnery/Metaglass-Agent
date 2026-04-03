import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "orchestrator")

DATABASE_URL: str = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)
