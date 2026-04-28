"""session_context: drop context_type/content, add data/mime_type

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-28
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("session_context", "context_type")
    op.drop_column("session_context", "content")
    op.add_column(
        "session_context",
        sa.Column("data", sa.LargeBinary, nullable=False),
    )
    op.add_column(
        "session_context",
        sa.Column("mime_type", sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_column("session_context", "mime_type")
    op.drop_column("session_context", "data")
    op.add_column(
        "session_context",
        sa.Column("content", sa.Text, nullable=False),
    )
    op.add_column(
        "session_context",
        sa.Column("context_type", sa.Text, nullable=False),
    )
