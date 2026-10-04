---
name: context-recall
description: >
  Retrieve full pre-compaction conversation history from saved transcript
  files when the compact summary is insufficient or earlier session details
  are missing. Use when asked about past decisions, tool results, or content
  that predates the latest compaction; when the agent would say it does not
  remember; or when the compact summary's Context recovery / fallback note
  names a transcript path. Triggers: "what did we discuss earlier", "before
  the context was reset", "older messages", "pre-compaction", "context
  recall", "recover history", "컴팩션 이전 대화", "과거 히스토리",
  "예전에 뭐라고 했지".
---

# Context Recall

Compaction already saves transcripts on disk. Prefer those files over guessing
or redoing work. This skill complements the compact summary's
`### Context recovery` suffix — it does not replace it.

## Workflow

### 1. Prefer an explicit path from the compact summary

- If `### Context recovery` names `.libragent/pre_compaction_epoch_{N}.md`,
  read that path with `workspace__readFile`.
- If a fallback note names
  `.libragent/tool-results/compaction/fallback-….md`, read that **exact**
  path. Those files live under internal `tool-results` and are **not**
  discoverable via `listDirectory` / `globFiles` — do not try to browse for
  them.

### 2. Otherwise discover epoch transcripts

```
workspace__globFiles(path=".libragent", filePattern="pre_compaction_epoch_*.md")
```

or `workspace__listDirectory(path=".libragent")`.

Epoch numbers are **monotonic** (`1`, `2`, `3`, …). Retention keeps only the
newest ~3 files, so `pre_compaction_epoch_1.md` may already be gone. Always
read the **highest N** first (most recent compaction).

### 3. Read concrete paths only

```
workspace__readFile(path=".libragent/pre_compaction_epoch_{N}.md")
```

Never pass globs to `workspace__readFile`. Read older epochs only if the
newest file is insufficient.

## What's Inside

Each epoch file is Markdown with:

- `# Pre-compaction Transcript` header and session id
- `---\n[timestamp] ROLE` separators
- User/assistant text (truncated ~1500 bytes per block)
- Thinking blocks (truncated ~1500 bytes)
- `[TOOL CALL] name(args)` lines — **not** tool result bodies

For tool outputs, inspect workspace files those tools wrote (or other session
artifacts). Do not expect result payloads inside the epoch file.

## Do Not

- Hard-code `epoch_1` / `epoch_2` — discover first, then pick highest N
- Pass wildcards to `workspace__readFile`
- Assume fallback paths under `.libragent/tool-results/` are listable
- Re-research from scratch when an epoch file exists
- Answer "I don't remember" when an epoch or fallback path is available
