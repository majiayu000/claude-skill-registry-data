---
name: ck-create-note
description: "Record knowledge, decisions, and tickets in the knowledge base (the model can read and write it). Creates or updates a schema-valid entry and rebuilds the index. Run: /ck-create-note <what to record> — or /ck-create-note <TICKET-ID>."
disable-model-invocation: true
---

# ck-create-note

Writes ONE entry into the **knowledge folder** (`knowledge.path` from `.claude/contextkit/contextkit.config.json`, read/write) — the project's "second brain". Three types, one schema, one generated index.

> If `.claude/contextkit/` is missing (script or `contextkit.config.json` not found) →
> ContextKit is not installed here: stop, and install via `/ck-setup` in the hub.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

Paths in the config are relative to `$CK_ROOT`.

## Schema (frontmatter — required: `id`, `type`, `summary`)

```yaml
---
id: DEC-3
type: decision
status: accepted
summary: One sentence.
related: "[[DEC-1]]"
updated: 2026-01-01
---
```

- `id` — stable key, and the filename (`<id>.md`).
- `type` — `note`, `decision`, or `ticket` (or a type the project added).
- `status` — only for `decision` (`proposed`, `accepted`, `superseded`) and `ticket` (`open`, `done`).
- `summary` — one sentence, ≤120 characters. This is what the index shows.
- `related` — optional wikilinks. `updated` — optional date.

- **decision** → body as a light ADR: `## Context` · `## Decision` · `## Consequences`.
- **note** → a short free body (fact / background). No status.
- **ticket** → work in progress. With no argument, take the id from the branch (`ticketPattern`):
  ```bash
  CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
  git -C "$CK_ROOT" branch --show-current
  ```
  No match → ask. On **create** (`status: open`), record 3–6 testable criteria as `## Definition of Done` (a `- [ ]` checklist) — propose them from the context and check them with the user, so "done" is fixed before the work, contract-first. On **close** (`status: done`), check the list briefly: tick the open items, or mark them as dropped on purpose.
- Types and statuses are the **minimal default**. A project may extend them in the config (`schema.types` / `schema.status`) — for example `person` / `workflow` as first-class types with no status. They get their own section in the index.

## Flow

1. **Choose the id.** Decisions `DEC-<n>`, notes `NOTE-<slug>`, tickets = the ticket id. If `<id>.md` already exists → **update** it (body / status / `updated`).
2. **Check what is already there** — `/ck-read-note <topic>` or read `INDEX.md`. When a decision replaces an older one: set the old one to `status: superseded` and link it via `related`.
3. **Write the file** at `<knowledgePath>/<id>.md`. Keep the schema.
4. **Link it.** One capture rarely touches a single file. Set `related` here **and** add the back-link on the other entry (otherwise the graph sees the edge from one side only). Update affected person or ticket entries. Set a replaced decision to `status: superseded`. Prefer 2–3 consistent pages over one isolated atom.
5. **Lint + index + log** in one call (stops on schema errors, with no log line):
   ```bash
   CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
   python3 "$CK_ROOT/.claude/contextkit/scripts/knowledge.py" --sync <op> "<id> — <short topic>"
   ```
   `<op>` = `note` · `decision` · `ticket` (matching the entry type).
6. The knowledge base is **its own git repo** → commit the change (including `LOG.md`).

## Writing style (optimized for the model; a person does not read the index)

- Terse: one fact per line. No prose, filler, or repetition.
- Point, do not copy: `[[wiki-links]]`, `repo@sha`, `file:line`. No code blocks.
- Keep only what a later session or decision needs. Drop the rest.
