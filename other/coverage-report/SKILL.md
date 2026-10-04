---
name: coverage-report
description: "Produce the latest deterministic C0/C1 coverage report for a .NET service. Use when the user asks for a 'coverage report', 'coverage status', 'what's covered', 'C0 C1 numbers', or wants to check the gate. Runs dotnet-coverage + ReportGenerator (numbers are tool output, never estimated), then joins uncovered files against the manifest to explain every inclusion, exclusion, and cannot-test entry. Runnable any time."
---

# coverage-report

Numbers come only from the tool. The model never estimates, infers, or rounds coverage.
The model's only role is joining tool output to the manifest's reasons and narrating the
observations section.

Read `${CLAUDE_PLUGIN_ROOT}/rules/coverage-report.base.md` and the repo's
`.claude/coverage/refs/coverage-manifest.yml` first.

## One command, any time

The whole report is one wrapper — no arguments needed (it auto-detects the `.sln`):

```
./.claude/coverage/tools/report.sh
```

It collects coverage, joins it against the manifest, and **writes a dated per-run folder
`.claude/coverage/reports/<YYYY-MM-DD>/` containing `REPORT.md`, `REPORT.html`, and
`CANNOT-TEST.md`**, then prints the Markdown. It exits non-zero only for a check named in the
manifest's `gate.enforce` (empty by default, so a breach prints as `ADVISORY` and the script still
succeeds); a failing build or test run is fatal regardless, from `run-coverage.sh`. Each run writes its own dated folder rather than overwriting a fixed
path, so prior dates are preserved for comparison; override the date with `REPORT_DATE=YYYY-MM-DD`
to re-emit under a specific day. `CANNOT-TEST.md` is generated from the manifest `cannot_test`
entries (grouped by blocking construct, each row citing target, reason, and unlock), not
hand-written. This is the *identical* join CI runs — the report a developer sees locally is the report on
the PR. When invoked as the `coverage-report` skill, just run it and surface the result;
don't re-derive numbers by hand.

## Steps

1. **Run the wrapper.** `./.claude/coverage/tools/report.sh` (or, before init has copied it,
   `${CLAUDE_PLUGIN_ROOT}/scripts/report.sh`). Pass a solution path or repo-filter only if
   auto-detect is wrong. If the tools or solution are missing, report that — never fabricate
   numbers. All numbers come from the tool + the deterministic join in `coverage-gate.py`; the
   model does not parse XML or compute percentages.

   The script prints `KIT_VERSION=`, `KIT_DRIFT=` and `FILE_FILTER=` before collecting. **Check all
   three.** `KIT_DRIFT=` is `<state> <manifest kit_version> <kit semver>`: any state other than
   `current` means this repo has not been reconciled against the current kit, and the report carries
   a note saying so. **Surface it in one line and name `coverage-redo` as what applies it. Do not
   apply any migration here**: a report that quietly changed the measured scope would make its own
   numbers unreproducible. The one exception is the stale-tool-copy refresh below, which changes no
   classification. See `${CLAUDE_PLUGIN_ROOT}/MIGRATIONS.md` ("Preflight"). Stale
   tool copies no longer need asking about: `report.sh` runs `kit-sync.py` first, which installs the
   current copies and applies the `auto` manifest entries, printing `[kit-sync]` lines for each. Relay
   those lines and remind the user to COMMIT the changed files, since CI runs the committed copies and
   not their kit checkout. If the sync printed nothing, the repo was already current. If `FILE_FILTER` lacks an
   exclusion for a shared directory that is present in the repo, stop and fix
   `scope.vendored_paths` before trusting the number.

2. **Latent bugs are DATA, not narration.** The script's report is complete and deterministic
   (verdict, headline, Do-next, insights, by-bucket, and the red section 7). Suspected bugs frozen
   by characterization belong in manifest `latent_bugs:`, where `coverage-gate.py` renders them as
   section 7 plus the ACTION REQUIRED banner. Put them there, not in a hand-written section: the
   report is regenerated on every run, so appended prose is lost, and a defect backlog that
   evaporates is worse than none. Verify the banner's A/B/C count matches what the backfill found,
   and add no narrated section of your own.

3. **At baseline only.** Write the measured Adjusted overall into `baseline.recorded_overall`
   (with `basis: in-scope`) so it becomes the ratchet floor. Not on ordinary report runs.
   Stamp `baseline.scope_lines` at the same time, from the report's "Total lines (Adjusted)"
   denominator. It is what lets the gate distinguish a real regression from a filter mistake:
   without it, a scoping error presents as a coverage collapse and the ratchet blames the tests.

## Report shape — the Unit Test Report (produced by `coverage-gate.py`)

Fixed six-section report card. Header carries commit / branch / date / tooling / verdict;
coverage is two-pass throughout — **Adjusted** (target set, the headline + ratchet basis) and
**Raw** (all instrumented), for C0, C1, and Method.

```
# Unit Test Report — <repo>
<commit · branch · date · tooling · verdict (gate PASS/FAIL · Adjusted C0/C1)>

## 1. Test Results     total / passed / failed / skipped / flaky / duration (from .trx)
## 2. Coverage Summary Raw | Adjusted | Baseline | Δ, for C0 / C1 / Method; + the Gate block
                       (ratchet always; diff-coverage + scope-change guard in PR mode, --base)
## 3. Coverage by Layer columns: Layer | Raw lines | Raw branches | Testable lines |
                       Testable branches | C0 | C1 — where C0/C1 cells are "NN% (covered/total)"
                       over the testable slice (covered counts fold into the cell, no separate
                       covered columns). Rows are
                       human LAYER names (Application/Service — TARGET, Infrastructure/Integration,
                       Presentation/Workers, Models/DTOs, Generated, Non-product) mapped from the
                       manifest categories — NEVER the raw `excl: <category>` strings (an `excl:` row
                       showing a coverage % read as "excluded but covered??"). Raw = all code in the
                       layer; Testable = its unit-testable slice (whole file in the target layer; only
                       carve-out methods elsewhere); C0/C1 are of the testable slice. Only the target
                       layer feeds the Adjusted headline. + a per-file table (same columns + the file's
                       Layer) so a 1631-line infra file reading as 131 testable lines is clear.
## 4. Risk Hotspots    methods with complexity ≥5 and coverage <80%, sorted TARGET-FIRST, with a
                       "What to do" column + per-bucket guidance (target=unit-test; integration=
                       integration test/extract carve-out; e2e=E2E/refactor) and a takeaway line
                       calling out how many are real in-scope unit gaps. Methods already in
                       cannot_test are omitted (they belong to §6, not shown as gaps).
## 5. Excluded Code    manifest exclusions grouped by category — mechanism = "manifest pattern"
## 6. Not Testable     split by nature: 6a Design debt (seam-fixable, should trend to zero) ·
                       6b Structural (compiler/unreachable/dead/framework-mismatch — will NOT move).
                       Columns: target · where (lines) · why · category · mitigation. A systematic-
                       seam callout quantifies clusters (e.g. "N share Guid.NewGuid → one seam").
## 7. Latent bugs   (rendered from manifest `latent_bugs:`) red, ACTION REQUIRED, if any
```

Honest-reporting rules baked into the generator (do not "fix" these to mimic a different stack):
- **Tooling** reflects the real collector — Microsoft Code Coverage (`dotnet-coverage`) +
  ReportGenerator + xUnit — *not* Coverlet (dormant in this kit).
- **Mechanism** (section 5) is the manifest join applied at report time; source is never
  annotated with `[ExcludeFromCodeCoverage]` and coverlet `--exclude` is not used.
- **Flaky** (section 1) is `—`: a single non-retry run cannot observe flakiness.
- **Layers** (section 3) are the repo's actual buckets, architecture-driven — not a fixed
  `Domain`/`Application` template.

Numbers (sections 1–4) are tool output joined deterministically; the model never edits them.
The full per-file drill-down lives in the HTML report — the Markdown is the executive view.

## Approving a scope change (reviewer sign-off)

Read this only while `scope` is one of the enforced checks (`gate.enforce` in the manifest). With
enforcement off, a scope breach is reported as `ADVISORY`, the run is green, and no label is needed
or useful; review the reported breach on its merits instead.

The `coverage-scope-change` label is the reviewer sign-off for an intentional scope reduction. It
maps to `coverage-gate.py --allow-scope-change`. Applying it waives only the **scope-change guard**
(grown `exclusions`/`cannot_test`, new **product** source under an excluded path) and a **lowered
ratchet floor**. It does NOT waive diff coverage on changed lines, nor a genuine ratchet drop below
the recorded floor. Those still fail the gate.

**A PR that only adds tests never needs this label.** The guard skips added test files and reports
how many it ignored. If it flags one anyway, the repo is on a kit older than 0.14.0 (refresh
`.claude/coverage/tools/`) or its tests sit somewhere the directory heuristic misses, which is what
`gate.test_path_patterns` is for. Reaching for the label there is the wrong fix: it waives the whole
guard for that PR, including any real scope reduction riding along with it.

To sign off, **ADD the label** (its name must be exactly `coverage-scope-change`). This is where a
real reviewer got stuck, so state it plainly:
- The workflow triggers on `labeled` (see the template), so adding the label **starts a fresh run**
  whose event payload contains the label. That run reads the label and passes.
- Do **NOT** click "Re-run jobs" to pick up a just-added label. GitHub "Re-run" replays the
  ORIGINAL event payload, which had no label, so the `contains(...labels...)` check stays false and
  the gate fails again, confusingly.
- If your workflow's trigger lacks `labeled` (an older scaffold), push any commit or toggle the
  label off and on to force a `synchronize` run whose payload includes the label.
