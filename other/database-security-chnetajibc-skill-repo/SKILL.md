---
name: database-security
description: "Least-privilege database access: roles, read-only agents, destructive-query prevention, MCP access rules. Use when wiring app, agent, or MCP access to any database."
---

# database-security

The database enforces what application bugs forget: least privilege, read-only by default for agents, no destructive queries without explicit authorization.

## Activate when

- Creating roles, connection strings, or MCP/database tool access.
- Letting an agent query production or staging data.
- Reviewing migrations touching permissions or sensitive columns.

## Do NOT activate for

- Schema/query performance (see postgres-operations).

## Procedure

1. Roles: app role gets only the statements it needs on only its schema; separate migration role; no superuser for apps or agents.
2. Agent/MCP access: read-only connection, explicit table/column allowlist, row cap + statement timeout, query validation before execution; block `DROP/DELETE/UPDATE/TRUNCATE/ALTER/GRANT` unless the task explicitly authorizes a scoped write with owner sign-off.
3. Secrets: credentials from the secret manager, never code or logs; rotate on exposure.
4. Sensitive data: encrypt in transit and at rest, minimize logged fields, mask PII in traces and error messages.
5. Verify: connect as the app/agent role and confirm a forbidden statement fails; confirm destructive patterns are rejected by the guardrail, not just by policy text.

## References
- `../postgres-operations/` for operational procedures.
- `../../security/secrets-supply-chain/` for secret handling.
