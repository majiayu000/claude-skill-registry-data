---
name: full-review
description: Run the layered review pipeline — architecture, code correctness, security, UI, and UX — then synthesize findings into one severity-ranked report. Use when the user runs /full-review, before merging a feature, or after completing a significant change.
---

# Full Review Pipeline

**Orchestrate** the specialized reviewer agents over the target, then **synthesize** ONE merged report. Do not review inline yourself — delegate so each pass has clean, focused context.

Read `learnings.md` beside this file before starting; append an entry when reviewers duplicated, missed a dimension, or a synthesis rule needed changing.

## Governing Principle

> **Separation of review concerns.** Each reviewer owns one dimension of quality. Overlap is caught at merge time, not by bloating individual reviewers. The same design principles that guided the building do the judging.

## Procedure

1. **Discover** the target files and capture the diff once (`git diff` + `git diff --staged`; if clean, the last commit).
2. **Decompose** the review into independent passes. Launch reviewer subagents **in parallel**, passing each the diff/file list and its focus:
   - `system-reviewer` — architecture, boundaries, data flow
   - `code-reviewer` — correctness, stack idioms, clean code
   - `security-reviewer` — auth, sessions, input trust, secrets
   - `ui-reviewer` — only if the diff touches component/style files
   - `ux-reviewer` — only if the diff touches routes or user-facing flows
3. **Synthesize** results into one report. De-duplicate (the same missing validation may be flagged by code + security — report once, tag both). Discard vague findings with no file:line anchor.
4. **Instrument** — after the report, run the project's linter and type-checker. Append any tool-caught errors as additional findings.

## Report format

```
## Review: <scope> — <n> findings

### 🔴 Blocker (security holes, data loss, broken documented rules)
### 🟡 Should fix (correctness risks, pattern violations, a11y gaps)
### 🟢 Consider (cleanups, simplifications, debt reduction)
```

Each finding: `file:line` — one-sentence defect — one-sentence concrete fix. End with a short "what this diff did well" line (reinforce good patterns) and offer: "run `/teach` on any finding to understand it deeply."

## Constraints

- Findings must be verifiable in the code, not stylistic taste.
- The project's own documented rules outrank general best practice — **discover** them by reading architecture docs.
- Do not auto-fix anything; report only, unless the user then asks.
- The report must be actionable: every finding has a concrete fix, not just "this looks wrong."

## Handoffs

- User wants to understand a finding → `/teach`.
- Finding reveals a missing design → `/system-design`.
- Finding reveals a pattern violation → `/patterns`.
