"""empty message

Revision ID: 872fe0371398
Revises: 97d224da2983
Create Date: 2017-02-19 19:07:27.082902

"""

# revision identifiers, used by Alembic.
revision = '872fe0371398'
down_revision = '97d224da2983'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('member_number', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('members', 'member_number')
    ### end Alembic commands ###
