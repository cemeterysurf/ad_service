"""initial migration

Revision ID: 515d4611b26e
Revises: 
Create Date: 2024-03-27 22:49:45.440101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from backend.database.tables import AdType


# revision identifiers, used by Alembic.
revision: str = '515d4611b26e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('full_name', sa.String(255)),
        sa.Column('phone', sa.String(255))
    )

    op.create_table(
        'session',
        sa.Column('token', sa.String, primary_key=True),
        sa.Column('expires', sa.DateTime),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'))
    )

    op.create_table(
        'ad',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255)),
        sa.Column('body', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('price', sa.String(255), nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('type', sa.Enum(AdType)),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"))
    )

    op.create_table(
        'comment',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('body', sa.Text),
        sa.Column('ad_id', sa.Integer, sa.ForeignKey("ad.id", ondelete="CASCADE")),
        sa.Column('created_by', sa.Integer, sa.ForeignKey("user.id", ondelete="SET NULL"))
    )

    op.create_table(
        'complaint',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('body', sa.Text),
        sa.Column('created_by', sa.Integer, sa.ForeignKey("user.id", ondelete="SET NULL")),
        sa.Column('ad_id', sa.Integer, sa.ForeignKey("ad.id", ondelete="CASCADE"))
    )

def downgrade():
    op.drop_table('complaint')
    op.drop_table('comment')
    op.drop_table('ad')
    op.drop_table('session')
    op.drop_table('user')
