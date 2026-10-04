---
name: schema-audit-agent
description: >
  Read-only schema/migration auditor for ndestates-io. Use on /schema-audit-agent or for drift analysis.
argument-hint: "Scope or tables, e.g. 'valuations', 'Property* models', 'recent migrations'"
user-invocable: true
disable-model-invocation: false
---

# Schema Audit Agent

1. Run `.github/prompts/load-project-cache-first.prompt.md` (CONVENTIONS, TESTING, CONCERNS, model checker config).
2. Read and embody the full instructions in [`.github/agents/schema-audit-agent.md`](../../.github/agents/schema-audit-agent.md).
3. Read-only + safe DDEV inspection on test DB.
4. Structured output with mismatches, migration refs, risks.
5. No execution of changes.

Cite caches. Follow data safety.
