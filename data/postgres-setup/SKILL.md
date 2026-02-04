---
name: postgres-setup
description: Set up PostgreSQL database with standardized schema.sql pattern. Use when starting a new project that needs PostgreSQL, setting up database schema, or creating setup scripts for postgres.
---

# PostgreSQL Database Setup Pattern

This skill helps you set up a PostgreSQL database following a standardized pattern with proper separation of schema and setup scripts.

## When to Use This Skill

Use this skill when:
- Starting a new project that needs PostgreSQL
- You want a clean separation between schema definition (SQL) and setup logic (Python)
- You need support for both production and test databases
- You want consistent environment variable patterns

## What This Skill Creates

1. **`database/schema.sql`** - SQL schema with table definitions
2. **`dev_scripts/setup_database.py`** - Python setup script
3. **Documentation** of required environment variables

## Step 1: Gather Project Information

**IMPORTANT**: Before creating files, ask the user these questions:

1. **"What is your project name?"** (e.g., "arcana", "trading-bot", "myapp")
   - Use this to derive:
     - Database name: `{project_name}` (e.g., `arcana`)
     - User name: `{project_name}` (e.g., `arcana`)
     - Password env var: `{PROJECT_NAME}_PG_PASSWORD` (e.g., `ARCANA_PG_PASSWORD`)

2. **"What tables do you need in your schema?"** (optional - can create skeleton if unknown)

## Step 2: Create Directory Structure

Create these directories if they don't exist:
```
{project_root}/
├── database/
└── dev_scripts/
```

## Step 3: Create schema.sql

Create `database/schema.sql` with:

### Best Practices to Follow:
- Use `CREATE TABLE IF NOT EXISTS` for idempotency
- Use `UUID` for primary keys with `gen_random_uuid()` as default
- Use `BIGINT` (Unix timestamps) for all date/time fields (NOT TIMESTAMP, NOT TIMESTAMPTZ)
- Add proper foreign key constraints with `ON DELETE CASCADE` or `ON DELETE SET NULL`
- Add indexes on foreign keys and commonly queried fields
- Use `TEXT` instead of `VARCHAR` (PostgreSQL best practice)
- Add comments using `COMMENT ON COLUMN` for documentation

### Template Structure:
```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example table
CREATE TABLE IF NOT EXISTS example_table (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at BIGINT NOT NULL DEFAULT extract(epoch from now())::bigint,
    updated_at BIGINT
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_example_created_at ON example_table(created_at);

-- Add comments
COMMENT ON TABLE example_table IS 'Description of what this table stores';
COMMENT ON COLUMN example_table.created_at IS 'Unix timestamp of creation';
```

If user provides specific tables, create schema accordingly. Otherwise, create a skeleton with one example table.

## Step 4: Create setup_database.py

Create `dev_scripts/setup_database.py` using this template, **substituting project-specific values**:

```python
#!/usr/bin/env python
"""
Database setup script for {PROJECT_NAME}
Creates the {project_name} database and user with proper permissions, then applies database/schema.sql

Usage:
  python setup_database.py --pg-password <postgres_password>
  python setup_database.py --pg-password <postgres_password> --pg-user <superuser>
  python setup_database.py --pg-password <postgres_password> --test-db
"""

import os
import sys
import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def main():
    """Setup {project_name} database and user"""
    parser = argparse.ArgumentParser(description='Setup {PROJECT_NAME} database')
    parser.add_argument('--pg-password', required=True,
                       help='PostgreSQL superuser password (required)')
    parser.add_argument('--pg-user', default='postgres',
                       help='PostgreSQL superuser name (default: postgres)')
    parser.add_argument('--test-db', action='store_true',
                       help='Create {project_name}_test database instead of main {project_name} database')
    args = parser.parse_args()

    pg_host = os.environ.get('POSTGRES_HOST', 'localhost')
    pg_port = os.environ.get('POSTGRES_PORT', '5432')
    pg_user = args.pg_user
    pg_password = args.pg_password

    if args.test_db:
        {project_name}_db = '{project_name}_test'
        print("Setting up TEST database '{project_name}_test'...")
    else:
        {project_name}_db = os.environ.get('{PROJECT_NAME}_PG_DB', '{project_name}')
    {project_name}_user = os.environ.get('{PROJECT_NAME}_PG_USER', '{project_name}')
    {project_name}_password = os.environ.get('{PROJECT_NAME}_PG_PASSWORD', None)

    if {project_name}_password is None:
        print("Error: {PROJECT_NAME}_PG_PASSWORD environment variable is required")
        sys.exit(1)

    print(f"Setting up database '{{project_name}_db}' and user '{{project_name}_user}'...")
    print(f"Connecting to PostgreSQL at {pg_host}:{pg_port} as {pg_user}")

    try:
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            database='postgres',
            user=pg_user,
            password=pg_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", ({project_name}_user,))
            if not cursor.fetchone():
                print(f"Creating user '{{project_name}_user}'...")
                cursor.execute(f"CREATE USER {project_name}_user WITH PASSWORD %s", ({project_name}_password,))
                print(f"✓ User '{{project_name}_user}' created")
            else:
                print(f"✓ User '{{project_name}_user}' already exists")

            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ({project_name}_db,))
            if not cursor.fetchone():
                print(f"Creating database '{{project_name}_db}'...")
                cursor.execute(f"CREATE DATABASE {{project_name}_db} OWNER {{project_name}_user}")
                print(f"✓ Database '{{project_name}_db}' created")
            else:
                print(f"✓ Database '{{project_name}_db}' already exists")

            print("Setting permissions...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {{project_name}_db} TO {{project_name}_user}")
            print(f"✓ Granted all privileges on database '{{project_name}_db}' to user '{{project_name}_user}'")

        conn.close()

        print(f"\\nConnecting as '{{project_name}_user}' to apply schema...")
        {project_name}_conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            database={project_name}_db,
            user={project_name}_user,
            password={project_name}_password
        )
        {project_name}_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        schema_path = os.path.join(repo_root, 'database', 'schema.sql')
        if not os.path.exists(schema_path):
            print(f"Error: schema file not found at {schema_path}")
            sys.exit(1)

        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        with {project_name}_conn.cursor() as cursor:
            print("Ensuring required extensions...")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
            print(f"Applying schema from {schema_path}...")
            cursor.execute(schema_sql)
            print("✓ Schema applied")

        {project_name}_conn.close()
        print("✓ Database setup complete")
        print(f"Database: {{project_name}_db}")
        print(f"User: {{project_name}_user}")
        print(f"Host: {pg_host}:{pg_port}")

    except psycopg2.Error as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**CRITICAL**: Replace ALL instances of:
- `{PROJECT_NAME}` → uppercase project name (e.g., `ARCANA`, `MYAPP`)
- `{project_name}` → lowercase project name (e.g., `arcana`, `myapp`)

## Step 5: Create Documentation

Add a section to the project's README.md (or create SETUP.md) documenting:

### Command Line Arguments

**Required:**
- `--pg-password` - PostgreSQL superuser password

**Optional:**
- `--pg-user` - PostgreSQL superuser name (default: postgres)
- `--test-db` - Create test database instead of main database

### Environment Variables

**PostgreSQL connection (optional)**:
- `POSTGRES_HOST` - PostgreSQL host (default: localhost)
- `POSTGRES_PORT` - PostgreSQL port (default: 5432)

**Project-specific**:
- `{PROJECT_NAME}_PG_DB` - Database name (default: {project_name})
- `{PROJECT_NAME}_PG_USER` - Application user (default: {project_name})
- `{PROJECT_NAME}_PG_PASSWORD` - Application user password (REQUIRED)

### Setup Instructions

```bash
# Set required environment variables
export {PROJECT_NAME}_PG_PASSWORD="your_app_password"

# Run setup script (pass postgres superuser password as argument)
python dev_scripts/setup_database.py --pg-password "your_postgres_password"

# With custom superuser name
python dev_scripts/setup_database.py --pg-password "your_postgres_password" --pg-user "admin"

# For test database
python dev_scripts/setup_database.py --pg-password "your_postgres_password" --test-db
```

## Step 6: Make Script Executable

Run:
```bash
chmod +x dev_scripts/setup_database.py
```

## Step 7: Create Database Driver (Optional but Recommended)

If the project needs a database driver/connection manager, create one following this pattern:

### File: `src/{project_name}/driver/database.py`

**Key patterns to follow:**

1. **Connection Pooling**: Use `ThreadedConnectionPool` from psycopg2
   ```python
   from psycopg2.pool import ThreadedConnectionPool

   self.pool = ThreadedConnectionPool(
       min_conn,  # e.g., 2
       max_conn,  # e.g., 10
       host=db_host,
       database=db_name,
       user=db_user,
       password=db_passwd
   )
   ```

2. **Context Managers**: Provide context managers for connections and cursors
   ```python
   @contextmanager
   def get_cursor(self, commit=True, cursor_factory=None):
       """Context manager for database cursors with automatic commit/rollback"""
       with self._get_connection() as conn:
           cursor = conn.cursor(cursor_factory=cursor_factory)
           try:
               yield cursor
               if commit:
                   conn.commit()
           except Exception:
               conn.rollback()
               raise
           finally:
               cursor.close()
   ```

3. **Always Use RealDictCursor for Loading Data**: When reading from database, use RealDictCursor
   ```python
   from psycopg2.extras import RealDictCursor

   with self.get_cursor(commit=False, cursor_factory=RealDictCursor) as cursor:
       cursor.execute("SELECT * FROM table WHERE id = %s", (id,))
       result = cursor.fetchone()
       return Model.from_dict(dict(result))
   ```

4. **Unix Timestamps Everywhere**: Convert database timestamps to/from unix timestamps
   ```python
   # When saving to DB - store as BIGINT
   created_at = int(time.time())

   # When loading from DB - already BIGINT, use as-is
   # In models, store as int (unix timestamp)
   # Only convert to datetime for display/formatting purposes
   ```

5. **Proper Cleanup**: Ensure pool is closed on destruction
   ```python
   def close(self):
       if self.pool and not self.pool.closed:
           self.pool.closeall()

   def __del__(self):
       if hasattr(self, 'pool'):
           self.close()
   ```

### Example Driver Structure:
```python
class {ProjectName}DB:
    def __init__(self, db_host, db_name, db_user, db_passwd, min_conn=2, max_conn=10):
        self.pool = ThreadedConnectionPool(...)

    @contextmanager
    def get_cursor(self, commit=True, cursor_factory=None):
        # Context manager for cursors
        pass

    def load_item_by_id(self, item_id: str) -> Item:
        with self.get_cursor(commit=False, cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            result = cursor.fetchone()
            if not result:
                raise Exception(f"Item {item_id} not found")
            return Item.from_dict(dict(result))

    def save_item(self, item: Item) -> str:
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO items (name, created_at) VALUES (%s, %s) RETURNING id",
                (item.name, int(time.time()))
            )
            return str(cursor.fetchone()[0])
```

## Design Principles

This pattern follows these principles:

### Database Schema:
1. **Separation of concerns** - SQL in .sql files, setup logic in Python
2. **Idempotency** - Safe to run multiple times
3. **Test database support** - Easy to create isolated test environments
4. **Unix timestamps** - Always use BIGINT for dates/times (not TIMESTAMP types)
5. **UUIDs for keys** - Better for distributed systems
6. **Environment-based config** - No hardcoded credentials

### Database Driver (if applicable):
1. **Connection pooling** - Use ThreadedConnectionPool for efficient connection reuse
2. **Context managers** - Automatic commit/rollback and resource cleanup
3. **RealDictCursor for reads** - Always use RealDictCursor when loading data for easy dict conversion
4. **Unix timestamps** - Store as BIGINT, convert only for display
5. **Proper cleanup** - Close pool on destruction

## Example Usage in Claude Code

User: "Set up postgres database for my project"
Claude: "What is your project name?"
User: "trading-bot"
Claude:
1. Creates database/ and dev_scripts/ directories
2. Creates database/schema.sql with skeleton
3. Creates dev_scripts/setup_database.py with:
   - TRADING_BOT_PG_PASSWORD
   - trading_bot database and user
4. Documents environment variables needed
5. Makes script executable
