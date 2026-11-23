---
name: ck-read-note
description: "Look up project knowledge (notes, decisions, tickets) through the generated INDEX instead of reading every entry. Use it so earlier decisions are considered before a new one. Run: /ck-read-note <topic/question>"
disable-model-invocation: false
---

# ck-read-note

Answers questions from the **knowledge folder** (the "second brain") with few tokens: the index first, then only the matching entries. Never read the whole folder.

> If `.claude/contextkit/` is missing (script or `contextkit.config.json` not found) →
> ContextKit is not installed here: stop, and install via `/ck-setup` in the hub.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

Paths in `.claude/contextkit/contextkit.config.json` are relative to `$CK_ROOT`.

## Flow

1. **Read `INDEX.md`** (`$CK_ROOT/<knowledge.path>/INDEX.md`). One file is the whole map: each entry is `[[id]] (status) — summary`, grouped into Decisions / Notes / Tickets. If the index is missing or looks stale → `/ck-doctor` (it rebuilds the index).
2. **From the `summary` lines**, pick the 1–3 relevant entries. Open only those (`<knowledgePath>/<id>.md`). Follow `related` wikilinks at most 1 hop.
3. **Answer** with a pointer to `[[id]]`. For decisions, name the status (`superseded` → point at the successor via `related`).
4. **File the answer back when it is worth keeping.** If the answer was a non-trivial synthesis (a comparison, an analysis, a newly noticed link between several entries), suggest `/ck-create-note` — otherwise the work disappears into the chat. Questions then grow the knowledge base too, as well as new captures. Do not file a plain lookup (that is noise).
5. If the index has nothing on it, say so: not documented. If it should be recorded → suggest `/ck-create-note`.

`knowledge.path` comes from `.claude/contextkit/contextkit.config.json`. Before a **new decision**, always check here whether one already exists (including one that was superseded).
