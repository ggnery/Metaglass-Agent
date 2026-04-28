import enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    LargeBinary,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, relationship

_GEN_UUID = text("gen_random_uuid()")
_NOW = text("NOW()")
_EMPTY_JSONB = text("'{}'::jsonb")


class Base(DeclarativeBase):
    pass


# ── Device ────────���─────────────────────────────────���───────────────
class Device(Base):
    __tablename__ = "device"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=_GEN_UUID,
    )
    device_name = Column(Text, nullable=True)
    device_model = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=False, server_default=_EMPTY_JSONB)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=_NOW)

    users = relationship("User", back_populates="device")
    sessions = relationship("Session", back_populates="device")


# ── User ────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=_GEN_UUID,
    )
    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("device.id", ondelete="SET NULL"),
        nullable=True,
    )
    name = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    preferred_language = Column(Text, nullable=False, server_default=text("'pt-BR'"))
    metadata_ = Column("metadata", JSONB, nullable=False, server_default=_EMPTY_JSONB)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=_NOW)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=_NOW)

    device = relationship("Device", back_populates="users")
    sessions = relationship("Session", back_populates="user")

    __table_args__ = (Index("idx_user_device_id", "device_id"),)


# ── Session ─────────────────────────────────────────────────────────
class SessionState(enum.Enum):
    active = "active"
    lost = "lost"
    closed = "closed"


class Session(Base):
    __tablename__ = "session"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=_GEN_UUID,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("device.id", ondelete="SET NULL"),
        nullable=True,
    )
    state = Column(
        Enum(SessionState, name="session_state", create_type=False),
        nullable=False,
        server_default=text("'active'"),
    )
    initial_metadata = Column(JSONB, nullable=False, server_default=_EMPTY_JSONB)
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=_NOW)
    last_heartbeat = Column(
        DateTime(timezone=True), nullable=False, server_default=_NOW
    )
    ended_at = Column(DateTime(timezone=True), nullable=True)
    end_reason = Column(Text, nullable=True)

    user = relationship("User", back_populates="sessions")
    device = relationship("Device", back_populates="sessions")
    contexts = relationship("SessionContext", back_populates="session")

    __table_args__ = (
        Index("idx_session_user_id", "user_id"),
        Index("idx_session_device_id", "device_id"),
        Index(
            "idx_session_state",
            "state",
            postgresql_where=text("state = 'active'"),
        ),
    )


# ── SessionContext ──────────────────────────────────────────────────
class SessionContext(Base):
    __tablename__ = "session_context"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=_GEN_UUID,
    )
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("session.id", ondelete="CASCADE"),
        nullable=False,
    )
    data = Column(LargeBinary, nullable=False)
    mime_type = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSONB, nullable=False, server_default=_EMPTY_JSONB)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=_NOW)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    session = relationship("Session", back_populates="contexts")

    __table_args__ = (
        Index(
            "idx_session_context_session_active",
            "session_id",
            created_at.desc(),
        ),
        Index(
            "idx_session_context_cleanup",
            "expires_at",
        ),
    )
