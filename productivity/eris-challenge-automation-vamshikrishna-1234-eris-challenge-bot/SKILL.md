---
name: eris-challenge-automation
description: Route and operate reusable Project Eris workflows in Claude Code for Ready, Status, Status & Fix, Create X Tasks, Finish X Linked Tasks, supplied Shipd challenge/dataset links, revisions, and resilient autonomous batches.
---

# Eris Challenge Automation for Claude Code

This is a runtime adapter, not a second policy copy.

1. Read `${CLAUDE_PROJECT_DIR}/.codex/skills/eris-challenge-automation/SKILL.md`
   completely and follow it as the canonical workflow.
2. Read the canonical references that workflow selects for the request.
3. Read [references/claude-runtime.md](references/claude-runtime.md) before any
   multi-task work or live Shipd action.
4. Run `${CLAUDE_PROJECT_DIR}/validate-portable.ps1` and inspect the controller
   status before changing state.
5. Interpret `$ARGUMENTS` as the user's workflow request. Preserve exact task
   counts and exact challenge/dataset pair ordering.

Where canonical text names Codex-specific tools, apply the mapping in the
Claude runtime reference. Do not translate away source, license, novelty,
truth, leakage, shortcut, stability, grader, validation, or safety gates.

Use the controller ledger throughout. A failed candidate is an attempt inside
its immutable slot, not a finished slot. A transient rate limit, reconnect, or
expired session is a retryable runtime condition, not a rejection.

For `Create X Task(s)`, create exactly X immutable controller slots and assign
one `eris-slot-worker` project subagent to each slot. Dispatch them immediately
when capacity permits; otherwise queue or run workers in waves. A concurrency
limit changes scheduling, never the requested success count. The coordinator
must remain active, reconcile worker checkpoints, and re-dispatch unfinished
slots until every slot reaches the invocation's goal stage.
