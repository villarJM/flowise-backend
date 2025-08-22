"""Convert all IDs to Integer with autoincrement

Revision ID: 64e0c6719700
Revises: b5c58f281083
Create Date: 2025-08-18 17:43:30.407655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64e0c6719700'
down_revision = 'b5c58f281083'
branch_labels = None
depends_on = None


def upgrade():
    # Drop all foreign key constraints first
    op.drop_constraint('daily_reports_project_id_fkey', 'daily_reports', type_='foreignkey')
    op.drop_constraint('project_comments_project_id_fkey', 'project_comments', type_='foreignkey')
    op.drop_constraint('time_entries_project_id_fkey', 'time_entries', type_='foreignkey')
    op.drop_constraint('time_entries_interrupted_by_fkey', 'time_entries', type_='foreignkey')
    op.drop_constraint('user_projects_project_id_fkey', 'user_projects', type_='foreignkey')
    op.drop_constraint('work_schedules_project_id_fkey', 'work_schedules', type_='foreignkey')
    
    # Create sequences for autoincrement first
    op.execute('CREATE SEQUENCE IF NOT EXISTS auth_providers_id_seq OWNED BY auth_providers.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS daily_reports_id_seq OWNED BY daily_reports.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS project_comments_id_seq OWNED BY project_comments.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS projects_id_seq OWNED BY projects.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS time_entries_id_seq OWNED BY time_entries.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS user_projects_id_seq OWNED BY user_projects.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS weekly_reports_id_seq OWNED BY weekly_reports.id')
    op.execute('CREATE SEQUENCE IF NOT EXISTS work_schedules_id_seq OWNED BY work_schedules.id')
    
    # Convert all ID columns to INTEGER with USING clause
    op.execute('ALTER TABLE auth_providers ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'auth_providers_id_seq\') END')
    op.execute('ALTER TABLE daily_reports ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'daily_reports_id_seq\') END')
    op.execute('ALTER TABLE project_comments ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'project_comments_id_seq\') END')
    op.execute('ALTER TABLE projects ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'projects_id_seq\') END')
    op.execute('ALTER TABLE time_entries ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'time_entries_id_seq\') END')
    op.execute('ALTER TABLE user_projects ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'user_projects_id_seq\') END')
    op.execute('ALTER TABLE weekly_reports ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'weekly_reports_id_seq\') END')
    op.execute('ALTER TABLE work_schedules ALTER COLUMN id TYPE INTEGER USING CASE WHEN id ~ \'\\d+\' THEN id::INTEGER ELSE nextval(\'work_schedules_id_seq\') END')
    
    # Convert foreign key columns to INTEGER
    op.execute('ALTER TABLE daily_reports ALTER COLUMN project_id TYPE INTEGER USING CASE WHEN project_id ~ \'\\d+\' THEN project_id::INTEGER ELSE 1 END')
    op.execute('ALTER TABLE project_comments ALTER COLUMN project_id TYPE INTEGER USING CASE WHEN project_id ~ \'\\d+\' THEN project_id::INTEGER ELSE 1 END')
    op.execute('ALTER TABLE time_entries ALTER COLUMN project_id TYPE INTEGER USING CASE WHEN project_id ~ \'\\d+\' THEN project_id::INTEGER ELSE 1 END')
    op.execute('ALTER TABLE time_entries ALTER COLUMN interrupted_by TYPE INTEGER USING CASE WHEN interrupted_by IS NOT NULL AND interrupted_by ~ \'\\d+\' THEN interrupted_by::INTEGER ELSE NULL END')
    op.execute('ALTER TABLE user_projects ALTER COLUMN project_id TYPE INTEGER USING CASE WHEN project_id ~ \'\\d+\' THEN project_id::INTEGER ELSE 1 END')
    op.execute('ALTER TABLE work_schedules ALTER COLUMN project_id TYPE INTEGER USING CASE WHEN project_id ~ \'\\d+\' THEN project_id::INTEGER ELSE 1 END')
    
    # Set default values for autoincrement
    op.execute('ALTER TABLE auth_providers ALTER COLUMN id SET DEFAULT nextval(\'auth_providers_id_seq\')')
    op.execute('ALTER TABLE daily_reports ALTER COLUMN id SET DEFAULT nextval(\'daily_reports_id_seq\')')
    op.execute('ALTER TABLE project_comments ALTER COLUMN id SET DEFAULT nextval(\'project_comments_id_seq\')')
    op.execute('ALTER TABLE projects ALTER COLUMN id SET DEFAULT nextval(\'projects_id_seq\')')
    op.execute('ALTER TABLE time_entries ALTER COLUMN id SET DEFAULT nextval(\'time_entries_id_seq\')')
    op.execute('ALTER TABLE user_projects ALTER COLUMN id SET DEFAULT nextval(\'user_projects_id_seq\')')
    op.execute('ALTER TABLE weekly_reports ALTER COLUMN id SET DEFAULT nextval(\'weekly_reports_id_seq\')')
    op.execute('ALTER TABLE work_schedules ALTER COLUMN id SET DEFAULT nextval(\'work_schedules_id_seq\')')
    
    # Recreate foreign key constraints
    op.create_foreign_key('daily_reports_project_id_fkey', 'daily_reports', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('project_comments_project_id_fkey', 'project_comments', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('time_entries_project_id_fkey', 'time_entries', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('time_entries_interrupted_by_fkey', 'time_entries', 'time_entries', ['interrupted_by'], ['id'])
    op.create_foreign_key('user_projects_project_id_fkey', 'user_projects', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('work_schedules_project_id_fkey', 'work_schedules', 'projects', ['project_id'], ['id'])


def downgrade():
    # Drop all foreign key constraints first
    op.drop_constraint('daily_reports_project_id_fkey', 'daily_reports', type_='foreignkey')
    op.drop_constraint('project_comments_project_id_fkey', 'project_comments', type_='foreignkey')
    op.drop_constraint('time_entries_project_id_fkey', 'time_entries', type_='foreignkey')
    op.drop_constraint('time_entries_interrupted_by_fkey', 'time_entries', type_='foreignkey')
    op.drop_constraint('user_projects_project_id_fkey', 'user_projects', type_='foreignkey')
    op.drop_constraint('work_schedules_project_id_fkey', 'work_schedules', type_='foreignkey')
    
    # Remove default values and drop sequences
    op.execute('ALTER TABLE auth_providers ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE daily_reports ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE project_comments ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE projects ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE time_entries ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE user_projects ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE weekly_reports ALTER COLUMN id DROP DEFAULT')
    op.execute('ALTER TABLE work_schedules ALTER COLUMN id DROP DEFAULT')
    
    op.execute('DROP SEQUENCE IF EXISTS auth_providers_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS daily_reports_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS project_comments_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS projects_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS time_entries_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS user_projects_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS weekly_reports_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS work_schedules_id_seq')
    
    # Convert all ID columns back to VARCHAR
    op.execute('ALTER TABLE auth_providers ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE daily_reports ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE project_comments ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE projects ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE time_entries ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE user_projects ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE weekly_reports ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    op.execute('ALTER TABLE work_schedules ALTER COLUMN id TYPE VARCHAR USING id::VARCHAR')
    
    # Convert foreign key columns back to VARCHAR
    op.execute('ALTER TABLE daily_reports ALTER COLUMN project_id TYPE VARCHAR USING project_id::VARCHAR')
    op.execute('ALTER TABLE project_comments ALTER COLUMN project_id TYPE VARCHAR USING project_id::VARCHAR')
    op.execute('ALTER TABLE time_entries ALTER COLUMN project_id TYPE VARCHAR USING project_id::VARCHAR')
    op.execute('ALTER TABLE time_entries ALTER COLUMN interrupted_by TYPE VARCHAR USING CASE WHEN interrupted_by IS NOT NULL THEN interrupted_by::VARCHAR ELSE NULL END')
    op.execute('ALTER TABLE user_projects ALTER COLUMN project_id TYPE VARCHAR USING project_id::VARCHAR')
    op.execute('ALTER TABLE work_schedules ALTER COLUMN project_id TYPE VARCHAR USING project_id::VARCHAR')
    
    # Recreate foreign key constraints with VARCHAR types
    op.create_foreign_key('daily_reports_project_id_fkey', 'daily_reports', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('project_comments_project_id_fkey', 'project_comments', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('time_entries_project_id_fkey', 'time_entries', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('time_entries_interrupted_by_fkey', 'time_entries', 'time_entries', ['interrupted_by'], ['id'])
    op.create_foreign_key('user_projects_project_id_fkey', 'user_projects', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('work_schedules_project_id_fkey', 'work_schedules', 'projects', ['project_id'], ['id'])
