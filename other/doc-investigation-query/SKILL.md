---
name: doc-investigation-query
description: Answer questions by reading every captured investigation in the registry (default ~/.claude/investigation-registry/, override with $CLAUDE_DOC_HOME). Investigations are written by /sdd:doc-investigation and are typed bug, exploration, or improvements. Ask things like "what was the vehicle-lookup cache bug?", "how does a lead reach the cache?", "which investigations touch LeadService?", "have we seen ReportToken reuse before?", "list the exploration notes for lead-service", "which improvement plans are still open?".
argument-hint: "free-text investigation question"
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(grep:*)
---

# Investigation Query


---

## Registry Path

All registry reads resolve through a single environment variable:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry"
```

- **Default** (no env var set): `~/.claude/investigation-registry/`.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g. a cloned GitLab repo for team-shared findings.

The same variable controls `/sdd:doc-catalog`, `/sdd:doc-spec`, and `/sdd:doc-adr`, so every registry moves together. Investigations are keyed by service exactly like ADRs and specs: `investigation-registry/<service>/<date>-<slug>.md`.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Lists every service subdir under `~/.claude/investigation-registry/` |
| 2 | Detects whether the question targets one (or a few) specific services and narrows scope |
| 3 | Reads every investigation file in scope |
| 4 | Answers `$ARGUMENTS` using the combined knowledge |
| 5 | Cites every claim as `<service>/<file>` |

---

## Step 1 — Check Registry

```bash
find "${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry" -name "*.md" -type f 2>/dev/null | head -1 | grep -q .
```

If empty, abort:

```
No investigations found in ~/.claude/investigation-registry/.

Capture one with /sdd:doc-investigation after researching code, then re-run this query.
```

---

## Step 2 — Detect Target Service(s)

The registry is organized into per-service subdirs. Most questions concern a single service, so reading every file wastes tokens. Detect when the question references a specific service and narrow the read scope.

### Procedure

1. **List available service subdirs:**

   ```bash
   ls -1 "${CLAUDE_DOC_HOME:-$HOME/.claude}/investigation-registry/" 2>/dev/null
   ```

2. **Tokenize `$ARGUMENTS` and extract kebab-case candidates** — sequences containing a `-`, e.g. `lead-service`, `consumer-portal`. Service names always contain a hyphen, so plain English words are filtered out automatically.

3. **Match each candidate against the subdir list, case-insensitive.** Accept:
   - **Exact matches** — `lead-service` → `lead-service`
   - **Prefix matches** longer than 4 characters — `consumer` → `consumer-portal`

   Reject kebab-case tokens that match no subdir (they are likely feature or symptom phrases, not services).

4. **Aggregate-question check** — if the question contains any of these signals, ignore matches and read the full registry:

   - `services` (plural), `which services`, `all services`, `every service`, `any service`
   - `across services`, `between services`, `compare`, `ever`, `before`, `have we seen`
   - `the registry`, `all investigations`, `every investigation`

5. **Decide scope:**

   | Matches found | Aggregate phrase? | Scope |
   |---------------|-------------------|-------|
   | 0             | —                 | All services |
   | 1             | no                | That service only |
   | 1             | yes               | All services |
   | 2+            | no                | Just the matched services |
   | 2+            | yes               | All services |

6. **Announce the scope before reading.**

   Narrow:
   ```
   Detected target service: lead-service (4 investigations). Reading only this subdir.
   ```

   Broad:
   ```
   Reading the full investigation registry — the question references multiple services or no specific one:
     consumer-portal               (2 investigations)
     lead-service                  (4 investigations)
   ```

---

## Step 3 — Read In-Scope Investigations

Read every `*.md` file in the chosen subdirs. Each file's `type` frontmatter
(`bug`, `exploration`, or `improvements`) tells you which of the three fixed shapes it
uses — build a combined knowledge base of:

- **Frontmatter** — `title`, `service`, `date`, `type`, `source`, `verified_at` (the
  commit the doc was written against — use it to judge staleness), and on `improvements`
  files also `status` (`proposed` / `in-progress` / `done` / `superseded` / `abandoned`)
  and `updated`
- **bug files** — Problem / Symptoms (what broke), Investigation (what was checked, with
  SQL/code), Findings / Root Cause (why), Fix (may be `[TBD]`), Related Classes,
  Future Signals
- **exploration files** — Question / Context (what was being understood), Map +
  How It Works (the mechanism/flow), Key Findings, Caveats & Gotchas, Open Questions,
  Future Signals
- **improvements files** — Goal (the requirement), Current State, Gap Analysis (gaps
  with ADOPT/PARTIAL/REJECT verdicts), Plan (proposed changes), Out of Scope (what was
  rejected and why), Open Decisions, Future Signals

All three shapes share **Future Signals** (the "next time, check/start here" heuristic),
so treat that section uniformly across types.

Track which **service** each file belongs to (parent directory), its **date** and
**slug** (filename), and its **type** (frontmatter).

---

## Step 4 — Answer the Question

Use the combined knowledge to answer `$ARGUMENTS`.

### Query types and how to answer them

**Incident recall** — "what was the vehicle-lookup cache bug?"
- Read the matching file's Problem + Root Cause + Fix; summarize the story.

**Impact / target scan** — "which investigations touch LeadService?"
- Grep Related Classes + Investigation across in-scope files for the class/file; group hits by service + date.

**Pattern / recurrence** — "have we seen ReportToken reuse before?"
- Aggregate question; read the full registry; surface every file whose Findings/Root Cause/Symptoms mention the pattern, oldest first.

**Future-signal lookup** — "what should I check first if multiple vehicles disappear?"
- Search Future Signals sections for the matching heuristic and quote it.

**Root-cause search** — "which bugs were cache-invalidation issues?"
- Search Root Cause sections across in-scope files. Limit to `type: bug` files.

**How-it-works lookup** — "how does a lead reach the cache?" / "do we have notes on the consent flow?"
- Prefer `type: exploration` files; read their Map + How It Works sections.

**Improvement-plan lookup** — "what's the plan to meet the CLAUDE.md gist?" / "which improvement plans are still open?"
- Prefer `type: improvements` files; read their Goal + Gap Analysis + Plan. Filter by
  `status` for open vs done ("open" = `proposed` or `in-progress`; closed = `done` /
  `superseded` / `abandoned`), and read the Plan checklist to report which steps remain.
  Surface what was rejected from Out of Scope when asked why something was *not* done.

**Type filter** — "list the exploration notes for lead-service" / "which bug write-ups exist?" / "which improvement plans exist?"
- Filter in-scope files by the `type` frontmatter field, then list title + date (+ `status` for improvements).

---

## Step 5 — Format the Answer

Cite the source for every claim using `<service>/<file>`:

```
Question: Have we seen ReportToken reuse cause problems before?

Yes — once (lead-service/2026-06-10-vehicle-lookup-stale-rows.md):

  Problem:     Vehicle lookup returned inconsistent results.
  Root Cause:  Cache invalidation bug — ReportToken is reused intentionally by DataVendor,
               so the person_search_cache row was served stale.
  Fix:         <...>
  Future Signal: If multiple vehicles disappear after a person lookup, check cache
               expiration first.

Sources: lead-service/2026-06-10-vehicle-lookup-stale-rows.md
```

If the answer cannot be determined from the in-scope investigations:

```
Could not find this in the in-scope investigations.
There may be no capture for <service> yet — record one with /sdd:doc-investigation, or
rephrase without naming a specific service to broaden the scope.
```

---

## Related Skills

- `doc-investigation` — captures the investigations this skill reads
- `doc-adr-query` — same pattern for architecture decisions
- `doc-spec-query` — same pattern for feature specs
- `doc-catalog-query` — same pattern for service catalogs
