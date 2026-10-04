---
name: tdd
description: Guides feature work and bug fixes through a red-green-refactor loop using vertical slices. Use when the user wants test-first development, acceptance criteria implemented safely, or one behavior delivered at a time.
---

# Test-Driven Development

Use TDD to implement one observable behavior at a time.

The loop is:

```txt
one failing test -> smallest implementation -> refactor -> next test
```

Do not write all tests first. Do not implement the whole feature before the first failing test proves the path.

## Read First

Before editing code, inspect:

- `docs/agents/test-commands.md`
- `docs/agents/domain.md`
- `CONTEXT.md`
- relevant ADRs under `docs/adr/`
- existing tests near the behavior
- package scripts or equivalent task definitions

If setup docs are missing, infer commands from the repo. Ask only if the verification command or behavior target is unclear.

## Workflow

### 1. Clarify Behavior

Identify public behavior before test shape.

Capture:

- User-visible outcome.
- Acceptance criteria.
- Public interface or entry point.
- Existing behavior that must not regress.
- Out-of-scope behavior.

Ask the user only for product or acceptance decisions that cannot be answered from files or code.

### 2. Choose The First Vertical Slice

Pick the thinnest end-to-end behavior that proves the feature direction.

A vertical slice should:

- Be independently verifiable.
- Touch real integration points when reasonable.
- Avoid layer-only work with no observable outcome.
- Produce a small but meaningful behavior.

If the requested work is large, list slices and start with the smallest useful one.

### 3. Select Test Level

Prefer tests through public interfaces.

Good targets:

- Public function or module API.
- HTTP endpoint.
- CLI command.
- UI behavior through user interaction.
- Integration boundary already used by the repo.

Avoid:

- Private methods.
- Internal call counts.
- Mocking the unit that owns the behavior.
- Tests that break when implementation changes but behavior stays the same.

See `references/test-quality-guide.md` for examples.

### 4. Red

Write exactly one failing test for one behavior.

Then run the focused test command.

Confirm:

- The test fails.
- The failure is expected.
- The test would pass only if the desired behavior exists.

If the test passes immediately, the behavior may already exist or the test is weak. Investigate before continuing.

### 5. Green

Write the smallest implementation that passes the current test.

Rules:

- Do not add speculative behavior.
- Do not implement future slices.
- Do not refactor while red.
- Keep changes near the behavior owner.

Run the focused test command again.

### 6. Refactor

Refactor only after green.

Look for:

- Duplicate test setup.
- Names that do not match domain language.
- Shallow pass-through modules.
- Interface shape that makes future tests awkward.
- Code that can be moved behind a deeper public interface.

Run the test command after each meaningful refactor.

### 7. Repeat

For the next acceptance criterion, repeat:

```txt
Red -> Green -> Refactor
```

Each test should be informed by what the previous cycle revealed.

Stop when the agreed acceptance criteria are covered or when a new product decision is needed.

## Mock And Stub Rules

Use real collaborators when they are cheap, deterministic, and local.

Use stubs when:

- External services are unavailable.
- Time, randomness, network, or filesystem must be controlled.
- The collaborator is not the behavior under test.

Use mocks sparingly. If a test mainly asserts calls between internal modules, it is probably testing implementation detail.

When choosing a mock or stub, state the reason.

## Bug Fix TDD

For a bug:

1. Reproduce the bug first. Use `diagnose` if the cause is unclear.
2. Turn the repro into a failing regression test at the best public interface.
3. Implement the smallest fix.
4. Run the original repro and the regression test.

Do not write a regression test at a shallow seam that cannot express the real bug pattern.

## UI Work

For UI behavior, test the user-visible outcome when the repo supports it.

Prefer:

- role/text based queries,
- route behavior,
- form submission behavior,
- visible state changes,
- accessible interactions.

Avoid:

- class names as the main assertion,
- snapshot-only confidence,
- testing component internals.

## When Tests Are Missing

If the repo has no test setup:

- Identify the smallest safe verification command.
- Propose where a test should live.
- Ask before adding new test tooling.
- If tooling is out of scope, leave a manual verification checklist.

Do not silently add new frameworks.

## Verification

At the end, provide:

- Behaviors covered.
- Test files added or changed.
- Commands run and results.
- Any command that could not run and why.
- Remaining acceptance criteria.
- Refactor notes or architecture concerns.

See `references/red-green-refactor.md` for the compact cycle checklist.
