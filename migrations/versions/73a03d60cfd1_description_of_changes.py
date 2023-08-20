"""description of changes

Revision ID: 73a03d60cfd1
Revises: 33c89322a778
Create Date: 2023-03-03 16:30:07.289349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73a03d60cfd1'
down_revision = '33c89322a778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_response', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
