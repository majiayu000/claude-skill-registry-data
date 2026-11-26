---
name: handoff
description: Use when handing in-progress work to a teammate or ending a session with unfinished, uncommitted work — writes a short recovery note with branch, state, decisions and resume steps.
type: skill
user-invocable: false
---

# Handoff

## Overview

A pointer for the next reader, not a transcript. Compaction, the session-start re-injection of `tasks/todo.md` and recent handoffs, and the workflow artifact already carry your own session forward; write a handoff when a **teammate** (or a fresh session tomorrow) must pick up unfinished work.

## When To Use

- Handing work to a teammate, or ending a session with non-trivial uncommitted work
- The engineer asks to "save state" or "hand off" — not when everything is committed with a clear message

## Workflow

Resolve the helpers once (project-local first, then the plugin root):

```bash
res() { [ -n "${MTK_HELPER_ROOT:-}" ] && echo "$MTK_HELPER_ROOT/scripts/$1" || ([ -f "scripts/$1" ] && echo "scripts/$1" || echo "${CLAUDE_PLUGIN_ROOT}/scripts/$1"); }
WFA="$(res workflow-artifact.sh)"; HS="$(res handoff-state.sh)"
```

**Resume mode first.** If the request is to continue / resume / pick up, or `/mtk handoff` arrives while `bash "$HS" list --open --branch "$(git branch --show-current)"` shows an open note and the engineer did not ask to save state: do **not** write a note (three sessions regenerated one instead of resuming).

1. `bash "$WFA" resume "$(bash "$HS" field <note> workflow)"` — online, so PR drift is checked. Read the note.
2. `bash "$HS" accept <note>` (`expire` for an obsolete note). If a helper is missing or exits non-zero, say the note's state was not updated.
3. Continue from `next_command`; the user's latest message wins over the note.

**Write mode.** The script renders the whole note (frontmatter, git facts, PRs/CI, units, traps); you supply only the next step, decisions and open questions.

1. Active workflow: `bash "$WFA" checkpoint "$MTK_WF_UUID" --next "<what the next session does first>" --decision "<decision — one-line reason>"… [--needs-user "<question> | default: <default>"]`. No active workflow: `MTK_WF_UUID=$(bash "$WFA" init TASK --goal "<goal>")`, then checkpoint.
2. Exit 3 means `--next` names a finished unit: fix the text and re-run (nothing was written).
3. Notes are git-ignored via `docs/handoffs/.gitignore`, created by the script; they expire after 14 days.
4. Update the workflow's Claude Artifact per `.claude/references/artifact-publishing.md` (no-op when unavailable or `MTK_ARTIFACT_PUBLISH=0`; disk first).
5. Tell the engineer the note path and any artifact URL: "after /clear, type anything — the next session is offered this checkpoint".

## Verification

- [ ] Write mode: `checkpoint` exited 0 and the note path was reported (exit 3 fixed and re-run)
- [ ] Resume mode: `resume` ran, `handoff-state.sh accept` ran on the note (or its failure was reported), and no new note was written
