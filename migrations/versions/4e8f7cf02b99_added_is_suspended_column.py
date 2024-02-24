"""added is_suspended column

Revision ID: 4e8f7cf02b99
Revises: 
Create Date: 2024-02-22 20:51:11.103457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e8f7cf02b99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('role', sa.Enum('Admin', 'User'), server_default='User', nullable=False),
    sa.Column('is_suspended', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('category', sa.Enum('Transport', 'Accommodation'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_companies_name'), ['name'], unique=True)

    op.create_table('accomodation_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('location', sa.String(length=128), nullable=False),
    sa.Column('available_rooms', sa.Integer(), nullable=True),
    sa.Column('images', sa.String(length=255), nullable=False),
    sa.Column('price_per_night', sa.Float(), nullable=False),
    sa.Column('average_rating', sa.Float(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation(accomodation)',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_included', sa.SmallInteger(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('checkin', sa.Date(), nullable=True),
    sa.Column('checkout', sa.Date(), nullable=True),
    sa.Column('days_in_room', sa.Integer(), nullable=True),
    sa.Column('rooms', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('price_net', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation(travel)',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_included', sa.SmallInteger(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('travelling_services',
    sa.Column('ts_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('seats', sa.Integer(), nullable=True),
    sa.Column('depurture_time', sa.DateTime(), nullable=False),
    sa.Column('arrival_time', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('depurture_city', sa.String(length=32), nullable=False),
    sa.Column('arrival_city', sa.String(length=32), nullable=False),
    sa.Column('registration_number', sa.String(length=9), nullable=True),
    sa.Column('company_id', sa.String(length=6), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('ts_id'),
    sa.UniqueConstraint('registration_number')
    )
    op.create_table('Reviews(accomodation)',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('accomodation_id', sa.String(length=9), nullable=True),
    sa.Column('review_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['accomodation_id'], ['accomodation_services.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Reviews(travels)',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('travel_id', sa.String(length=6), nullable=False),
    sa.Column('review_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['travel_id'], ['travelling_services.ts_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accomodation_bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accomodation_reservation_id', sa.Integer(), nullable=True),
    sa.Column('accomodation_service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['accomodation_reservation_id'], ['reservation(accomodation).id'], ),
    sa.ForeignKeyConstraint(['accomodation_service_id'], ['accomodation_services.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('travel_bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('travelling_reservation_id', sa.Integer(), nullable=True),
    sa.Column('travelling_service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['travelling_reservation_id'], ['reservation(travel).id'], ),
    sa.ForeignKeyConstraint(['travelling_service_id'], ['travelling_services.ts_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('travel_bookings')
    op.drop_table('accomodation_bookings')
    op.drop_table('Reviews(travels)')
    op.drop_table('Reviews(accomodation)')
    op.drop_table('travelling_services')
    op.drop_table('reservation(travel)')
    op.drop_table('reservation(accomodation)')
    op.drop_table('accomodation_services')
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_companies_name'))

    op.drop_table('companies')
    op.drop_table('Users')
    # ### end Alembic commands ###
