"""add is_active_field

Revision ID: 2ba42c5b0398
Revises: a45d98fb3c79
Create Date: 2023-05-16 11:01:15.001850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ba42c5b0398'
down_revision = 'a45d98fb3c79'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('is_active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'is_active')
    # ### end Alembic commands ###