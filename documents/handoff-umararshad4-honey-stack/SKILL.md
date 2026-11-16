---
name: handoff
description: "Write or restore a handoff doc so a fresh session can pick up this work."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills handoff (Codex copy); garrytan/gstack 1.60.1.0 context-save, context-restore; cursor/plugins pstack 0.15.25 recall"
---

# Handoff

A handoff carries this session's state to a fresh one. The next agent has none of this conversation, so the doc is everything it knows. Write it for a capable stranger who has the repo but not your memory.

Pick the branch from the argument:
- `handoff` or `handoff <focus>`: **Write**. A focus ("next: the billing ticket") tailors the doc to what the next session will do.
- `handoff restore` (or `resume`, `pickup`), optionally with a title fragment or path: **Restore**.

## Write

### 1. Gather state

Read it from the repo, not from memory: `git rev-parse --abbrev-ref HEAD; git status --short; git diff --stat; git log --oneline -10`. Outside git, list the files you edited this session. Take checks from this session's transcript: only commands you ran and whose output you read.

Done when: branch, changed files and check results are in hand.

### 2. Write the doc

Compute the path in shell so the name is sanitized. It goes in the OS temp dir (Windows: `%TEMP%`), outside the workspace, so it never lands in a commit:

```bash
REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\{1,\}/-/g; s/^-//; s/-$//')
FILE="${TMPDIR:-/tmp}/handoff-${REPO:-repo}-$(date +%Y%m%d-%H%M).md"
[ -e "$FILE" ] && FILE="${FILE%.md}-$$.md"; echo "$FILE"
```

Each handoff is a new file; earlier ones stay. Use this shape and drop empty sections:

```markdown
---
repo: <absolute repo path>
branch: <branch>
saved: <ISO-8601 time>
status: in-progress | blocked | ready-for-review
---
# Handoff: <3-6 word title>
## Goal
<1-3 sentences: what the user wants and why. The next session's focus, if given.>
## State
- [done] / [in flight] / [verified, uncommitted] / [blocked: <why>] / [not started] <thread>
## Decisions
- <decision>: <why> (user) | (delegated to me)
- Tried and dropped: <approach>: <why it failed>
## Files touched
- `path/to/file`: <what changed>
## Checks run
- `<command>` → <result>
- Not run: <check> (<why>)
## Next steps
1. <concrete action naming the file, command or ticket>
## References
- <plan, spec, ADR, issue, PR, commit: path, URL or SHA>
## Suggested skills
- `<skill>`: <which step needs it and why>
```

- **Reference, don't paste.** Plans, specs, ADRs, issues, commits and diffs already exist; point at them. Paste only what lives nowhere else: a decision and its reason, the one line of an error that matters.
- **Decisions and dead ends are the payload.** Code state is recoverable from git; why you chose X and that Y already failed is not.
- **Redact.** API keys, tokens, passwords, connection strings and personal data become `<REDACTED>`; name the env var instead of its value.
- Keep it to about a screen. Cut detail before you cut a thread.

Done when: the file is saved, every thread has a status tag, and every next step names a file, command or ticket.

### 3. Report

Give the absolute path and the line to start the next session with: "Run `handoff restore`" (or "Read `<path>` and continue from Next steps"). The user opens the fresh session with `/clear` on Claude or `/new` on Codex.

## Restore

### 1. Find it

```bash
ls -1 "${TMPDIR:-/tmp}"/handoff-<repo>-*.md /tmp/handoff-<repo>-*.md 2>/dev/null | sort -r | head -5
```

`<repo>` is the sanitized name from Write step 2. The filename timestamp is the order; mtime drifts. Take the newest unless the user named a fragment or path. None found: say so, ask for the path, and stop.

Done when: one handoff is chosen and its path stated.

### 2. Check it against live state

Read the whole doc. It is a snapshot, so compare its `branch`, files and `saved` time with the current `git rev-parse --abbrev-ref HEAD`, `git status --short` and `git log --since=<saved>`. Name any drift in one line (other branch, new commits, files changed since).

Done when: drift is listed, or confirmed none.

### 3. Resume

Brief the user in at most five lines: goal, state, the next step. Load the suggested skills. Then start next step 1. Stop and ask instead when the status is `blocked` or the drift contradicts the next step.

Done when: next step 1 is underway, or the blocker is named to the user.
