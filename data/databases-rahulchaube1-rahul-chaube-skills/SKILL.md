---
name: databases
description: SQL design, indexing, migrations, and query optimization.
---

# Databases

SQL design, indexing, migrations, and query optimization.

## Core Guidelines

- **Migrations**: Always write migrations for schema changes. Do not perform direct database mutations.
- **Indexes**: Create indexes for columns frequently used in WHERE, JOIN, and ORDER BY clauses.
- **Normalization**: Keep schemas clean, structured, and normalized.
