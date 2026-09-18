"""create otp table

Revision ID: c499e10a187e
Revises: 772a6810e7cc
Create Date: 2026-09-13 14:02:11.515079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c499e10a187e'
down_revision: Union[str, Sequence[str], None] = '772a6810e7cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table(
        "otp",
        sa.Column("userid",sa.Integer,nullable=True),
        sa.Column("otp",sa.Integer,nullable=True),
        sa.ForeignKeyConstraint(
            ["userid"],
            ["user.userid"]
        )
    )

def downgrade():
   op.drop_table("otp")
