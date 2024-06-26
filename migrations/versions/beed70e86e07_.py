"""empty message

Revision ID: beed70e86e07
Revises: d80e4711630e
Create Date: 2024-04-27 00:59:27.199615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beed70e86e07'
down_revision = 'd80e4711630e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_people_favorite',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'people_id')
    )
    op.drop_table('favorite_people')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_people',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('height', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('weight', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='favorite_people_pkey')
    )
    op.drop_table('user_people_favorite')
    # ### end Alembic commands ###
