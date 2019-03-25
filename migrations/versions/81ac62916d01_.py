"""empty message

Revision ID: 81ac62916d01
Revises: 
Create Date: 2019-03-25 22:26:19.043133

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '81ac62916d01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.VARCHAR(length=250), nullable=True),
                    sa.Column('deadline', sa.Date(), nullable=True),
                    sa.Column('completed', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###