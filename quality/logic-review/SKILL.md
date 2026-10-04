---
name: logic-review
description: Review the logic inside one Go function and its tests. Trigger to review a method, trace branches or edge cases, or check whether tests would catch a bug. Line-level correctness only.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

# Logic review

A logic review reads one function at a time. It traces every path
through the function. It then checks that a test drives each path and
fails when that path breaks.

A method is a function with a receiver. This skill says "function"
for both.

This skill owns the line-level pass. The `review` skill owns the full
gate pass. The `test-review` skill owns the package suite audit.
Route suite-level findings to `test-review`. Route gate concerns to
`review`.

## Stance

Read the function before its tests. Derive the contract yourself
first. Then read the tests against your contract. Tests read first
anchor the review on the code the tests already cover.

Confirmed findings only. Every finding needs a reproduction, a
severity, a file:line, and a minimal fix. Report first. Fix nothing
during the pass, unless the user asked for the fix.

## The function pass

Work one function at a time. Do these steps in order.

### Step one: state the contract

Write one line: inputs, outputs, error conditions, and the
invariants the function holds. Read the doc comment and the callers.
The comment, the callers, and the code must state the same contract.
A mismatch is a finding.

### Step two: enumerate the paths

List every path: each branch arm, each early return, each error
return, each loop body, each switch case. Write the list down. A
path you cannot name is a path you cannot review.

### Step three: trace each path with boundary values

Run each path in your head with concrete values. Pick values at the
boundaries of the input space:

- empty, one element, many elements
- zero, minimum, maximum
- nil pointer, zero struct, empty string
- duplicate, self reference, unknown key

### Step four: hunt the fault classes

Check the function against the fault classes. Read
`.agents/skills/logic-review/references/method-faults.md` for the full catalog with examples.
The short list:

- inverted, duplicated, or always-true conditions
- off-by-one in loop bounds and slice cuts
- aliasing: append sharing, slice header reassignment
- nil map write, nil pointer dereference
- shadowed or unchecked error, result used after an error
- missing switch default, dead branch
- lock copied by value, read path without the lock
- truncation on integer conversion, truncating division

### Step five: check the invariants

Every rule a comment states must live in a `Validate` method in this
repo. A rule that lives only in a comment is a finding.

## The test-logic pass

For each path from the function pass, find the test that drives it.
Apply the mutation check: flip the branch, drop the guard, or break
the return value. Ask which test fails. A path with no failing test
is a gap. Confirm a gap with a scratch test in the host's temporary
directory when the
confirm is cheap. Never edit repo code to prove a finding.

Then read each test as code. Tests carry the same fault classes as
the code they test. Read `.agents/skills/logic-review/references/test-faults.md` for the full
catalog. The short list:

- the expected value comes from calling the code under test
- the assertion reads a copy, a cached snapshot, or the wrong field
- a swallowed error: logged, not failed
- t.Errorf inside a goroutine
- a table case skipped by an early continue
- state leakage between table cases
- loop-variable capture in a parallel subtest
- non-nil only, length only, or an error substring two paths share

Assertion discipline: every failure message shows got and want. Use
t.Fatalf when continuing the test is pointless. Pin each error path
with a substring unique to that path.

Some mutations do not change behavior. An equivalent mutant is not a
test gap. Do not report it.

## Evidence

This skill declares no command execution. Read the tool list before you
plan the evidence.

- When the invoking agent has command execution, confirm every finding with
  a run: `go test ./<pkg>/`. Report the command and its output. When the
  function touches shared state, run `go test -race ./<pkg>/`. A scratch
  test needs a write tool as well, which this skill does not declare
  either; without both, do not claim one.
- Without command execution, give the reproduction as the exact input, the
  path through the code, and the wrong result, and report the evidence
  `NOT_RUN` with that reason. Do not report it as a confirmed run.
- A finding with neither a run nor a traced reproduction is a guess. Do not
  report it.

## Output format

Report five sections.

1. The contract. One line per function reviewed.
2. The path table. One row per path: path, driving test, verdict.
   Verdicts: pinned, weak, untested.
3. Findings. Reproduction, severity, file:line, minimal fix.
4. Evidence. The command behind each finding and its output. A finding
   traced but not run is `NOT_RUN` with the reason.
5. Handoffs. Suite-level gaps go to `test-review`. Gate concerns go
   to `review`.

## Bounds

- Follow the writing standard. One idea per sentence. No
  audit-finding labels.
- Do not change repo code during the pass.
- Stay on one function at a time. A package-wide sweep belongs to
  the `test-review` skill, not this one.
