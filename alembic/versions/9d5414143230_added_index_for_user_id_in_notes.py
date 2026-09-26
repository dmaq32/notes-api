"""Added index for user_id in Notes

Revision ID: 9d5414143230
Revises: 134258ba6645
Create Date: 2026-09-26 15:35:25.100601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d5414143230'
down_revision: Union[str, Sequence[str], None] = '134258ba6645'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
