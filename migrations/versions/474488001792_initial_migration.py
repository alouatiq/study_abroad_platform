"""Initial migration

Revision ID: 474488001792
Revises: 
Create Date: 2025-03-26 14:12:21.062978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '474488001792'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('advisor',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.Column('country_of_residence', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('agencies',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('students',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.Column('nationality', sa.String(length=100), nullable=True),
    sa.Column('country_of_residence', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('programs',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('agency_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('university', sa.String(length=255), nullable=True),
    sa.Column('field', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('fee', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('duration', sa.String(length=50), nullable=True),
    sa.Column('languages', sa.String(length=50), nullable=True),
    sa.Column('proficiency_level', sa.String(length=50), nullable=True),
    sa.Column('eligibility_criteria', sa.String(length=255), nullable=True),
    sa.Column('available_scholarships', sa.Boolean(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agency_id'], ['agencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advisor_applications',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('advisor_id', sa.String(length=36), nullable=False),
    sa.Column('program_id', sa.String(length=36), nullable=False),
    sa.Column('assistance_approval', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['advisor_id'], ['advisor.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advisor_assignments',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('advisor_id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('program_id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['advisor_id'], ['advisor.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_programs',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('program_id', sa.String(length=36), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_programs')
    op.drop_table('advisor_assignments')
    op.drop_table('advisor_applications')
    op.drop_table('programs')
    op.drop_table('students')
    op.drop_table('agencies')
    op.drop_table('advisor')
    # ### end Alembic commands ###
