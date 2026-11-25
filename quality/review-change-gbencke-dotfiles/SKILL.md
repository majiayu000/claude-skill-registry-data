---
name: review-change
description: >
  Evidence-backed PR, branch, or patch review with cumulative finding reconciliation,
  invariant coverage, and propose → challenge → judge steps that each run in a fresh
  pi process via bin/run-phase.mjs. Supports focused verification without whole-PR
  approval. Validates reports before delivery.
argument-hint: "[pr-url|pr-number|branch|patch-file] [base] [--lenses a,b,c] [--verify finding-id,...]"
---

# review-change

You are the orchestrator. Review only: do not apply fixes or run reviewed code.
Read `docs/report-contract.md` from the extension directory. Schema v2 is required.
Relative references in this skill are relative to that directory. Node helpers
belong to the extension, not the target.

You freeze input, collect history, and map coverage. You do **not** play the
reviewer, challenger, or judge: each of those steps runs in a fresh `pi -p`
process launched by `bin/run-phase.mjs`, which injects the `agents/*.md` role pack,
lens rules, and your notes into that child's context. pi has no subagents; a
process per step keeps the phases independent (ADR 0006). All (lens, slice)
tasks share one pool in `bin/run-lenses.sh`, one slot per lens; a free slot takes
the next task of any lens. No `Agent` tool.

Create the work dir first, in system temp and never inside the target:
`WORK=$(mktemp -d -t adversarial-review-XXXXXX)`. Task files and child logs live there.

## 0 — Resolve and freeze the input

Parse target, optional base, `--lenses`, and `--verify`. An empty target means the
current branch; report that choice. Unrecognized prose is **not** a branch or a
license to turn a focused allegation into a full review. Stop with usage instead.
An explicit `--verify` selects finding verification; otherwise scope is the full
change under the selected lenses.

Resolve the absolute Git root as `TARGET_DIR`. Record UTC time, repository, target,
PR number (or null), full `base_sha`/`head_sha`, and the input's intent:

- **PR URL/number:** use `gh pr view` for title, body, head/base names and OIDs.
  Freeze those OIDs; use their three-dot diff when available locally. A live
  `gh pr diff` is usable only if PR OIDs checked before/after it are unchanged.
  GitHub's actual base wins over a stale local `main`. If `gh` fails, stop.
- **Branch:** resolve its commit. Honor an explicit base. Without one, use the
  matching PR's actual base OID; if there is no PR, resolve hosted `main` through
  `gh api`. If freshness cannot be established, request an explicit base rather
  than silently treating local `main` as current. Record commit messages as intent
  and include matching PR title/body when available.
- **Patch:** read it, compute SHA-256, record absolute `patch_path`, use target
  `patch:<digest>` and null Git SHAs. Intent is unknown: solution-fit is
  correctness-only unless the user supplies requirements. State that context is
  limited to what can be matched to the patch, not an arbitrary checkout.

Save the diff as `$WORK/change.diff`. Empty diff: say so and stop.
Use a clean checkout at the frozen head for source context. Read-only Git metadata
checks must confirm it matches; do not checkout, stash, reset, fetch, or modify
refs to make it match. If objects/context are unavailable or the working tree
changes, mark `snapshot_consistent: false` and deliver INCOMPLETE, not approval.
Do not mix current working-tree source with a different reviewed revision.

### Requirements

With JIRA credentials, extract ticket keys from the branch, PR, and commit subjects;
fetch API v2 summary/description/status/type/parent. Never print credentials.
Prioritize the primary story and linked implementation spec; separate inherited
cross-repository requirements from work owned by this PR. A PR number/issue text
is not evidence that a requirement has shipped.

No credentials/no key/fetch failure: record the limitation without stopping.
Exact-head existing CI logs may be read with `gh` to settle test claims. Do not use
old PR-description pass counts or coverage from another SHA as current evidence.
No repository tests/builds or live service/cloud calls are allowed in this skill.

## 1 — Load the cumulative ledger

Before discovery, collect matching history:

```bash
node <extension>/bin/report-tools.mjs collect <TARGET_DIR> <target> [pr-number] > "$WORK/prior.json"
```

Read the resulting ledger, source paths, and relevant prior evidence. Preserve the
collector's `prior_reports` digests. Every known ID must survive, either directly
or as an evidence-backed alias. Do not restart F1 numbering; reuse stable IDs.
Legacy IDs are supplied by the collector. Reconcile wording variants explicitly,
not by guessing that findings in the same file are identical.

Assign each prior issue one of: open, fixed_verified, disproved, deferred,
not_rechecked. Use the closure requirements in `docs/report-contract.md`.
Missing findings are **not** fixed findings. A clean recent report cannot erase
older open concerns. Preserve first-seen date, confidence, severity, and evidence
when a finding is not rechecked. Separate severity from certainty.

For `--verify id,...`, resolve IDs against this ledger (accept a legacy report-local
ID only when the user identifies its source report). Verify only those findings;
carry every other finding as not_rechecked with its prior disposition. No overall
implementation/solution-fit/SHIP verdict is allowed in verification mode.

## 2 — Mechanical impact and behavior coverage

Extract changed exported symbols, routes, flags, data contracts, and action names.
Build the reverse importer/caller map using the repo's indexed analysis or ast-grep
(fallback grep). Record test references separately. Restrict results to TARGET_DIR;
parent-workspace/sibling-repo hits and stale excerpts are not trustworthy coverage.
Record gaps; do not infer no callers or no tests from missing graph results.

Then build a compact invariant/behavior matrix BEFORE proposing fixes:

- Entry point and reachable mode/flag/permission combinations.
- Shared mutable state, **all writers**, and the final consumer/business outcome.
- Success, rejection, cancellation, supersession, replacement, unmount, and
  never-settling work where relevant. Check both safety and liveness.
- Downstream effects: payload sent, state committed, user-visible result, persisted
  operation. Do not stop at an intermediate request if a later callback books.
- Test/assertion or exact-head CI evidence that discriminates the behavior.

For each row record criticality and verified / unresolved / not_inspected /
not_applicable, with evidence or a concrete next check. Do not enumerate impossible
Cartesian combinations; prove render/caller eligibility before claiming a UI race.
An inspected hunk or a listed test name does not by itself verify a behavior.

All diff sections remain in scope. For large changes, group into coherent behavior
slices and explicitly inventory what each slice covers. If the budget is too small,
mark the remaining critical rows uninspected; do not redefine the change as reviewed.

## 3 — Select lenses and discover, then challenge

Read every `lenses/*/lens.md` plus the repo overlay (`run-phase.mjs` appends
same-named overlay rules to each child's context).
Apply all matched lenses. `test-surface` and `blast-radius` always apply to change
reviews; language lenses match changed files only. `--lenses` explicitly overrides
the set. Never prompt for a lens picker. State the selected lenses and scope.
`LENS_SLUG` is the sole lens name or `multi`.

All (lens, slice) tasks run from one shared pool.

1. **Write every task first.** For each lens, for each slice it applies to,
   write `$WORK/tasks/<lens>/<NN>-<slice>.task.json` (`NN` = zero-padded slice
   order):

   ```json
   {
     "id": "<slice>-<lens>",
     "mode": "change",
     "target_dir": "<TARGET_DIR>",
     "work_dir": "<WORK>",
     "lens": "<lens>",
     "scope": "Slice <slice>: <what it covers>. Diff: <WORK>/change.diff. <source line>",
     "paths": ["<changed files in the slice>"],
     "context": "<intent and requirements; ledger rows and stable IDs to reuse; invariant rows; blast-radius callers; queued gaps>"
   }
   ```

   `<slice>` and `<lens>` are slugs (letters, digits, `.`, `_`, `-`). The
   `<source line>` tells the child where pinned source lives:
   - Git target, clean checkout at head: `Checkout is at head <head_sha> (base
     <base_sha>); read files directly; git show <sha>:<path> for base versions.`
   - Patch: `Patch <patch_path> (sha256 <digest>); no pinned SHAs. Context is the
     working tree only where it matches the patch.`

2. **Run all lenses at once:**

   ```bash
   nohup <extension>/bin/run-lenses.sh "$WORK/tasks" > "$WORK/tasks.log" 2>&1 &
   ```

   Poll `$WORK/tasks.log` (sleep between checks, each check under your tool
   timeout) until its `run-lenses: … done` line appears. Each task runs up
   to two children, each limited to 30 minutes (`timeout_seconds`),
   so a single foreground call can outlive any tool timeout.

   Each slot runs `run-phase.mjs pair` per task: a **propose** child
   (`<id>-propose`), then — only if it proposed something — a **challenge**
   child (`<id>-challenge`) that gets the proposal verbatim. Never start the
   judge before every task is done.
3. **Read `$WORK/tasks/manifest.tsv`** (lens, task, exit, result, log). Rows with
   exit 0: append `result` (envelopes; `[]` when nothing was proposed) to
   `ENVELOPES`, sorted by lens then task name (rows arrive in completion order). Read result JSON only to update coverage and queue gaps. Never
   add, rescue, or drop a finding yourself.

**`--verify id,...`:** skip propose and `run-lenses.sh`. For each ID, write
`$WORK/<id>-verify.findings.json` holding that ledger finding verbatim (a
one-element array) and one challenge task: `"id": "<id>-verify-challenge"`,
`"mode": "verification"`, `"lens"`: the finding's first recorded lens (use
`blast-radius` if none is recorded), `"scope": "Verify prior finding <id> at <source
line>"`, `"paths"`: its file plus the files of any claimed fix, `"findings_file"`,
and the claimed fix commit and closure evidence to check in `context`. One child
per finding ID, run one after another with `run-phase.mjs challenge <task>`
(tool timeout ≥ 35 minutes); every envelope goes into `ENVELOPES`.

A non-zero manifest row or exit is a failed step: record those coverage rows as
`not_inspected` with next check `rerun; see <log>` and the matching `.err` files
in `$WORK`. Never retry silently or do the failed phase yourself. Exit 2 means a
bad task file: fix it and rerun that one task (`run-phase.mjs pair <task>`).

Queue uncovered sibling paths/new concerns for one extra pass before judgment:
tasks under `$WORK/tasks-gaps/<lens>/` (new ids), run with `run-lenses.sh` the
same way. Missing reachable source or inspectable CI is an
evidence-gathering task, not a runtime uncertainty. If still unresolved or over
budget, mark coverage incomplete rather than looping or inventing a conclusion.

Put root-cause grouping expectations in the judge `context`: all relevant writers
covered, tests that would fail if the ownership/field guard, error propagation, or
cancellation release were removed. No mutation experiments here.

## 4 — Judge child

Recheck the pinned source/PR OIDs (or patch digest) and recollect history if
another report arrived. Write `$WORK/<LENS_SLUG>-judge.task.json`:

```json
{
  "id": "<LENS_SLUG>-judge",
  "mode": "change | verification",
  "target_dir": "<TARGET_DIR>",
  "work_dir": "<WORK>",
  "envelope_files": ["<every ENVELOPES path>"],
  "prior_file": "<WORK>/prior.json",
  "intent": "<PR title/body, ticket summary, or 'unknown intent (patch)'>",
  "report_md": "<TARGET_DIR>/.gbencke/adversarial-review/reports/<UTCstamp>-<target>-<scope>-<LENS_SLUG>.md",
  "meta": {"target": "<target>", "pr_number": <n or null>, "date": "<UTC ISO, Z>", "head_sha": "<full SHA or null>", "base_sha": "<full SHA or null>", "patch_sha256": "<digest or null>", "patch_path": "<absolute, patch reviews only>", "snapshot_consistent": true, "lenses": ["<selected lenses>"]},
  "context": "<repository, target, pr_number, full base/head SHAs or patch path + digest, UTC date, snapshot_consistent, lenses, scope (full | verify + finding IDs), coverage matrix, blast radius, failed steps with logs, not-reviewed limitations>"
}
```

`scope` in the filename is `full` or `verify`.
`meta` repeats the pinned identity as data. The launcher needs it only when the
judge input is over its budget (about 150 KB of envelopes plus prior ledger):
then shard judges decide in parallel, code assembles the ledger and applies the
gates, and one final judge adds cross-shard merges, coverage and notes (ADR 0007).
A shard that fails is retried once on its own; a second failure ends the judge
step. Same `run-phase.mjs judge <task>` command either way. Verification
judges are never sharded.

Run `run-phase.mjs judge <task>`.
The judge child applies `agents/judge.md` and the v2 gates and returns the sidecar
plus short prose notes; the launcher renders the markdown, writes both files
exclusively and validates them, printing `REPORT: <md>` only on
success. On a validation failure it removes both files; run at most one more
judge with a new `id`, a new timestamp, and the validator errors appended to
`context`. Never remove a prior finding or relabel skipped work to get a green
result. A second failure ends the review without a `REPORT:` line.

## 5 — Deliver

Confirm the published sidecar is still valid (another run may have reported
since), then read it:

```bash
node <extension>/bin/report-tools.mjs validate <absolute-sidecar>
```

If this fails, emit no `REPORT:` line and say why. Chat: scoped verdict (none
for verification), confirmed/uncertain counts, top five findings or targeted
dispositions, incomplete coverage if any, and the report path.
Last line: `REPORT: <absolute-markdown-path>`. The extension validates the
finalized message again; the matrix runner independently checks the artifact.

## Hard boundaries

No subagents: every propose/challenge/judge step is a `run-phase.mjs` child. No
source changes; no repository code/tests/builds; no live services. Read-only
Git/gh/JIRA input gathering and the extension's data-only helpers are allowed.
Scratch belongs in `$WORK`. Keep phases honest and sources pinned.
The release criterion is verified closure within scope, not an empty newest report.
