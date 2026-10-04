---
name: coverage-redo
description: "Re-audit and reconcile a repo that was already onboarded with an OLDER version of this kit, and apply every kit update since. Use when a repo already has a coverage-manifest.yml, generated tests, and a report, and you want to redo/re-run/recheck/reconcile/upgrade/migrate it against the current rules, or to pull in new kit features (latent-bug backlog, vendored-path scoping, baseline scope_lines, dated reports, structured carve-outs): works out the version delta from MIGRATIONS.md and applies it, re-sweeps to spot misclassifications (false exclusions such as DbContext-injected services wrongly frozen, mixed folders collapsed to one glob), corrects the manifest in place, migrates it to the current schema, generates tests only for the newly-found gaps while keeping existing tests intact, and writes a fresh report. Triggers: 'the new dotnet-coverage-kit has new updates, review and apply it to this repo', 'apply the kit updates to this repo', 'the kit was updated', 'upgrade the kit here', 'redo coverage', 're-run coverage-init', 'recheck the manifest', 'reconcile coverage', 'upgrade the manifest', 'fix an old manifest', 'the manifest is from v1'."
---

# coverage-redo

Reconcile a repo that an EARLIER kit version already onboarded. It re-runs the classification
against today's rules, corrects the existing manifest rather than replacing it, migrates it to
the current schema, fills only the gaps in test coverage, and regenerates the report. It is the
idempotent successor to `coverage-init` for repos that already have a manifest, tests, and a
report.

It is also the **kit-upgrade entry point**. "The kit has new updates, review and apply them to this
repo" is this skill, run as a version delta: step 1 works out which kit changes this repo has not
picked up (from `MIGRATIONS.md`) and the rest of the steps apply them. There is no separate upgrade
command and no per-feature request to make: every change since the repo's recorded `kit_version:`
is in scope for one run.

Use `coverage-init` instead when there is NO manifest yet (greenfield). Use this skill when a
manifest exists and may be stale, because the classification rules have improved since it was
written (for example: a constructor-injected `DbContext` is now a testable seam, not an
`integration-scope` exclusion; mixed files must be per-file structured carve-outs, not one
folder glob).

## Non-negotiables

These are what make a redo safe to run on a live repo:

1. **Existing tests are kept intact and reused.** Never delete, rewrite, or "regenerate" a test
   that already exists and passes. The backfill only ADDS tests for spots that are newly in
   scope and not already covered. A reclassification that would orphan an existing test is
   reported for a human to resolve, never actioned by deleting the test.
2. **Correct the manifest, do not rewrite it.** Preserve the human-curated content: the
   `baseline`, the `gate` thresholds, intentional gray-zone exclusions, and every carve-out that
   is still valid. Produce a reviewable DIFF of changes with a reason each, not a fresh file.
3. **Migrate the schema.** Convert legacy `CARVE-OUT:` prose to structured `carve_outs:`, split
   any carve-out-bearing folder glob or multi-file pattern into per-file entries (the gate warns
   on these), and recategorize stale `cannot_test` entries to the canonical natures, adding the
   now-required `mitigation`.
4. **Never silently move the ratchet.** Bringing newly-found testable code into scope grows the
   Adjusted denominator and can lower the recorded coverage. The re-baseline decision is explicit
   and human-gated (step 8). Lowering the floor is a reviewed change, never automatic.
5. **Stop for human confirmation of the corrected manifest BEFORE generating any test** (step 6).
   Generating tests off an unreviewed reclassification is exactly the mistake this skill exists
   to fix.

## Preconditions

Same as `coverage-init`: run on the production branch (master), fast-forwarded to the remote,
with a clean working tree. Additionally:

- **A manifest must already exist** at `.claude/coverage/refs/coverage-manifest.yml`. If not,
  stop and tell the user to run `coverage-init` instead.
- **The existing suite must be green.** Run it first. A reconciliation built on a red suite is
  untrustworthy, and you cannot tell a real gap from a pre-existing failure. If red, stop and
  report the failures.
- **Refresh the installed kit files.** Copy the current `scripts/` (`coverage-gate.py`,
  `run-coverage.sh`, `report.sh`) and `templates/coverage.runsettings` into
  `.claude/coverage/tools/` and `refs/` if they differ from the kit, so the gate and report use
  the corrected logic. Do not touch the repo-owned `coverage-manifest.yml` or `unit-testing.md`
  here; those are reconciled in step 5.

## Steps

1. **Detect the prior state and compute the kit-version delta.** Record what exists: the manifest
   (and any `schema_version`), the test projects and roughly how many tests, the last report, and
   whether the manifest uses legacy prose `CARVE-OUT:` (a v1 signal) or an exclusion that is a folder
   glob carrying carve-outs (an ambiguity the current gate flags).

   Then build the delta, which is what makes "apply the new kit updates" a bounded run. Start with
   the deterministic check (`coverage-gate.py --manifest <manifest> --print-kit-drift`, which prints
   `<current|behind|unstamped|ahead> <manifest stamp> <kit semver>`), then:
   - Read the repo's `kit_version:` from the top of the manifest. Absent means the repo predates the
     stamp: walk **every** entry in `MIGRATIONS.md`.
   - Read the current kit version from `${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/marketplace.json`
     (the `dotnet-coverage-kit` entry). If it equals the manifest's stamp, still run each entry's
     **Detect** check once: a stamp only records what was applied, and a hand-edited manifest can
     have drifted.
   - Walk `${CLAUDE_PLUGIN_ROOT}/MIGRATIONS.md` from the repo's version forward and run every
     entry's **Detect** check against this repo. Detection is authoritative; the version is only an
     ordering hint.
   - Report the delta as one list up front: which entries apply, which are already satisfied.
     Entries marked `auto` you apply yourself in the steps below. Entries marked `sign-off` are
     folded into the SINGLE manifest confirmation in step 6, never asked one at a time.

   **This step is the review the user asked for. Do not stop here for permission to continue**: the
   only gate is step 6.

2. **Re-sweep the whole repo.** Run the classification sweep EXACTLY as `coverage-init` step 4:
   enumerate every source file, clear `coverage/sweep/`, write `files.json`, and run the
   `coverage-sweep` workflow at a user-chosen parallelism with the CURRENT rubric (the table in
   `coverage-init`, including the exclusion-signal principle and the DbContext-seam note). This
   is what surfaces the misclassifications the old manifest baked in. The sweep is read-only on
   source.

3. **Diff the sweep against the existing manifest (single, at main).** Read the on-disk evidence
   (`coverage/sweep/chunk-*.json`) and the current manifest. Produce a reconciliation, not a
   rewrite. Apply **every `MIGRATIONS.md` entry whose Detect check fired in step 1** in this same
   pass: the bullets below spell out the ones that come up most often, and the ledger is the complete
   list (the ledger wins if the two ever disagree). Classify every delta into:
   - **False exclusion to fix:** the sweep found a testable method inside a file the manifest
     excludes (the DbContext-injected-service case, a mixed folder collapsed to one glob, a
     branching validator under a `**/Model/**` glob). Add the carve-out, or promote the file to
     `target`, per the current rubric.
   - **Schema migration:** legacy prose `CARVE-OUT:` becomes a structured `carve_outs:` list;
     a carve-out-bearing folder/multi-file pattern is split into one per-file entry each with its
     own `carve_outs` and `excluded_rest`; a `cannot_test` entry with a non-canonical category is
     moved to the canonical nature and given a `mitigation`. A manifest with no `target` block is
     given the default (C0 95% / C1 85% on the Adjusted slice) so the report reads against the goal;
     the existing `gate` and `baseline` are preserved (raising the diff gate to the target is a
     reviewed change, not automatic).
   - **Add the `scope` block if the manifest has none** (every manifest written before it existed).
     Set `scope.file_filter` to the expression the repo's CI workflow currently passes to
     `run-coverage.sh`, verbatim, including its exclusions. Reading it out of CI is the point: for
     older repos the exclusions live *only* there, so local runs have been measuring a different
     file set than CI all along, and copying it in is what ends that split. Then check the repo for
     shared libraries copied in as directories and list them in `scope.vendored_paths`.
   - **Stamp `baseline.scope_lines`** from the "Total lines (Adjusted)" denominator of the report
     produced in step 7, so the gate can tell a scoping mistake from a regression. Do this even
     when preserving an existing floor: the floor and the scope size it was measured against belong
     together, and a floor without one is why an inflated denominator reads as lost coverage.
   - **Migrate frozen bugs into `latent_bugs:`.** A manifest written before that block existed
     recorded suspected defects, if at all, as prose in an old report's Observations section or
     appended to `CANNOT-TEST.md`. Both are lost on the next `report.sh` run, so treat any you find
     as unrecorded. Sweep the existing test suite for tests that assert a bug on purpose (names like
     `..._ThrowsRuntimeBinderException` or `..._IgnoresCurrentStudioFilter`, or an assertion whose
     expected value is plainly wrong) and give each a `latent_bugs:` entry with its `pinned_by` test.
     This is what stops a green suite from being read as a correct one.
   - **Check for newly VENDORED reference projects.** An org moving shared libraries out of sibling
     checkouts and into each consumer repo is a common change between an onboarding and a redo, and
     it is invisible to a manifest written before the move: the directory is new, it sits under the
     repo root, and the `+*<repo>*` include swallows it. Look for directories that are copies of
     another repo (own `.sln`, own README, assembly names following another repo's convention) and
     list each in `scope.vendored_paths`. Then confirm the sweep did not classify anything inside
     them, and DELETE any target, carve-out, or `cannot_test` entry that points into one, since a
     prior run may have generated tests for foreign code. Those deletions are the one case where
     removing an existing test is correct, so call them out explicitly in the step-9 report.
   - **Preserve:** an exclusion the sweep still agrees with, a still-valid carve-out, the
     `baseline`, and the `gate` block are carried over unchanged.
   - **Gray zone:** a genuine disagreement (vendored-vs-product, a host blanket that may hide a
     slice) is carried into the step-9 report as an explicit question, not resolved silently.
   Apply `coverage-init` step 5's pattern-vs-path verification to every new or split pattern.

4. **Guard the existing tests.** For every reclassification, check the existing test files: a
   method moving INTO scope that already has a carve-out test means that test now counts toward
   Adjusted (reuse it, intact). A method moving OUT of scope that has a test is a potential
   orphan: flag it in the report, do not delete it. Assert that no existing, passing test is
   invalidated by a manifest change; if one is, that delta is a question for the human.

5. **Critique the reconciled draft (single, not parallel).** Run `coverage-init` step 6's
   cross-project self-critique on the corrected manifest and the sweep evidence, with two added
   checks specific to redo: (a) no existing test was orphaned by a reclassification, and (b) the
   migration is complete (no prose `CARVE-OUT:` and no carve-out-bearing multi-file pattern
   remain). Reconcile clear-cut corrections in a loop; leave only genuine gray zones.

6. **Write the corrected manifest and STOP for confirmation.** Write the reconciled, migrated
   manifest (do not clobber without showing the diff). Present the diff grouped as: kit updates
   applied (each `MIGRATIONS.md` entry, with its version and whether it was `auto` or needs
   sign-off), false exclusions fixed, schema migrations, entries preserved, and open questions. Every
   `sign-off` item from the delta is presented HERE, in this one gate, together with the sweep
   corrections. Ask the user to confirm or correct before any test is generated. This is the hard
   gate: do not proceed to step 7 in the same turn without confirmation.

7. **Generate tests for the NEW gaps only, and run it to completion.** Run `generate-tests` in
   characterization mode (this is existing code: freeze current behavior) with the reconciled
   manifest. Its worklist is the newly-in-scope carve-outs and targets; items already covered by
   existing tests are checked off and left untouched, per that skill's rules. Untestable-as-is units
   are routed to `cannot_test` with a `mitigation`, exactly as in a normal backfill.

   **The manifest confirmation in step 6 is the ONE gate. After it, execute autonomously.** For a
   large newly-found backlog, fan it out with the parallel backfill: ask the user for the agent
   count ONCE (or default to 3 on "go"), then run the fan-out to completion. Follow the
   `generate-tests` fan-out contract EXACTLY (write `coverage/backfill/worklist.json` first and
   confirm it is non-empty; pass `args` as a JSON object with `worklistManifest`, never an inline
   `worklist` and never a stringified payload; invoke via `scriptPath`). Do NOT re-ask per batch,
   re-explain the plan between phases, fresh-relaunch a run that can be resumed, or drop back to
   sequential `Agent()` calls: those are the exact behaviors that turned a real redo into dozens of
   back-and-forth turns. The goal is "every testable part has a branch-covered test or a cited
   `cannot_test` entry"; keep going until that holds, reporting progress, not asking permission to
   continue.

8. **Re-baseline decision (explicit, human-gated).** Re-measure with `coverage-report`. Because
   newly-in-scope code entered the Adjusted denominator, the recorded coverage may have moved.
   Present the old floor and the new measured Adjusted, and ask the user which to record. Never
   lower `baseline.recorded_overall` automatically; raising it (once the new gaps are covered) is
   the normal outcome.

9. **New report and comprehensiveness gate.** Regenerate the dated `reports/<YYYY-MM-DD>/REPORT.{md,html}` + `CANNOT-TEST.md` via
   `report.sh`. Assert `coverage-init` step 11's comprehensiveness gate PLUS the redo-specific
   ones: every enumerated file accounted for, no orphaned test, migration complete (the gate's
   ambiguous-carve-out warning is empty). Report the before/after: files reclassified, carve-outs
   added, tests generated, tests reused unchanged, and the coverage delta.

   **Stamp `kit_version:` at the top of the manifest** with the version read in step 1, and list
   every `MIGRATIONS.md` entry applied in this run. The stamp is what makes the NEXT upgrade a small
   delta instead of a full walk, so it is written only after the entries actually landed: never stamp
   a version whose entries were skipped, deferred, or left as open questions. If the user declined a
   `sign-off` item, keep the older stamp and say which entry is still outstanding.

   Then stop and hand the human the summary and any open questions.

## What this skill reuses (do not re-specify)

- Sweep enumeration, parallelism prompt, and evidence-to-disk contract: `coverage-init` step 4 +
  the `coverage-sweep` workflow.
- Synthesis, pattern-vs-path verification, and the cross-project critique: `coverage-init`
  steps 5 and 6.
- The backfill loop, characterization vs spec mode, and the parallel backfill: `generate-tests`.
- Measurement, the report, and the baseline contract: `coverage-report` and `coverage-gate.py`.

## Base references
- `${CLAUDE_PLUGIN_ROOT}/MIGRATIONS.md` (the version-delta ledger read in step 1)
- `${CLAUDE_PLUGIN_ROOT}/skills/coverage-init/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/generate-tests/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/coverage-report/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/rules/unit-testing.base.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/coverage-manifest.yml`
- `${CLAUDE_PLUGIN_ROOT}/workflows/coverage-sweep.workflow.js`
