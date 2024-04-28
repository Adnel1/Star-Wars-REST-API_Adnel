"""empty message

Revision ID: 1e274bdafd93
Revises: beed70e86e07
Create Date: 2024-04-28 17:23:17.781387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e274bdafd93'
down_revision = 'beed70e86e07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_planet_favorite',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'planet_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_planet_favorite')
    # ### end Alembic commands ###
