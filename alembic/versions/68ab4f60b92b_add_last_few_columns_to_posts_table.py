"""add last few columns to posts table

Revision ID: 68ab4f60b92b
Revises: e5e80ca3246e
Create Date: 2024-04-26 18:45:10.403336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68ab4f60b92b'
down_revision: Union[str, None] = 'e5e80ca3246e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('posts' ,sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text
        ('NOW()')),)

    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
