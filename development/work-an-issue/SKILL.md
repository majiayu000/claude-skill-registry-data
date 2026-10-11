---
name: work-an-issue
description: End-to-end workflow for resolving one GitHub issue in dynamic-neural-field-composer - branch, TDD, build, review, docs, PR. Use when asked to fix, implement, or close a specific issue number.
---

# Work an issue

One issue, one branch, one PR. Do not stack unrelated changes.

## 1. Understand

```bash
gh issue view <N> --comments
```

Restate in your own words: the goal, and the **success criterion** - the observable thing
that will be true when this is done. If you cannot state a success criterion, the issue is
too vague to work unattended; stop and say so.

## 2. Branch

Never commit to `main`. Branch from an up-to-date base:

```bash
git fetch origin
git switch -c <type>/<slug> origin/main
```

Branch type is one of `bug/ feat/ chore/ ci/ docs/ test/ refactor/`. Keep the slug short
and specific: `bug/connection-dim-check`, not `bug/fix-the-connection-dimension-problem`.

## 3. Failing test first

Write the test that reproduces the bug or specifies the feature. Add it to
`tests/CMakeLists.txt` if it is a new file. Build and **watch it fail** - a test that passes
before you have implemented anything is testing nothing.

Follow the suite's existing conventions: `EXPECT_NEAR` with an explicit tolerance for
floating point, file-local `makeField`/`makeStimulus` helpers rather than a shared header,
fixtures with `SetUp`/`TearDown` for anything touching the filesystem.

## 4. Instrument before theorising

If the failing test does not immediately tell you *why*, *do not reason about the control
flow by reading source*. Add logging, run it, and read what actually happened:

```cpp
tools::logger::log(tools::logger::DEBUG,
    "field 'u' step 42: max activation 0.87 at index 51, below threshold 1.0, no bump");
```

Write messages as plain natural-language sentences carrying the values that matter. Guessing
at the flow costs more than instrumenting it. Remove the instrumentation before the PR
unless it earns a permanent place at `DEBUG`.

## 5. Implement

Minimally. The smallest change that makes the test pass and nothing more.

Before writing any helper function, **search `tools/` first** - `math.h`, `utils.h`,
`profiling.h`, `logger.h`, `fft_convolution.h`, and `exceptions/exception.h`. If something
close already exists, extend or reuse it. A new free function duplicating an existing helper
will be rejected in review.

## 6. Build and test

Use the `build-and-test` skill. Green means the full suite, not just your new test.

## 6b. Performance check

If the diff touches the simulation hot path — `src/elements/`, `src/simulation/`, `src/tools/`,
`include/tools/math.h`, `include/tools/fft_convolution.h`, `include/tools/simd_dispatch.h` —
use the `perf-regression-test` skill.

Skip it otherwise, and say you skipped it. A silent skip reads as a pass.

An inconclusive result (too noisy, or no baseline for this machine) is not a pass. Report it as
unverified rather than moving on quietly.

## 7. Review your own diff

Use the `project-code-review` skill on `git diff origin/main...HEAD`. Fix what it finds
before asking anyone else to look.

## 8. Docs

Use the `docs-check` skill. Doxygen on new public API, wiki page for user-visible changes,
and no stale references left behind.

## 9. Changelog

Add an entry under `[Unreleased]` in the repo-root `CHANGELOG.md` — the one beside
`README.md`, not inside `dynamic-neural-field-composer/`. Create the `[Unreleased]` heading
if the last release consumed it.

Pick the subsection matching the work; the file uses `Added`, `Changed`, `Fixed`,
`Removed`, `Performance`, `Tests`, `Documentation`, `Build` and `CI`. Create it in that
order if absent.

Write for someone reading the release notes months from now with no access to the issue:
what changed, and why it mattered. Reference the issue as `(#N)`. Match the surrounding
entries' density — they are full sentences, not one-line summaries.

Every issue gets an entry, CI- and test-only work included. It is easier to drop a line at
release time than to reconstruct one from a diff.

## 10. Ship

```bash
git add -A && git commit -m "<type>: <lowercase summary>"
git push -u origin <branch>
gh pr create --title "<type>: <summary>" --body "<what / why / how to verify>

Closes #<N>"
```

Do **not** merge. The PR waits for human review.

## 11. Hand back

Report: PR URL, what changed, what you verified (with the test count), and anything you
deliberately left out.

## Stop conditions

Stop and ask rather than guessing when:

- **Backwards compatibility cannot be preserved.** This is never your call to make alone.
- The issue admits two readings that would produce materially different work.
- Tests fail for reasons unrelated to your change - report the pre-existing failure, do not
  paper over it or "fix" it as a side quest.
- The fix requires a design or product decision the issue does not settle.

When you stop, say exactly what you completed, what is blocked, and what you need.
