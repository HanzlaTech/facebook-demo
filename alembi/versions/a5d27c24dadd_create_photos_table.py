"""create photos table

Revision ID: a5d27c24dadd
Revises: c499e10a187e
Create Date: 2026-09-13 21:04:09.568714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5d27c24dadd'
down_revision: Union[str, Sequence[str], None] = 'c499e10a187e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
 op.create_table(
    "photos",
    sa.Column("userid",sa.Integer,nullable=True),
    sa.Column("image_url",sa.BLOB,nullable=True),
    sa.Column("image_type",sa.VARCHAR(30),nullable=True),
    sa.ForeignKeyConstraint(
       ["userid"],
       ["user.userid"]
    )
 )

def downgrade() :
 op.drop_table("photos")
