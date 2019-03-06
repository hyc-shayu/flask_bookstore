"""initial migration

Revision ID: d64120a272a0
Revises: 
Create Date: 2019-03-06 14:31:52.662274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64120a272a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_favorite_book',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.add_column('book', sa.Column('author', sa.String(length=50), nullable=True))
    op.add_column('book', sa.Column('image_url', sa.String(length=255), nullable=True))
    op.add_column('book', sa.Column('introduction', sa.String(length=512), nullable=True))
    op.add_column('book', sa.Column('press', sa.String(length=100), nullable=True))
    op.add_column('book', sa.Column('publish_time', sa.Date(), nullable=True))
    op.add_column('book', sa.Column('sales_volume', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'sales_volume')
    op.drop_column('book', 'publish_time')
    op.drop_column('book', 'press')
    op.drop_column('book', 'introduction')
    op.drop_column('book', 'image_url')
    op.drop_column('book', 'author')
    op.drop_table('user_favorite_book')
    # ### end Alembic commands ###