"""empty message

Revision ID: 4fbab2f3a0ea
Revises: 8a6308e6bfa1
Create Date: 2017-02-05 19:25:18.235000

"""

# revision identifiers, used by Alembic.
revision = '4fbab2f3a0ea'
down_revision = '8a6308e6bfa1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_doctor', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'username')
    )
    op.drop_table('user')
    op.add_column('doctors', sa.Column('user_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('doctors', 'user_id')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('authenticated', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', 'username', name='user_pkey')
    )
    op.drop_table('users')
    ### end Alembic commands ###
