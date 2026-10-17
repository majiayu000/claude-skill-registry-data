---
name: verification-loop-current
description: Verify a substantial code change against the repository's actual acceptance gates, preserving command exit status, complete failure accounting, tested input identity, and meaningful behavioral evidence before claiming completion.
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  source-commit: 846ffb75da9a5f4e677d927af1ad4a1951652267
  revision-status: experimental-unbenchmarked
---

# Verification tied to the actual change

Read the repository instructions, manifests, lockfiles, CI and relevant tests.
Identify the requested behavior, supported environments and exact required gates.
Use existing authorization. Preserve unrelated changes and determine the intended
base from current Git/remote state; do not assume `HEAD~1` represents the task.

## Choose checks that can expose the failure

Write down observable acceptance conditions before implementing or revising tests.
For a bug, reproduce the failure where practical, then check the repair and related
regressions. Test behavior, useful boundaries and plausible wrong outcomes.
Multiple related assertions can establish one behavior. Tests that repeat an
implementation, placeholder bodies, package metadata and a success message do
not establish correctness.

Use the project's actual test runner, scripts and configuration. A package manager
or an installed Bun binary does not identify the runner. Resolve installed tool
APIs and current stable dependencies; preserve a reproducible environment.
Follow repository coverage gates and inspect missing relevant coverage. Do not
invent an 80% universal requirement or equate coverage with a correct oracle.

Start with checks affected by the change, then run required broader gates.
Repeat checks when new edits, failures, input changes or unresolved concerns
justify it. A timer or completing every function is not sufficient reason to
repeat an expensive unchanged suite. Reversible presentation-only edits do not
need tests that merely restate them.

## Preserve real status and evidence

Capture each command's exit status and complete bounded log before displaying
excerpts. A default POSIX pipeline reports the last program's status: piping a
failed build through `head`, `tail` or `grep` can report success and truncate
errors. Preserve the producer's status with the chosen shell's supported
mechanism, or invoke it directly through a process API. In PowerShell, capture
the native command's `$LASTEXITCODE` immediately before subsequent commands.
Do not assume POSIX and PowerShell pipeline behavior is identical.

Record the exact command, environment/tool versions, input revision/signatures,
status, diagnostics and artifact location. Distinguish failure, timeout, abort,
skipped, unavailable and not-run from passed. Retain the first failure and its
cause when a corrected invocation later passes. A harness error is not a test
failure or successful task outcome. Keep credential-bearing logs private and
publish only suitable evidence.

Read structured test reports and complete denominators. Check that the intended
tests actually ran and that output-producing wrappers preserve failure. Explain
genuine platform skips and remaining coverage; do not disable required tests,
hide retries or suppress findings to make a report green.

## Verify security and scope

Run the repository's configured secret, dependency and code-scanning checks at
their intended scope. Two grep strings or checking console logging cannot prove
the repository clean. Include relevant languages, dependencies, generated files
and history when required. Fix validated causes, retain unresolved findings and
report unavailable scanners explicitly. Never turn off checks or add exemptions
to satisfy a count.

Review all changed file groups, staged/unstaged edits and relevant untracked
outputs. Confirm generated artifacts and locks match their inputs. Check that
the patch stays within the task's authorized scope and preserves unrelated data.
After a meaningful input change, invalidate affected verification evidence and
rerun the appropriate gate. Hosted checks must match the exact delivered head.

## Report the practical conclusion

Lead with the resulting behavior, then state the relevant tests and their scope.
Report planned/executed/passed/failed/skipped/not-run checks and material limits.
Use a completion verdict only when the requested acceptance criteria and required
gates are verified. Otherwise name the concrete remaining work and keep the task
active. Do not extrapolate a focused pass to untested platforms, remote security,
all skill categories or coding-agent superiority.

This experimental overlay corrects the original verification guidance. Actual
shell controls reproduce the lost-exit-status defect, but no independent matched
agent trial has established this overlay's benefit over default behavior.
