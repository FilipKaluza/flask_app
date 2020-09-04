"""Create users table

Revision ID: ba266d924497
Revises: 
Create Date: 2020-09-04 12:11:51.476791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba266d924497'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String),
        sa.Column("password", sa.String))



def downgrade():
    op.drop_table("user")
