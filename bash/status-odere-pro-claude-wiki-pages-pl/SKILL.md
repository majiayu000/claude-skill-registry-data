---
name: status
description: >
  One-command health check. Exercises every hook path and reports pass/fail
  per hook — without writing to vault/. Trigger when the user says "status",
  "health check", "is everything wired up", "did the install work",
  "dashboard", or invokes /claude-wiki-pages:status directly. Strictly
  read-only against vault content; any accidental write is the skill's own
  bug.
allowed-tools: Read Bash Glob Grep
---

# LLM Wiki — Status

Confirm every piece of Layer 4 orchestration is wired and fires. Leave the
vault exactly as you found it.

This skill answers the question: "If I ran the pipeline right now, which
hooks would fire and which would silently skip?"

## When to invoke

- Immediately after installing the plugin — verify the install.
- After editing hooks or scripts — verify the edit.
- When the user suspects a hook is not firing (e.g., frontmatter violations
  slip through).
- Periodically, as a smoke test.

## Reading contract

- `hooks/hooks.json` — the hook wiring manifest.
- Every script referenced from `hooks/hooks.json` — confirm executable, valid
  shell, returns expected exit codes for synthetic inputs.
- `vault/CLAUDE.md` — the schema, to construct valid and invalid test
  payloads.
- The user's project tree — only to determine the vault path; never its
  contents.

## Writing contract

Zero writes to `vault/`. Specifically:

- No log append (this skill is a diagnostic; logging health checks clutters
  the log).
- No scratch files under `vault/`.
- Transient test payloads may be constructed in a tempdir outside `vault/`
  (e.g., `$TMPDIR`) and must be removed before the skill returns.

The skill enforces its own non-mutation invariant: compare `git status
vault/` (or a checksum of `vault/`) before and after; any diff is a skill
bug and must be surfaced as a FAIL.

## Workflow

Run these checks in order. Each produces one line in the report.

1. **Dependency check.** `jq`, `bash >= 3.2`, every hook script readable and
   executable.
2. **`SessionStart` preamble.** Synthesize a session open; confirm the
   schema-reminder preamble is printed.
3. **`PreToolUse` frontmatter gate.** Attempt a synthetic Write with
   malformed frontmatter; confirm exit code 2.
4. **`PreToolUse` raw-immutability gate.** Attempt a synthetic Write under
   `vault/raw/`; confirm exit code 2.
5. **`PreToolUse` wikilink gate.** Attempt a synthetic Write that uses a
   markdown link where a wikilink is required; confirm exit code 2.
6. **`PreToolUse` attachment gate.** Attempt a synthetic source-page Write
   with a missing `attachment_path`; confirm exit code 2.
7. **`PostToolUse` reminder.** Perform a read-only synthesis of a wiki write;
   confirm the index-reminder message appears.
8. **`SubagentStop` ingest gate.** Simulate the completion of an ingest
   agent; confirm `verify-ingest.sh` runs.
9. **`SubagentStop` lint gate.** Simulate the completion of a lint-fix
   agent; confirm the lint gate runs.
10. **Schema read.** Confirm `vault/CLAUDE.md` parses as YAML frontmatter
    - markdown, `schema_version` is an integer, and the plugin supports it.

## Report format

```
STATUS — <YYYY-MM-DD> — vault: <path>

  [  OK ] dependency check
  [  OK ] SessionStart preamble
  [ FAIL ] PreToolUse frontmatter gate — <reason>
  ...

Summary: <N passed> / <N total>. No wiki writes.
```

Exit codes:

- `0` — every line `OK`.
- `1` — any FAIL.
- `2` — skill self-invariant violated (vault was mutated).

## Completion signal

On full pass:

```
READY: all <N> hook paths green. Vault unchanged.
```

On any failure:

```
FAILED: <N>/<M> hook paths failing. See report above.
```
