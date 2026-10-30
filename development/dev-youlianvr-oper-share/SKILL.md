---
name: dev
description: >-
  Writing and changing code: Ponytail simplicity, grounded style rules, local and
  feature-wide systematic debugging, completion verification, architecture
  improvements, defensive bash, API/database design, money-path safety, hardening
  and observability, RAG pipelines. One contract; the parts under parts/ carry the
  rules — open the ones the task needs.
---

# dev — writing and changing code

> Home branch in Memora: `root/skill/dev`. Every part is a method, not a mode:
> read the section you need, never a large file end to end.

## Choosing a part

**Everyday quality**

| Part | What it covers |
|---|---|
| `parts/ponytail/` | Main route: simplest clear complete solution; existing tools and code first, no silent scope cuts or weaker checks |
| `parts/coding-style/` | Grounded APIs and versions, project conventions, coherent changes, optional complexity diagnostics |
| `parts/simplify/` | Reduce needless complexity once behavior is understood; cleanup stays separate from correctness fixes |
| `parts/systematic-debugging/` | Reproduce and repair a local bug or a whole feature journey; trace dependencies and affected consumers |
| `parts/debug-incident-protocol/` | Hung, regressed or silently failing runtime, stale code, duplicate consumers, a restart that must be verified |
| `parts/testing-discipline/` | Writing and reviewing tests, test sensitivity, isolation of storage and external effects, what verification a change needs |
| `parts/architecture-simplicity/` | Module and layer design, library versus own code, god-files, "an abstraction for growth", schema evolution without data loss |
| `parts/improve-codebase-architecture/` | Structural improvement passes on an existing codebase |
| `parts/agent-refactor-safety/` | Extracting modules, splitting a monolith, moving symbols, repairing behavior lost after an edit |
| `parts/bash-defensive-patterns/` | Defensive bash: quoting, `set -euo pipefail`, safe temp files, portability traps |
| `parts/changelog-discipline/` | Keep a CHANGELOG as a decision log: what changed, why, what was rejected |
| `parts/cross-platform-gotchas/` | Python/bash installers on Linux, macOS and Windows: paths, encodings, package managers, WSL stubs |

**API, data and service design**

| Part | What it covers |
|---|---|
| `parts/api-design-reviewer/` | Review API designs for consistency, ergonomics and contract quality |
| `parts/api-test-suite-builder/` | Build API test suites from contracts or specs |
| `parts/database-designer/` | Schema design: normalization, indexes, constraints, migrations |
| `parts/sql-database-assistant/` | Working SQL for Postgres, MySQL and SQLite — queries, tuning, schema changes |
| `parts/jsonc-surgical-edit/` | Edit JSON/JSONC configs by offsets without losing comments, ordering or manual entries |
| `parts/money-path-safety/` | Anything that debits, credits or grants: idempotency, atomicity, buckets, hard gates, charge after success |
| `parts/hardening-observability/` | Rate limits, metrics, log tiers, "database is locked", why metrics lie, a security pass |

**AI and retrieval plumbing**

| Part | What it covers |
|---|---|
| `parts/rag-architect/` | Design RAG pipelines: chunking, embeddings, retrieval evaluation |
| `parts/langchain-rag/` | LangChain-specific RAG implementation patterns |
| `parts/llm-cost-optimizer/` | Reduce LLM cost: model tiering, caching, prompt compression |

**Deciding and routing**

| Part | What it covers |
|---|---|
| `parts/production-first-decisions/` | A consequential tool or design choice with unresolved evidence: compare, research the gap, spike the load-bearing claim |
| `parts/using-superpowers/` | Choose and compose task-relevant skills when the route is unclear |
| `parts/fastapi/` | FastAPI and Pydantic conventions: `Annotated`, return types, routers, async versus sync, SSE and byte streaming, frontend serving, OpenTelemetry |

## Rules

- **Main route** → understand the task and the code → `ponytail` + `coding-style` → verification
  through the real usage path. A method, not an approval ceremony.
- **Bug** → `systematic-debugging` for cause and consumer-wide repair; a hung process or a
  suspicious restart → `debug-incident-protocol`. Verification stays a completed act, not a
  separate gate: BOOT §5 already forbids reporting unexercised claims.
- **Refactor versus cleanup** → behavior-preserving cleanup is `simplify`; structural redesign is
  `improve-codebase-architecture`; a risky mechanical sweep is `agent-refactor-safety`.
- **Tests** → `testing-discipline`. Implementation order is not a completion gate; the mandatory
  TDD package was retired by the owner on 2026-10-04.
- **Forks worth `ask_questions`**: a change of public contract, a schema migration that can lose
  data, a new dependency or service, money or quota semantics, an irreversible data operation.
  Ordinary implementation detail is decided here and stated in one line.
- **Findings that outlive the task** become Memora nodes under `root/skill/dev` (or the project
  branch); `_memory/reports/` keeps only large tables and dated evidence.
- **Shipping the change** → the `ship` router.

## Related

`ship` (release, dependencies, git), `discipline` methods now living in the parts above,
`review` (`verify`, `diagnosing-bugs`), `loops` for repeated work.
