---
name: backfill-feature
description: Use when the user says "/backfill-feature", "backfill the ADR", "this feature has no ADR", "I need to document what's already there before I change it", or wants to capture an existing feature's architectural rationale and behaviour *before* modifying it. Reads the relevant code, drafts a reverse-engineered ADR (what is, why it probably looks like this) + Gherkin spec (current behaviour) + characterization tests that lock the current behaviour green. Hands off to /plan-change so the actual change can be layered on top of a documented, tested baseline.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(rg:*), Bash(fd:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(go:*), Bash(cargo:*), Bash(pytest:*), Bash(just:*), Bash(make:*), Read, Edit, Write, Grep, Glob, Skill
---

# backfill-feature - characterize existing code before changing it

When you reach to modify code that has no ADR or spec, you're working
blind: you don't know what the original author intended, what
constraints were considered, or what behaviour the rest of the system
depends on. `/backfill-feature` builds that picture *before* the
change, so the change lands on solid ground.

It writes three things in order:

1. A reverse-engineered **ADR** ("here's what's true today, here's
   why I think it ended up this way, here's what's load-bearing").
2. A **Gherkin spec** capturing current behaviour.
3. **Characterization tests** that lock current behaviour green.

After backfill, `/plan-change` runs to layer the actual change on top
of the (now-documented, now-tested) baseline.

## When to use

- Modifying code that has no ADR for its area.
- Refactoring a non-trivial module that "just grew."
- Picking up a feature from someone who's left.
- Anywhere "I should write some tests for this first" would be the
  responsible move.

Skip for:

- Trivial changes (copy edits, one-line bug fixes in isolated helpers).
- Code that already has ADR + spec + tests covering the area.
- Brand-new features (use `/plan-change` directly - nothing to
  backfill).

## Phase 0 - Discover the area

The user identifies the feature being touched. Find the code:

```bash
# User says "the orders cancellation flow"
rg -l 'cancelOrder|order_cancel|cancellation' --type ts --type tsx --type go
```

Then check what already exists:

```bash
# Any ADR mentioning the area?
rg -l '<keywords>' docs/adr/ 2>/dev/null

# Any spec?
rg -l '<keywords>' specs/ features/ tests/features/ 2>/dev/null

# Any tests?
fd --type f '<keywords>' tests/ __tests__/ spec/
```

If any of these already exist, **read them** - the backfill might be
partial (an ADR but no spec, or tests but no documentation). Don't
re-write something that's already there.

## Phase 1 - Read the code

Read the relevant files. For TS/JS, use `tslsp outline` first to see
structure, then `Read` the interesting parts. For other languages,
use the project's symbol-aware tooling if available.

Build a working picture of:

- **What it does.** User-visible behaviour and API surface.
- **How it's structured.** Layers, responsibilities, data flow.
- **What it depends on.** External services, libraries, configuration.
- **Where it's load-bearing.** Who calls it, what would break if it
  changed.
- **What looks intentional vs accidental.** Naming conventions, error
  handling patterns, retry logic - all hints.

Show this picture back to the user before drafting:

```
Here's what I think this feature does. Correct me where I'm wrong:

  - <one-line summary of behaviour>
  - <key architectural choice 1>
  - <key architectural choice 2>
  - <load-bearing dependency or invariant>

Anything missing, wrong, or unclear?
```

**This is a hard gate.** Do not proceed to Phase 2 until the user has
confirmed the picture. If you write characterization tests against the
wrong baseline, the upcoming change gets designed against the wrong
baseline too - and the lock-in actively works against the user. Iterate
the readback as many times as it takes. The user is the source of
truth for "why."

## Phase 2 - Draft the ADR

Write a "what is" ADR with frontmatter marked as **retroactive**:

```markdown
---
status: Retroactive
title: Order cancellation flow
captured-on: 2026-06-08
captured-from: existing code in src/orders/, no prior ADR
---
```

Body sections:

- **Context**: what was true when this was first built, as best you
  can reconstruct. Note uncertainty explicitly ("unclear from git
  history whether X was a deliberate choice or accidental").
- **Decision**: what the code does today.
- **Alternatives**: any obvious alternatives that *weren't* chosen,
  with best-guess reasons. Mark these as inferences.
- **Consequences**: what the current shape makes easy and what it
  makes hard - relevant because the upcoming change will brush
  against one or the other.

The retroactive marker matters. Future readers should know this ADR
documents observed reality, not a deliberation that happened in real
time.

## Phase 3 - Draft the spec

Write a Gherkin spec capturing current behaviour. Cover the golden
path and the edge cases the code actually handles. Mark it as
characterization:

```gherkin
# Characterization spec - captures current behaviour as observed in
# the code at <commit-sha>. See <adr-link> for the retroactive ADR.

Feature: Order cancellation
  ...
```

Cross-link both ways with the ADR, same as `/plan-change` does.

## Phase 4 - Write characterization tests

This is the lock-in step. Without tests, the backfill is just
documentation - the change you're about to make could still break
behaviour silently.

Write tests that:

- Cover the golden path scenarios from the spec.
- Cover the edge cases the spec calls out.
- Pin exact outputs - numeric results, error messages, retry
  behaviour, whatever the current code produces.
- Run in the project's existing test setup (don't introduce a new
  framework for the backfill).

Run them. They should all pass green against the current code:

```bash
<test-runner> <new-test-files>
```

If anything fails, the test is wrong (or the spec is wrong) -
characterization tests by definition pass against current behaviour.
Fix the test, not the code.

**If the test suite can't run in this environment** (no `node_modules`,
no test runner installed, no language toolchain), don't silently skip
verification. Mark the test file with an `@unverified` annotation in
its header comment ("characterization tests written by inspection, not
yet executed against the code") and surface this clearly to the user:

```
WARNING: <N> characterization tests written but not executed.
The test runner (<expected-runner>) isn't available in this
environment. Run them before relying on the baseline:

    <how-to-run>

Until then, the lock-in is theoretical.
```

Treat this as a soft gate rather than a hard one: the ADR + spec are
still useful, but the user has to know the tests haven't actually
caught anything yet.

## Phase 5 - Commit each artefact

Three commits, in order, so the history shows the baseline being
established:

```bash
git add <adr-path>
git commit -m "ADR <id>: <feature> (retroactive)"

git add <spec-path>
git commit -m "spec: <feature> (characterization)"

git add <test-paths>
git commit -m "tests: characterize <feature> behaviour"
```

Match the repo's commit convention if it differs.

## Phase 6 - Hand off

The baseline is locked. The change can now be designed on top with
confidence. Invoke `/plan-change` with the new ADR + spec as context.

```
Backfill complete:
  ADR:   <path> (retroactive)
  Spec:  <path> (characterization)
  Tests: <N> tests, all green     | <N> tests written, @unverified

Calling /plan-change next to design the change.
```

If the tests are `@unverified` (Phase 4 soft-gate fired), call this
out explicitly in the hand-off message - don't claim "all green" when
the runner never ran. The downstream `/plan-change` discussion should
know whether the baseline is actually locked or only documented.

## Operating rules

- **Be honest about inference.** Distinguish "the code does X" from
  "we probably did X because Y" - the second is a guess and should be
  labelled.
- **Don't fix bugs during backfill.** If you spot a bug in the
  existing code, note it in the report but don't change behaviour
  here - the tests would diverge from current behaviour, defeating
  the lock-in. Fix bugs in the *next* step, where they're a deliberate
  change captured in `/plan-change`.
- **Tests must lock current behaviour exactly.** Even quirky behaviour
  ("returns null when input is empty string instead of throwing").
  The point is to detect drift, not to polish the code.
- **Skip if it's already documented.** If the area has an ADR + spec +
  tests, there's nothing to backfill. Say so.

## Composing with other skills

- **Before:** `/start-feature` usually routes here when existing code
  has no ADR.
- **After:** `/plan-change` to design the change on top of the
  baseline.
