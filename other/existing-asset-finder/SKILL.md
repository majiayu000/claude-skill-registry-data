---
name: existing-asset-finder
description: Use when someone asks to check whether something already exists, find an existing solution before creating one, search for a similar skill, report, table, dashboard, script, or workflow, or avoid duplicate work. Also use proactively before creating any new file, script, report, skill, database object, dashboard, or workflow, to confirm nothing usable already exists.
argument-hint: [proposed asset name, problem description, or file path]
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(find *), Bash(ls *), Bash(psql *)
---

## What This Skill Does

Searches the project (files, skills, docs, config, and the database where possible) for
an existing asset that already solves the problem before anything new gets created.
Produces a report and a REUSE / EXTEND / MERGE / CREATE / STOP recommendation.

This skill is **read-only**. It never creates, edits, or deletes anything, and never
takes action on its own recommendation — a later, separate request must explicitly
authorize any build/change work.

## Input

`$ARGUMENTS` is the proposed asset: a name, a short problem/feature description, a
report or table name, a script purpose, a workflow description, or a file path.

If `$ARGUMENTS` is empty or too vague to search on (e.g. a single generic word), ask
one clarifying question before searching: "What should this asset do, or what would
someone call it?" Ask this directly as free text — a proposed asset's purpose/name has
no finite menu of good answers, so it's exempt from the clickable-question convention in
`skill-builder/reference.md`.

## Step-by-Step Workflow

**1. Understand the request**
Restate in one line what's being proposed: its purpose, expected inputs/outputs, and
likely names (including plausible synonyms and business terms — e.g. "churn report"
might also be called "attrition report" or "customer loss dashboard").

**2. Search broadly, not just by exact name**
Search all of the following, using the asset name AND synonyms/business terms AND
expected functionality/output (not filename matches alone):

- Repository source files and nested project folders
- `.claude/skills/` (all levels: project, and any visible personal/plugin skills)
- `CLAUDE.md` (project root and any nested ones)
- Documentation folders (`docs/`, `README*`, wikis if present as files)
- Scripts directories
- Reports / evidence / output folders (e.g. `output/`, `reports/`, `evidence/`)
- Configuration files (may reference existing jobs, dashboards, or integrations)

Use `Grep`/`Glob` for content and filename search, and `Bash(find *)` / `Bash(ls *)`
for directory discovery. Do at least 3 distinct search angles (name, synonym,
functional description) before concluding something isn't present. Never declare an
asset absent after a single filename search.

**3. Check for a database (PostgreSQL) match, if relevant**
- If the asset could be (or overlaps with) a database object (table, view, function,
  materialized view), first check whether a Postgres connector/MCP tool or a `psql`
  CLI with valid connection info is available in this environment.
- If available: query `information_schema.tables`, `information_schema.columns`,
  `information_schema.routines`, and `pg_matviews`/`pg_views` (read-only `SELECT`
  queries only — never `INSERT`/`UPDATE`/`DELETE`/`DDL`) for names and column patterns
  matching the request and its synonyms.
- If no live DB access is available: fall back to grepping code/docs/config for
  references to matching table or object names, and explicitly mark the database
  itself as **not directly searched** in the report — do not imply it was checked.

**4. Compare and classify**
For every plausible hit found, classify it as one of:
- **Exact match** — solves the same problem, same scope
- **Partial match** — solves part of it, or solves it with a narrower/broader scope
- **Obsolete** — appears related but stale, deprecated, or superseded
- **Conflicting** — same name/purpose but inconsistent or contradictory implementation
- **Unrelated** — surfaced by search but doesn't actually apply

**5. Recommend one decision**
Pick exactly one:
- **REUSE** — an exact match exists; use it as-is
- **EXTEND** — a partial match exists; add to it rather than duplicating
- **MERGE** — multiple overlapping/conflicting assets exist; they should be
  consolidated (describe how)
- **CREATE** — nothing usable exists; safe to build new
- **STOP** — evidence is inconclusive or conflicting enough that a human should decide
  before anyone builds or reuses anything

**6. Report evidence and canonical location**
State exactly which matches drove the recommendation, and suggest the canonical
location/name the asset should live at or be referenced from going forward.

## Output Format

```
# Asset Discovery Report: [proposed asset]

## Request understood as
[one-line restatement + likely synonyms searched]

## Searched
- [location]: [searched / not searched — why]
...

## Findings
| Asset | Location | Classification | Notes |
|---|---|---|---|
| ... | ... | exact/partial/obsolete/conflicting/unrelated | ... |

## Recommendation: [REUSE / EXTEND / MERGE / CREATE / STOP]
[evidence-based justification, 2-4 sentences]

**Suggested canonical location:** [path or name]

## Unsearched / Unknown
[any directories, repos, or systems that could not be checked — e.g. "no DB connector
available; database itself not directly queried, only code references checked"]
```

## Notes

- Never create, edit, or delete files, tables, or skills as part of this workflow —
  report only. If the person wants the recommendation acted on, that's a separate,
  explicit follow-up request.
- Never run write/DDL SQL. Read-only `SELECT` against `information_schema` or catalog
  views only.
- Known limitation: `allowed-tools`' `Bash(psql *)` pattern matches on command text, not SQL
  semantics — it cannot technically distinguish a read-only `SELECT` from a destructive
  statement passed via `-c`/`--command`. The SELECT-only rule above is enforced by this
  instruction, not by the tool scoping itself.
- If a system genuinely can't be searched (no access, no tool, no connector), say so
  plainly in the report rather than omitting it or implying coverage.
- Prefer functional/synonym search over exact-name search — most duplicates get built
  because they were named differently, not because no one looked at all.
- Keep the report evidence-based: cite the actual file paths, table names, or skill
  names found, not general impressions.
- Clickable-question convention: this skill has exactly one user-facing question (the
  Input section's clarifying question), and it's genuine free text with no finite set of
  good answers, so no `AskUserQuestion` conversion applies here.
