---
name: review-implementation
user-invocable: false
version: 1.10.0
argument-hint: <path-or-glob>
allowed-tools: Read, Grep, Glob, Bash, WebFetch
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal scope/classification engine composed by review-change (and reused by
  the audit skills): consumes the synthesized findings table, verifies every
  applicable axis is represented, and classifies each finding into a decision
  table (fix-now / replan-in-unit / decision-required / proposal / ignore).
  Findings only — never refactors.
---

# Review Implementation (internal scope/classification engine)

The classification engine the review/audit skills compose: it consumes the
**synthesized findings table** (the fused output of the applicable per-axis
passes), verifies every applicable axis is represented, and returns the
classified decision table — then stops. Never refactors or edits code. It owns
the **scope/axis-coverage contract** and the **classification rubric** (the
current-unit contract + routing) that `review-change`, `audit-pr`, and
`product-audit` reference instead of restating.

It does **not** scan the diff: every finding concern has exactly one owning
pass (see the [axis ownership map](references/FIND.md)) — the per-axis passes
(`review-code`, `review-security`, `review-verify`, `review-perf`,
design/a11y/brand/SEO) find, and this engine classifies. No broad findings
scan here.

## When to use

- Invoked by `review-change` (the user-facing review entry) as its
  classification engine, over the fused findings table.
- The audit skills reference its rubric and coverage contract.

## Scope

The caller's scope statement (the branch diff vs. the default branch, or the
passed path/glob) is authoritative; the synthesized table was gathered over it.
State the scope at the top of the classified report.

## Step 0 — Discover the project (always first)

Per the agent guide's **Workflow conventions** + **documentation map**, read
what THIS skill needs: the architecture/layering rules, the testing philosophy,
and any runtime/platform, security, money, i18n/SEO/a11y and bundle rules. Pull
the project's specific risk axes from its guardrail skills where present. The
`FIND.md` axis map is the default; the project's docs refine which axes are
applicable.

## Step 1 — Verify axis coverage (the synthesized table)

For the declared scope, confirm **every applicable axis is represented** in the
synthesized findings table — one finding owner per axis, per the `FIND.md`
map: an axis the change touches that the table says nothing about is a
**missing-axis finding** (axis `coverage`), not a silent pass. Overlapping
signals from different passes on the same defect collapse into one row during
synthesis — the table must contain neither duplicates nor gaps. State which
axes were applicable and confirm each appears.

## Step 2 — Classify (the current-unit contract)

Read [Classify and route](references/CLASSIFY.md) and classify every row of the
synthesized table without reopening source files: `ignore` first (the claim),
then the current-unit contract (fix-now / replan-in-unit / decision-required
for in-scope work), then `proposal` for genuinely independent future
capabilities. One pass — no per-pass or per-reviewer classification.

## Context budget

The input is the synthesized table, not the diff. Read at most 10 non-diff
files in full for surrounding context (callers, contracts, SPEC); targeted
reads (≤ 50 lines of a named range) and grep/glob results don't count. Record
each classification as its table row immediately and drop raw file content.

## Guardrails

- **Findings + table only. Never refactor or edit code in this skill.**
- **One classifier.** Classification happens HERE, once, over the fused
  table — never per-reviewer, never re-litigated in the per-axis passes.
- Honor the dead-code exception — staged/planned code is not dead code.
- Don't inflate severity; separate "correctness/security" from "taste".
- Don't deflate either: current-unit work is never `postpone`/`tradeoff`/
  `wontfix`/`disputed` and never a new issue — size routes to
  `replan-in-unit`, not to a downgrade (current-unit contract in `CLASSIFY.md`).
- Otherwise per the project's **Workflow conventions** (docs-language,
  evidence): cite `file:line`, mark uncertainties *verify*.

## Relationship to other skills

- **Classification engine of `review-change`** — the user-facing review skill
  runs the applicable per-axis passes (the finders), fuses their tables, then
  composes this engine to classify. `audit-pr` and `product-audit` reuse this
  rubric.
- Sits in **Stage 4** of the feature workflow (verification & review).
- `fix-now` folds into the current unit; `replan-in-unit` runs
  `node scripts/unit-route.mjs <unit>`, whose `route: replan` line names the
  planner that appends user-confirmed phases before `execute-phase`;
  `decision-required` blocks for the user; independent work becomes proposals
  the user routes to `triage-issue` (D3).

## Done when

- A synthesized table consumed, axis coverage verified (no applicable axis
  missing, no duplicate rows), every finding classified with reasoning and
  routed — and **no code changed**.
