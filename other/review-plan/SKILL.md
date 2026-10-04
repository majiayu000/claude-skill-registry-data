---
name: review-plan
description: XP-style plan review that identifies gaps, hidden assumptions, and critical misses. Triggers on 'review the plan', 'check the plan', 'audit the plan'. Reviews plans for YAGNI violations, missing feedback loops, and over-engineering.
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Workflow
metadata:
  author: Fishbowl Team
  version: "0.2.0"
---

# XP Plan Review

STARTER_CHARACTER = 👁️

## Activation Triggers

- "review the plan"
- "/review-plan"
- "check the plan"
- "audit the plan"

## Process

### 1. Find the Plan

Search for plan files:
- Recent plan in context window user is referring to
- `.claude/plans/`
- `plans/`
- `docs/plans/`
- File mentioned by user

If multiple found, ask which one.

### 2. Run the Review Workflow

The multi-agent review — one independent reviewer per lens (Gaps, Hidden
Assumptions, Critical Misses, plus the five XP Violations: YAGNI, Simplicity,
Step Size, Feedback Loops, Tech Debt), dedup, and an adversarial-verify pass
where skeptics vote to kill unconvincing findings — is encoded as a
**deterministic Workflow** so the fan-out, dedup, and verification run reliably
instead of relying on prose. The reviewers are `Plan` agents, exactly as before.

Invoke the `Workflow` tool with the bundled script, passing whichever plan
reference you resolved in step 1 (`path` for a file, or `plan` for raw text):

```
Workflow({
  scriptPath: "${CLAUDE_PLUGIN_ROOT}/skills/review-plan/workflow.js",
  args: { path: "[PATH]" }   // or { plan: "[plan text]" }
})
```

The workflow runs two phases (both autonomous — no human gate):

- **Review (8 parallel Plan reviewers, independent):** one per lens — Gaps in
  Knowledge · Hidden Assumptions · Critical Misses · YAGNI · Simplicity · Step
  Size · Feedback Loops · Tech Debt. Each returns findings with issue, impact,
  recommendation, and priority (critical > important > nice-to-have). Empty /
  issue-less findings are dropped; near-duplicate findings across lenses are merged.
- **Verify (adversarial skeptics, Haiku, one per unique finding):** each skeptic
  tries to KILL the finding — assumes false positive until the plan's content
  proves otherwise. Findings the skeptic votes down or scores below 50 confidence
  are dropped.

It returns `{ findings }` — the merged, ranked list (priority then confidence),
where each kept finding carries `{ issue, impact, recommendation, priority, lenses, confidence, justification }`.

### 3. Present and Confirm

After the workflow returns, present the kept findings to the user (group by
priority: critical > important > nice-to-have). If `findings` is empty, tell the
user the plan passed review and stop.

Use AskUserQuestion:
```
Question: "Based on these [N] issues, how would you like to proceed?"
Header: "Update Plan"
Options:
  - "Fix all" - Update plan to address all issues
  - "Select items" - Choose specific issues to address
  - "Skip" - Keep plan as-is
```

### 4. Update Plan (Only After Confirmation)

If user confirms:
- Make targeted edits
- Keep changes minimal
- Preserve original structure
