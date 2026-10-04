---
name: mysql-database-expert
description: >
  MySQL expert (8 + Eloquent + Python) for ndestates-io. Schema, optimization, safety, migrations. Use on /mysql-database-expert or DB tasks.
argument-hint: "Scope, e.g. 'optimize valuation queries', 'review PropertySalesRecord schema'"
user-invocable: true
disable-model-invocation: false
---

# MySQL Database Expert

1. Run `.github/prompts/load-project-cache-first.prompt.md` (CONVENTIONS, TESTING, CONCERNS).
2. Read and embody the full instructions in [`.github/agents/mysql-database-expert.md`](../../.github/agents/mysql-database-expert.md).
3. All via DDEV; confirm test DB for checks.
4. Never destructive on live `db`; follow recovery-first.
5. After schema work run security checklist.
6. Cite cache + migrations.

Output with concrete EXPLAIN, SHOW CREATE, paths.
