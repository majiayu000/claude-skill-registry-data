---
name: review-debt
user-invocable: false
version: 1.1.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal tech-debt transform pass of the agentic-workflow review pack —
  composed in-turn by review-change and product-audit; not a menu entry.
  Transforms the synthesized findings table into explicit debt items, each with
  a re-trigger condition; it does not rescan the diff. Findings only; never
  edits code.
---

# Review Tech Debt (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The caller's **synthesized findings table** (the fused, classified decision
table). This pass does **not** rescan the diff: debt-shaped findings are already
in the table, and every ownership decision already happened in the finder axes
(`review-code`, `review-verify`, …). State the scope — the change the table was
synthesized over — at the top of the returned table.

## Transform (evaluate EVERY row — none is optional; n/a must be stated)

Turn the table's tech-debt-shaped rows (TODO/FIXME/HACK, duplication, stale or
orphaned abstractions, dead code, complexity hotspots, missing tests,
workarounds pinned to upstream fixes) into explicit, payable debt items:

✓ Restate each debt-shaped finding at `file:line` with what it defers
✓ Attribute it to the axis already recorded in the table — never re-litigate ownership
✓ Confirm every debt item carries a TRIGGER: the condition under which it must be
  paid (e.g. "3rd consumer appears", ">100k rows") — a debt item without a
  trigger is itself a finding
✓ Verify no current-unit debt was mislabeled non-blocking: current-unit work
  cannot be `postpone`/`tradeoff`/`wontfix` — a table showing one is flagged back
  to the classifier, never reclassified here
✓ Honor the dead-code exception: staged/planned code cross-checked against the
  roadmap/SPEC/TASKS is not dead code — mark *verify* when unsure, never assert

## Return exactly

```
REVIEW TECH DEBT — scope: <scope>

| # | Finding | Sev | Evidence | Suggested fix |
|---|---------|-----|----------|---------------|
| 1 | <what>  | critical|major|minor | <file:line> | <trigger + smallest action> |

Rows: <n> transformed, <n> with trigger, <n> findings, <n> n/a (<which + why>)
Summary: <1-2 sentences>
Decision: PASS | FAIL
```

For this pass, the Suggested fix column carries the TRIGGER — the condition
under which the debt must be paid — alongside the smallest action.

FAIL if any critical or major finding is open; PASS otherwise. Minor findings
never block — they surface in the caller's report as debt notes.

## Done when

- Every debt-shaped row of the synthesized table was transformed with evidence
  (`file:line`) or explicitly marked n/a with the reason.
- Every debt item carries a trigger; no current-unit debt was mislabeled.
- The fixed-format block above is returned — nothing more, nothing less — and
  no code was changed.
