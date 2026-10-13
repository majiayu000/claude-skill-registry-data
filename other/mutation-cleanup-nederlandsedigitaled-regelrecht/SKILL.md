---
name: mutation-cleanup
description: Works through the surviving mutants that cargo-mutants reports for packages/engine — classify each one as a real test gap, a mutant not worth killing, or dead code, then fix it and verify with `just mutants-diff`. Use when picking up the weekly "Mutatietesten" issue, when asked to improve engine test coverage, or when a pull request fails the Mutation Testing (diff) gate.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Mutation cleanup

Surviving mutants are the engine's untested behaviour, listed. This skill is the
method for working them down, so that every round is worked the same way and the
weekly count means the same thing from week to week.

## What a surviving mutant is

`cargo-mutants` applies one small change to the engine at a time (flip a
comparison, delete a match arm, return `Default::default()` from a function) and
runs the test suite. A mutant that survives is a change no test noticed. That is
either a gap in the tests or code nothing depends on.

It is not a bug report. The mutated code is not in the repository, and the count
on its own says nothing about correctness. It says how much of the engine's
behaviour the tests actually pin down.

Two workflows produce them:

- `.github/workflows/mutation-testing.yml` runs the full set every Monday and
  opens an issue labelled `mbot:survivors` with the counts and a report.
- `.github/workflows/mutation-diff.yml` runs on every pull request that touches
  `packages/engine/**`, over the changed lines only. That gate is why new gaps
  should not reach this backlog.

## Step 1: Get the list

From the weekly issue, take the run id and download the report:

```bash
gh run download <RUN_ID> -n mutation-report
```

`missed.txt` has one line per surviving mutant: file, line, column, and the
change that was applied. `caught.txt`, `timeout.txt` and `unviable.txt` hold the
rest. `README.md` in the same artifact has the counts and the per-file
distribution.

Working from a failing pull-request gate instead? The gate splits its mutants
over shards, and each shard leaves its files in its own artifact,
`mutation-report-diff-shard-N`. Only a red shard has something to fix; the
list is short by construction.

## Step 2: Work one file at a time

Not one line at a time. Mutants cluster in a handful of files, and the context
built reading a file pays off across all of its mutants. Take the files in
descending order of surviving count; the distribution is in the report.

## Step 3: Classify before touching anything

Every mutant is one of three things. Decide which before writing code.

### A real gap in the tests

Write a test that fails on the mutated code and passes on the real code. Verify
it in that order: apply the mutation by hand, watch the test go red, revert the
mutation, watch it go green. A test you did not see fail proves nothing.

Put the test where the behaviour lives. Unit tests for a single function, a BDD
scenario when the gap is about how a law evaluates end to end. A mutant in
`operations.rs` that changes a comparison usually wants a unit test; one in
`service.rs` that changes resolution order usually wants a scenario.

Before writing a new test, check whether one already claims to cover this. Often
a mutant survives next to a test that reads as though it pins the behaviour. Then
the gap is that test, and the fix is to make its fixture construct the premise
its own doc-comment describes. A survey of this repository found fourteen such
tests: a longest-prefix test with no shorter competing article, a retain test
whose only candidate was filtered out upstream, an assertion about a variable
nothing references. Each one was a mutation survivor, and each read as coverage.

Rewriting the existing test beats adding a second one beside it. A second test
leaves the first as a decoy for the next reader.

### A mutant that says nothing

Debug helpers, `Display` implementations, `bin/` targets such as
`validate_annotations.rs`, WASM binding shims. Pinning these down with
assertions adds maintenance and no safety.

Record the decision so it stays recorded:

```rust
#[mutants::skip]  // Debug-only; asserting on the format pins nothing that matters.
fn render_internal(&self) -> String { … }
```

or, for a whole area, an `exclude_re` entry in `packages/.cargo/mutants.toml`
with a comment saying why. This is a valid outcome, not a way out. The count
drops because the question was answered, and the next reader inherits the
answer instead of the question.

### Dead code

Delete it. Do not write a test around code that nothing calls. Check first that
it is genuinely unreachable and not merely unused by tests.

## Limits

The engine decides legal outcomes: benefit entitlements, allowances, tax
calculations. These limits follow from that.

- Never write an assertion that pins an arbitrary implementation detail just to
  kill a mutant. A test describes behaviour that is wanted. If you cannot say
  which behaviour a test protects, it is the wrong test.
- If killing a mutant means changing behaviour rather than coverage, stop and
  raise it. A surviving mutant can be the first sign that the code is wrong, and
  that is a decision for a human, not a cleanup.
- Never weaken or delete an existing test to make something pass.
- `REVIEW.md` in the repository root holds the project's review dimensions and
  applies here too.

## Step 4: Verify

```bash
just mutants-diff        # mutates only your own changed lines, minutes not hours
just mutants             # the full set, over five hours; CI shards it instead
```

`just mutants-diff` must be clean before committing. It runs the same check as
the pull-request gate, so a clean result here means a green gate there.

Exit code 2 means a mutant survived in your own changed lines, which is the
gate doing its job. Exit code 3 means a test ran out of time under mutation.

Commit per file, in small commits, conventional-commit subjects in Dutch.

## What the numbers do next

The weekly run compares against the previous week and reports what is new, what
was solved, and what moved between `caught` and `timeout`. As long as more than
25 mutants survive, the timeout multiplier stays fixed so the weeks stay
comparable. Below that it starts rotating over 3, 2 and 5, which exposes mutants
that only die because a test ran out of time rather than because an assertion
caught them. Those are the next layer of the same question, and the same three
classifications apply to them.
