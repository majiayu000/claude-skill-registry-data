---
name: flow-plan-review
description: Carmack-level plan review via rp-cli context builder + chat. Use when reviewing implementation plans, architecture docs, or design specs. Triggers on mentions of plan review, design review, or architecture review.
---

# Plan Review Mode (CLI)

Conduct a John Carmack-level review of implementation plans using RepoPrompt's context builder and chat.

**Role**: Code Review Coordinator (NOT the reviewer)
**Tool**: rp-cli for context building and chat delegation

## Input

Arguments: #$ARGUMENTS
Format: `<plan-file-or-beads-id> [additional context or focus areas]`

Accepts:
- Plan file path: `plans/<slug>.md`
- Beads ID(s) or title(s) directly

Example: `/flow:plan-review docs/plan/auth-refactor.md focus on security and error handling`

## FIRST: Determine Review Mode

Check: `which rp-cli >/dev/null 2>&1`
If NOT available: inform user rp-cli is required for this skill.

**If review mode was already chosen earlier in this conversation** (e.g., user answered "2a" or "2b" during `/flow:plan` or `/flow:work` setup):
→ Use that mode, don't ask again.

**If invoked directly without prior context**, ask:

```
Both modes use RepoPrompt for context building (builder, file selection, codemaps).
The difference is where the review happens:

Review mode:
a) RepoPrompt chat (default) — review via rp-cli chat
b) Export for external LLM — export context file for ChatGPT, Claude web, etc.

(Reply: "a", "b", "export", or just tell me)
```

Wait for response. Parse naturally.

## Critical Requirement

**DO NOT REVIEW THE PLAN YOURSELF** – you are a coordinator, not the reviewer.

Your job is to:
1. Use `rp-cli -e 'windows'` to find the RepoPrompt window
2. Use `rp-cli -w <id> -e 'builder ...'` to build context around the plan
3. Use `rp-cli -w <id> -e 'chat ...'` to execute the review

The **RepoPrompt chat** conducts the actual review with full file context.

## Workflow

Read [workflow.md](workflow.md) and follow each phase in order. Phases include window selection, context building, and review execution.

## rp-cli Reference

Read [rp-cli-reference.md](rp-cli-reference.md) for command syntax and examples.
