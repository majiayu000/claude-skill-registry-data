---
name: close
description: Block D of the harness workflow. After the owner merges, cleans up the issue's branch and working files safely and condenses its notes. Invoke as /close <issue> [epic].
argument-hint: <issue-number> [epic]
disable-model-invocation: true
---

# Close: Block D

Arguments: `$ARGUMENTS`. The first is the issue number; `epic` means this closes an epic.

## 1. Script part

Run `node .claude/scripts/close.cjs <n>`. It deletes nothing it can't prove is safe:

- the PR must be `MERGED`
- the working tree must be clean
- the local branch tip must equal the merged PR's head

Exit codes:

- **3 (aborted):** report its message and **both SHAs** to the owner, and stop. Don't delete anything by hand.
- **2 (error):** report it and stop.
- **0:** go on. Its report lists what it deleted and the memory files that mention the issue.

## 2. Model part

- **Condense each memory file the report lists:** keep the outcome, the deferred follow-ups and the lasting lessons; drop the step-by-step. Don't delete a memory that other work still needs. Make the edits; don't ask first (D4).
- **On `epic`:** run one knowledge audit. Brief the `red-team` to check the ADRs and docs the epic touched against the code's current behaviour. Its findings come to the owner like any others.

## 3. Report

One short message:

- what the script deleted and kept
- the memory files you changed, each with one line on what you condensed
- the audit result, on `epic`

The issue comments (plan and handoff) stay as the record.
