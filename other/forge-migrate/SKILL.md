---
name: forge-migrate
description: Use when upgrading forge-skills across a major version (e.g., from v2.x or v3.0/3.1 to v3.2+), when .forge/ artifacts exist but lack forge:meta headers, when forge-sync reports a wall of "untracked" rows, or when the user asks "why doesn't sync see my existing files".
---

# forge-migrate

## Overview

Backfill `forge:meta` headers onto pre-existing `.forge/` artifacts so they enter the dependency tracking system. Reads filenames against the canonical artifact table in `references/forge-dependency-graph.md` to infer `generated_by` and `depends_on`. Sets `generated_at` to the file's mtime (UTC), and computes `content_hash` from the current contents. Read-then-write only — never regenerates an artifact, just annotates what's already there.

## When to Use

- Upgrading from a pre-3.2.0 forge-skills release where `.forge/` artifacts had no headers
- `forge-sync` reports every artifact as "untracked" / "no header"
- A teammate without the plugin produced `.forge/` files on a shared branch and you want them tracked
- Need to bring legacy artifacts under the dependency graph without re-running expensive skills (interviews, audits)

## When NOT to Use

- The artifact is genuinely stale and should be regenerated — use the source skill instead (e.g., `/spec` to refresh `prd.md` rather than back-stamping it)
- `.forge/` doesn't exist — there's nothing to migrate
- All artifacts already have valid `forge:meta` headers — `forge-sync` will tell you this; migration is a no-op
- The file isn't on the canonical artifact list — don't invent dependencies for ad-hoc files

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll just re-run every skill to get fresh headers" | Forces re-interview and re-audit — burns hours when a 30-second backfill is correct |
| "The files work without headers" | They work for reading. They break for `forge-sync`, `/forge-migrate` itself, and downstream staleness detection. |
| "I'll write the headers by hand" | Hand-written headers drift from the schema. The skill enforces UTC, hash format, dependency inference. |
| "Use today's timestamp — it's close enough" | Today's timestamp tells `forge-sync` the artifact is newer than its upstream. False UP_TO_DATE. Use the file's mtime. |
| "All artifacts depend on prd.md, just list that" | Inferring `depends_on` from the canonical graph keeps cascade rules correct. Don't fabricate dependencies. |

## Red Flags

- A migrated artifact has `generated_at` set to `now` instead of file mtime
- `generated_at` is local time instead of UTC with `Z` suffix
- `content_hash` is missing or not 8 hex chars
- A file not on the canonical artifact list received a fabricated `generated_by`
- The skill regenerated content instead of just adding a header

## Core Process

### Step 1: Scan `.forge/` for unheadered files

For every file under `.forge/` (recursively):
- Read the first ~30 lines.
- If a `<!-- forge:meta -->` block (or `# forge:meta` for YAML) is present and well-formed → skip, already tracked.
- If absent or malformed → candidate for migration.

If `.forge/` doesn't exist, exit: "Nothing to migrate."

### Step 2: Match each candidate against the canonical graph

Read `references/forge-dependency-graph.md`. Look up each candidate's filename in the "Artifact-producing skills" table to recover:
- `generated_by` (the skill that owns this filename)
- `depends_on` (the canonical upstream set)

For unmatched files (not on the canonical list), do NOT fabricate a header. Report them under "unmatched — manual review" and move on. Common cases: ad-hoc notes, half-finished drafts, project-specific extensions.

For globbed outputs (`contracts/*.md`, `adr/*.md`, `redacted/*`), every file in the directory inherits the parent skill's `depends_on`.

### Step 3: Compute metadata per file

For each matched candidate:
- `generated_at`: read the file's mtime via `stat`; convert to ISO 8601 UTC with `Z` suffix (e.g., `2026-05-12T14:30:00Z`). If mtime is unavailable, fall back to "now" UTC and flag for user awareness.
- `content_hash`: sha256 over the entire current file body; take the first 8 hex chars.
- `depends_on`: from Step 2.
- `generated_by`: from Step 2.

### Step 4: Confirm with the user before writing

Present the proposed migration plan:

```
3 files will receive backfilled headers:

  .forge/prd.md
    generated_by: spec-driven-development
    generated_at:  2026-04-22T09:15:00Z (file mtime)
    depends_on:    [.forge/idea-brief.md]
    content_hash:  3f9a2b1c

  .forge/architecture.md
    ...

  .forge/contracts/auth-service.md
    ...

1 file will NOT be migrated (unmatched):

  .forge/scratch-notes.md  — not in canonical artifact table

Proceed? Y/n
```

Do not write until confirmed. Migration is structurally non-destructive, but the user's confirmation is the chain-of-custody event.

### Step 5: Prepend headers

For each confirmed file, prepend the `forge:meta` block at the top. For Markdown, use the HTML comment form. For YAML, use the `# forge:meta` indented form. Do NOT modify any other content.

After writing, verify by re-reading the first lines and confirming the block parses.

### Step 6: Report

Print a summary:

```
Migrated 3 files. Unmatched: 1 (.forge/scratch-notes.md — review and either add to canonical graph or delete).

Run /sync next to see the chain status with these new headers.
```

Recommend `/sync` as the natural follow-up — the user just installed headers; verifying the dependency chain is the immediate next step.

## Verification

- [ ] Every candidate file's `generated_at` is set to its mtime in UTC with `Z` suffix (not "now")
- [ ] Every `content_hash` is 8 hex chars, computed over the entire current file body
- [ ] `generated_by` for each migrated file matches an entry in the canonical artifact table
- [ ] `depends_on` for each migrated file matches the canonical graph (not fabricated)
- [ ] Files not on the canonical list are reported under "unmatched", not migrated with invented headers
- [ ] Glob outputs (`contracts/*.md`, `adr/*.md`) each got their own header
- [ ] User confirmed the migration plan before any file was written
- [ ] No artifact's body content was modified — only the header was prepended
- [ ] `/sync` recommended as next step
