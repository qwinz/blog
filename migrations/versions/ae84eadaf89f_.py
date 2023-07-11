"""empty message

Revision ID: ae84eadaf89f
Revises: ba0e4b1079dd
Create Date: 2023-07-10 16:55:20.957304

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae84eadaf89f'
down_revision = 'ba0e4b1079dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('update_time', sa.DateTime(), nullable=True))
        batch_op.drop_column('updated_time')
        batch_op.drop_column('created_time')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_time', sa.DateTime(), nullable=True))
        batch_op.drop_column('updated_time')
        batch_op.drop_column('created_time')

    with op.batch_alter_table('tb_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('update_time', sa.DateTime(), nullable=True))
        batch_op.drop_column('updated_time')
        batch_op.drop_column('created_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_time', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('updated_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('update_time')
        batch_op.drop_column('create_time')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_time', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('updated_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('update_time')

    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_time', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('updated_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('update_time')
        batch_op.drop_column('create_time')

    # ### end Alembic commands ###
