---
name: security-scan
description: |-
  Use when the user asks for a security scan or review of a repository, a scoped path (package, folder, or submodule), or a Git-backed change set (pull request, commit, branch diff, or working-tree patch). Point it at the target; it runs the full threat-model, discovery, validation, and attack-path pipeline and writes a report. Do not use to triage externally supplied findings or to fix a single finding.
metadata:
  short-description: Security scan (repository, scoped path, or diff)
---

# Security Scan

Audit a target for security vulnerabilities, keep the phases separate, and produce final markdown and JSON reports.
Resolve the target mode first, then run the shared pipeline with that mode's scope rules.

## Modes

Resolve exactly one mode from the request before substantive work:

| Target the user names                                      | Mode          | Capability profile   | Scope reference                                                              |
| ---------------------------------------------------------- | ------------- | -------------------- | ---------------------------------------------------------------------------- |
| Whole repository, or a path / package / folder / submodule | repo / scoped | `security_scan`      | `references/repository-wide-scan.md` (and the repo-wide references it lists) |
| Pull request, commit, branch diff, or working-tree patch   | diff          | `security_diff_scan` | `references/scan-scope-diff.md`                                              |

## Capability Preflight

Read `references/config-preflight.md` and run the preflight with the capability profile for the resolved mode (`security_scan` for repo/scoped, `security_diff_scan` for diff) before substantive scan work.
Follow the returned block/warn/suggest/ready results.
On a `blocked` or `incomplete` result, present the exact reasons and advisory guidance to the user and ask before proceeding; do not auto-fail.
Do not treat a config value that differs from a suggested patch as a warning unless the capability requirement itself is unmet.

## Scope and Cost Gate

This scan is exhaustive — it deep-reviews files with one file-review subagent per file (or tiny shard), so the work scales with the number of files reviewed.
After the capability preflight returns `ready` and the target and mode are resolved, and before any substantive (model-heavy) work — threat model, ranking, or dispatching file-review subagents — scope the work with the scaling rule, present it, and get explicit approval.

1. Build the cheap, deterministic file inventory (no model work).
   For repo/scoped: `<python_command> <plugin_dir>/scripts/generate_rank_input.py make-repo-rank-input --repo <repo_root> --scope <scope> --out <discovery_dir>/rank_input.jsonl` — its row count is the in-scope source-like file count.
   For diff: `make-diff-rank-input` — its rows are the changed files, all deep-reviewed.
   Reuse this `rank_input.jsonl` in discovery; do not regenerate it.
2. Scope the work with the scaling rule: repo/scoped ≈ `files × planned top-percent / 100` files getting full-file review (about one file-review subagent pass each), plus ranking, validation, attack-path, and report; diff ≈ the changed-file count.
   You may also give a rough input-token count for one full review pass as the total size of the in-scope files in characters divided by about 4 (the ~4-chars-per-token rule), times the pass count.
   Report token counts, not money — do not estimate a dollar cost; that depends on token pricing, model, and input/output/cache ratios that change.
3. Present the scope plainly: target and mode, in-scope file count, planned `top-percent`, the approximate number of file-review passes, and the optional token-count figure.
   Then stop and wait for the user's explicit approval (for example "proceed") before starting the threat model, ranking, or any file-review subagent.
   This is a binary go/no-go on the scan as scoped — do not propose narrowing the scope, lowering `top-percent`, or switching modes.
   Silence or a vague "scan my repo" is not approval; proceed without waiting only if the user's request already explicitly approved this scope.

## Phase Sequence

Keep these phases distinct and run them in linear order.
Each phase is a reference in this skill:

1. `references/phase-threat-model.md`
2. `references/phase-finding-discovery.md`
3. `references/phase-validation.md`
4. `references/phase-attack-path-analysis.md`
5. Generate final output

For each phase: read that phase reference, load only the inputs it requires, complete its workflow and checklist, then read the next.
Do not read ahead into later phases until the current one has completed.
Do not amortize effort across phases.
Treat explicit invocation of this scan as the user's authorization to use the subagents the workflow requires; if subagents are unavailable, explain the limitation instead of claiming exhaustive coverage.

## Artifact Resolution

The path references in this skill are default locations.
If the user explicitly provides a different path for a required input or output, use theirs instead.
If a required input is still missing, stop and ask.
Use the shared artifact path conventions in `references/scan-artifacts.md`.

## Goal Setup

After the capability preflight returns `ready`, if your host has goal/todo/task-tracking tools, create a goal capturing the coverage objective; otherwise state the same objective in your first visible update and track it yourself.
The objective should state that the scan must not stop until the resolved in-scope files/worklist rows are covered and the required coverage artifacts prove that closure.

If a compatible active goal already exists, continue under it instead of creating a duplicate.
Do not mark the goal complete until:

- every in-scope file or worklist row has a completion receipt, or an explicit `deferred`, `not_applicable`, or `suppressed` closure with exact reason (repo/scoped closure: `references/repository-wide-scan.md`; diff closure: `references/scan-scope-diff.md`)
- every candidate that reached discovery has the required discovery, validation, and attack-path ledger receipts, or an explicit deferred reason for the missing proof
- the final markdown report has been written to the resolved scan path

## Execution Plan

Start this plan only after the capability preflight has returned `ready` and the `Scope and Cost Gate` has been approved by the user.
Follow it in order; do not skip ahead to a later phase until the current phase has produced its intended output.

1. Resolve the target, mode, `repo_name`, `security_scans_dir`, `scan_id`, `scan_dir`, and `artifacts_dir` using `references/scan-artifacts.md`.
2. Create or adopt the scan goal described in `Goal Setup`.
3. Follow `references/phase-threat-model.md` first.

- Copy the repository-scoped threat model to the per-scan threat model path without alteration for auditability.
- Treat the per-scan threat model path as the source-of-truth threat model for later phases.

4. Follow `references/phase-finding-discovery.md` against the resolved scope:

- repo / scoped: read `references/repository-wide-scan.md` and every reference it lists.
  Stop at discovery only when the ranked runtime-surface worklist exists and the coverage ledger has closed every applicable high-impact and seeded root-control row as `suppressed`, `not_applicable`, or `deferred` with exact reasons.
  Open, reportable, or unresolved seeded rows continue to validation.
- diff: read `references/scan-scope-diff.md`.
  Generate `rank_input.jsonl` from the changed files and deep-review every row.
  If discovery finds no technically plausible candidates, finalize a no-findings report and stop.

5. Follow `references/phase-validation.md` for each candidate from discovery and each open, reportable, or deferred seeded/root-control ledger row that still needs closure.

- Pass the resolved scope, discovery notes, and candidate inventory to validation.
  Validation preserves or suppresses provided instances; it does not independently broaden or narrow the requested scope.
- Each candidate finding's candidate-ledger path from `references/scan-artifacts.md` is part of the validation input.
  Every candidate must have a discovery receipt before validation and a validation receipt before final reporting.
- When multiple candidates or ledger rows need validation and subagents are available, divide validation across subagents by candidate or row; each owns its candidate/row, evidence, artifact paths, and candidate-ledger path, and writes the validation report update and receipt.

6. Follow `references/phase-attack-path-analysis.md` for findings and validation closure rows that still need reportability, attack-path, and severity analysis.

- Each candidate finding's candidate-ledger path is part of the attack-path input.
  Every candidate that reaches this phase needs an attack-path receipt before final reporting, even when the final decision is `ignore`, suppressed, or deferred.
- When multiple validated candidates or closure rows need attack-path analysis and subagents are available, divide the work by candidate or row.

7. Author the complete canonical JSON contract last using `references/final-report.md`; do not hand-author reports.
   Then run `python <plugin_dir>/scripts/finalize_scan_contract.py --scan-dir <scan_dir> --source-root <repo_root>` to project the validated JSON into the final markdown report.

- Populate the optional structured details in `references/finding-detail-fields.md` from the same validated evidence used in the generated report.

## Scan Scope

- Phase 1 (threat model generation) is repository-scope by default, unless the user explicitly asks for narrower scope or provides an authoritative threat model or sufficiently repository-specific guidance such as `AGENTS.md`.
- Phase 2 onward stays within the resolved scope.
  For repo/scoped mode the resolved repository or scoped path is in scope; for diff mode the changed code and directly supporting files are in scope.
  See the mode's scope reference for full rules.

## Final Output

Populate all final report semantics in the canonical manifest, findings, and coverage JSON using `references/final-report.md`.
Then run `python <plugin_dir>/scripts/finalize_scan_contract.py --scan-dir <scan_dir> --source-root <repo_root>`; finalization owns markdown report generation.

## Hard Rules

Read `references/shared-hard-rules.md` first.
The mode's detailed rules live in its scope reference (`references/repository-wide-scan.md` for repo/scoped, `references/scan-scope-diff.md` for diff).
Across both modes:

- Do not begin substantive scan work (threat model, ranking, or any file-review subagent) until the `Scope and Cost Gate` has presented the scope and the user has explicitly approved it.
  Explicit invocation authorizes the workflow and subagent use, not the run as scoped; get that approval separately unless the user's request already gave it.
  The gate is a binary go/no-go; do not propose narrowing the scope.

- Create or adopt the scan goal only after the capability preflight has returned `ready`, and before substantive scan work.
  Do not complete it until the resolved in-scope files/worklist rows, candidate ledgers, and final report meet the `Goal Setup` closure criteria.

- For every scan scope, candidate-finding coverage is required.
  Do not finalize a candidate finding until its candidate-ledger path from `references/scan-artifacts.md` shows discovery, validation, and attack-path receipts for that exact candidate, or an explicit deferred reason for the missing proof.

- Subagent dispatch must have explicit ownership: ranking subagents own one generated `rank_shards/*.input.jsonl` shard of at most five rows and write only its matching worker-local `.output.jsonl`; file-review subagents own one assessed file or tiny shard and return full-file receipts plus pre-dedupe finding objects with candidate-local validation evidence and attack-path facts; validation subagents own one candidate or ledger row; attack-path subagents own one validated candidate or closure row; the parent agent owns bounded worker orchestration, ledger reconciliation, aggregation, cross-file dedupe, and final closure.

- These subagent-dispatch rules are purpose-built for security scanning and take precedence over any general subagent skill (e.g. `subagent-patterns`) during a scan.

- Candidate ids are optional links from coverage rows to findings; a not_applicable, suppressed, or deferred row is still required when the surface was in scope.

- Final assembly must start from reportable validation closure rows and surviving candidates.
  Do not drop a reportable seeded/root-control row because attack-path analysis or discovery spent more prose on a neighboring same-family finding.

- Final reporting is incomplete when a promoted high-impact finding's affected lines omit the concrete root-control file/line discovered or seeded during discovery, such as a codec, converter, parser feature setup, class filter, resource-path control, protocol state transition, or self-service update guard.
  Add the root-control affected line or explicitly suppress/defer it with exact counterevidence before finalizing.

- Preserve independently reachable sibling instances through final reporting.
  Repeated vulnerable templates, query builders, parser operations, auth/object endpoints, or shared-helper callers need separate finding entries, affected lines, and dispositions; put grouping in summary prose only after the individual instances are emitted.

- For query/parser injection, do not suppress syntax-control evidence solely because a later business check appears to limit impact.
  Carry the injection candidate until validation proves the exact query API and post-query guard defeat semantic change for that instance.
