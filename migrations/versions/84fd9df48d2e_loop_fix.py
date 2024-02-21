"""loop fix

Revision ID: 84fd9df48d2e
Revises: 210862092e06
Create Date: 2024-02-21 12:52:19.579030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84fd9df48d2e'
down_revision = '210862092e06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accomodation_services', schema=None) as batch_op:
        batch_op.alter_column('company_id',
               existing_type=sa.VARCHAR(length=6),
               type_=sa.Integer(),
               existing_nullable=True)

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.alter_column('category',
               existing_type=sa.VARCHAR(length=12),
               type_=sa.Enum('Transport', 'Accommodation'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.alter_column('category',
               existing_type=sa.Enum('Transport', 'Accommodation'),
               type_=sa.VARCHAR(length=12),
               existing_nullable=True)

    with op.batch_alter_table('accomodation_services', schema=None) as batch_op:
        batch_op.alter_column('company_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=6),
               existing_nullable=True)

    # ### end Alembic commands ###
