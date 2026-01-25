"""create water_quality table

Revision ID: 3c3d0d3329a6
Revises: 9c2720dd95c3
Create Date: 2026-01-14 15:42:01.923430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c3d0d3329a6'
down_revision: Union[str, Sequence[str], None] = '9c2720dd95c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "water_quality",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "water_object_id",
            sa.Integer,
            sa.ForeignKey("water_objects.id", ondelete="CASCADE"),
            nullable=False,
        ),

        sa.Column("Z", sa.Integer),
        sa.Column("H", sa.Integer),
        sa.Column("G", sa.Integer),
        sa.Column("A", sa.Integer),
        sa.Column("D", sa.Integer),
        sa.Column("W", sa.Integer),
        sa.Column("T", sa.Integer),
        sa.Column("Tw", sa.Integer),
        sa.Column("pH", sa.Integer),
        sa.Column("O", sa.Integer),
        sa.Column("I", sa.String),
        sa.Column("M", sa.Integer),
        sa.Column("Thw", sa.Integer),
        sa.Column("Ka", sa.Integer),
        sa.Column("SAR", sa.Integer),
        sa.Column("IIWP_Dc", sa.Integer),
        sa.Column("Tr", sa.Integer),
        sa.Column("Fl", sa.Integer),
        sa.Column("Fa", sa.Integer),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )



def downgrade() -> None:
    """Downgrade schema."""
    pass
