"""active-done

Revision ID: 547a75a9770e
Revises: 559420d0a963
Create Date: 2023-05-25 16:37:46.306713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '547a75a9770e'
down_revision = '559420d0a963'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile_lesson', sa.Column('is_done', sa.Boolean(), nullable=True))
    op.drop_column('profile_lesson', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile_lesson', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('profile_lesson', 'is_done')
    # ### end Alembic commands ###
