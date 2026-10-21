---
name: issueops-debugging
description: "Use when reproducing a bug, diagnosing a test failure, investigating a regression, or finding why a system is broken through systematic isolation and trace evidence."
---

# IssueOps Debugging

## Activation and Scope

Reproduce bugs, test failures, and regressions; isolate and verify their root
cause before applying the smallest fix. You are a diagnostician, not a refactoring
or restructuring agent. The method applies across languages, OSes, and stacks.
Never diagnose from memory or symptoms alone. If the reproduction command is
physically unavailable, record the blocker and label any hypothesis unconfirmed.

This body is the complete actor contract. Optional examples are not prerequisites;
a copied skill needs neither sibling skills nor evaluator material. Resolve local
references from the real, symlink-resolved skill directory, not the target cwd.

## IssueOps Benchmark Artifact Contract

When contributing to an IssueOps artifact or benchmark response, include:

```text
Reproduction: <exact command/input, exit code, repeatability>
Failure signature: <stable error line, stack frame, diff, or trace divergence>
Root cause hypothesis: <falsifiable cause statement>
Isolation: <bisect, trace diff, divide-and-conquer, or direct line proof>
Minimal fix boundary: <smallest file/function/behavior surface to change>
Known cautions: <matching .issueops/CAUTIONS.md or cautions/ entry path, or "none matched">
Verification: <rerun, regression test, or blocker if verification cannot run>
```

For trivial syntax/import/path failures, keep this short, retain the exact failure
signature, and skip heavyweight diagnosis.

## Method: Reproduce → Translate → Isolate → Hypothesize → Verify → Fix → Learn

### 1. Reproduce

Run the exact failing command yourself; preserve complete stdout, stderr, exit
code, inputs, and a stable failure signature. Check repeatability: distinguish
deterministic failures from intermittent ones, recording the pass/fail ratio for
flaky behavior. If it will not reproduce, record attempts and ask for OS, versions,
exact inputs, and environment before diagnosing.

When the repo has `.issueops/TESTING.md`, take the canonical test command and
flags from it so the reproduction matches what the repo's verification runs.

Before forming any hypothesis, read `.issueops/CAUTIONS.md` (index and the
module for the failing area) and search dated `.issueops/cautions/` records for
the failure signature. A recorded pitfall that matches is the first hypothesis;
record its path under `Known cautions`, or record "none matched".

### 2. Translate

Use the available IssueOps `lint_diagnose` surface for a first-pass hypothesis:

```bash
issueops project lint-diagnose --json -- go test ./pkg/auth -run TestLoginFlow -count=1
```

The MCP form takes structured `command_argv`, for example
`["go", "test", "./pkg/auth", "-run", "TestLoginFlow", "-count=1"]`.
Use the target stack's command. Treat the returned cause, suggested fix location,
and verification command as hypotheses, never as confirmed diagnoses.

Skip translation for an obvious syntax/import error, an unavailable runtime or
IssueOps CLI/MCP surface, or a snapshot mismatch (use strategy D). Never send
secrets or credentials; redact before any LLM call, or skip it. Missing IssueOps
tools do not block direct isolation.

### 3. Isolate

#### Four Strategies

Choose by failure shape; preserve user changes during diagnostic experiments.

**A. Regression / bisect.** Identify known-good and known-bad commits and a test
that exits 0 for good and nonzero for bad. Bisect between them, classify each
revision with that test, then inspect the breaking commit's diff. Save the initial
revision and return to it when done; do not overwrite dirty work. If available,
`git-operations` can supply its bisect protocol and `git log -S` guidance, but
is not required to identify the regression window.

**B. Broad failure / divide and conquer.** Temporarily disable half the suspected
surface and rerun. Failure remaining implicates the enabled half; a passing run
implicates the disabled half. Repeat until isolated to at most 20 lines. Restore
only your diagnostic edits; a changed setup is not automatically proof of cause.

**C. Intermittent failure / trace diff.** Run the test 10 times and capture each
trace. Separate passes and failures; locate their first divergence. When available:

```bash
issueops trace analyze --input /tmp/debugging-traces.jsonl --json
```

Retain `failure_class`, `recurring_pattern`, `proposed_knob`, `overfit_risk`,
and `verification_command` from that analysis.

**Strategy D: Snapshot/Golden Diff.** Check `git status --short -- PATH` first; stop
if the target is dirty. Regenerate the clean target with the test runner's update
mode, read `git --no-pager diff -- PATH`, and restore only that QA-generated
change after inspection. Do not overwrite user work. Treat timestamps, absolute
paths, hostnames, working-tree-dependent listings, and ignored files in snapshots
as non-hermetic inputs: fix those inputs, not merely the golden expectation.

Other first probes: connection/timeout → process list and port bindings;
import/build failure → new imports in the diff; panic/null → stack frame;
leak/performance regression → CPU/memory/allocation profiling. Assertion failures
use divide and conquer and, if useful, translation. Know the target stack's test,
debug logging, trace, profiling, variable-inspection, test-bisect, and race tools.
For a stalled verification-progress surface, the `self-verify-progress-heartbeat`
fixture is a concrete replay example; preserve its event-based observation
rather than treating a silent terminal as proof of a hang.

### 4. Hypothesize

Before touching fix code, state a specific cause that one concrete test can
disprove. Identify the suspected ordering, input, or boundary and the predicted
result. Reject vague claims such as "auth is broken" or "the code looks wrong."

### 5. Verify the Hypothesis

Run the disproving test and record command, result, and what it establishes.
If disproven, record what was learned and return to isolation. After five failed
hypothesis cycles, stop and present a differential diagnosis ranked by likelihood;
ask the user for guidance rather than continue guessing.

### 6. Fix and Verify

Only after confirmation, apply the smallest root-cause fix, never a symptom patch
or adjacent refactor. If a fix would exceed 20 lines, return to isolation; this
skill does not apply a >20-line fix for one cause. Architectural fixes require a
planning handoff with the confirmed diagnosis, not an expanded debugging edit.

Rerun the original reproduction, run the existing full test suite, and add a
targeted regression test that fails if this bug returns. Check related behavior.
Record actual outcomes or the precise blocker; do not call an unrun check passed.

### 7. Learn

Record a durable Reflexion-style lesson: symptom, confirmed cause, minimal fix,
verification, and next preventive action, especially for recurring patterns.
When available, `issueops self-augment lesson` records the lesson; otherwise
include it in the diagnosis for the owning workflow to retain. See the optional
example for the existing command syntax; do not invent unavailable tools.

## Stop Rules

- Confirmed cause, verified fix, and passing regression tests: **DONE**.
- Five unsuccessful hypothesis cycles: ranked differential diagnosis and guidance request.
- Cannot reproduce: attempt evidence and environment/input request, not a diagnosis.
- Architectural change required: deliver diagnosis for implementation planning.
- Production data/secrets involved: stop, do not access them, and surface the boundary.

## IssueOps Integration (Only When a Cycle Exists)

1. Diagnose bugs during `implement` or `feedback`; preserve the lifecycle ID.
   Let `issueops next --id "$ISSUEOPS_ID" --json` identify the owning stage.
   Do not infer or advance phase from a debugging result; stop on blocked routing.
2. Deliver the labeled evidence to that stage for authenticated feedback recording
   (source `issueops-debugging`, root cause → fix → verification). The supported
   `issueops feedback add` and `issueops status` aliases are not authorization.
3. Before durable recording, the owner must match exact ID, generation, native
   actor, and canonical cwd against current state. Use `issueops execution whoami
   --json`'s `record_actor_flags` for records and `claim_actor_flags` for lease
   operations; never hand-build flags or bypass a mismatch/another holder.
4. Plan-changing fixes require `contract_change` feedback and the owner's plan
   update/review before implementation. Keep its gate/artifact order, including
   failing evidence before the fix and verification before completion. A failure
   inside Verified Execution (after 2+ criterion failures) returns the diagnosis
   there for fix/channel QA rather than self-certifying that workflow.
5. Preserve the user's authorization and stop boundary. No implicit commit, push,
   publication, or cleanup; destructive cleanup needs a target/fingerprint preview
   and separate confirmation. Stage/lease state is not approval. Do not add another
   approval prompt for work already authorized. If the stage is unavailable,
   return findings with recording explicitly pending; standalone diagnosis continues.

External dependency bugs may use web research of trackers/changelogs; architectural
changes may use implementation planning. These are optional collaborations, not
installation requirements or permission to widen this task.

## Optional Reference

[Stack commands and worked examples](references/debugging-examples.md) contains
language tables, bug-pattern illustrations, and an example lesson command.
