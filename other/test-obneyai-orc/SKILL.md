---
name: test
description: Run the project test suite using Polylith's poly test command
argument-hint: "[brick:NAME] [:all | :all-bricks | :dev]"
---

# Run Tests

Run the Polylith test suite from the workspace root.

## Command

```
clojure -M:poly test $ARGUMENTS
```

## Usage

- `/test` — run tests for changed bricks
- `/test :all-bricks` — run all brick tests
- `/test :all-bricks :dev` — run all brick tests including from the development project
- `/test brick:user-service :dev` — run tests for a specific brick from all projects including dev
- `/test :project` — run changed brick tests + changed project tests

Prefer a named `brick:NAME` while iterating. Broaden to changed bricks or
`:all-bricks` only when the change crosses those boundaries. A failing test is
evidence to investigate; do not weaken, skip, or over-mock it merely to get a
green run. Real-LLM end-to-end obligations must use the configured real provider,
be explicitly environment-gated, and must not substitute mocked model behavior.

## After running

Report the test summary (passes, failures, errors). If there are failures, show the failing test names and assertion details.
