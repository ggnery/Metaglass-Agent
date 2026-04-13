from collections.abc import Callable
from datetime import UTC, datetime, timedelta
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
        initial_metadata: dict | None = None,
    ) -> SessionModel:
        """
        Creates a new session in 'active' state.
        Fetches the device_id automatically from the user's profile.
        """
        user_uuid = UUID(user_id)

        with self.db_factory() as db:
            # Fetch the user to get their associated device_id
            user = db.query(User).filter(User.id == user_uuid).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")

            session = SessionModel(
                user_id=user_uuid,
                device_id=user.device_id,
                state=SessionState.active,
                initial_metadata=initial_metadata or {},
                last_heartbeat=datetime.now(UTC),
            )

            db.add(session)
            db.commit()
            db.refresh(session)

        return session

    def get_session(self, session_id: str) -> SessionModel | None:
        """
        Retrieves session state.
        """
        session_uuid = UUID(session_id)
        with self.db_factory() as db:
            return (
                db.query(SessionModel).filter(SessionModel.id == session_uuid).first()
            )

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

    def reap_sessions(
        self, active_timeout_seconds: int, lost_timeout_seconds: int
    ) -> tuple[int, int]:
        """
        Transitions active sessions to 'lost' and lost sessions to 'closed'
        based on their last_heartbeat.
        Returns (reaped_to_lost_count, reaped_to_closed_count).
        """
        now = datetime.now(UTC)
        active_cutoff = now - timedelta(seconds=active_timeout_seconds)
        lost_cutoff = now - timedelta(seconds=lost_timeout_seconds)

        reaped_to_lost = 0
        reaped_to_closed = 0

        with self.db_factory() as db:
            # active -> lost
            stmt_lost = (
                update(SessionModel)
                .where(SessionModel.state == SessionState.active)
                .where(SessionModel.last_heartbeat < active_cutoff)
                .values(state=SessionState.lost)
            )
            res_lost = cast(CursorResult, db.execute(stmt_lost))
            reaped_to_lost = res_lost.rowcount

            # lost -> closed
            stmt_closed = (
                update(SessionModel)
                .where(SessionModel.state == SessionState.lost)
                .where(SessionModel.last_heartbeat < lost_cutoff)
                .values(
                    state=SessionState.closed,
                    ended_at=now,
                    end_reason="timeout",
                )
            )
            res_closed = cast(CursorResult, db.execute(stmt_closed))
            reaped_to_closed = res_closed.rowcount

            db.commit()

        return reaped_to_lost, reaped_to_closed
