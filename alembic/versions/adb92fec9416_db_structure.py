"""DB structure

Revision ID: adb92fec9416
Revises: 
Create Date: 2020-06-17 16:35:22.947513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adb92fec9416'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('asin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('asin', sa.VARCHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('asin'),
    sa.UniqueConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('product_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('asin_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('ratings_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['asin_id'], ['asin.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_product_info_asin_id'), 'product_info', ['asin_id'], unique=False)
    op.create_table('review',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('asin_id', sa.Integer(), nullable=False),
    sa.Column('total_reviews', sa.Integer(), nullable=False),
    sa.Column('positive_reviews', sa.Integer(), nullable=False),
    sa.Column('answered_questions', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['asin_id'], ['asin.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_review_asin_id'), 'review', ['asin_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_review_asin_id'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_product_info_asin_id'), table_name='product_info')
    op.drop_table('product_info')
    op.drop_table('asin')
