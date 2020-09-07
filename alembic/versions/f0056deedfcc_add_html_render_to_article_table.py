"""add html render to article table

Revision ID: f0056deedfcc
Revises: ba266d924497
Create Date: 2020-09-07 18:55:37.007372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0056deedfcc'
down_revision = 'ba266d924497'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("article", sa.Column("html_render", sa.String, server_default=""))


def downgrade():
    op.drop_column("article", "html_render")
