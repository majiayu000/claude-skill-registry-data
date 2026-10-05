---
name: resolve-review
description: Work through a code-review report's findings and fix them in priority order, with confirmation on anything non-trivial. Trigger on:- resolve review, address findings, fix the review, clear blocking items.
argument-hint: "report (path to specs/NNN-<slug>/review.md), which: all | blocking | should-fix | nit"
allowed-tools: Read, Edit, Grep, Glob, Bash
disable-model-invocation: true
---

# Resolve Review

Takes a `code-review` report and works through its findings, fixing them one at a time
in priority order. This skill remediates — it does not re-judge whether something is a
real issue. If a finding looks wrong on inspection, say so and skip it rather than
silently ignoring it or arguing it away.

## Assumptions (flag if wrong)

- The report is an `open`-status `code-review` output at `specs/NNN-<slug>/review.md`,
  with findings grouped under **Blocking** / **Should-fix** / **Nit** headers, each with
  file:line, what's wrong, why it matters, and a suggested fix.
- Fixing scope is limited to what's named in the finding — not an invitation to refactor
  around it.

Read `.specify/memory/constitution.md` first for the pipeline map and the review status
vocabulary.

## Arguments

- `report` — path to the review report to work from. If omitted, look for the most
  recent `specs/*/review.md` with `status: open` and confirm it's the right one before proceeding.
- `which` — which severity tier(s) to address:
  - `all` (default) — Blocking, then Should-fix, then Nit, in that order.
  - `blocking` / `should-fix` / `nit` — just that tier.

## Workflow

1. **Read the report.** Parse out findings per severity tier, each with its file:line and
   suggested fix.

2. **Work the findings via the constitution's Item-execution loop**, in tier order:
   Blocking, then Should-fix, then Nit (Nit only if `which` includes it). Two
   review-specific points on top of the loop:
   - A finding that looks wrong on inspection — not a real bug, or the fix would break
     something else — is a *skip with reason*, not a silent pass. This skill remediates;
     it doesn't re-review the other findings.
   - For Nit, ask once up front — apply all, or list for the user to pick — rather than
     prompting per item.

3. **Set the report's `status:` to `worked-on`** and bump `updated:`. Never `closed` —
   only `code-review` closes a thread, after re-checking the fixes.

4. **Offer to re-run `code-review`** on the same scope to confirm the findings are
   actually resolved, rather than trusting this pass's own fixes. Don't run it
   automatically — ask first, since it may not be needed for a `nit`-only pass.

## Boundaries

- Don't fix things the report didn't flag, even if you notice them along the way — note
  them instead (a one-liner in the summary, or point at `/notice` if it looks like a
  recurring pattern).
- Don't reduce a Blocking or Should-fix finding's severity to make it easier to skip.
- If more than a couple of findings turn out to need real design decisions rather than
  straightforward fixes, stop and flag that the report may need `/designit` rather than
  direct patching — don't improvise architecture mid-fix.