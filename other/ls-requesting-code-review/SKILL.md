---
name: ls-requesting-code-review
description: Use when requesting code review before merge or after substantial changes; provide focused requirements, diff range, and severity-calibrated review instructions.
metadata:
  version: "1.0"
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/obra/superpowers
    source_path: skills/requesting-code-review/SKILL.md
    source_commit: d884ae04edebef577e82ff7c4e143debd0bbec99
    source_ref: v6.1.1
    source_sha256: 1017ccdd5bc61fab67c654cf118cbdb520464b313073a0a6b9a6b9aa647a3ad6
    license: MIT
    import_date: "2026-07-03"
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Requesting Code Review

Request a focused code review to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation, never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each substantial task in a controller-led worker/tester/reviewer flow
- After completing a major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Request a read-only code review:**

Ask a reviewer to use the template at [references/code-reviewer.md](references/code-reviewer.md).

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong, with reasoning

## Example

```
[Just completed Task 2: Add verification function]

You: Requesting code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Request code review]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Reviewer returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Controller-led development:**
- Review after each substantial task
- Catch issues before they compound
- Fix before moving to the next task

**Executing Plans:**
- Review after each task or at natural checkpoints
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [references/code-reviewer.md](references/code-reviewer.md)
