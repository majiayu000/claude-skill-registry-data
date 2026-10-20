---
name: refactor-repo
description: >-
  Audit a whole codebase or one module for accumulated complexity and shrink it: a read-only
  inventory, a ranked proposal, then, only after approval, refactor/ branches under a
  behavior-preservation gate. Not for one branch's diff (use shrink-diff).
argument-hint: "[module-or-path]"
disable-model-invocation: true
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a git working tree, for the before/after `git diff --stat`
  totals the report is built on. Applying and verifying a refactor additionally needs whatever
  runtime, package manager, and test runner the target repo already uses - none is assumed.
license: Apache-2.0
---

# Refactor repo

The whole-codebase counterpart of `shrink-diff`: the same standard, but with no diff to scope
it, so scope discipline comes from process instead. This is the high-risk mode — a repo-wide
refactor applied in one pass produces an unreviewable diff and regressions in code that had no
motivating change. Never apply anything in the same breath as finding it: **inventory → propose
→ approval → apply**.

## Procedure

### Phase 1 — Inventory (read-only)

Scope is the whole repo, or the module/directory the user names. No edits in this phase.

Hunt the same categories as `shrink-diff`, plus the ones only time produces:

- **Duplication anywhere** — parallel implementations that have drifted apart count double;
  they are a live bug source, not just bloat.
- **Dead code** — unreachable branches, unused exports and symbols, obsolete compatibility
  shims, feature flags fully rolled out.
- **Over-abstraction** — single-implementation interfaces, single-caller wrappers, config for
  constants, layers that only forward.
- **Information leakage** — one design decision (a file format, a status string, an ordering
  rule) known by two or more modules, so changing it means editing each. Unlike duplication the
  code may look different everywhere. The fix moves the decision behind one module.
- **Shallow modules worth deepening** — a module whose interface is nearly as large as what it
  hides, so every caller repeats the same sequence of calls, the same setup, or the same
  knowledge of its internals. The fix is the opposite of inlining: merge the module and the
  logic its callers repeat into one module with a smaller interface. Record the caller count,
  since that is what deepening pays back.
- **Retroactive ladder violations** (below).

For each area, also record its **test coverage status** — it decides in Phase 3 what may be
applied there.

### The retroactive ladder

Walk each piece of code in scope down the write-less-code ladder, in hindsight:

1. **Does it need to exist at all?** Dead code, an unused parameter or flag, a speculative hook
   nothing calls → delete it.
2. **Stdlib does it?** Replace the custom version.
3. **Native platform feature covers it?** Replace the custom version.
4. **An already-installed dependency solves it?** Replace the custom version. Never add a new
   dependency to shrink code: its install, supply-chain, and upgrade cost outlasts the lines saved.
5. **Can it be one line?** Make it one line.
6. **Only then:** keep it, as the minimum that works — collapse single-implementation
   abstractions, inline single-caller wrappers, turn config-for-a-constant back into a constant.

### Phase 2 — Propose, then stop

Deliver a ranked candidate table:

| #   | What / where | Payoff (est. lines removed, readability) | Risk | Est. diff size | Coverage |
| --- | ------------ | ---------------------------------------- | ---- | -------------- | -------- |

Group candidates into clusters sized so each cluster makes one reviewable PR (the size limits in
`ceh-git-workflow:pull-request`). Then **stop and wait for the user to select clusters**. Invoking
this skill approved the campaign, not any specific candidate — never proceed past this point
unprompted. With no human to select (a headless run), the ranked table is the deliverable: end the
run there and apply nothing, because no cluster was approved.

A deepening candidate carries its proposed interface in the table: the signatures callers would
use after, beside the calls they make today, so the user judges the design rather than a label.
When the user selects one, settle its open design questions before any code: ask them a round at a
time, each with a recommended answer, starting with what the new interface hides and what it must
still expose. The answers become the cluster's scope, and a question left open keeps the cluster
unapplied.

### Phase 3 — Apply approved clusters

- One `refactor/<cluster>` branch per approved cluster, branched from `main`, because many
  small PRs beat one big one.
- Behavior preservation (below) gates every edit. In areas with no coverage the rule is
  skip-and-report, not apply-carefully — careful is not a gate.
- A cluster that grows past its estimated diff size mid-apply gets split or stopped, not pushed
  through.

## Rules

### Behavior preservation

A refactor changes shape, never behavior:

- Never mix a behavior change into a refactor. If shrinking reveals a bug, report it — fixing it
  is separate work.
- Where tests cover the touched code, run them before and after; both runs must be green. A red
  before-run is a finding to report, not a license to proceed.
- Where no tests cover it, apply only mechanical transforms (delete provably-dead code, inline,
  rename, extract) and flag anything riskier instead of applying it.
- For anything past a mechanical transform — an extraction across files, an implementation swap, a
  dependency or runtime upgrade — pin current behavior first with
  `ceh-testing:verify-behavior-preserved` (characterization tests, golden files, differential run)
  and commit those pins on their own before touching the code. A green existing suite is the weaker
  check: it only proves what it already covered.
- Commit refactors with the `refactor:` type, separate from any other change.

### Replacing and redesigning

- Migrate callers, then delete. To replace an API, move every caller to the new one, prove no
  caller of the old one is left with a grep or the type checker, then delete the old one in the
  same cluster. A shim that keeps both alive is the two-path state this campaign exists to end.
- Redesign when patches pile up. When an area holds a third special case for the same concept,
  or a fix keeps breaking a neighbour, propose a redesign from what the code must do today rather
  than another patch. It is a candidate like any other: it goes in the Phase 2 table and waits
  for approval.

## Output

### Phase 4 — Report

Per cluster: candidates applied with before/after `git diff --stat` totals, candidates skipped
with reasons (coverage, size, risk), and any bug found while refactoring — reported, not fixed.
Save the report to `.agents_workspace/refactor/<YYYY-MM-DD>.md` and name the path in the reply,
because the skipped candidates and the unfixed bugs have no other record.
