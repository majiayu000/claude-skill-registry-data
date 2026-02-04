---
name: database-explorer
description: Allows read-only access to the SQL database to allow querying and analysis using natural language
---

# Database Explorer

## Instructions

This skill allows read-only access to SQL databases, enabling you to convert natural language queries into SQL queries 
and analyze data without requiring the user to write complex SQL by hand.

### Available Commands

Use the `query-db.ts` script with tsx to interact with the database. The script supports the following commands:

All commands support an optional `--connection` (or `-c`) flag to specify which database connection to use. If not specified, the `default` connection is used.

1. **List all tables**:
   ```bash
   tsx src/query-db.ts tables
   # Or with a specific connection:
   tsx src/query-db.ts --connection my-postgres-db tables
   ```

2. **Introspect entire schema** (get all tables and their columns):
   ```bash
   tsx src/query-db.ts introspect
   # Or with a specific connection:
   tsx src/query-db.ts -c my-mysql-db introspect
   ```

3. **Describe a specific table**:
   ```bash
   tsx src/query-db.ts describe <table_name>
   # Example:
   tsx src/query-db.ts describe users
   ```

4. **Execute a SQL query** (read-only):
   ```bash
   tsx src/query-db.ts query "SELECT * FROM users LIMIT 10"
   # With specific connection:
   tsx src/query-db.ts --connection=production query "SELECT * FROM users LIMIT 10"
   ```

### Important Notes

- **Read-only mode**: Only SELECT, SHOW, DESCRIBE, and EXPLAIN queries are allowed. Any attempt to execute INSERT, UPDATE, DELETE, or DDL statements will be rejected.
- **Database configuration**: Database connections are defined in the root `config.ts` file. Each connection has a name and TypeORM DataSourceOptions:
  - A connection named 'default' will be used when `--connection` is not specified
  - Supported database types: MySQL/MariaDB, PostgreSQL, SQLite
- **JSON output**: All results are returned as JSON, making them easy to parse and present to the user.
- **Multiple connections**: Use the `--connection` flag to switch between different database connections defined in your config.

### Workflow

When the user asks a database question:

1. **First time or unclear schema**: Start by introspecting the schema or listing tables to understand the database structure:
   ```bash
   tsx src/query-db.ts tables
   ```

2. **Understand table structure**: If you need details about a specific table:
   ```bash
   tsx src/query-db.ts describe users
   ```

3. **Convert natural language to SQL**: Based on the user's question and the schema, write an appropriate SQL query. Make sure
   to correctly format the string according to the DB type, which is given in the config.ts file for the active connection:
    - postgres/sqlite
   ```
   SELECT "id", "name", "email" FROM "users" WHERE "createdAt" > '2024-01-01' LIMIT 20;
   ```
   - mysql/mariadb
   ```
   SELECT `id`, `name`, `email` FROM `users` WHERE `createdAt` > '2024-01-01' LIMIT 20;
   ```
   

4. **Execute the query**:
   ```bash
   tsx src/query-db.ts query "SELECT id, name, email FROM users WHERE created_at > '2024-01-01' LIMIT 20"
   ```

5. **Present results**: Format and present the JSON results in a user-friendly way, highlighting key insights. Ask the user if they want to save the report. If yes, save it in `output/reports/<connection_name>/<descriptive_filename>.md`.

### Best Practices

- Cache schema information during a conversation to avoid repeated introspection calls
- Cache last results in temp files in case user wants reports generated
- Use LIMIT clauses to avoid overwhelming results
- For large tables, describe them first before querying
- Explain your SQL queries to the user in plain language
- If a query fails, explain why and suggest alternatives
- Consider performance: use indexes, avoid SELECT * on large tables
- Use aggregate functions (COUNT, SUM, AVG) for statistical queries

## Examples

### Example 1: Finding recent records

**User**: "Show me the 10 most recent users"

**Assistant**:
1. First, introspect schema to find user-related tables
2. Identify the `users` table with relevant columns
3. Execute:
   ```bash
   tsx src/query-db.ts query "SELECT `id`, `username`, `email`, `created_at` FROM `users` ORDER BY `created_at` DESC LIMIT 10"
   ```
4. Present the results in a formatted table
5. Ask if a report is wanted, if so, save to md file and make sure to include the raw SQL queries that were used.

### Example 2: Analyzing data distribution

**User**: "How many items do we have in each category?"

**Assistant**:
1. Check schema to understand table relationships
2. Execute:
   ```bash
   tsx src/query-db.ts query "SELECT `category`, COUNT(*) as `item_count` FROM `items` GROUP BY `category` ORDER BY `item_count` DESC"
   ```
3. Present results with insights

### Example 3: Using multiple connections

**User**: "Compare user counts between development and production databases"

**Assistant**:
1. Query development database:
   ```bash
   tsx src/query-db.ts --connection development query "SELECT COUNT(*) as `user_count` FROM `users`"
   ```
2. Query production database:
   ```bash
   tsx src/query-db.ts --connection production query "SELECT COUNT(*) as `user_count` FROM `users`"
   ```
3. Present comparison with analysis
