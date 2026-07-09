"""rename UserOrm password to hashed_password

Revision ID: b234d1efddc5
Revises: bcf95b31ddad
Create Date: 2026-07-09 23:26:01.802061

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b234d1efddc5"
down_revision: Union[str, Sequence[str], None] = "bcf95b31ddad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "password",
        new_column_name="hashed_password",
        existing_type=sa.String(length=255),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        new_column_name="password",
        existing_type=sa.String(length=255),
        existing_nullable=False,
    )
