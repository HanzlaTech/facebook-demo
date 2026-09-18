"""create user table

Revision ID: 772a6810e7cc
Revises: 
Create Date: 2026-09-12 16:39:31.158953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '772a6810e7cc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("Userid",sa.Integer,primary_key=True,nullable=True,autoincrement=True),
        sa.Column("Email",sa.String(100),nullable=False,unique=True),
        sa.Column("Password",sa.String(255),nullable=False),
        sa.Column("Verified",sa.Boolean,nullable=False),
        sa.Column("image",sa.String(100),nullable=False),
        sa.Column("Gender",sa.String(10),nullable=False),
        sa.Column("BirthDate",sa.DATE,nullable=False)
        
    )

def downgrade() :
   op.drop_table("user")