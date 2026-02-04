---
name: rails-database-indexes
description: Design and implement database indexes for optimal query performance. Use when creating tables, optimizing slow queries, or improving database performance.
---

# Rails Database Indexes Specialist

Specialized in designing effective database indexes for ActiveRecord models.

## When to Use This Skill

- Creating new database tables
- Optimizing slow queries
- Adding foreign key indexes
- Implementing composite indexes
- Ensuring unique constraints

## Core Principles

- **Index Foreign Keys**: Always index foreign key columns
- **Index Frequently Queried Columns**: Columns in WHERE, ORDER BY
- **Composite Indexes**: Multiple columns used together
- **Unique Indexes**: Enforce uniqueness at database level
- **Selective Indexing**: Index columns with high cardinality

## Implementation Guidelines

### Migration Generation Workflow

**ALWAYS generate migrations using Rails generator commands first:**

```bash
# Generate a new migration
bundle exec rails generate migration AddIndexesToUsers

# For simple index additions, you can specify columns
bundle exec rails generate migration AddIndexToUsers email:index

# For complex indexes, use a descriptive name
bundle exec rails generate migration AddCompositeIndexesToOrders
```

This creates a timestamped migration file like `db/migrate/20250120XXXXXX_add_indexes_to_users.rb`.

### Basic Index Migration

After generating the migration file, edit it to add index definitions:

```ruby
class AddIndexesToUsers < ActiveRecord::Migration[7.0]
    def change
        # Single column index
        add_index :users, :email

        # Unique index
        add_index :users, :email, unique: true

        # Foreign key index
        add_index :orders, :user_id

        # Composite index
        add_index :orders, [:user_id, :status]

        # Named index
        add_index :posts, :published_at, name: 'idx_posts_published'
    end
end
```

### Foreign Key Indexes

```bash
# Generate table creation migration
bundle exec rails generate migration CreateOrders
```

Edit the generated migration:

```ruby
class CreateOrders < ActiveRecord::Migration[7.0]
    def change
        create_table :orders do |t|
            t.references :user, foreign_key: true, index: true
            t.string :status
            t.decimal :total_amount

            t.timestamps
        end

        # Additional indexes
        add_index :orders, :status
        add_index :orders, :created_at
    end
end
```

### Composite Indexes

```bash
# Generate migration for composite indexes
bundle exec rails generate migration AddCompositeIndexesToOrders
```

Edit the generated migration:

```ruby
class AddCompositeIndexes < ActiveRecord::Migration[7.0]
    def change
        # WHY: Queries often filter by user_id AND status together
        add_index :orders, [:user_id, :status]

        # WHY: Queries filter by category and sort by created_at
        add_index :posts, [:category_id, :created_at]

        # Order matters in composite indexes!
        # This index helps: WHERE user_id = X AND status = Y
        # This index also helps: WHERE user_id = X
        # This index does NOT help: WHERE status = Y
    end
end
```

### Unique Indexes

```bash
# Generate migration for unique indexes
bundle exec rails generate migration AddUniqueIndexesToUsers
```

Edit the generated migration:

```ruby
class AddUniqueIndexes < ActiveRecord::Migration[7.0]
    def change
        # Single column unique
        add_index :users, :email, unique: true

        # Composite unique (user can have one profile per type)
        add_index :user_profiles, [:user_id, :profile_type], unique: true

        # Case-insensitive unique (PostgreSQL)
        execute <<-SQL
            CREATE UNIQUE INDEX index_users_on_lower_email
            ON users (LOWER(email));
        SQL
    end
end
```

### Partial Indexes (PostgreSQL)

```bash
# Generate migration for partial indexes
bundle exec rails generate migration AddPartialIndexes
```

Edit the generated migration:

```ruby
class AddPartialIndexes < ActiveRecord::Migration[7.0]
    def change
        # WHY: Index only active users for performance
        add_index :users, :email, where: 'active = true', name: 'index_active_users_on_email'

        # WHY: Index only published posts
        add_index :posts, :published_at, where: 'published = true'
    end
end
```

### Index Types

```bash
# Generate migration for specialized indexes
bundle exec rails generate migration AddSpecializedIndexes
```

Edit the generated migration:

```ruby
class AddSpecializedIndexes < ActiveRecord::Migration[7.0]
    def change
        # B-tree (default, good for equality and range queries)
        add_index :users, :created_at

        # GiST for full-text search (PostgreSQL)
        execute <<-SQL
            CREATE INDEX index_posts_on_content_search
            ON posts USING GiST (to_tsvector('english', content));
        SQL

        # GIN for JSONB columns (PostgreSQL)
        add_index :events, :metadata, using: :gin
    end
end
```

### Removing Indexes

```bash
# Generate migration to remove indexes
bundle exec rails generate migration RemoveUnusedIndexes
```

Edit the generated migration:

```ruby
class RemoveUnusedIndexes < ActiveRecord::Migration[7.0]
    def change
        # Remove unused index
        remove_index :users, :username

        # Remove by name
        remove_index :posts, name: 'idx_posts_published'
    end
end
```

## Index Strategy Guidelines

### When to Add Indexes

- Foreign key columns (always)
- Columns in WHERE clauses (frequently)
- Columns in ORDER BY clauses
- Columns in JOIN conditions
- Columns with unique constraints

### When NOT to Add Indexes

- Tables with few rows (< 1000)
- Columns with low cardinality (few distinct values)
- Columns that are rarely queried
- Small tables that fit in memory

### Composite Index Order

```ruby
# Query: WHERE user_id = X AND status = Y ORDER BY created_at
# Best index order:
add_index :orders, [:user_id, :status, :created_at]

# This index can serve:
# 1. WHERE user_id = X
# 2. WHERE user_id = X AND status = Y
# 3. WHERE user_id = X AND status = Y ORDER BY created_at
```

## Analyzing Indexes

```ruby
# Check query execution plan
User.where(email: 'test@example.com').explain

# PostgreSQL: Check index usage
ActiveRecord::Base.connection.execute(<<-SQL)
    SELECT
        schemaname,
        tablename,
        indexname,
        idx_scan,
        idx_tup_read,
        idx_tup_fetch
    FROM pg_stat_user_indexes
    ORDER BY idx_scan;
SQL
```

## Tools to Use

**Correct tool order for creating indexes:**

1. `Bash`: Generate migration with `rails generate migration` command
2. `Edit`: Modify the generated migration file to add index definitions
3. `Bash`: Run `rails db:migrate` to apply changes
4. `Read`: Review existing indexes and schema

### Bash Commands

```bash
# Generate migration
bundle exec rails generate migration AddIndexToUsers email:index

# Run migration
bundle exec rails db:migrate

# Check schema
bundle exec rails db:schema:dump

# PostgreSQL: List indexes
bundle exec rails dbconsole
\di

# Check slow queries (PostgreSQL)
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

## Workflow

1. **Identify Slow Queries**: Use monitoring or logs
2. **Analyze Query Plan**: Use EXPLAIN
3. **Generate Migration**: Use `rails generate migration` command
4. **Edit Migration**: Add index definitions to generated file
5. **Run Migration**: Apply to database with `rails db:migrate`
6. **Verify Performance**: Test query speed
7. **Monitor**: Check index usage over time

## Related Skills

- `rails-query-optimization`: Understanding query patterns
- `rails-model-design`: Understanding associations

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## Key Reminders

- **ALWAYS use `rails generate migration` to create migration files**
- Never create migration files directly with `Write` tool
- Use `Edit` tool to modify generated migration files
- Always index foreign keys
- Index columns used in WHERE and ORDER BY
- Composite index order matters (most selective first)
- Unique indexes enforce data integrity
- Monitor index usage and remove unused indexes
- Indexes speed up reads but slow down writes
- Use partial indexes for conditional queries (PostgreSQL)
- Test index impact with EXPLAIN
