"""empty message

Revision ID: 5cc563e1e117
Revises: 
Create Date: 2021-12-29 16:23:10.246557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cc563e1e117'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crawling',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('link', sa.Text(), nullable=False),
    sa.Column('snippet', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.Text(), nullable=True),
    sa.Column('sni_tran', sa.Text(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_download',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('crawling_id', sa.Integer(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('sum_tran', sa.Text(), nullable=True),
    sa.Column('body_text', sa.Text(), nullable=True),
    sa.Column('body_tran', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['crawling_id'], ['crawling.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('machine_learning',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('crawling_id', sa.Integer(), nullable=True),
    sa.Column('news_val', sa.Integer(), nullable=True),
    sa.Column('art_val', sa.Integer(), nullable=True),
    sa.Column('cos_val', sa.Integer(), nullable=True),
    sa.Column('ml_val', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['crawling_id'], ['crawling.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('machine_learning')
    op.drop_table('article_download')
    op.drop_table('crawling')
    # ### end Alembic commands ###
