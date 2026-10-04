---
name: doc-adr-query
description: Answer architecture-decision questions by reading every ADR in the registry (default ~/.claude/adr-registry/, override with $CLAUDE_DOC_HOME). ADRs are written by /sdd:doc-adr. Ask things like "why did consumer-portal pick PostgreSQL for circuit-breaker state?", "which services have superseded ADRs?", "what decisions reference Cognito?", "show me every ADR about retries".
argument-hint: "free-text decision question"
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(grep:*)
---

# ADR Query

---

## Registry Path

All registry reads resolve through a single environment variable:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry"
```

- **Default** (no env var set): `~/.claude/adr-registry/` — identical to the original behavior.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g., a cloned GitLab repo for team-shared ADRs.

The same variable controls `/sdd:doc-adr`, `/sdd:doc-catalog`, `/sdd:doc-catalog-query`, `/sdd:doc-spec`, and `/sdd:doc-spec-query`, so all doc registries move together.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Lists every service subdir under `~/.claude/adr-registry/` |
| 2 | Detects whether the question targets one (or a few) specific services and narrows scope |
| 3 | Reads every ADR file in scope |
| 4 | Answers `$ARGUMENTS` using the combined knowledge |
| 5 | Cites every claim as `<service>/<ADR-file>` |

---

## Step 1 — Check Registry

```bash
find "${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry" -name "*.md" -type f 2>/dev/null | head -1 | grep -q .
```

If empty, abort:

```
No ADRs found in ~/.claude/adr-registry/.

Run /sdd:doc-adr in a project — it creates the ADR and stores it in this registry in one step.
```

---

## Step 2 — Detect Target Service(s)

The registry is organized into per-service subdirs. Most questions concern a single service ("why does creditbureau-service do X?"), so reading every ADR across the registry wastes tokens. Detect when the question references a specific service and narrow the read scope.

### Procedure

1. **List available service subdirs:**

   ```bash
   ls -1 "${CLAUDE_DOC_HOME:-$HOME/.claude}/adr-registry/" 2>/dev/null
   ```

2. **Tokenize `$ARGUMENTS` and extract kebab-case candidates** — sequences containing a `-`, e.g., `creditbureau-service`, `consumer-portal`, `package-orchestrator`. Service names always contain a hyphen, so plain English words are filtered out automatically.

3. **Match each candidate against the subdir list, case-insensitive.** Accept:
   - **Exact matches** — `creditbureau-service` → `creditbureau-service`
   - **Prefix matches** longer than 4 characters — `creditbureau` → `creditbureau-service`

   Reject kebab-case tokens that don't match any subdir (e.g., `circuit-breaker` is a topic, not a service).

4. **Aggregate-question check** — if the question contains any of these signals, ignore matches and read the full registry:

   - `services` (plural), `which services`, `all services`, `every service`, `any service`, `multiple services`
   - `across services`, `between services`, `compare`
   - `the registry`, `all ADRs`, `every ADR`

5. **Decide scope:**

   | Matches found | Aggregate phrase? | Scope |
   |---------------|-------------------|-------|
   | 0             | —                 | All services |
   | 1             | no                | That service only |
   | 1             | yes               | All services |
   | 2+            | no                | Just the matched services |
   | 2+            | yes               | All services |

6. **Announce the scope before reading.**

   Narrow to one:
   ```
   Detected target service: creditbureau-service (1 ADR). Reading only this subdir.
   ```

   Narrow to several:
   ```
   Detected target services: consumer-portal (2 ADRs), creditbureau-service (1 ADR).
   Reading these subdirs only.
   ```

   Broad (no match, or aggregate question):
   ```
   Reading the full ADR registry — the question references multiple services or no specific one:
     consumer-portal               (2 ADRs)
     creditbureau-service            (1 ADR)
   ```

---

## Step 3 — Read In-Scope ADRs

Read every `.md` file in the subdirs chosen by Step 2 (one, several, or all). Build a combined knowledge base of:

- **Title** — the ADR's `# ADR-NNN: <Title>` heading (3-digit ADR number, e.g. `# ADR-001: ...`)
- **Status** — `Accepted`, `Superseded by ADR-NNN`, `Deprecated`, etc.
- **Context** — the problem/constraint that forced the decision
- **Decision** — what was chosen, and which alternatives were ruled out
- **Consequences** — trade-offs the team accepted
- **Related** — Jira tickets, MRs

Track which **service** each ADR belongs to (from its parent directory name).

---

## Step 4 — Answer the Question

Use the combined ADR knowledge to answer `$ARGUMENTS`.

### Query types and how to answer them

**Decision lookup** — "why did we pick X over Y?"
- Search Context + Decision sections across the in-scope ADRs
- Quote the rejected alternative and its reason

**Topic scan** — "what ADRs touch retries / Cognito / Moxo?"
- Grep all in-scope ADR bodies for the keyword
- Group hits by service

**Status filter** — "which decisions have been superseded?"
- Filter by `Status: Superseded by ...`
- Show the supersedes chain when present

**Cross-service patterns** — "do multiple services persist circuit-breaker state in Postgres?"
- This is an aggregate question; Step 2 should have chosen the full registry
- Find ADRs with similar Context across different service subdirs
- Note convergence or divergence

**Consequence search** — "which decisions added a DB read on the hot path?"
- Search Consequences sections for the impact phrase

---

## Step 5 — Format the Answer

Cite the source ADR for every claim using `<service>/<ADR-file>`:

```
Question: Why did consumer-portal pick PostgreSQL for circuit-breaker state?

Context (consumer-portal/PROJ-17097-ADR-001-use-postgresql-circuit-breaker.md):
  The DataVendor integration needs durable open/closed state shared across
  service replicas. Redis was the default candidate.

Decision:
  Use PostgreSQL with a singleton row. Redis was ruled out because the
  service already runs Postgres and adding Redis would expand the
  ops footprint for a single ~kilobyte of state.

Consequences:
  + No new infrastructure component
  + State survives restarts
  - One extra DB read per DataVendor call

Sources: consumer-portal/PROJ-17097-ADR-001-use-postgresql-circuit-breaker.md
```

If the answer cannot be determined from the in-scope ADRs:

```
Could not find this in the in-scope ADRs.
The ADRs for <service> may be missing — run /sdd:doc-adr in that project,
or rephrase the question without naming a specific service to broaden the scope.
```

---

## Related Skills

- `doc-adr` — creates an ADR and stores it in `~/.claude/adr-registry/<service>/`
- `doc-catalog-query` — same pattern for service catalogs
