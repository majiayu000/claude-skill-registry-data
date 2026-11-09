---
name: database-cli-query
description: Run or structure database connectivity and query workflows through supported CLI tools for MSSQL, MySQL, PostgreSQL, SQLite, Azure Storage Tables, Cosmos DB metadata, and Databricks SQL.
engines: [AGNOSTIC]
---

## When to use
Use when a task needs deterministic command-line connectivity tests or query execution against supported database engines, or when you need reusable CLI command examples for operators.

## Output
- selected engine-specific command form
- required environment variables and auth assumptions
- executed query or metadata command
- result summary and any CLI limitations encountered

## Workflow
1. Confirm the target engine and required auth shape.
2. Validate CLI availability and required environment variables.
3. Execute minimal connectivity/query command first (for example `SELECT 1`).
4. Run target query/filter and summarize outputs.
5. For engines without direct query CLI support, return the supported metadata path and fallback guidance.

## Command
- `./commands/database-cli-query.sh <engine> [options]`

