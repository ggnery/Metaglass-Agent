import os
from dataclasses import dataclass


@dataclass
class Config:
    GRPC_PORT: str = os.getenv("GRPC_PORT", "50051")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "orchestrator")

    DATABASE_URL: str = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_GRPC_PORT: int = int(os.getenv("QDRANT_GRPC_PORT", "6334"))

    # Session Reaper Config
    REAPER_INTERVAL_SECONDS: int = int(os.getenv("REAPER_INTERVAL_SECONDS", "30"))
    ACTIVE_SESSION_TIMEOUT_SECONDS: int = int(
        os.getenv("ACTIVE_SESSION_TIMEOUT_SECONDS", "60")
    )
    LOST_SESSION_TIMEOUT_SECONDS: int = int(
        os.getenv("LOST_SESSION_TIMEOUT_SECONDS", "3600")
    )
