"""Initial schema: device, user, session, session_context

Revision ID: 0001
Revises:
Create Date: 2026-04-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Extensões ───────────────────────────────────────────────
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')

    # ── device ──────────────────────────────────────────────────
    op.create_table(
        "device",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("device_name", sa.Text, nullable=True),
        sa.Column("device_model", sa.Text, nullable=True),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    # ── user ────────────────────────────────────────────────────
    op.create_table(
        "user",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("device_id", UUID(as_uuid=True), sa.ForeignKey("device.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.Text, nullable=True),
        sa.Column("email", sa.Text, nullable=True),
        sa.Column("preferred_language", sa.Text, nullable=False, server_default=sa.text("'pt-BR'")),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )
    op.create_index("idx_user_device_id", "user", ["device_id"])

    # ── session ─────────────────────────────────────────────────
    op.create_table(
        "session",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        sa.Column("device_id", UUID(as_uuid=True), sa.ForeignKey("device.id", ondelete="SET NULL"), nullable=True),
        sa.Column("state", sa.Enum("active", "lost", "closed", name="session_state", create_type=True), nullable=False, server_default=sa.text("'active'")),
        sa.Column("initial_metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_reason", sa.Text, nullable=True),
    )
    op.create_index("idx_session_user_id", "session", ["user_id"])
    op.create_index("idx_session_device_id", "session", ["device_id"])
    op.create_index(
        "idx_session_state",
        "session",
        ["state"],
        postgresql_where=sa.text("state = 'active'"),
    )

    # ── session_context ─────────────────────────────────────────
    op.create_table(
        "session_context",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("session_id", UUID(as_uuid=True), sa.ForeignKey("session.id", ondelete="CASCADE"), nullable=False),
        sa.Column("context_type", sa.Text, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("metadata", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "idx_session_context_session_active",
        "session_context",
        ["session_id", sa.text("created_at DESC")],
    )
    op.create_index(
        "idx_session_context_cleanup",
        "session_context",
        ["expires_at"],
    )

    # ── Função: cleanup_expired_context ─────────────────────────
    op.execute("""
        CREATE OR REPLACE FUNCTION cleanup_expired_context()
        RETURNS INT
        LANGUAGE plpgsql
        AS $$
        DECLARE
            deleted_count INT;
        BEGIN
            DELETE FROM session_context WHERE expires_at < NOW();
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            RETURN deleted_count;
        END;
        $$;
    """)

    # ── Função + Trigger: updated_at automático ─────────────────
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$;
    """)

    op.execute("""
        CREATE TRIGGER trg_user_updated_at
            BEFORE UPDATE ON "user"
            FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_user_updated_at ON \"user\"")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at()")
    op.execute("DROP FUNCTION IF EXISTS cleanup_expired_context()")

    op.drop_table("session_context")
    op.drop_table("session")
    op.drop_table("user")
    op.drop_table("device")

    sa.Enum(name="session_state").drop(op.get_bind(), checkfirst=True)

    op.execute('DROP EXTENSION IF EXISTS "pg_trgm"')
    op.execute('DROP EXTENSION IF EXISTS "pgcrypto"')
