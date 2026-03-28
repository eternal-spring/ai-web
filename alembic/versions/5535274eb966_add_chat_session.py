"""add_chat_session

Revision ID: 5535274eb966
Revises: 5f45e1b6d7a1
Create Date: 2026-03-28 23:18:10.352068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5535274eb966'
down_revision: Union[str, Sequence[str], None] = '5f45e1b6d7a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat_session",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True, comment="Session title."),
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            nullable=False,
            comment="Session creation date.",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_chat_session_user_id"), "chat_session", ["user_id"], unique=False)

    op.add_column(
        "chat_history",
        sa.Column("session_id", sa.Integer(), nullable=True),
    )
    op.create_index(op.f("ix_chat_history_session_id"), "chat_history", ["session_id"], unique=False)
    op.create_foreign_key(
        "fk_chat_history_session_id",
        "chat_history",
        "chat_session",
        ["session_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_chat_history_session_id", "chat_history", type_="foreignkey")
    op.drop_index(op.f("ix_chat_history_session_id"), table_name="chat_history")
    op.drop_column("chat_history", "session_id")

    op.drop_index(op.f("ix_chat_session_user_id"), table_name="chat_session")
    op.drop_table("chat_session")
