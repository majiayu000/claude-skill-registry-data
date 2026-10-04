---
id: database-security
version: "1.1.0"
title: "Database Security"
description: "Prevent SQL and NoSQL injection, unsafe ORM and raw-query use, over-privileged database identities, weak tenant isolation, and unauthenticated database transport. Use when generating SQL or raw query strings, NoSQL filters, ORM models or queries, database migration files, or connection strings."
category: prevention
severity: critical
applies_to:
  - "when generating SQL or raw query strings"
  - "when generating NoSQL queries, filters, or aggregation pipelines"
  - "when generating ORM model code or queries"
  - "when generating database migration files"
  - "when wiring connection strings or database transport settings"
languages: ["sql", "python", "javascript", "typescript", "go", "ruby", "java", "kotlin", "csharp"]
token_budget:
  minimal: 1300
  compact: 1850
  full: 2800
rules_path: "rules/"
related_skills: ["secret-detection", "api-security", "logging-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP SQL Injection Prevention Cheat Sheet"
  - "OWASP NoSQL Security Cheat Sheet"
  - "OWASP Database Security Cheat Sheet"
  - "CWE-89: Improper Neutralization of Special Elements in an SQL Command"
  - "CWE-943: Improper Neutralization of Special Elements in Data Query Logic"
---

# Database Security

## Rules (for AI agents)

### ALWAYS
- Bind every untrusted data value through the driver or ORM parameter API. Never place
  it into SQL with language-level interpolation or concatenation — `+`, f-strings, `%`
  formatting, `.format()`, JavaScript template interpolation. Driver placeholders
  (`%s`, `?`, `$1`, `:name`, `@name`) are the binding *mechanism*, not string
  formatting; confusing the two is how this rule is most often misread. The same
  applies to values read back out of the database and used to build a later query:
  stored input is still input, and second-order injection is this bug with a delay.
- Prefer the ORM's structured query-expression API over textual SQL. Where raw SQL is
  genuinely needed, use that framework's documented parameter-binding mechanism and
  never interpolate untrusted values into it.
  `references/orm-safe-query-examples.md` carries the verified form per framework.
- For SQL structure that cannot be a bind parameter — table and column identifiers,
  sort direction, sometimes the operator itself — map the external value to a fixed
  operator-controlled allowlist. Never copy an untrusted identifier or SQL fragment
  into the statement, escaped or not.
- Treat a NoSQL query as a structure, not a string. Build filters with the driver's
  typed query objects, and coerce every request-supplied value to its expected scalar
  type before it reaches a filter. A JSON body substituting `{"$ne": null}` where a
  string was expected turns an equality check into a match-all — operator injection
  needs no quote to break out of.
- Give each application its own database identity with the minimum grants it needs,
  and separate runtime privileges from migration privileges. The runtime identity must
  not receive schema-owner or DDL rights merely because migrations require them.
- For shared-table multi-tenancy, enforce tenant isolation at a deliberate security
  boundary. Where database RLS is used: confirm the application role cannot bypass it
  — a superuser, a `BYPASSRLS` role, and the table owner itself all bypass policies
  unless the table is set to `FORCE ROW LEVEL SECURITY` — test write policies as well
  as read, and bind the tenant context transaction-locally. A session-scoped tenant
  context that survives a connection's return to the pool serves tenant A's rows to
  tenant B.
- Authenticate the database server, do not merely encrypt to it. Encryption without
  certificate verification (`sslmode=require`, MySQL `sslMode=REQUIRED`,
  `TrustServerCertificate=True`) stops passive capture but not a redirected
  connection. Where the client is what establishes trust, use a verifying mode —
  PostgreSQL `verify-full`, MySQL Connector/J `VERIFY_IDENTITY`,
  Microsoft.Data.SqlClient with `TrustServerCertificate=False` — against the
  deployment's trusted CA configuration.
- Obtain database credentials from an operator-controlled secret-management mechanism;
  prefer workload identity or short-lived dynamic credentials where the platform
  supports them. A runtime-injected environment variable is an acceptable fallback,
  not the target — it is readable through process inspection, crash dumps, and many
  orchestrator APIs. Any static credential must support rotation and revocation. See
  `secret-detection` for what counts as a committed credential.

### NEVER
- Manually quote or escape an untrusted SQL value as a substitute for the framework's
  documented parameterization mechanism.
- Use an ORM raw-query method (`.raw()`, `.objects.raw()`, `$queryRawUnsafe`,
  `session.execute(text(...))`) with an interpolated f-string or template literal. Raw
  SQL is not the problem; interpolation into it is.
- Evaluate server-side JavaScript over untrusted input (`$where`, `mapReduce`,
  `$accumulator`). There is no safe form of it — it is code execution inside the
  database.
- Run application workloads as the database superuser: `root`, `postgres`, `sa`.
- Grant destructive DDL capability to the normal application runtime identity.
- Send database traffic across an untrusted network without authenticated encryption,
  or disable certificate verification to work around a certificate error.
- Expose a database listener broadly to the public internet. Restrict reachability to
  explicitly authorized application and administrative sources, and prefer private
  connectivity for application traffic where the platform supports it.
- Emit database credentials, connection strings containing secrets, or sensitive bound
  values to logs. `logging-security` owns the shape this should take — statement
  template, parameter names, a hashed value identifier — and the redactor that
  enforces it.

### KNOWN FALSE POSITIVES
- Encryption without client-side certificate verification is not a finding where the
  channel is already authenticated by other means: a Unix domain socket (where
  `sslmode` does not apply at all), a cloud SQL proxy or sidecar terminating an
  authenticated tunnel, or a service mesh enforcing mTLS. The finding is an
  unauthenticated connection across a network, not the literal string
  `sslmode=require`.
- Some ORMs and DB-API drivers (Django, SQLAlchemy 1.x, psycopg2) use `%s` as a
  *parameter marker*, not a Python format placeholder. `cursor.execute(sql, [value])`
  with an unquoted `%s` is the safe form, not a violation.
- Trusted analyst-authored ad-hoc SQL in a dedicated analytics environment may
  intentionally contain dynamic SQL structure. Keep that capability behind explicit
  authorization and appropriately scoped data access. A read-only account limits
  modification but does not make untrusted query fragments safe, and does not prevent
  unauthorized reads.
- Static SQL with no untrusted dynamic values — `SELECT 1`, fixed schema
  introspection, constant migration statements — does not need artificial bind
  parameters to satisfy this skill.

## Context (for humans)

Injection has remained a recurring OWASP Top 10 risk across editions. SQL injection
stays a high-impact member of that category even as the category's relative ranking
moves between releases, and it has not gone away because the failure mode is *easy by
default*: any language with string concatenation lets you produce a query. AI
assistants readily generate "works in dev" code that interpolates user input —
particularly for sort columns, dynamic filters, and pagination, which are exactly the
places a bind parameter cannot be used and an allowlist has to be.

The NoSQL variant is worth naming separately because it does not look like injection.
Nothing is quoted, nothing is escaped, and there is no string to break out of — the
attacker replaces a scalar with an operator object and the query's *shape* changes.
Reviewers who have learned to spot concatenated SQL will read straight past it.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/orm-safe-query-examples.md` — the verified safe call per framework,
  placeholder styles, and the allowlist pattern for identifiers
- `rules/sql_injection_sinks.json`
- `rules/orm_safe_patterns.json`
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).
- [OWASP NoSQL Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html).
- [CWE-89](https://cwe.mitre.org/data/definitions/89.html) — SQL Injection.
- [CWE-943](https://cwe.mitre.org/data/definitions/943.html) — Data query logic injection.
- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).
