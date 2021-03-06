"""empty message

Revision ID: b34706ddacba
Revises: 9a677e5efa1a
Create Date: 2022-01-05 21:30:14.592189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b34706ddacba'
down_revision = '9a677e5efa1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('p_member',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('p_member',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
