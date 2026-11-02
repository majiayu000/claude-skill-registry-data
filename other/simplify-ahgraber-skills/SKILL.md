---
name: simplify
description: |-
  Use to cut slop out of working code: duplication, dead code, needless indirection, comment noise, defensive padding. Point it at the current changes, a file, a directory, or the whole repo. Triggers: 'simplify this', 'clean this up', 'de-slop this code', 'strip the cruft', 'tighten this diff', 'this code is bloated', 'audit this for slop'. Not for judging correctness or merge readiness (use code-review), and not for structural change that needs a plan and approval (use refactor).
---

# Simplify: Remove Slop from Working Code

## Overview

Simplify assumes the code is correct and asks whether it is as simple as it could be.
It exists because models drift additively: left alone, agent-written code accumulates verbosity and structural padding that prompting alone does not prevent.
This skill is the recurring corrective pass.

Ask the user which mode to use:

- **audit** mode to report findings but make no changes.
- **fix** mode audit, then apply safe edits and preserve behavior exactly.

Scope is configurable: the default is the current change set, but a file, a directory, or the whole repo are equally valid targets when the user names one.

Every pass ends with a report persisted to a dated file: a path given for this run, else a location set by project instructions, else the first existing `.review/`, `._scratch/`, or `.scratch/` at the repo root, else `$TMPDIR` (see `references/edit-ledger.md`).
The file matters most for deletions, because a diff shows what was removed but cannot carry why removing it was safe.

Anything a configured linter or formatter already flags is out of scope.
Run the tool instead, and review only what those tools cannot check.

## When to Use

- Code is written, tests pass, and it needs cleaning before anyone reads it.
- A change works but feels padded: wrappers on wrappers, checks that cannot fire, flags with one caller.
- A feature was deleted, and the code that only served it needs to go too.
- The comments in a change are noise and need auditing, or its docstrings narrate the function bodies instead of stating the contract.
- Someone wants to know how much slop is in a file, a package, or the repo before deciding whether to touch it.

## When Not to Use

- Judging code belongs to `code-review`: correctness, edge cases, security, test adequacy, merge readiness.
- Structural change that needs a plan belongs to `refactor`: decomposing a large function, splitting a module, breaking an import cycle.
- If the tests are red, stop.
  Simplify assumes the code is correct; if it is not, the findings are irrelevant and the edits unsafe.
- Simplify never adds capability.
  New behavior is a different task.

## Invocation Notice

- Tell the user when this skill is running: `simplify`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## What Goes Elsewhere

When a lens agent surfaces one of these, record it in the ledger and tell the user.
Do not act on it here.

| Finding                                              | Belongs to                              |
| ---------------------------------------------------- | --------------------------------------- |
| Wrong behavior, broken contract, unhandled edge case | `code-review`                           |
| Missing or incorrect error handling                  | `code-review`                           |
| Security exposure                                    | `code-review` (via `securing-code`)     |
| Tests absent, inadequate, or asserting internals     | `code-review`                           |
| Concurrency defects, leaks, hot-path cost            | `code-review`                           |
| Docs or specs describing behavior that changed       | ledger suggestion; user decides         |
| Function decomposition, module split, layering fix   | ledger Deferred; `refactor` can execute |

Excess belongs to simplify; absence belongs to code-review.
For example, error handling that catches and re-raises unchanged is a simplify finding, and missing error handling is a code-review finding.

## Edit Tiers

Classify every finding before applying anything.
Audit mode applies nothing, and the tiers still hold: they record which findings a fix pass would take on the spot and which need a decision from the user first.

**Tier 1 — apply directly — is any edit whose behavior preservation you can verify right now**, with the check established in Phase 0, within the stated scope.
Deleting dead code, collapsing a forwarding wrapper, flattening nesting with a guard clause, fixing a stale comment, unifying duplicated logic: all Tier 1 when the verification passes afterward.

**Tier 2 — record as a proposal, never apply** — is everything you cannot verify now, plus these regardless of verifiability:

- It changes an exported signature or public API, including deleting an export.
- It requires editing an existing test's assertions to pass.
- It conflicts with a spec.
- It removes something that still has a consumer.

Tier 2 items go to the ledger's Deferred section with a proposed move, a blast-radius estimate, and a verification plan.
They are proposals for the user; the `refactor` skill knows how to execute a Deferred list, but nothing obligates that path.

If an edit needs a test's assertions changed to pass, the behavior changed.
Revert it and record it as Tier 2.
Fixing a stale comment or a typo inside a test file is an ordinary Tier 1 edit; the rule guards assertions, not file paths.

## Verification Levels

A Tier 1 edit is safe only when verification can confirm it.
Establish the strongest available check before editing, and use it for every edit:

1. **Full test suite** with the relevant code exercised.
2. **Typecheck plus lint**, when no suite exists or it does not cover the target.
3. **Characterization test** written before a risky edit to pin current behavior; it stays afterward.
4. **Parse and import smoke checks**, when the repo has no checks at all.
5. **Report-only.**
   If nothing above is available for the target, do not edit it; record the finding instead.

Record the check in the ledger header.
If a check fails after an edit and the failure looks unrelated, re-run once before attributing it to the edit.
For a risky deletion whose safety rests on a covering test, confirm the test actually guards it: break the invariant deliberately and check the test fails.

## Removal Rule

Agent-written code accumulates unused parts, so removal is the default.
For a candidate with no consumer and no live reason, remove it unless you can name a reason to keep it.

Ask two questions of every removal candidate:

1. **Who consumes this?**
   A caller, a test that asserts its behavior, a spec clause, a documented public entry point, a runtime hook.
   Static search is not sufficient to answer "nobody": also sweep text — string-keyed dispatch, config keys, entry-point declarations, fixtures, templates, serialized data, environment examples.
   Code registered by string does not appear in the import graph, so a static search misses it.
2. **If nothing consumes it, does history reveal a reason that still applies?**
   Read blame, the introducing commit, and adjacent comments.
   A platform quirk that is still shipped, a workaround for a bug still open: keep, and record the reason.
   A shim whose other side is gone: the reason expired; remove.

Record both answers in the ledger.
If both return empty, audit should propose the removal, while fix should process the removal.

Boundary cases:

- **Compatibility with unshipped code is not protected.**
  A shim or interface that only ever existed within the current unshipped work is not a consumer; delete it on sight.
  If a piece of code only makes sense to someone who watched this session happen, it is overfitted.
- **Deleting any exported symbol is a public API change**: Tier 2, whatever the consumer search says.
- **A guard needs evidence.**
  Absence of failure and absence of the hazard look identical from the outside.
  If you cannot show the hazard is impossible, keep the guard and record the doubt.

**Report the direction of travel.**
State what was removed and what was added, and if the pass grew the surface area, say why.
Never delete to move a number; line count is a report, not a target.

## Phase 0 — Gate

### 1. Mode

**Mode** decides whether the pass ends at the ledger.
Do not assume the mode based on context; the user must name it (elicit if unspecified).

Recommend fix as the default for a file- or change-set scope, and audit as the default for a directory or repo scope.

### 2. Scope

Take the scope the user named: a file, a directory, the repo, or a change set (elicit if unspecified).
When the scope is the current changes (the default), run `scripts/build_review_packet.py` to resolve it deterministically and pre-bake one packet — diff plus changed-file list — that the lens agents read by path.
Fall back to `git diff` or `git diff HEAD` for a manual change set; with no git changes and no named scope, use the files edited earlier in this conversation.
For a file, directory, or repo scope, the file list is the packet; note that broad scopes deserve narrow lens selection or the pass sprawls.

### 3. Lens selection

**Lenses** are independent, and a user may only want one.

| Lens                   | Covers                                                                                                                                 | Reference                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Duplication & reuse    | Code that re-implements something the codebase already has; near-duplicate blocks; a value computed or read more than once in one path | —                                    |
| Obfuscative complexity | Indirection without abstraction, premature generalization, special-casing shared code, action at a distance, defensive noise, ceremony | `references/obfuscation-patterns.md` |
| Removal                | Dead code, orphans, shims whose other side is gone, branches on now-constant flags                                                     | Removal Rule above                   |
| Comments               | Narration, restatement, staleness, point-in-time rot                                                                                   | `references/comment-audit.md`        |
| Docstrings             | Implementation narration where the contract belongs, restated signatures, staleness                                                    | `references/docstring-audit.md`      |
| Semantic naming        | Misleading names, one concept under several names, semantically duplicated constants                                                   | —                                    |
| Data representation    | Structures that can represent invalid states, replicate information, or leave every consumer to enforce their rules                    | `references/data-representation.md`  |

Refer to lenses by name everywhere: in dispatch, in the ledger, and in anything the user reads.

When one path computes or reads the same value more than once, the fix reuses the first result.
Reusing a read is Tier 2 unless the finding shows the data cannot change between the two reads, because reuse changes how fresh the value is.

Semantic naming covers only what a linter cannot: a `get*` that mutates, the same value named three ways across layers, the same constant defined twice with different spellings.
Stylistic naming and formatting stay with the linter.

Data-representation findings are Tier 2 by default.
Changing a data structure changes an exported signature, a stored format, or both, so the check cannot confirm preservation on the spot.
Record the proposal and let `refactor` execute it.
The exception is a type used nowhere outside the scope and never stored or sent anywhere, which is rare enough to justify each time.
The data-representation lens also differs from the others in what it must return: a finding needs its test results, not a description of the shape.

If the request already names a concern, run the matching lenses and say which you selected.
Otherwise ask which to run, offering all seven as the default.
Do not fan out seven agents on a request the user meant narrowly.

State the mode and the lenses back before Phase 1 starts.
Never switch modes mid-pass: an audit that turns up an obvious fix stays an audit, and the user can ask for the fix pass next.

### 4. Baseline

Find the codebase's tests and checks and establish the strongest check available by running all - tests, checks, lint rules, etc.
If the suite exists and is red, stop and report; without a green start, no later failure is attributable.
Record the baseline test and check run with the associated commands and results in the ledger.

### 5. Specs

Look for a spec source: an `openspec/` or `specs/` tree, or artifacts from the `sdd` family.
When one exists, every edit must leave the code compliant with it.
Suggested spec revisions go in the ledger, and this skill never applies them.

## Phase 1 — Triage

Read the scope to understand what the code is doing and why.
Intent matters: code that looks over-built can be implementing a requirement the diff does not show.

## Phase 2 — Lens Agents

Dispatch one agent per selected lens, all in a single message.

Give each agent the packet path (or file list), its lens reference, the Edit Tiers rules, and the Removal Rule.
Tell each agent the scope is a floor and not a ceiling: the duplication lens's search for existing utilities is inherently outside it, and the removal lens must check consumers across the whole repo.

**Agents report; they do not edit.**
This constraint holds regardless of audit/fix mode: parallel edits conflict, and verification has to run against one coherent state.
Dispatch, tiering, and the removal proof are the same in audit mode; only Phase 3 differs.

Each finding comes back with the file and line, the lens, what to change, why, and a tier with the reason for that tier.
An agent that cannot justify Tier 1 assigns Tier 2.

## Phase 3 — Resolve Findings

Both modes start the same way: aggregate the findings, drop duplicates across lenses, and re-check every Tier 1 classification yourself.
An agent that wants its finding applied has an incentive to under-report blast radius.

**Audit mode stops with aggregation and reporting.**
Write the ledger per `references/edit-ledger.md` in its audit shape: every finding recorded, nothing applied, and the tier kept on each entry, because the tier is what tells the user which findings a later fix pass takes without a decision from them.
Do not edit a file, not even a one-word comment fix.

**In fix mode, continue:**

1. Apply Tier 1 edits **one at a time**: make the edit, run the check, then move on.
   A failure attributes itself to the edit that caused it.
2. On failure, revert that edit and reclassify it as Tier 2 with the failure recorded.
   Do not weaken an assertion, relax a type, or skip a test to get to green.
3. Write the ledger per `references/edit-ledger.md`.

Group trivially independent edits (comment deletions across files) into one verification step when running checks per edit would be absurd; the unit of revert is then the group.

Skip a false-positive finding and record it in the ledger's Skipped section.
Do not argue with it.

**Rationale goes in the ledger, not the code.**
Do not leave a comment explaining what you removed or why you changed something.
The reader has the ledger next to the diff, and a comment narrating this pass is accurate for one commit and misleading afterward.

## Phase 4 — Report

Tell the user, briefly:

In audit mode:

- What was found, grouped by lens, and how many of those findings a fix pass would apply without asking (the Tier 1 count)
- The largest removal candidates, and the lines each would take out
- What is in Deferred, and the ledger path
- The check a fix pass would run, and its result if you ran it
- That nothing was changed, and that a second pass in fix mode applies the Tier 1 findings

In fix mode:

- What was applied, grouped by lens
- What was removed, and the net line movement
- What is in Deferred, and the ledger path
- The check, with baseline and final results

Deferred items are proposals: the user decides what happens to them, and `refactor` is one way to execute the structural ones.
Do not start that work here.

## References

- `references/edit-ledger.md` — the persisted report: location, sections, and the deletion-proof format.
- `references/obfuscation-patterns.md` — obfuscative-complexity pattern catalog with the disconfirming test for each.
- `references/comment-audit.md` — comment keep/delete/fix criteria and the docstring boundary.
- `references/docstring-audit.md` — the caller test for docstrings: contract vs. implementation narration, and what consumes a docstring before you edit it.
- `references/data-representation.md` — data-representation tests, where to look, and the evidence each finding must carry (shared with `code-review`).
