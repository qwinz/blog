"""empty message

Revision ID: 33c887170eff
Revises: 518acbc9de0e
Create Date: 2023-07-11 20:59:40.616774

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '33c887170eff'
down_revision = '518acbc9de0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_constraint('category_ibfk_1', type_='foreignkey')
        batch_op.drop_column('blog_id')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('create_time',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('create_time',
               existing_type=sa.DateTime(),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=True)

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blog_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('category_ibfk_1', 'blog', ['blog_id'], ['id'])

    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###
