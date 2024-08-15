"""init db

Revision ID: 77e91aff819b
Revises: 9fbe05d43a8f
Create Date: 2021-07-03 22:06:25.577217

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '77e91aff819b'
down_revision = '9fbe05d43a8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db_item',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.BigInteger(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_db_item_created_at'), 'db_item', ['created_at'], unique=False)
    op.create_index(op.f('ix_db_item_deleted'), 'db_item', ['deleted'], unique=False)
    op.create_index(op.f('ix_db_item_description'), 'db_item', ['description'], unique=False)
    op.create_index(op.f('ix_db_item_title'), 'db_item', ['title'], unique=False)
    op.create_table('db_user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('deleted_at', sa.BigInteger(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_db_user_created_at'), 'db_user', ['created_at'], unique=False)
    op.create_index(op.f('ix_db_user_deleted'), 'db_user', ['deleted'], unique=False)
    op.create_index(op.f('ix_db_user_email'), 'db_user', ['email'], unique=True)
    op.create_index(op.f('ix_db_user_full_name'), 'db_user', ['full_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_db_user_full_name'), table_name='db_user')
    op.drop_index(op.f('ix_db_user_email'), table_name='db_user')
    op.drop_index(op.f('ix_db_user_deleted'), table_name='db_user')
    op.drop_index(op.f('ix_db_user_created_at'), table_name='db_user')
    op.drop_table('db_user')
    op.drop_index(op.f('ix_db_item_title'), table_name='db_item')
    op.drop_index(op.f('ix_db_item_description'), table_name='db_item')
    op.drop_index(op.f('ix_db_item_deleted'), table_name='db_item')
    op.drop_index(op.f('ix_db_item_created_at'), table_name='db_item')
    op.drop_table('db_item')
    # ### end Alembic commands ###
