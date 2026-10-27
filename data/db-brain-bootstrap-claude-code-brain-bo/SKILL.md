---
name: db
description: Query the database — list schemas, tables, describe a table, or run SQL. Accepts arguments like schemas, tables, describe <table>, or raw SQL.
---

# DB Skill

Query the database in non-interactive mode.

## Usage

```
/db schemas              # List available schemas
/db tables               # List all tables
/db describe users       # Describe the users table
/db SELECT COUNT(*) FROM orders  # Run raw SQL
```

## Instructions

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `schemas` | `{{DB_LIST_SCHEMAS_CMD}}` |
| `tables` | `{{DB_LIST_TABLES_CMD}}` |
| `describe <table>` | `{{DB_DESCRIBE_CMD}} <table>` |
| `<raw-sql>` | `{{DB_QUERY_CMD}} "<sql>"` |

### ⚠️ Always use non-interactive mode:
- PostgreSQL: `psql -c "SQL" | cat`
- MySQL: `mysql -e "SQL" | cat`
- SQLite: `sqlite3 db.sqlite "SQL"`
- MongoDB: `mongosh --eval "db.collection.find()" --quiet`

### Rules:
- Read `claude/build.md` for the DB connection string and credentials
- NEVER run destructive SQL (DROP, TRUNCATE, DELETE without WHERE) without explicit user confirmation
- NEVER commit credentials — always use env var references
- For `$DB_PATH` (SQLite): check project config files for the actual path
