---
name: knowledge-management
version: 1.2.0
author: Ashay Kubal @ Qball Inc.
description: "Use when PERFORMING knowledge actions: capturing decisions, searching the knowledge base, or creating knowledge entries."
when_to_use: "Invoke for create/search/update/delete operations on the knowledge base. Do NOT load for passive knowledge queries (what exists, reading entries directly) — those are better served by direct file reads."
argument-hint: "[show|search|create|update|link|deprecate|supersede|delete|status] [entry-id]"
tags: knowledge, decisions, patterns, search
allowed-tools: Read, Bash, Glob, Grep
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Knowledge Management Skill

## Purpose

This skill provides guidance for Claude on managing persistent project knowledge in the CLEAR framework. It covers capturing decisions, searching the knowledge base, viewing entries, managing lifecycle (linking, deprecation, supersession, update, deletion), and understanding automatic knowledge hooks.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op. Reference files are left unchanged.

## Command Reference

All CLIs at `$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/`. Run with `--clear-dir=./.clear`.

| Action | CLI Command |
|--------|-------------|
| Create new entry | `capture-cli --create --type=<type> --title="..." --description="..."` |
| Update entry fields (tags, description) | `capture-cli --update --id=<id> --tags="..." --description="..."` |
| Change entry type (regenerates ID) | `capture-cli --update --id=<id> --type=<new-type>` |
| Add file link to entry | `capture-cli --update --id=<id> --add-related-file=<path>` |
| Search knowledge base | `search-cli --query="..."` |
| Show entry details | `show-cli --id=<id>` |
| Knowledge base overview | `status-cli` |
| Link entry to workpackage | `link-cli link <id> --to=<wp-id>` |
| Unlink from workpackage | `link-cli unlink <id>` |
| Deprecate entry | `deprecate-cli <id> --reason="..."` |
| Supersede entry | `supersede-cli <old-id> <new-id>` |
| Delete entry | `delete-cli <id> --reason="..." --force` |
| Rebuild search index | `index-cli --mode=full --force` |
| Incremental index update | `index-cli --mode=incremental` |
| File-to-entry lookup | `file-index-cli --lookup=<path>` |
| Rebuild file index | `file-index-cli --rebuild` |

> **Key distinction:** `link-cli` manages **workpackage associations** only. To add **file links** (`related_files`), use `capture-cli --update --add-related-file`.

## When to Take Action vs. Just Answer

### TAKE ACTION (run CLIs) when user says:
- "capture this decision" / "save this as a technical decision" → `/cf-knowledge create` or `capture-cli --create`
- "search knowledge for X" / "find what we decided about X" → `search-cli --query=X`
- "show me TD-001" → `/cf-knowledge TD-001` or `/cf-knowledge show TD-001`
- "create a business rule for X" → `capture-cli --create --type=business-rule`
- "rebuild the knowledge index" → `index-cli --mode=full --force`
- "link TD-001 to WP-P3.2" → `/cf-knowledge link TD-001 --to=P3.2`
- "deprecate LES-003" → `/cf-knowledge deprecate LES-003 --reason="..."`
- "update TD-001 tags" → `/cf-knowledge update TD-001 --tags=new-tag1,new-tag2`
- "delete LES-003" → `/cf-knowledge delete LES-003 --reason="..." --force`
- "knowledge status" → `/cf-knowledge status`

### JUST READ FILES (no CLIs) when user asks:
- "what decisions have we made?" → Read entries in `.clear/knowledge/entries/`
- "list all patterns" → Grep for `type: architectural-pattern` in `.clear/knowledge/entries/`
- "do we have any knowledge about X?" → Grep `.clear/knowledge/entries/` for keywords

**Do NOT use Write or Edit on `.clear/` files.** All mutations go through CLIs, which use `fs.writeFileSync` (invisible to the PreToolUse guard).

## Knowledge Types

| Type | ID Prefix | `--type` flag value | Use for |
|------|-----------|---------------------|---------|
| Technical Decision | TD-XXX | `technical-decision` | Architectural / tech-stack choices made by the project team |
| Business Rule | BR-XXX | `business-rule` | Mandatory invariants, prohibitions, validation requirements |
| Architectural Pattern | PAT-XXX | `architectural-pattern` | Reusable design patterns the project applies |
| Lesson Learned | LES-XXX | `lesson-learned` | Insights from past mistakes / hindsight reflections |
| Institutional Wiki | IW-XXX | `institutional-wiki` | External standards, regulations, reference docs |
| Stakeholder | SH-XXX | `stakeholder` | People / teams / orgs involved with the project |
| Process | PROC-XXX | `process` | Recurring workflows, runbooks, procedural guides |

All entries are stored in `.clear/knowledge/entries/` (flat directory, no subdirectories).

The SQLite search index is at `.clear/knowledge/index.db`.

## Entry Statuses

| Status | Meaning | Surfaced in hooks? | Appears in index? |
|--------|---------|--------------------|--------------------|
| `active` | Current, valid entry | Yes | Yes |
| `pending` | Newly created, not yet validated | No | No |
| `deprecated` | Stale, no longer applicable | No | No |
| `superseded` | Replaced by another entry | No | No |
| `archived` | Retained for history | No | No |

New entries created via `capture-cli --create` start as `active`. Use `pending` status when an entry needs review before surfacing (e.g., auto-extracted entries). Pending and deprecated entries are excluded from the file-knowledge-index and load-cli output.

## Unified Entry Point: `/cf-knowledge`

The `/cf-knowledge` command routes to all knowledge subcommands via `router.ts`:

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/router.js" \
  <subcommand> [args] --clear-dir=./.clear
```

**Available subcommands:**

| Subcommand | Purpose | Example |
|------------|---------|---------|
| `status` | Knowledge base overview (default) | `/cf-knowledge status` |
| `show` | Display entry details | `/cf-knowledge show TD-001` |
| `link` | Link entry to workpackage | `/cf-knowledge link TD-001 --to=P3.2` |
| `unlink` | Unlink entry from workpackage | `/cf-knowledge unlink TD-001` |
| `deprecate` | Deprecate an entry | `/cf-knowledge deprecate TD-001 --reason="..."` |
| `supersede` | Replace one entry with another | `/cf-knowledge supersede TD-001 TD-005` |
| `update` | Update entry metadata (or type-change with `--type`) | `/cf-knowledge update TD-001 --tags=...` |
| `delete` | Delete an entry | `/cf-knowledge delete LES-003 --reason="..." --force` |

**Direct ID shorthand:** `/cf-knowledge TD-001` is equivalent to `/cf-knowledge show TD-001`.

## CLI Reference

All CLIs are at `$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/`. Always run with `--help` first if unsure about flags.

### capture-cli — Create and Update Knowledge Entries

```bash
# Create a new entry
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/capture-cli.js" \
  --clear-dir=./.clear \
  --create \
  --title="<Decision Title>" \
  --type=technical-decision \
  --tags="tag1,tag2,tag3" \
  --description="<Brief description>" \
  --session=<session-number>

# Update an existing entry
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/capture-cli.js" \
  --clear-dir=./.clear \
  --update \
  --id=<entry-id> \
  --tags="new-tag1,new-tag2" \
  --description="Updated description" \
  --add-related-file="src/auth/middleware.js" \
  --session=<session-number> \
  --workpackage=<workpackage-id>
```

**Create modes:** `--detect` (scan text for capture triggers), `--confirm` (process user confirmation), `--create` (direct creation), `--check-state` (check pending capture).

**Create flags:** `--title`, `--type`, `--tags`, `--description`, `--session`, `--supersedes=<id>` (mark as superseding another), `--workpackage=<id>` (auto-link to workpackage after creation).

**Institutional-wiki (`--type=institutional-wiki`) flags:** `--source=<string>` (canonical external citation, e.g., "ISO 27001:2022"), `--source-updated=<date>` (when the source was last revised), `--scope=<string>` (one-line statement of what this entry covers). Stored as frontmatter and surfaced in the body template's Source/Scope/Content sections. Silently ignored on non-IW types.

**Process (`--type=process`) flags:** `--trigger-event=<string>` (the event that initiates the process, e.g., `"session-start"`, `"deploy-trigger"`), `--frequency=<string>` (execution cadence, e.g., `"weekly"`, `"on-demand"`, `"every release"`), `--tools=<string>` (tools/commands used, e.g., `"just, jq, gh"`), `--automation-hook=<string>` (reference to an automation entrypoint, e.g., a script path). Stored as frontmatter and surfaced in the body template's Trigger / Prerequisites / Steps / Verification sections. Silently ignored on non-PROC types. A fifth PROC frontmatter field — `promotion_status` — is reserved for the process-to-skill promotion lifecycle; no CLI flag is plumbed at create time, and the field stays null until promotion runs.

**Stakeholder (`--type=stakeholder`) flags:** `--entity-type=<string>` (**REQUIRED** at CLI boundary; e.g., `"team"`, `"individual"`, `"org"`, `"role"` — `createEntry` rejects SH creation with a `status:error` envelope when omitted, mirroring the title+type cross-context gate), `--role=<string>` (e.g., `"Platform Lead"`, `"On-call rotation"`), `--owns=<path,path,...>` (comma-separated relative paths the stakeholder owns; trim + filter empty; absolute paths and `..` traversal rejected — same rule as `--add-related-file=`), `--contact=<string>` (e.g., `"#payments-oncall"`, `"team@example.com"`). Stored as frontmatter and surfaced in the body template's Entity / Role / Owns / Contact sections. Triggers lazy `buildOwnerIndex()` after the first SH entry create — `.clear/state/owner-index.json` maps `owns` paths to SH entry IDs and is consulted by PreToolUse alongside the file-knowledge-index. Silently ignored on non-SH types.

**Audit + observability flags:** `--via=<mode>` declares the capture origin (modes: `direct_create | pattern_detected | extraction | bulk`; default `direct_create` applied at audit-emit time). `--matched-pattern=<description>` echoes the `CapturePatternDef.description` string when the entry was triggered by a YAML capture pattern (used by daemon/curation tools to attribute fires to specific patterns). `--session-id=<guid>` and `--session-number=<n>` together enable canonical audit-log emission to `.clear/audit/session_N.jsonl` for create operations — the production hook chain (`scripts/knowledge/knowledge-capture.sh`) reads these from `.clear/state/session.json` automatically; direct CLI users supply them explicitly. If either is absent, audit emit is silently skipped (legacy `--session=<n>`-only path preserved). Decline / failure / state-expired events are written to `.clear/state/capture-pattern-log.jsonl` regardless of session flags — that surface is daemon-curated, not single-event audit.

**Update flags:** `--id=<id>` (required), `--tags=<comma-separated>`, `--description=<text>`, `--add-related-file=<path>` (repeatable), `--session=<number>`.

**Type-change (`--update --id=<id> --type=<new-type>`):** Pass `--type=` in update mode to reclassify an entry under a new type with regenerated ID. The old entry is preserved on disk with `status: superseded` and `superseded_by: NEW-NNN`; a new entry is created at `NEW-NNN.md` with the body copied verbatim and `supersedes: OLD-NNN`. All third-party entries that referenced the old ID via `supersedes` or `superseded_by` are cascaded to the new ID — the cascade is mandatory. Type-change emits a `'supersede'` audit row (from the unified supersession primitive) plus a `'update'` audit row with `metadata.operation: 'type-change'` so queries can filter type-changes specifically. Type-change to `stakeholder` requires `--entity-type=...` at the CLI boundary (mirrors the create-time SH gate). Type-change is rejected on entries already `superseded` or `deprecated`, or when the new type matches the current type. The return JSON has `oldId`, `newId`, `action: 'type-change'`, and `cascadedRefs` at the top level.

Output is JSON. Parse to confirm success and extract the entry ID and file path.

### Tagging Guidelines

Tags are the primary search signal (P1 exact match). Poor tagging forces multiple search passes. Follow these rules for every capture and update operation.

**MANDATORY: Every entry MUST have at least one domain tag and one specific tag.**

#### Tag Tiers

1. **Domain tags** (REQUIRED — at least 1)
   Broadest category the entry belongs to. Enables "show me everything about X" queries.
   Examples: `database`, `ipc`, `ui`, `packaging`, `testing`, `auth`, `config`, `build`

2. **Specific tags** (REQUIRED — at least 1)
   Precise technology, library, or concept. Enables targeted lookup.
   Examples: `better-sqlite3`, `electron-rebuild`, `wal`, `vite`, `nsis`

3. **Architectural tags** (when applicable)
   Cross-cutting concerns. Enables "show me all performance decisions" queries.
   Examples: `architecture`, `performance`, `error-handling`, `security`, `scalability`

4. **Project-scoped tags** (when applicable)
   Project components or structure. Enables "show me all task-service knowledge."
   Examples: `task-service`, `settings-service`, `poll-engine`, `phase-1`

5. **Lifecycle tags** (when applicable)
   Nature of the decision. Enables "what did we defer?" queries.
   Examples: `deferred`, `workaround`, `constraint`, `migration`, `deprecated`

#### Rules

- Minimum 2 tags per entry (1 domain + 1 specific)
- Use lowercase, hyphenated format (e.g., `error-handling`, not `Error Handling`)
- Prefer existing tags over inventing new ones — check `/cf-knowledge status` for established tags before creating synonyms
- When unsure about domain tag, ask: "If someone searched for everything about this topic, what single word would they use?"

**Edge-case exception:** If a genuine outlier makes 2-tag compliance impossible (e.g., highly cross-cutting or generalised entry), use the closest available tags and note the exception in the entry description. Do NOT stall on tagging — proceed with the best available pairing rather than ask the user mid-capture, unless the entry's domain is so ambiguous that no defensible tags exist.

### delete-cli — Delete a Knowledge Entry

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/delete-cli.js" \
  <entry-id> --reason="<reason>" --clear-dir=./.clear
```

**Flags:**
- `--reason=<text>` — Reason for deletion (required)
- `--force` — Skip confirmation for active entries
- `--clear-dir=<path>` — Path to .clear directory (required)

Shows impact analysis (linked WPs, supersession chains, related entries) before deletion. Without `--force`, active entries require explicit confirmation.

### search-cli — Search Knowledge Base

```bash
# Search by query
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/search-cli.js" \
  --clear-dir=./.clear \
  --query="authentication approach"

# Detect search intent in user text
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/search-cli.js" \
  --clear-dir=./.clear \
  --detect-only --text="what did we decide about caching"
```

Uses 3-pass search: P1 (tag exact match), P2 (title keyword), P3 (TF-IDF cosine similarity). Flags: `--max-results=<n>`, `--include-superseded`.

### show-cli — Display Entry Details

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/show-cli.js" \
  --clear-dir=./.clear --id=TD-001
```

### load-cli — Load Knowledge at Session Start

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/load-cli.js" \
  --clear-dir=./.clear \
  --level=balanced \
  --context="auth,security" \
  --workpackage=P3.2
```

Levels: `minimal`, `balanced`, `comprehensive`. Ranks entries by relevance score (active status, tag matches, recency, type).

### index-cli — Rebuild Knowledge Index

```bash
# Full rebuild
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/index-cli.js" \
  --clear-dir=./.clear --mode=full --force

# Incremental update
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/index-cli.js" \
  --clear-dir=./.clear --mode=incremental
```

Rebuilds the SQLite search index (`.clear/knowledge/index.db`). The index is automatically rebuilt inline after every `--create` and `--update` operation. Manual rebuild is only needed after direct file edits or if search results seem stale.

### link-cli — Link Entry to Workpackage

```bash
# Link
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/link-cli.js" \
  link TD-001 --to=P3.2 --clear-dir=./.clear

# Unlink
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/link-cli.js" \
  unlink TD-001 --clear-dir=./.clear
```

### deprecate-cli — Deprecate an Entry

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/deprecate-cli.js" \
  TD-001 --reason="Superseded by new approach" --clear-dir=./.clear
```

Shows impact analysis (linked WPs, supersession chains) before proceeding. Use `--force` to skip confirmation.

### supersede-cli — Replace One Entry with Another

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/supersede-cli.js" \
  TD-001 TD-005 --clear-dir=./.clear
```

Marks old entry as superseded, links both entries. Use `--force` to skip chain depth validation.

### status-cli — Knowledge Base Overview

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/status-cli.js" \
  --clear-dir=./.clear
```

Shows entry counts by status/type, recent activity, index health, and supersession chains.

### file-index-cli — File-to-Knowledge Index

```bash
# Rebuild reverse index
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/file-index-cli.js" \
  --rebuild --clear-dir=./.clear

# Look up entries linked to a file
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/file-index-cli.js" \
  --lookup=src/auth/middleware.js --clear-dir=./.clear

# Update index for a specific entry
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/knowledge/cli/file-index-cli.js" \
  --update=TD-001 --clear-dir=./.clear
```

## Automatic Knowledge Hooks

These run without user action:

| Hook Event | Script | What It Does |
|------------|--------|--------------|
| SessionStart | `knowledge-load.sh` | Loads top N entries by relevance via `load-cli`. Also drains pending index updates via `knowledge-drain.sh` |
| UserPromptSubmit | `knowledge-search.sh` | Pattern-matches prompts for search intent, runs `search-cli` |
| UserPromptSubmit | `knowledge-capture.sh` | Detects decision/pattern/lesson phrases, starts multi-turn capture |
| PreToolUse | `pre-tool.sh` | Looks up edited file in `file-knowledge-index.json`, surfaces linked entries |
| PostToolUse | `post-tool.sh` | After Write/Edit, surfaces linked entries for review |
| PreCompact | `session-precompact.sh` | Drains pending index updates via `knowledge-drain.sh` before context compaction |
| Stop | `session-stop.sh` | 3-tier knowledge assessment: Level A (deterministic path match), Level B (`change-pattern-cli` evaluation), Level C (threshold-based capture prompt when >=3 files changed without A/B match). Prompts capture when modified files are knowledge-relevant |

**Internal helpers** (not user-facing):
- `knowledge-drain.sh` — Shared function that drains pending index updates (marker-file fallback recovery). Called by `knowledge-load.sh` at session start and `session-precompact.sh` at PreCompact.
- `change-pattern-cli` — Evaluates changed files against knowledge patterns for Level B assessment in the Stop hook.

## Token Efficiency

**Decision framework for load-level selection:**

- Session start with no specific WP context → `load-cli --level=minimal` (top-N relevance-ranked summaries only)
- Active WP work or focused investigation → `load-cli --level=balanced` (default — summaries + recent activity)
- Deep cross-cutting investigation or audit work → `load-cli --level=comprehensive` (full bodies for top entries)
- Quote a single entry's full body → `show-cli --id=<id>` (do not re-load the whole base)

**Budget allocation reference:**

- Per-entry summary (hook surfacing / load-cli minimal): ~0.5% of context
- Per full entry (show-cli or load-cli comprehensive): ~2-5%
- Target total knowledge load: <10% of session budget — if approaching this, prefer minimal + targeted show-cli over comprehensive load
