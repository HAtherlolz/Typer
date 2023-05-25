"""Initial migration

Revision ID: 3fb8acdc7517
Revises: ef5d5ec66ca5
Create Date: 2023-05-24 22:39:56.651931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fb8acdc7517'
down_revision = 'ef5d5ec66ca5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profile_lesson', 'seconds_spent',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('profile_lesson', 'is_done',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profile_lesson', 'is_done',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('profile_lesson', 'seconds_spent',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
