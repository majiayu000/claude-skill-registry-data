---
name: dota-testing
description: >
  Governs testing standards and the Definition of Done for Dota AI Coach
  — unit/integration tests, GSI fixture and replay-simulator tests,
  FairPlay tests, ML leakage and temporal validation tests, computer
  vision tests, performance benchmarks, and end-to-end tests, across both
  the .NET application and any Python (data/ML) tooling. Use whenever
  writing or reviewing tests, fixing a bug, adding a feature, touching
  live-data or ML code, or deciding whether a change is actually done.
  This is the project's completion gate — a change isn't finished because
  it compiles or looks right, it's finished when it meets this skill's
  Definition of Done, which differs by what kind of change it is.
---

# Dota AI Coach Testing

This project has several kinds of tests that exist for specific,
non-overlapping reasons — a unit test proves logic is correct in
isolation, a FairPlay test proves a feature isn't leaking information a
player couldn't legitimately have, a temporal validation test proves a
model isn't cheating on its own evaluation. Treat "add tests" as "add the
*right* tests for what changed," not as a single undifferentiated
checkbox — the wrong test can pass while the actual risk in a change goes
completely unchecked.

## Test categories and what each one proves

Full detail per category is in the reference files; this is what each
category exists to catch, so you can pick the right one(s) for a given
change:

- **Unit tests** — a single unit of logic (a function, a class) behaves
  correctly in isolation, independent of infrastructure. See
  `references/unit-and-integration-tests.md`.
- **Integration tests** — multiple units correctly compose across a real
  (or realistically faked) boundary — e.g. the GSI pipeline end to end,
  or a Recommendation Engine actually consuming real Feature Engine
  output. See `references/unit-and-integration-tests.md`.
- **GSI fixture tests** — parsing/normalization logic behaves correctly
  against real or realistic captured GSI payloads, since GSI has no
  official spec (per `dota-gsi`) and fixtures are the closest thing to a
  contract. See `references/gsi-testing.md`.
- **GSI replay simulator tests** — a *sequence* of GSI payloads (not just
  one) is handled correctly over time — partial-payload merging, stale-
  state detection, reconnection gaps. See `references/gsi-testing.md`.
- **FairPlay tests** — a live feature only consumes data with an allowed
  `fairPlayClassification`, and no `FORBIDDEN`/`SPECTATOR_ONLY`/
  `POSTGAME_ONLY` data reaches a live path. See
  `references/fairplay-and-ml-tests.md`.
- **ML leakage tests** — a model's features are actually reachable at
  their claimed inference timestamp, with no future/hidden information
  smuggled in through a shortcut. See `references/fairplay-and-ml-tests.md`.
- **Temporal validation tests** — model evaluation actually used a
  correctly-ordered temporal split, not a shuffled/random one that
  silently reintroduces leakage. See `references/fairplay-and-ml-tests.md`.
- **CV tests** — computer-vision extraction is correct against known
  screen captures, and correctly reports "unavailable" rather than
  guessing when the relevant screen region isn't visible. See
  `references/cv-and-performance-tests.md`.
- **Performance benchmarks** — live-path code (GSI ingestion, CV
  extraction, model inference) stays within latency budgets appropriate
  for a real-time overlay, and doesn't silently regress over time. See
  `references/cv-and-performance-tests.md`.
- **End-to-end tests** — a realistic scenario (e.g. a simulated match
  from GSI replay through to a displayed recommendation) works through
  the whole live pipeline, not just each piece individually. See
  `references/end-to-end-tests.md`.

## Regression tests for bug fixes

**Every bug fixed should receive a regression test when practical.** A
bug that recurs after being fixed once is a sign the fix addressed the
symptom, not the underlying gap in test coverage — the regression test
*is* the actual fix; patching the code without one just delays the next
occurrence. "When practical" allows for genuine exceptions (e.g. a bug
that's environment-specific and not meaningfully reproducible in a test
harness), but that should be a deliberate, stated exception, not the
default. See `references/regression-testing.md` for how to write a
regression test that actually catches a recurrence, not just the exact
input that happened to be reported.

## Definition of Done

A change is not done because it compiles, runs once successfully, or
"looks right." It's done when it satisfies the Definition of Done for its
change type — see `references/definition-of-done.md` for the full,
change-type-specific checklists. Summary of the non-negotiable gates:

- **.NET changes** require `dotnet build` and `dotnet test` passing.
- **Python changes** (data/ML tooling) require `ruff`, `pyright`, and
  `pytest` passing.
- **Live-data changes** (new GSI field, new CV feature, new ML feature,
  anything touching opponent info or replay data — per `dota-fairplay`'s
  trigger list) require FairPlay validation, in addition to whichever of
  the above apply.

These are gates, not suggestions — a change touching live data that
passes `dotnet test` but hasn't been through FairPlay validation is not
done, regardless of how clean the code looks.

## Relationship to other skills

This skill doesn't duplicate the substance of testing guidance that
already lives elsewhere — it's the index and the completion gate:
- `dota-gsi` — GSI fixture format and the replay simulator's design.
- `dota-fairplay` — the FairPlay classification system and its own
  testing requirements (this skill enforces that those tests exist and
  gate live-data changes; `dota-fairplay` defines what they check).
- `dota-ml` — leakage tests, temporal validation, calibration, and the
  full pre-training/pre-ship/live-deployment checklists (this skill
  incorporates them into the overall Definition of Done).
- `dota-architecture` — architecture tests enforcing the dependency
  graph are their own test category, covered briefly in
  `references/unit-and-integration-tests.md` and owned in depth by
  `dota-architecture`.
