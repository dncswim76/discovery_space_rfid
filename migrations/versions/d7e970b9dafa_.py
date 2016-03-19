"""empty message

Revision ID: d7e970b9dafa
Revises: 5f77961e1546
Create Date: 2016-02-26 17:46:54.741411

"""

# revision identifiers, used by Alembic.
revision = 'd7e970b9dafa'
down_revision = '5f77961e1546'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member_visits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('MemberID', sa.Integer(), nullable=True),
    sa.Column('Date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['MemberID'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('visits')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visits',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('MemberID', sa.INTEGER(), nullable=True),
    sa.Column('Date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['MemberID'], [u'members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('member_visits')
    ### end Alembic commands ###