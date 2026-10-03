---
name: db
description: Interact with the TMI PostgreSQL database for queries and administration. Use when asked to show data, check tables, or run SQL queries.
allowed-tools: Bash, Read
---

# Database Interaction Skill

You are helping the user interact with the TMI PostgreSQL database.

## Database Connection Information

**IMPORTANT**: All database connection information and credentials are stored in `config-development.yml`:

- **Host**: localhost (from host machine perspective)
- **Port**: 5432
- **User**: tmi_dev
- **Password**: dev123
- **Database**: tmi_dev
- **Container Name**: tmi-postgresql

## Tool Requirements

**PostgreSQL command-line tools (psql) are NOT installed on the host machine.**

You MUST use `docker exec` to run `psql` commands inside the `tmi-postgresql` container.

## Standard Database Operations

### Interactive psql Session

To start an interactive psql session:
```bash
docker exec -it tmi-postgresql psql -U tmi_dev -d tmi_dev
```

### Execute Single SQL Query

To run a single SQL query:
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "YOUR SQL QUERY HERE"
```

### Execute SQL from File

To execute SQL from a file:
```bash
docker exec -i tmi-postgresql psql -U tmi_dev -d tmi_dev < /path/to/file.sql
```

Or using heredoc:
```bash
docker exec -i tmi-postgresql psql -U tmi_dev -d tmi_dev <<'EOF'
YOUR SQL QUERY HERE
EOF
```

## Common Database Tasks

### List All Tables
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "\dt"
```

### Describe Table Schema
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "\d table_name"
```

### Count Records
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "SELECT COUNT(*) FROM table_name;"
```

### View Table Data
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "SELECT * FROM table_name LIMIT 10;"
```

### Run Migrations
Migrations are located in `auth/migrations/` directory. See the migration commands in the Makefile or use:
```bash
make migrate
```

### Database Reset
To reset the database (drop and recreate schema):
```bash
make heroku-reset-db  # Works for local database too
```

## TMI Database Schema

Key tables in the TMI database:
- `users` - User accounts and authentication
- `threat_models` - Top-level threat model entities
- `diagrams` - Threat model diagrams (DFD, etc.)
- `cells` - Diagram cells (nodes and edges)
- `threats` - Identified threats
- `documents` - Document attachments
- `repositories` - Code repository links
- `notes` - Text notes
- `assets` - Asset inventory items
- `metadata` - Flexible key-value metadata for entities

## Best Practices

1. **Always use parameterized queries** when dealing with user input to prevent SQL injection
2. **Use transactions** for multi-statement operations
3. **Check container status** before executing commands:
   ```bash
   docker ps --filter "name=tmi-postgresql"
   ```
4. **Quote SQL properly** - use single quotes for SQL string literals, escape special characters
5. **Use heredoc for multi-line SQL** to avoid shell quoting issues:
   ```bash
   docker exec -i tmi-postgresql psql -U tmi_dev -d tmi_dev <<'EOF'
   SELECT * FROM table_name WHERE condition = 'value';
   EOF
   ```

## Error Handling

If you encounter errors:

1. **Container not running**: Start the database with `make start-database` or `make start-dev`
2. **Connection refused**: Check if the container is healthy: `docker ps`
3. **Authentication failed**: Verify credentials in `config-development.yml`
4. **Database does not exist**: Run migrations with `make migrate`

## Security Notes

- The credentials in `config-development.yml` are for **local development only**
- Never commit real production credentials to the repository
- The dev password (`dev123`) is intentionally simple for local development

## Examples

### Query threat models with their owners
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "
SELECT id, name, owner, created_at
FROM threat_models
ORDER BY created_at DESC
LIMIT 5;
"
```

### Find all assets of type 'software'
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "
SELECT a.id, a.name, a.type, tm.name as threat_model
FROM assets a
JOIN threat_models tm ON a.threat_model_id = tm.id
WHERE a.type = 'software';
"
```

### Check migration status
```bash
docker exec tmi-postgresql psql -U tmi_dev -d tmi_dev -c "
SELECT version, applied_at
FROM schema_migrations
ORDER BY version;
"
```

## Integration with Claude Code

When the user asks to:
- **"Show me..."** - Use SELECT queries
- **"Add/Create..."** - Use INSERT queries (but ask for confirmation first)
- **"Update/Modify..."** - Use UPDATE queries (but ask for confirmation first)
- **"Delete/Remove..."** - Use DELETE queries (but ALWAYS ask for confirmation first)
- **"Reset/Clear..."** - Suggest using `make heroku-reset-db` or specific DELETE queries

Always show the user the SQL query you're about to execute before running it, especially for INSERT, UPDATE, or DELETE operations.
