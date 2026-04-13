from collections.abc import Callable
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from qdrant_client import QdrantClient
from sqlalchemy import CursorResult, update
from sqlalchemy.orm import Session

from db.models import Device, SessionState, User
from db.models import Session as SessionModel


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

    def create_session(
        self,
        user_id: str,
        device_id: str | None = None,
        initial_metadata: dict | None = None,
    ) -> SessionModel:
        """
        Creates a new session in 'active' state.
        """
        user_uuid = UUID(user_id)
        device_uuid = UUID(device_id) if (device_id and device_id.strip()) else None

        session = SessionModel(
            user_id=user_uuid,
            device_id=device_uuid,
            state=SessionState.active,
            initial_metadata=initial_metadata or {},
            last_heartbeat=datetime.now(UTC),
        )

        with self.db_factory() as db:
            db.add(session)
            db.commit()
            db.refresh(session)

        return session

    def heartbeat(self, session_id: str) -> bool:
        """
        Updates the last_heartbeat timestamp and transitions state to 'active'.
        This handles resurrection from 'lost' to 'active'.
        """
        session_uuid = UUID(session_id)
        with self.db_factory() as db:
            # We transition to 'active' from any state except potentially 'closed'
            # following the rule: [*] -> active: Heartbeat
            stmt = (
                update(SessionModel)
                .where(SessionModel.id == session_uuid)
                .where(SessionModel.state != SessionState.closed)
                .values(
                    last_heartbeat=datetime.now(UTC),
                    state=SessionState.active,
                )
            )
            result = cast(CursorResult, db.execute(stmt))
            db.commit()
            return result.rowcount > 0

    def end_session(self, session_id: str) -> bool:
        """
        Gracefully closes a session.
        Rule: lost -> closed: EndSession (also supports active -> closed)
        """
        session_uuid = UUID(session_id)
        with self.db_factory() as db:
            stmt = (
                update(SessionModel)
                .where(SessionModel.id == session_uuid)
                .where(SessionModel.state != SessionState.closed)
                .values(
                    state=SessionState.closed,
                    ended_at=datetime.now(UTC),
                )
            )
            result = cast(CursorResult, db.execute(stmt))
            db.commit()
            return result.rowcount > 0
