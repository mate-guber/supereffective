"""rename columns in TypeMatchup table

Revision ID: a693d5f8f93d
Revises: 35908e8addc7
Create Date: 2026-07-27 17:43:24.893686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a693d5f8f93d'
down_revision: Union[str, Sequence[str], None] = '35908e8addc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('type_matchup', schema=None) as batch_op:
        batch_op.alter_column('attacker', new_column_name='attacker_id')
        batch_op.alter_column('defender', new_column_name='defender_id')



def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('type_matchup', schema=None) as batch_op:
        batch_op.alter_column('attacker_id', new_column_name='attacker')
        batch_op.alter_column('defender_id', new_column_name='defender')

