from collections.abc import Callable
from uuid import UUID

from qdrant_client import QdrantClient
from sqlalchemy.orm import Session

from db.models import Device, User


class SessionService:
    def __init__(self, db_factory: Callable[[], Session], qdrant: QdrantClient) -> None:
        self.db_factory = db_factory
        self.qdrant = qdrant

    def register_device(
        self,
        device_name: str | None = None,
        device_model: str | None = None,
        metadata: dict | None = None,
    ) -> Device:
        """
        Registers a new device in the database.
        """
        device = Device(
            device_name=device_name,
            device_model=device_model,
            metadata_=metadata or {},
        )

        with self.db_factory() as db:
            db.add(device)
            db.commit()
            db.refresh(device)

        return device

    def create_user(
        self,
        name: str | None = None,
        email: str | None = None,
        preferred_language: str = "pt-BR",
        device_id: str | None = None,
        metadata: dict | None = None,
    ) -> User:
        """
        Create a new user in the database.
        """
        # Ensure device_id is valid UUID or None (avoiding empty strings)
        device_uuid = UUID(device_id) if (device_id and device_id.strip()) else None

        user = User(
            name=name,
            email=email,
            preferred_language=preferred_language or "pt-BR",
            device_id=device_uuid,
            metadata_=metadata or {},
        )

        with self.db_factory() as db:
            db.add(user)
            db.commit()
            db.refresh(user)

        return user
