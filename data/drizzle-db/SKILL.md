---
name: drizzle-db
description: Query the project's database using Drizzle ORM. Use when the user asks about database contents, schema inspection, or data queries. Supports read-only mode for safety.
---

# Drizzle DB Connector

Execute SQL queries against the project's database through Drizzle ORM.

## When to use

- User asks about database contents or data
- Need to inspect database schema or tables
- Querying data for analysis or debugging
- Checking database state

## How to use

Run queries using the query script located in this skill's directory:

```bash
node .claude/skills/drizzle-db/scripts/query.js "SELECT * FROM users LIMIT 10"
```

The script:
- Connects to the database using the project's Drizzle configuration
- Executes the SQL query
- Returns results as JSON

## Configuration

This skill is configured during installation:
- `dialect`: Database type (sqlite/postgres/mysql)
- `databasePath`: For SQLite - direct path to .db file (e.g., ./apps/web/data/app.db)
- `drizzleConfigPath`: For Postgres/MySQL - path to drizzle.config.ts
- `readOnly`: Whether to enforce read-only queries (default: true)

Configuration is stored in `.claude/skills/drizzle-db/.config.json`

Example config for SQLite:
```json
{
  "dialect": "sqlite",
  "databasePath": "./apps/web/data/app.db",
  "readOnly": true
}
```

## Read-only mode

When `readOnly` is true (default), the following operations are blocked:
- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- TRUNCATE
- CREATE

Only SELECT queries are allowed for safety.

## Examples

```bash
# Get all users
node .claude/skills/drizzle-db/scripts/query.js "SELECT * FROM users"

# Count records
node .claude/skills/drizzle-db/scripts/query.js "SELECT COUNT(*) FROM posts"

# Join tables
node .claude/skills/drizzle-db/scripts/query.js "SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id"

# Get schema information
node .claude/skills/drizzle-db/scripts/query.js "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
```

## Limitations

- Requires Node.js and the project's Drizzle setup
- Read-only mode prevents data modifications by default
- Queries timeout after 30 seconds
- Results are limited to 1000 rows by default

## Troubleshooting

If queries fail:
1. Verify drizzle.config.ts path is correct in `.config.json`
2. Ensure database connection credentials are set
3. Check that Drizzle dependencies are installed: `npm install drizzle-orm`
4. Verify database is accessible from current environment
