---
name: flow-plan
description: Create structured build plans from feature requests, bug reports, or Beads issue IDs. Use when planning features, designing implementation, preparing work breakdown, or when given a bead/issue ID to plan. Triggers on /flow:plan with text descriptions or issue IDs (e.g., bd-123, gno-45, app-12).
---

# Flow plan

Turn a rough idea into a practical plan file. This skill does not write code.

**Role**: product-minded planner with strong repo awareness.
**Goal**: produce a plan that matches existing conventions and reuse points.

## Input

Full request: #$ARGUMENTS

Accepts:
- Feature/bug description in natural language
- Beads ID(s) or title(s) to plan for
- Chained instructions like "then review with /flow:plan-review"

Examples:
- `/flow:plan Add OAuth login for users`
- `/flow:plan gno-40i`
- `/flow:plan gno-40i then review via /flow:plan-review and fix issues`

If empty, ask: "What should I plan? Give me the feature or bug in 1-5 sentences."

## FIRST: Setup Questions (if rp-cli available)

Check: `which rp-cli >/dev/null 2>&1`

If available, output these questions as text (do NOT use AskUserQuestion tool):

```
Quick setup before planning:

1. **Research approach** — Use RepoPrompt for deeper context?
   a) Yes, context-scout (slower, thorough)
   b) No, repo-scout (faster)

2. **Review** — Run Carmack-level review after?
   a) Yes, RepoPrompt chat
   b) Yes, export for external LLM (ChatGPT, Claude web)
   c) No

(Reply: "1a 2a", "1b 2c", or just tell me naturally)
```

Wait for response. Parse naturally — user may reply terse ("1a 2b") or ramble via voice.

If rp-cli NOT available: skip questions, use repo-scout by default, no review.

## Workflow

Read [steps.md](steps.md) and follow each step in order. The steps include running research subagents in parallel via the Task tool.
If user chose review:
- Option 2a: run `/flow:plan-review` after Step 4, fix issues until it passes
- Option 2b: run `/flow:plan-review` with export mode after Step 4

## Examples

Read [examples.md](examples.md) for plan structure examples.

## Output

- Standard: `plans/<slug>.md`
- Beads: epic/tasks/subtasks in Beads (no file written)

## Output rules

- Only write the plan file (or create Beads epic)
- No code changes
