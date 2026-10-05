---
name: "OCR Review-to-Approval Loop"
description: "Drive a PR to an approved code review by looping OCR's multi-agent review and address steps. Runs /ocr:review then /ocr:address repeatedly until the review verdict is APPROVE, then one final /ocr:address for leftover suggestions, posting every review and every address round to the GitHub PR as comments. Use when the user asks to 'review and address in a loop', 'iterate review until approved', 'auto review-and-fix this PR', 'loop /ocr:review and /ocr:address', or to take a changeset all the way to a clean APPROVE with the default reviewer team. Wraps the /ocr:review (.ocr/commands/review.md) and /ocr:address (.ocr/commands/address.md) skills; needs a feature branch with an open GitHub PR and the gh CLI for posting."
---

# OCR Review-to-Approval Loop

## What This Skill Does

Orchestrates an autonomous **review → address → re-review** loop on a pull request,
using OCR's existing multi-agent review pipeline, until the review reaches an **APPROVE**
verdict — then runs one final address pass for leftover suggestions. Every review and every
address round is posted to the GitHub PR as a comment, producing a transparent, reviewable
audit trail.

It is a thin **orchestrator** over two skills it does not reimplement:
- **`/ocr:review`** → `.ocr/commands/review.md` (the 8-phase multi-agent review that emits a verdict)
- **`/ocr:address`** → `.ocr/commands/address.md` (corroborate feedback against code, then implement)

## When to Use

- "Review and address in a loop until it's approved."
- "Iterate /ocr:review and /ocr:address on this PR."
- "Auto review-and-fix PR #N to a clean approval."

## When NOT to Use (use the underlying skills directly)

- A **single** review with no auto-fixing → `/ocr:review`.
- Addressing **one** existing review's feedback → `/ocr:address`.
- There is no PR / not on a feature branch (this skill commits and posts).

## Prerequisites

- On a **non-default** git branch with an **open GitHub PR** (the loop commits + pushes each round).
- `gh` CLI installed and authenticated (for posting; skip with `--no-post`).
- OCR set up in the repo (`.ocr/` exists, `ocr` CLI available). Run `/ocr:doctor` if unsure.
- A green-ish working tree: any uncommitted changes will become part of what is reviewed.

## Arguments

```
/ocr-review-loop [pr] [--team <spec>] [--max-rounds N] [--no-final-suggestions] [--no-post]
```

- `pr` (optional): PR number. Default: the open PR for the current branch.
- `--team <spec>` (optional): reviewer team override (`reviewer-id:count,...`), forwarded to
  `/ocr:review`. **Default: the project's default team** (`ocr team resolve`).
- `--max-rounds N` (optional): safety cap on review rounds. **Default: 5.** The loop never
  runs forever.
- `--no-final-suggestions` (optional): stop at APPROVE; skip the final suggestions pass.
- `--no-post` (optional): run locally; do not post to GitHub. Present the trail in-chat instead.

---

## The Loop (core algorithm)

> Execute this inline, to completion, in the conversation. Do not schedule across turns or
> background the work. Drive each review's phases 4→7 within one turn (OCR's "don't strand
> the pipeline" rule). See `reference/loop-mechanics.md` for the exact CLI/session details
> and the GitHub comment templates.

**0. Preconditions.** Resolve the PR and branch; refuse to run on the default branch. Confirm
`gh` (unless `--no-post`) and OCR setup. Resolve the reviewer team (default unless `--team`).

**1. Review-address loop.** Starting at `round = 1`, while the verdict is not `APPROVE` and
`round <= max-rounds`:

1. **Review** — invoke `/ocr:review` (default team, or `--team`). It runs the full pipeline
   and finalizes `rounds/round-{round}/final.md` + `round-meta.json` with a `verdict`.
2. **Post the review** to the PR, headed `OCR review — Round {round}`. *(skip if `--no-post`)*
3. **Gate on the verdict** (read it from `round-meta.json` / `final.md`):
   - **`APPROVE`** → exit the loop (proceed to step 2 below).
   - **`NEEDS DISCUSSION`** → **STOP the loop.** This is a human gate — surface the
     clarifying questions to the user and await direction. Do **not** fabricate a fix.
   - **`REQUEST CHANGES`** → continue.
4. **Address** — invoke `/ocr:address` on `rounds/round-{round}/final.md`. Corroborate every
   item against the actual code; implement the **blockers and should-fixes** (these clear the
   gate); decline incorrect feedback with evidence; you MAY defer pure **suggestions** to the
   final pass. **Verify** (typecheck + lint + tests) until green, then **commit** (atomic,
   conventional) and **push**.
5. **Post the address round** to the PR: what was addressed, declined (with reasoning), and
   deferred. *(skip if `--no-post`)*
6. `round += 1`; loop.

**2. Final suggestions pass** (only after `APPROVE`, unless `--no-final-suggestions`):
invoke `/ocr:address` once more to clear remaining **suggestions**, verify, commit, push, and
post a final address comment that includes a **loop-summary table** (round → verdict → outcome).

**3. Stop conditions.** If `round` exceeds `max-rounds` without `APPROVE`, **stop** and report
the outstanding blockers — never loop indefinitely. If APPROVE was reached on round 1, skip the
loop body and go straight to the final suggestions pass.

---

## Guardrails (critical — do not skip)

- **Bounded.** Honor `--max-rounds` (default 5). If not approved by then, stop and surface why.
- **`NEEDS DISCUSSION` is a human gate.** Pause and ask; never invent a resolution for genuine
  ambiguity.
- **Corroborate, don't obey.** Per `.ocr/commands/address.md`: verify each finding against the
  code; implement valid items; **decline wrong feedback with evidence**. Don't gold-plate —
  fix only what the review actually raised.
- **Never push red.** Run the project's typecheck + lint + tests before every commit; fix
  failures before pushing.
- **Branch safety.** Refuse to run on the default branch; this skill commits and pushes.
- **Faithful reporting.** Report verdicts and outcomes honestly. If a blocker genuinely can't
  be fixed (needs a product/architecture decision), stop and say so rather than forcing APPROVE.
- **New round, same session.** Each iteration is a new OCR review round in the same session
  (a closed session starts `round-{n+1}`), reusing `discovered-standards.md` / `context.md`.

## Reference

- **Detailed per-round mechanics, verdict gating, session/round handling, and the GitHub
  comment templates** → [`reference/loop-mechanics.md`](reference/loop-mechanics.md)
- Underlying skills: [`/ocr:review`](../../../.ocr/commands/review.md),
  [`/ocr:address`](../../../.ocr/commands/address.md)
