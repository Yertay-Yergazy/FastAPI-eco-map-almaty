"""add coordinates and description to water_objects

Revision ID: c4e5f6a7b8c9
Revises: 8680215d72f2
Create Date: 2026-01-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = '8680215d72f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('water_objects', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('water_objects', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('water_objects', sa.Column('description', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('water_objects', 'description')
    op.drop_column('water_objects', 'longitude')
    op.drop_column('water_objects', 'latitude')
