"""rename lakes to water_objects

Revision ID: 9c2720dd95c3
Revises: 0b51613d63d8
Create Date: 2026-01-14 15:39:24.048432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c2720dd95c3'
down_revision: Union[str, Sequence[str], None] = '0b51613d63d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table("lakes", "water_objects")

def downgrade():
    op.rename_table("water_objects", "lakes")
