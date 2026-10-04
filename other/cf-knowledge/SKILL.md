---
name: cf-knowledge
version: 1.1.0
author: Ashay Kubal @ Qball Inc.
description: Manage the CLEAR knowledge base — search, view, capture, index, link, deprecate, and supersede entries. Use when the user asks about knowledge base entries, wants to capture a decision or lesson, search for patterns, or manage entry lifecycle.
user-invocable: true
argument-hint: "[subcommand|help] [id] [options]"
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Knowledge Management

Manage the CLEAR knowledge base: search, view, capture, index, link, deprecate, and supersede entries.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op. Reference files are left unchanged.

## When to Use This Skill

| Trigger | Examples |
|---------|---------|
| View overview | "Show me the knowledge base status", "What's in the KB?" |
| Search or find entries | "Search knowledge for caching pattern", "Find decisions about auth" |
| View entry details | "Show me TD-015", "What does LES-003 say?" |
| Load into context | "Load knowledge for this workpackage" |
| Rebuild index | "Rebuild the knowledge index", "Reindex knowledge" |
| Capture knowledge | "Capture this decision", "Save this as a lesson learned" |
| Deprecate an entry | "Deprecate PAT-003", "This pattern is outdated" |
| Link or unlink | "Link TD-012 to WP-04", "Unlink LES-001" |
| Supersede an entry | "TD-005 replaces TD-002", "Supersede PAT-001 with PAT-007" |

**Not for:** Project status (`/cf-status`), workpackage ops (`/cf-workpackage`), debug (`/cf-debug`).

---

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

> **Key distinction:** `link-cli` manages **workpackage associations** only.
> To add **file links** (`related_files`) to a knowledge entry, use the
> `capture-cli` update path with the `add-related-file` option.

---

## Pre-Flight Check

```bash
if [ ! -d ".clear" ]; then
  echo "ERROR: CLEAR not initialized. Run /cf-init first." >&2
  exit 1
fi
```

---

## Subcommand Table

| Subcommand | Type | Reference File | Intent Signals |
|------------|------|----------------|----------------|
| `search` | [R] | `references/search.md` | "search", "find", "look for" |
| `show` | [R] | `references/show.md` | "show", "details", "what does X say" |
| `load` | [R] | `references/load.md` | "load", "load knowledge", "bring in context" |
| `index` | [R] | `references/index.md` | "index", "reindex", "rebuild index" |
| `help` | [R] | `references/help.md` | "help", "how do I", "usage" |
| `capture` | [W] | `references/capture.md` | "capture", "save", "record this decision", "lesson learned" |
| `deprecate` | [W] | `references/deprecate.md` | "deprecate", "outdated", "no longer valid" |
| `dismiss` | [W] | `references/dismiss.md` | "dismiss deprecation", "acknowledge deprecation", "skip-replacement" |
| `ack` | [W] | `references/ack.md` | "ack", "acknowledge", "mark reviewed", "clear pending-review", "I've seen it" |
| `link` | [W] | `references/link.md` | "link", "associate", "connect to WP" |
| `unlink` | [W] | `references/unlink.md` | "unlink", "disconnect", "remove link" |
| `supersede` | [W] | `references/supersede.md` | "supersede", "replace", "X replaces Y" |

---

## Routing

Follow these steps **in order**. Track which step you reached — this determines whether confirmation is needed.

**Step 1 — Check `$ARGUMENTS` for an explicit subcommand.**
Check whether `$ARGUMENTS` literally starts with one of the subcommand keywords from the table above (e.g., `capture`, `search`, `deprecate`). This is a string match, not intent inference.
- If YES: load `references/{subcommand}.md`, pass remaining arguments. **Done — skip steps 2-4.**
- If NO (empty, missing, or does not start with a table keyword): continue to step 2.

**Step 2 — Infer intent from the user's natural language message.**
`$ARGUMENTS` did not contain an explicit subcommand. Determine which subcommand best matches the user's intent from their message. Use the subcommand table's intent signals, the "When to Use" examples, and the conversation context.
- If you can identify a specific subcommand with reasonable confidence: continue to step 3.
- If the user's message is purely a status or overview inquiry with no action intent (e.g., "show me the knowledge base status"): load `references/default.md`. **Done.** Only use this exit if the message contains no entity identifiers (entry ID, WP ID) and expresses no specific action intent.
- If you cannot determine intent with reasonable confidence: go to step 4.

**Step 3 — Confirm before write actions (NL-inferred only).**
You reached this step via intent inference (step 2), not explicit arguments (step 1).
- If the inferred subcommand is a **read** action ([R] in the table): load the reference file immediately.
- If the inferred subcommand is a **write** action ([W] in the table): **you MUST confirm before proceeding.** Ask: "I'll run **{subcommand}**{details}. Proceed?" where `{details}` includes the target identifier (e.g., " on TD-015", " superseding TD-002 with PAT-007"). For destructive actions (deprecate, supersede, delete), always include the target ID. Wait for the user's response. Only load the reference file after the user confirms.

**Step 4 — Ambiguity fallback.**
Ask the user: "I matched `/cf-knowledge` but I'm not sure which action you want. Did you mean: {top 2-3 candidates}?" Do NOT silently fall through to `default`.

---

## Error Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Invalid usage or missing arguments |
| 2 | Knowledge entry not found |
| 3 | Invalid operation (e.g., deprecate already deprecated) |
| 4 | Chain depth exceeded |
| 5 | Validation failed |

---

## Completion Checklist

- [ ] Pre-flight passed
- [ ] Correct reference loaded and executed
- [ ] Exit code 0, output displayed
