"""remove ulek columns from water_objects

Revision ID: ab463c56ebd1
Revises: abb245b97151
Create Date: 2026-01-14 15:44:00.955625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab463c56ebd1'
down_revision: Union[str, Sequence[str], None] = '3c3d0d3329a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    for col in [
        "Z","H","G","A","D","W","T","Tw","pH","O","I","M",
        "Thw","Ka","SAR","IIWP_Dc","Tr","Fl","Fa"
    ]:
        op.drop_column("water_objects", col)



def downgrade() -> None:
    """Downgrade schema."""
    pass
