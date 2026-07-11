"""add bookings table

Revision ID: 6b7e087d02da
Revises: b234d1efddc5
Create Date: 2026-07-11 21:33:28.774464

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6b7e087d02da"
down_revision: Union[str, Sequence[str], None] = "b234d1efddc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "bookings",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("room_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column("rooms", "title", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("rooms", "description", existing_type=sa.VARCHAR(), nullable=True)



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("rooms", "description", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("rooms", "title", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_table("bookings")

