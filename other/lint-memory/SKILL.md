---
name: lint-memory
type: standalone
version: 1.0.0
category: operations
description: Health check for the Claude memory system — finds orphans, dead links, contradictions, stale entries, and missing cross-references
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# /lint-memory

Memory health check. Finds problems, auto-fixes safe ones, flags the rest.

## What It Checks

1. **Dead links** — entries in MEMORY.md pointing to missing files
2. **Orphan files** — `.md` files in the memory directory not listed in MEMORY.md
3. **Contradictions** — same fact stated differently across files (e.g., two project statuses for same project)
4. **Stale project memories** — project status not updated in 30+ days
5. **Missing cross-links** — two memories that reference the same topic but don't link each other

## Scope

Default: `{agency-root}/memory/` (global) + `{agency-root}/projects/{agency-root-slug}/memory/` (per-conversation).
The per-conversation slug is the agency root path with `/` and `.` replaced by `-`
(e.g. `/home/ada/.claude` → `-home-ada--claude`) — derive it, never hardcode it.
Override: `/lint-memory [path]` to lint a specific directory.

Within a target directory, "in scope" excludes control/handoff filenames and
managed/log directories — defined once in `scripts/memory_scope.py`
(`EXCLUDE_NAMES` — next-session.md, decisions.md, heartbeat.md, .canary.md, etc.;
`EXCLUDE_DIRS` — sessions/, qa/, tasks/, inter-spawn-tasks/, agents/, outputs/) —
rather than restated inline here or duplicated per-script.

## Steps

### Step 1 — Read Indexes
Read `MEMORY.md` in each target directory. Parse all `[Title](file.md)` links.

### Step 2 — Check Dead Links
For each link in MEMORY.md: verify the file exists.
Auto-fix: remove entries for files that are missing (append `[DELETE YYYY-MM-DD]` to wiki-log.md).

### Step 3 — Check Orphans
List all `.md` files in the directory (excluding MEMORY.md, wiki-log.md, wiki-schema.md itself).
Flag files present on disk but absent from MEMORY.md.
Do NOT auto-delete orphans — present them for user review.

### Step 4 — Check Contradictions
For each memory file: extract key facts (project names, statuses, URLs, preferences).
Compare across files. Flag cases where the same entity appears with conflicting values.
Present contradictions for user resolution — never auto-resolve.

### Step 5 — Check Staleness
For project-type memories: check the file's last modification date (`git log` or `stat`).
Flag project memories not updated in 30+ days.

### Step 6 — Check Cross-Links
For memory files that share 2+ topic keywords (e.g., both mention "Acme Corp"):
Check if they contain `See also:` links to each other.
Suggest (but do not auto-add) missing cross-links.

### Step 6b — Check Graph God Nodes in Memory

Query the graphify MCP for the most-connected nodes:
```
mcp__graphify__god_nodes(top_n=20)
```

Filter results to nodes whose `source_file` contains `/.claude/memory/`. For each match
with `edge_count > 15`, flag it as a memory god node — a file doing too many jobs that
should be split into focused files.

If the graphify MCP is unavailable, skip this step silently.

### Step 7 — Report + Apply Safe Fixes

Output format:
```
MEMORY LINT — {date}

✅ {n} entries checked
❌ Dead links ({n}): [list] → auto-removed
⚠️  Orphan files ({n}): [list] → needs your review
⚠️  Contradictions ({n}): [list] → needs resolution
⚠️  Stale project memories ({n}): [list]
💡 Suggested cross-links ({n}): [list]
🔗 Graph god nodes in memory ({n}): [file (edges)] → consider splitting

Auto-applied: {n} fixes
Action needed: {n} items
```

### Step 8 — Update wiki-log.md
Append to `~/.claude/memory/wiki-log.md`:
```
[LINT YYYY-MM-DD] global — {n} dead links removed, {n} orphans found, {n} contradictions flagged, {n} god nodes flagged
```
