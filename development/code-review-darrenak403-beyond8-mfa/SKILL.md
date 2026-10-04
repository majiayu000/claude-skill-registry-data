---
name: code-review
description: >
  Always use this skill before claiming any work is done, fixed, passing, or complete —
  even if it seems obvious. Also use when receiving code review feedback from any source
  (human or automated), when finishing a task or major feature, before committing or
  creating a PR, or when about to express satisfaction with work. Covers three practices:
  receiving feedback with technical rigor (no performative agreement), triggering code
  review via /code-review command or cook/fix pipelines, and verification gates (run the
  command, read the output, then make the claim). Never skip — the cost of false completion
  claims is higher than the cost of verifying. References: code-review-reception.md,
  requesting-code-review.md, verification-before-completion.md.
---

# Code Review

Apply code review practices with technical rigor, evidence-based claims, and verification over performative responses.

## References

| Practice            | When to load                                          | File |
| ------------------- | ----------------------------------------------------- | ---- |
| Receiving feedback  | Unclear/questionable feedback, conflict with reviewer | `references/code-review-reception.md` |
| Requesting review   | After each task, before merge — use `/code-review`    | `references/requesting-code-review.md` |
| Verification gates  | Before any completion/success claim                   | `references/verification-before-completion.md` |

## Overview

Code review requires three distinct practices:

1. **Receiving feedback** — Technical evaluation over performative agreement
2. **Requesting reviews** — Systematic review via code-reviewer subagent
3. **Verification gates** — Evidence before any completion claims

## Core Principle

**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

## When to Use This Skill

### Receiving Feedback
Trigger when:
- Receiving code review comments from any source
- Feedback seems unclear or technically questionable
- Multiple review items need prioritization
- Suggestion conflicts with existing decisions

### Requesting Review
Trigger when:
- Completing tasks in subagent-driven development (after EACH task)
- Finishing major features or refactors
- Before merging to main branch
- After fixing complex bugs

Use `/code-review` (local) or `/code-review <PR>` (PR mode). Cook/fix pipelines invoke the `code-reviewer` agent automatically.

### Verification Gates
Trigger when:
- About to claim tests pass, build succeeds, or work is complete
- Before committing, pushing, or creating PRs
- Moving to next task
- Any statement suggesting success/completion

## Quick Decision Tree

```
SITUATION?
│
├─ Received feedback
│  ├─ Unclear items? → STOP, ask for clarification first
│  ├─ From human partner? → Understand, then implement
│  └─ From external reviewer? → Verify technically before implementing
│
├─ Completed work
│  ├─ Major feature/task? → Run /code-review (or it's automatic in cook/fix)
│  └─ Before merge? → Run /code-review <PR-number>
│
└─ About to claim status
   ├─ Have fresh verification? → State claim WITH evidence
   └─ No fresh verification? → RUN verification command first
```

## Receiving Feedback Protocol

### Response Pattern
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

### Key Rules
- No performative agreement: "You're absolutely right!", "Great point!", "Thanks for [anything]"
- No implementation before verification
- Restate requirement, ask questions, push back with technical reasoning, or just start working
- If unclear: STOP and ask for clarification on ALL unclear items first
- YAGNI check: search for usage before implementing suggested features

**Full protocol:** `references/code-review-reception.md`

## Verification Gates Protocol

### The Iron Law
**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

### Gate Function
IDENTIFY command → RUN full command → READ output → VERIFY confirms claim → THEN claim

### Red Flags — STOP
Using "should"/"probably"/"seems to", expressing satisfaction before verification, committing without verification, trusting agent reports.

**Full protocol:** `references/verification-before-completion.md`

## Bottom Line

1. Technical rigor over social performance — no performative agreement
2. Systematic review processes — use code-reviewer subagent
3. Evidence before claims — verification gates always

Verify. Question. Then implement. Evidence. Then claim.
