---
name: doc-spec-query
description: Answer feature/spec questions by reading every spec in the registry (default ~/.claude/spec-registry/, override with $CLAUDE_DOC_HOME). Specs are stored by /sdd:doc-spec or the SDD pipeline's /sdd:mr. Ask things like "what does the lead-dedupe feature do?", "which specs touch LeadProcessor?", "which specs still have open questions?", "what safe constraints apply to consent changes?", "what is the acceptance criteria for the DataVendor retry feature?".
argument-hint: "free-text spec/feature question"
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(grep:*)
---

# Spec Query

---

## Registry Path

All registry reads resolve through a single environment variable:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/spec-registry"
```

- **Default** (no env var set): `~/.claude/spec-registry/`.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g., a cloned GitLab repo for team-shared specs.

The same variable controls `/sdd:doc-catalog`, `/sdd:doc-catalog-query`, `/sdd:doc-adr`, and `/sdd:doc-adr-query`, so all registries move together. Specs are written here by `/sdd:doc-spec` or by `/sdd:mr` (which calls `spec-publish.sh`), keyed by service exactly like ADRs: `spec-registry/<service>/<slug>-spec.md`.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Lists every service subdir under `~/.claude/spec-registry/` |
| 2 | Detects whether the question targets one (or a few) specific services and narrows scope |
| 3 | Reads every spec file in scope |
| 4 | Answers `$ARGUMENTS` using the combined knowledge |
| 5 | Cites every claim as `<service>/<spec-file>` |

---

## Step 1 — Check Registry

```bash
find "${CLAUDE_DOC_HOME:-$HOME/.claude}/spec-registry" -name "*-spec.md" -type f 2>/dev/null | head -1 | grep -q .
```

If empty, abort:

```
No specs found in ~/.claude/spec-registry/.

Store a spec with /sdd:doc-spec <path>, or run the SDD pipeline through /sdd:mr
(which publishes automatically when a .specwork spec exists), then re-run this query.
```

---

## Step 2 — Detect Target Service(s)

The registry is organized into per-service subdirs. Most questions concern a single service ("what does lead-service's dedupe feature do?"), so reading every spec wastes tokens. Detect when the question references a specific service and narrow the read scope.

### Procedure

1. **List available service subdirs:**

   ```bash
   ls -1 "${CLAUDE_DOC_HOME:-$HOME/.claude}/spec-registry/" 2>/dev/null
   ```

2. **Tokenize `$ARGUMENTS` and extract kebab-case candidates** — sequences containing a `-`, e.g., `lead-service`, `consumer-portal`, `package-orchestrator`. Service names always contain a hyphen, so plain English words are filtered out automatically.

3. **Match each candidate against the subdir list, case-insensitive.** Accept:
   - **Exact matches** — `lead-service` → `lead-service`
   - **Prefix matches** longer than 4 characters — `consumer` → `consumer-portal`

   Reject kebab-case tokens that don't match any subdir (e.g., `lead-dedupe` is a feature slug, not a service).

4. **Aggregate-question check** — if the question contains any of these signals, ignore matches and read the full registry:

   - `services` (plural), `which services`, `all services`, `every service`, `any service`, `multiple services`
   - `across services`, `between services`, `compare`
   - `the registry`, `all specs`, `every spec`, `every feature`

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
   Detected target service: lead-service (3 specs). Reading only this subdir.
   ```

   Broad (no match, or aggregate question):
   ```
   Reading the full spec registry — the question references multiple services or no specific one:
     consumer-portal               (4 specs)
     lead-service                  (3 specs)
   ```

---

## Step 3 — Read In-Scope Specs

Read every `*-spec.md` file in the subdirs chosen by Step 2. Each spec follows the
canonical SDD structure — build a combined knowledge base of:

- **Title / Summary** — what the feature is and **why** (the `## Summary` section)
- **Behavior** — the acceptance criteria as observable behaviors (`## Behavior`)
- **Scope** — what is in and explicitly out of scope (`## Scope`)
- **Implementation Context / Expected Change Scope** — affected services, classes,
  files, layers (`## Implementation Context`, `## Expected Change Scope`)
- **Safe Constraints** — invariants the change must preserve: PII, idempotency,
  API backward-compat, SLA/retry, DB migration (`## Safe Constraints`)
- **Open Questions** — unresolved (`- [ ]`) vs resolved (`- [x]`) checkboxes
  (`## Open Questions`)

Track which **service** each spec belongs to (from its parent directory name) and
the feature **slug** (from the filename, `<slug>-spec.md`).

---

## Step 4 — Answer the Question

Use the combined spec knowledge to answer `$ARGUMENTS`.

### Query types and how to answer them

**Feature lookup** — "what does the lead-dedupe feature do?"
- Read the matching spec's Summary + Behavior; describe intent and acceptance criteria.

**Impact / target scan** — "which specs touch LeadProcessor / the consent flow?"
- Grep Implementation Context + Expected Change Scope (and Behavior) across in-scope
  specs for the class/file/concept; group hits by service + slug.

**Constraint search** — "which features require idempotency / forbid schema changes?"
- Search Safe Constraints sections for the invariant.

**Open-Questions filter** — "which specs still have unresolved open questions?"
- Filter specs whose `## Open Questions` contains an unchecked `- [ ]`.
- Distinguish unresolved (`- [ ]`) from resolved (`- [x]`).

**Acceptance criteria** — "what is the acceptance criteria for feature X?"
- Quote the numbered behaviors from that spec's `## Behavior`.

**Cross-service patterns** — "which services changed the consent flow?"
- Aggregate question; Step 2 should have chosen the full registry.
- Find specs with related Behavior/Implementation Context across service subdirs.

---

## Step 5 — Format the Answer

Cite the source spec for every claim using `<service>/<spec-file>`:

```
Question: What does the lead-dedupe feature do, and what must it preserve?

Summary (lead-service/dedupe-null-application-spec.md):
  Skip lead deduplication when applicationId is null instead of throwing, so
  ingestion no longer fails on partial leads.

Behavior:
  1) Given a null applicationId, skip dedupe and continue ingestion.
  2) Given a non-null applicationId, dedupe as before.

Safe Constraints:
  - Idempotent per applicationId
  - No schema change

Open Questions: none unresolved.

Sources: lead-service/dedupe-null-application-spec.md
```

If the answer cannot be determined from the in-scope specs:

```
Could not find this in the in-scope specs.
The specs for <service> may be missing — store one with /sdd:doc-spec, or run the
pipeline through /sdd:mr in that project, or rephrase without naming a specific
service to broaden the scope.
```

---

## Related Skills

- `doc-spec` — stores a spec in `~/.claude/spec-registry/<service>/`
- `spec` (sdd bundle) — authors the `spec.md` this registry stores
- `mr` (sdd bundle) — publishes the spec to `~/.claude/spec-registry/<service>/`
- `doc-adr-query` — same pattern for architecture decisions
- `doc-catalog-query` — same pattern for service catalogs
