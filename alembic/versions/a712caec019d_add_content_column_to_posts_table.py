"""add content column to posts table

Revision ID: a712caec019d
Revises: f8ae687c302e
Create Date: 2024-04-26 11:44:47.687207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a712caec019d'
down_revision: Union[str, None] = 'f8ae687c302e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String() ,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
