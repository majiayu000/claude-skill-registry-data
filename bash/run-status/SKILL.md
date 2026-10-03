---
description: >
  Show the state of the active research run: stages completed, branch
  scoreboard, selected solution, grounding ratio, artifacts present, and the
  suggested next stage command.
argument-hint: "[--run <run-id>]"
allowed-tools: Bash(python3 .claude/scripts/*), Read, Glob
---

# /run-status

Ledger status: !`python3 .claude/scripts/ledger.py status $ARGUMENTS`

Summarize the above for the user in two or three sentences, then state the
next stage command (in pipeline order: /investigate → /discover →
/write-paper → /verify-claims; "run complete" if final/paper.md exists).
If they want details, offer to show ranking.md, ground-report.json, or
verification-report.md from the run directory.
