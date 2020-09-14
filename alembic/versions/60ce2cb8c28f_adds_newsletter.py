"""adds newsletter

Revision ID: 60ce2cb8c28f
Revises: f0056deedfcc
Create Date: 2020-09-14 12:33:35.437550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60ce2cb8c28f'
down_revision = 'f0056deedfcc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "newsletter",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True))


def downgrade():
    op.drop_table("newsletter")
