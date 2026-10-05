---
name: neon-prisma-safety
description: "Trigger: Neon MCP, Prisma migration, SQL, schema, database branch. Safely change NutrIA persistence."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use for database investigation, schema or migration work.

# Hard Rules
- MCP connects only to a Neon development branch with anonymized/sample data.
- Never expose connection strings, PII or production results.
- Read schema before writing SQL. Require a reviewed migration and rollback for destructive changes.

# Execution Steps
1. Confirm target is non-production and branch name.
2. Inspect tables and schema.
3. Create a small migration, validate on the branch and run focused tests.
4. Document data-model changes in ADR/Engram.

# Output Contract
Return branch, schema impact, migration, validation evidence and rollback.
