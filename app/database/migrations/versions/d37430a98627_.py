"""empty message

Revision ID: d37430a98627
Revises: f1488295e53a
Create Date: 2025-06-04 19:35:50.871858

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd37430a98627'
down_revision = 'f1488295e53a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('transfers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sender_account', sa.String(length=100), nullable=False),
    sa.Column('receiver_bank', sa.String(length=100), nullable=False),
    sa.Column('receiver_account', sa.String(length=100), nullable=False),
    sa.Column('receiver_name', sa.String(length=100), nullable=False),
    sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=10), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('frequency', sa.Enum('monthly', 'daily', 'weekly', name='frequency_types'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('questions',
    # sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    # sa.Column('question', mysql.VARCHAR(length=128), nullable=True),
    # sa.PrimaryKeyConstraint('id'),
    # mysql_default_charset='latin1',
    # mysql_engine='InnoDB'
    # )
    op.drop_table('transfers')
    op.drop_table('users')
    # ### end Alembic commands ###
