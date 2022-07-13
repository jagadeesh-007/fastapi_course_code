"""add content column 

Revision ID: 31002c35d855
Revises: 0d74a0c8dac6
Create Date: 2022-07-10 22:07:56.343006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31002c35d855'
down_revision = '0d74a0c8dac6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
