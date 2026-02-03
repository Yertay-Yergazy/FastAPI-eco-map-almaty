"""drop coordinates table

Revision ID: 8680215d72f2
Revises: 7f8fd55ec58e
Create Date: 2026-01-31 15:20:51.495605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8680215d72f2'
down_revision: Union[str, Sequence[str], None] = '7f8fd55ec58e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Удаляем таблицу координат
    op.drop_table("coordinates")


def downgrade():
    # 2. Восстанавливаем таблицу (на случай rollback)
    op.create_table(
        "coordinates",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column(
            "water_id",
            sa.Integer,
            sa.ForeignKey("waters.id", name="fk_coordinates_water_id"),
        ),
    )
