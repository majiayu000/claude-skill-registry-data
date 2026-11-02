---
name: refactor
description: |-
  Use when changing the structure of working code without changing its behavior: decomposing an oversized function, extracting or merging a module, collapsing a layer, breaking an import cycle. Applies when the edit is structural enough to need a plan and explicit approval before it lands. Triggers: 'refactor this', 'decompose this function', 'split this module', 'break this dependency cycle', 'extract this into', 'restructure', 'work through the deferred items'. Not for slop cleanup (use simplify), judging a change (use code-review), fixing bugs, or adding behavior.
---

# Refactor: Behavior-Preserving Structural Change

## Overview

Refactor changes the structure of working code; it does not change behavior.

It differs from `simplify` by risk rather than size: simplify applies edits whose behavior preservation is verifiable on the spot, and refactor takes the edits that are not — the ones that move contracts, cross module boundaries, or touch files far from where the request started.
Those need a plan the user rules on before anything lands, because the resulting diff is too large to review after the fact.

Every move is approved individually and executed on its own, with verification green between moves.

## When to Use

- A function or class has grown past the point where it can be read.
- Two modules import each other, or a layer imports something below it that it must not.
- An abstraction has one implementation, and collapsing it touches every call site.
- A simplify pass left structural proposals and the user wants to work through them.
- Code needs to move: extracted to a new module, merged into an existing one, renamed across the tree.

## When Not to Use

- Slop cleanup belongs to `simplify`: duplication, dead code, comment noise, local de-nesting.
- Judging a change belongs to `code-review`: correctness, security, test adequacy, merge readiness.
- A bug gets fixed first.
  Changing behavior is a different task, so fix it and then refactor the result.
- Refactor never adds capability.
  New behavior is a different task too.
- A rewrite that trades semantics for speed does not preserve behavior, so optimization work does not belong here.
- Anything a configured linter or formatter flags is out of scope.
  Run the tool.

## Invocation Notice

- Tell the user when this skill is running: `refactor`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Phase 0 — Gate

### 1. Resolve the work

A proposal comes from one of three sources.
Use whichever the request provides:

- **A ledger.**
  The user points at a ledger file, or says "work through the deferred items".
  In that case take the newest `simplify-*.md` or `refactor-*.md` in the location project instructions set, `.review/`, `._scratch/`, `.scratch/` at the repo root, or `$TMPDIR`.
  Its Deferred section is the work list; each entry carries a proposed move, blast radius, and verification plan.
  If no ledger exists, say so and ask what to work on.
  A ledger written to `$TMPDIR` in another session or harness may not be visible here; ask for its path.
- **A report or finding list** from a review or another agent.
  Treat each item as a proposal to validate, not a decision already made.
- **A direct request**: decompose this, split that.
  Say once that a `simplify` pass first usually shrinks the job, because dead code and duplication are cheaper to delete than to carry into a new structure.
  If the user declines, proceed.

The ledger format lives in the `simplify` skill's `references/edit-ledger.md`; read it when consuming or writing one.
If that file is not available, the sections are simple enough to mirror from any existing ledger: Applied, Removed, Deferred, Skipped.

### 2. Baseline

Find the repo's checks and establish the strongest available check:

1. **Full test suite** with the target code exercised — confirm with coverage, not assumption.
2. **Typecheck plus lint**, when no suite covers the target.
3. **Characterization test** written first, pinning current behavior; it stays afterward as a regression guard.
4. **Stop.**
   Below level 3 there is no way to demonstrate behavior preservation, and a refactor that cannot demonstrate it is a rewrite.
   Say so and let the user decide.

Run the baseline before any edit.
If the suite is red, stop; without a green start, no later failure is attributable.
Record the check, the command, and the result — and the starting commit, which Phase 3's scope check needs.

### 3. Specs

Look for a spec source: an `openspec/` or `specs/` tree, or artifacts from the `sdd` family.
Structural change must leave the code compliant.
If a move cannot preserve compliance, record it and stop.
Suggested spec revisions go in the ledger, and this skill never applies them.

### 4. Graph tooling

If the `code-review-graph` MCP plugin is available, call `build_or_update_graph_tool()` then `list_graph_stats_tool()`.
If either call fails or the graph is empty, continue on the git-only path and do not retry.
See `references/code-review-graph-integration.md` for per-phase use.

The graph matters more here than in a review, because blast radius is what the plan is built from.
Without it, establish the same facts by grep: every caller, importer, subclass, and test of what you are about to move — and every textual reference: strings, config keys, fixtures, serialized data.

## Phase 1 — Plan (no edits)

Produce a plan before touching anything.

For each move, follow the procedure in `references/structural-moves.md` and record these fields:

| Field         | What to record                                                                 |
| ------------- | ------------------------------------------------------------------------------ |
| Move          | Which structural operation, on what                                            |
| Preconditions | What must be true for the move to preserve behavior                            |
| Blast radius  | Files touched, callers updated, tests affected, public surface changed         |
| Test impact   | Which tests must change, and why each is coupled to structure and not behavior |
| Verification  | What proves behavior is unchanged, beyond a passing suite                      |
| Order         | The sequence that leaves verification green between moves                      |

Count the blast radius; do not estimate it.

Split anything large into the smallest moves that each leave the tree green.
One 900-line move is not a plan the user can rule on.

State what you are **not** doing.
Do not widen the plan after approval.
The user approved what you presented, not a larger version of it.

## Phase 2 — Approval

Present the plan and stop.

The user approves moves individually, not the plan wholesale.
They will often want two of six.
Note declined moves in the ledger so the record shows they were considered.

Approval of a move covers the test changes its Test impact field enumerated; do not re-ask for those during execution.

Do not begin executing while asking.

## Phase 3 — Execute

Take one approved move at a time, in the planned order.

For each move:

1. Confirm verification is green.
2. Make the move, and only that move.
   If you notice something else, put it in the ledger.
3. Update every caller, importer, and subclass the plan identified.
4. Run the check.
5. If green, record the outcome and continue to the next move.
6. If red, revert the move entirely.
   Do not repair forward.
   Record what failed and why, so the proposal is not blindly retried later.

If a test edit surfaces that the approved plan did not enumerate, stop and get agreement first, stating three things:

| State                  | What it means                                                                     |
| ---------------------- | --------------------------------------------------------------------------------- |
| What changed           | The specific assertion, and what it asserted                                      |
| Why it was coupled     | What made it depend on structure and not on behavior                              |
| Why behavior is stable | What else proves the observable contract holds, now that this test no longer does |

A test edit that cannot supply all three is a behavior change, not a refactor.
Revert it and say so.

If the blast radius exceeds the plan, stop and re-plan.
Discovering three more call sites mid-move means the user approved a plan that was wrong.

## Phase 4 — Record

If the work came from a ledger, append an outcome block under each executed entry: what changed, files touched, verification result, anything discovered.
Note declined proposals.
Add new Deferred entries for structural work this pass surfaced but did not do.
If the work came from chat or a review report, write a fresh ledger for the pass instead (same format), named `refactor-<YYYY-MM-DD-HHMMSS>-<scope-slug>.md`.
Pick its destination in this order:

1. A path given for this run: by the user, a subagent brief, or an agent-bridge brief.
2. A location set by project instructions (AGENTS.md, CLAUDE.md, or the equivalent).
3. The first of `.review/`, `._scratch/`, or `.scratch/` that already exists at the repo root.
4. `$TMPDIR`.

Never create those repo directories; they belong to the user.
If the write fails, put the ledger in chat and say no file was written.

**Rationale goes in the ledger, not the code.**
Do not leave comments narrating the restructuring.

**Ledger IDs are ephemeral.** `T3` addresses an entry in one file.
It never appears in source, comments, commit messages, or PR descriptions.

Then report: moves executed, moves declined, net file and line movement, final verification result, ledger path, and what remains deferred.

## References

- `references/structural-moves.md` — the move catalog: preconditions, procedure, and verification for each operation.
- `references/code-review-graph-integration.md` — graph tool dispatch for blast-radius analysis and post-move verification.
- `simplify` skill, `references/edit-ledger.md` — the ledger format this skill consumes and appends to.
