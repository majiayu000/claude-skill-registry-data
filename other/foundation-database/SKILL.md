---
name: foundation-database
description: Set up database with schema, migrations, and connection management
argument-hint: [database-type: postgres|sqlite|mysql]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# Foundation — Database

Set up database layer: schema design, migrations, connection management, seed data.

## Input

Database type: `$ARGUMENTS` (default: detect from project config or ask)

## Process

1. Read the architecture doc for data model requirements
2. Design the initial schema based on the architecture
3. Set up:
   - Database connection management (pooling, retries)
   - Migration framework (alembic, knex, diesel, etc.)
   - Initial migration with the schema
   - Seed data for development
   - Connection configuration from environment
4. Create database utility functions (CRUD helpers if appropriate)
5. Add database to docker-compose if using Docker
6. Write tests that use a test database

## Rules

- Migrations must be reversible
- Connection pooling from the start
- Never hardcode connection strings
- Test database must be separate from dev database
- Seed data must be idempotent