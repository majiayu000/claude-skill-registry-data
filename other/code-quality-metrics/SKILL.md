---
name: code-quality-metrics
description: "Use when measuring code quality before and after cleanup, establishing quality baselines, detecting regressions across commits, or setting quantitative PR quality gates for signal, complexity, redundancy, and overhead."
---

# Code Quality Metrics

You are a measurement engineer, not a cleanup implementer. Quantify signal,
complexity, redundancy, and overhead using reproducible scope, commands, and tool
versions. Return measurements and targets; the cleanup executor changes code.
Do not infer semantic quality from numbers alone: shell heuristics are approximate
unless backed by AST analysis or tests.

## Entry and No-Input Guard

1. Capture `git status --short`, `git diff --stat HEAD`, and
   `git ls-files --others --exclude-standard`. Inventory staged, unstaged, and
   untracked files. Inspect/include untracked files; `git diff` alone misses them.
2. Identify the source-code scope. For predominantly docs/config changes with no
   source lines, report the four code metrics as **N/A** and give a line-delta summary.
   Treating prose comments as noise is meaningless.
3. With zero diff/zero measurable lines, report **insufficient-input**, never invent
   SNR, divide by zero, or claim a quality pass. Skip empty files.
4. Preserve tool errors. If a grep pattern errors or a nonempty diff measures zero,
   retry with `command grep` to bypass aliases such as ugrep/rg. Distinguish legitimate
   no-match status 1 from errors >1; failed git commands must not become plausible zeros.
5. Use installed/project-local tools. Global installation needs explicit user approval.

## IssueOps Benchmark Artifact Contract

When contributing to an IssueOps artifact or benchmark response, include this
measurement block, not a cleanup plan:

```text
Diff inventory: <staged, unstaged, and untracked files from git status>
SNR before/after: <baseline and post-cleanup values, or baseline only before cleanup>
Secondary metric: <entropy, redundancy, or channel overhead result>
Heuristic caveat: <AST-backed or approximate shell metric limitation>
No-input guard: <zero-diff/zero-line handling result>
```

## Four Metrics and Reproducible Procedures

For each measurement, record the exact input list, revision, tool versions, commands,
counts, and limitations. Use the same scope definition and commands at remeasurement;
record file-set changes rather than silently changing the workload.

### SNR: signal-to-noise ratio

`SNR = signal_lines / (signal_lines + noise_lines)`.
Signal lines affect observable behavior or cause a test failure if removed.
Noise includes comments restating code, dead/unreachable code, passthrough wrappers,
debug prints, commented-out code, and speculative abstractions.

For a shell estimate, capture added tracked lines once and check command status:

```bash
TRACKED_DIFF=$(git diff HEAD --) || exit
ADDED_LINES=$(printf '%s\n' "$TRACKED_DIFF" | command awk '/^\+[^+]/')
count_matches() {
  count=$(command grep -cE "$1")
  status=$?
  case "$status" in
    0) printf '%s\n' "$count" ;;
    1) printf '0\n' ;;
    *) return "$status" ;;
  esac
}
NOISE=$(printf '%s\n' "$ADDED_LINES" | count_matches '^\+[[:space:]]*(//|#|/\*|\*|console\.(log|debug|info)|print\(|log\.(debug|info|warn))') || exit
TOTAL=$(printf '%s\n' "$ADDED_LINES" | command awk 'NF { count++ } END { print count + 0 }') || exit
SIGNAL=$((TOTAL - NOISE))
if [ "$TOTAL" -eq 0 ]; then
  echo "Tracked SNR: insufficient-input (signal=0, noise=0, total=0)"
else
  SNR=$(echo "scale=2; $SIGNAL / $TOTAL" | bc)
  echo "Tracked SNR: $SNR (signal=$SIGNAL, noise=$NOISE, total=$TOTAL)"
fi
```

This snippet measures tracked additions only, not the entire inventory. For each
untracked source file, inspect its contents, count nonblank added lines using the
same classifier (without the diff `+`), and combine raw counts before division.
If a subset cannot be measured, report it explicitly, not as a full-scope score.

| SNR | Interpretation/action |
|---|---|
| ≥0.85 | Excellent; no cleanup needed |
| 0.70–<0.85 | Good; optional cleanup |
| 0.50–<0.70 | Needs cleanup before PR |
| <0.50 | Poor; block PR pending improvement |

### Entropy: cyclomatic complexity distribution

Count functions exceeding ceilings: **>6** is yellow; **>12** is red and must be
refactored by the cleanup executor. Record total functions and both exceedance counts.
Use language-native AST tooling where available; otherwise locate each function,
extract its body with language-appropriate boundaries, and count branch points
`if`, `else`, `for`, `while`, `case`, `&&`, `||`. Label this a heuristic; a whole-file
count or fixed-size excerpt is not an exact per-function complexity measurement.

### Redundancy: duplicate code ratio

`ratio = pairs of blocks with >80% token similarity / total block pairs`.
No block pairs means insufficient input, not division by zero.
Same-file adjacent-function length/token overlap is only candidate discovery.
Use AST-backed tooling for reliable results, e.g.
`golangci-lint run --enable-only dupl ./...` with project/default threshold, or
`npx jscpd --min-lines 6 --min-tokens 50 src/` with available project tooling.
Record duplicate blocks and the tool threshold; the baseline rule below separately
flags same-file blocks of more than six identical lines.

### Channel overhead: boilerplate-to-logic ratio

`overhead = boilerplate_lines / (boilerplate_lines + logic_lines)`.
Boilerplate includes imports, package/namespace declarations, serialization annotations,
getters/setters, constructor passthrough, DI wiring, and middleware setup.
Logic includes business rules, algorithms, type contracts, and domain error handling.
For every measured tracked/untracked file, count total lines, classify boilerplate,
derive logic = total - boilerplate, and report files **>50%** overhead.
Skip empty files; preserve classifier errors and label shell approximations.

Optional [measurement recipes](references/measurement-recipes.md) illustrate
language-specific scripts; the procedures and all required fields remain here.

## Phase 0: Baseline Before Cleanup

Measure before any cleanup pass. Save a valid JSON snapshot with captured values,
not the example values below. Store runtime evidence in
`.issueops/evidence/code-quality-metrics/` **only if ignored**, otherwise in IssueOps
state or temporary storage. Runtime snapshots are distinct from a cycle's committed
cleanup report; do not accidentally commit them.

```json
{
  "measured_at": "1970-01-01T00:00:00Z",
  "scope": "<measured revision>",
  "git_status_short": "<captured status>",
  "changed_files": ["<all measured staged, unstaged, untracked files>"],
  "snr": {"signal_lines": 0, "noise_lines": 0, "snr": 0.0, "passed": false},
  "entropy": {"functions_exceeding_6": 0, "functions_exceeding_12": 0, "total_functions": 0, "passed": false},
  "redundancy": {"duplicate_blocks": 0, "passed": false},
  "channel_overhead": {"files_over_50pct_boilerplate": 0, "total_files": 0, "passed": false}
}
```

Baseline criteria: SNR ≥0.60, zero functions >12 branch points, zero same-file
duplicate blocks >6 identical lines, and zero files >50% boilerplate.
No-input/N/A results must remain explicit, not masquerade as measured example zeros.

## Phase 1: Regression Against History

Load the previous snapshot from IssueOps state or the ignored evidence directory;
`issueops state read --key code-quality-metrics-latest` is the state read form.
Distinguish absent history from a failed read; never fabricate a prior measurement.
Record improvements. Block PR on:

- SNR drop >0.10; target recovery first.
- More functions >12 complexity.
- New redundant blocks.
- Channel overhead increase >10%.

## Phase 2: Target Card

Before cleanup, produce this table with actual baseline, chosen targets, and thresholds.
These rows preserve the target-card format; sample targets are not measured results:

| Metric | Baseline | Target | Threshold |
|---|---|---|---|
| SNR | measured | ≥0.75 | ≥0.60 |
| Entropy (>6) | measured functions | 0 | ≤1 |
| Entropy (>12) | measured functions | 0 | 0 |
| Redundancy | measured blocks | 0 | ≤1 |
| Overhead | measured files | 0 | ≤2 |

Priority: SNR noise recovery, >12 entropy, redundancy, then overhead.
Feed the card to the cleanup executor (ai-slop-clean or algorithm-optimization as
appropriate). They change code; you re-measure. High entropy is a prioritization
signal, not permission to bypass algorithm optimization's hot-path gate.

## Phase 3: Gate After Cleanup

Re-run Phase 0 with the **identical commands**, compare before/after, and record
both in the snapshot. Never claim improvement without a baseline and remeasurement.
All four metrics must pass targets; a single metric cannot establish a pass.
Do not accept cleanup without improved SNR, except the documented ceiling below.
Feed this result format to the execution quality gate:

```json
{
  "shannonAudit": {
    "snr": {"before": 0.58, "after": 0.74, "target": 0.60, "passed": true},
    "entropy": {"before": {"above_6": 4, "above_12": 1}, "after": {"above_6": 0, "above_12": 0}, "passed": true},
    "redundancy": {"before": 2, "after": 0, "passed": true},
    "channel_overhead": {"before": 3, "after": 0, "passed": true}
  },
  "overall": "PASS"
}
```

Use actual results, including failures, waivers, or no-input limitations; the sample
is not evidence. A baseline-only request stops after its measurements/target handoff
and does not invent a cleanup or after result.

## Pre-PR Checks

Inspect the complete inventory; use full SNR measurement for diffs >200 lines.
Flag source files >250 LOC (exclude tests), nesting depth >4, packages <60% test
coverage, and unused code. Adapt function boundaries and coverage tools to the language.
Use installed/project-local dead-code tools; preserve full output and exit status
before filtering (for example, staticcheck before filtering U1000).
Shell nesting/length estimates are warnings, not precise AST results.

## Integration and Stop Rules

In an IssueOps cleanup cycle, preserve this order: **baseline → regression → target
card → executor cleanup → identical-command gate → feedback record**.
Return gate results to the owning stage for authenticated `issueops feedback add`
and the `shannonAudit` quality-gate record. The stage owns exact lifecycle ID,
native actor, active generation/lease, canonical worktree, and recording/publication
authority. Do not invent flags or treat this skill as authorization to write records.

Planning may use the baseline for verification targets; debugging may use changed
signal lines as a diagnostic clue, not proof of an environmental cause.
Standalone measurements need no cycle, sibling installation, or evaluator material.
Resolve optional links from the real, symlink-resolved skill file, not cwd or the
unresolved host link; absent optional examples do not block a copied entrypoint.

- All four metrics pass thresholds and gate results are recorded: **DONE**.
- Unavoidable structural noise prevents SNR improvement: document the ceiling and
  mark the SNR threshold **"waived with justification"**, not an unqualified pass.
- Entropy unchanged after algorithmic refactoring: document the observed minimal-complexity ceiling.
- Commands fail or disagree: debug measurement, not source code; do not claim quality improvement.
- No measurable input/non-code scope: report insufficient-input/N/A and the scope summary; stop.
