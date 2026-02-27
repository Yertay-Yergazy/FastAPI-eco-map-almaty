"""replace_password_with_firebase_uid

Revision ID: dfcfe2385124
Revises: d1e2f3a4b5c6
Create Date: 2026-02-17 13:37:38.203210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfcfe2385124'
down_revision: Union[str, Sequence[str], None] = 'd1e2f3a4b5c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем колонку hashed_password
    op.drop_column('users', 'hashed_password')
    
    # Добавляем колонку firebase_uid
    op.add_column('users', sa.Column('firebase_uid', sa.String(), nullable=False))
    
    # Создаём индекс на firebase_uid (unique)
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)


def downgrade() -> None:
    # Удаляем индекс
    op.drop_index(op.f('ix_users_firebase_uid'), table_name='users')
    
    # Удаляем колонку firebase_uid
    op.drop_column('users', 'firebase_uid')
    
    # Возвращаем колонку hashed_password
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
