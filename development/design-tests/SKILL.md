---
name: design-tests
description: Designs the tests for a feature ("design tests for this", "write a test plan", "what should we test?") from its spec and its real implementation, and produces a test-design document (scenarios per acceptance criterion, an API test table, a coverage matrix, and spec-versus-code divergences) for an implementer to turn into test code. Use when asked to design tests, write a test plan, decide what to verify, or before tests are written for a change. It designs only; it doesn't write or run test code.
allowed-tools: Read, Grep, Glob
---

# Design tests

Turn a spec and the code that implements it into a test design someone can implement without guessing. The design names every case, where it runs, and exactly what it asserts.

## Inputs

- **The spec**: acceptance criteria, plan, or ticket. It defines what *correct* means.
- **The implementation** or diff under test. Read the real files: routes, handlers, services, validation schemas, guards, data writes.
- **Project settings**: on every invocation, read `.claude/shipyard/design-tests.md` in the project root if it exists; its settings win over everything inferred. It can set the test layers, a reference test per layer, response and error shapes, auth and tenancy conventions, how a foreign resource answers (404 or 403), and where the document goes. Its shape is in [references/overlay-example.md](references/overlay-example.md).

## Output

A test-design document in the shape of [references/doc-template.md](references/doc-template.md), returned in the reply. Write it to a file only when the caller asks for one.

## Rules

- **Shapes come from the code; expected behavior comes from the spec.** Read routes, field names, status codes, and tables from the code, never from spec prose, because shapes guessed from prose are how invented APIs get into tests. Take what *should* happen from the spec, because models asked to predict outcomes tend to assert what the current code does, bugs included.
- **Tag every expected outcome with its source**: `spec`, `code` (a shape read from the implementation), or `characterization` (current behavior with no spec behind it).
- **Record divergences; never resolve them silently.** Where the code disagrees with the spec, the expected result follows the spec, and the disagreement goes in the divergences section as a suspected bug or an open question. Never weaken an expectation so the current code passes.
- **Missing acceptance criteria**: derive cases from the code's observable behavior, tag them `characterization`, and list them for the owner to confirm. They describe what the code does, not what it must do.
- **Exact assertions.** Every case names the exact status, the exact fields, and the data change. Assertions like "not null", "a 2xx", or "response contains a key" pass on broken code. Every negative case also asserts the absence of side effects: no row changed, no event sent.
- **Layer by risk, not by ratio.** Authorization, tenant isolation, data writes, and transactions belong in tests that hit the real database and the real auth path, since mocks drift from the behavior they stand in for. Mock only external infrastructure, never the code under test. Each case says which layer and why.
- **Follow the project's test model.** Use its layers and fixtures, and propose a new layer only as an open question.
- **Design only.** Writing test files and running suites belong to whoever implements the design.

## Steps

```
- [ ] 1 Read settings, spec, and code
- [ ] 2 Detect test conventions
- [ ] 3 List acceptance criteria and divergences
- [ ] 4 Design scenarios per criterion
- [ ] 5 Build the API table
- [ ] 6 Coverage matrix and self-check
```

1. **Read settings, spec, and code.** Settings first, then the spec, then every implementation file on the path under test.
2. **Detect test conventions** when the settings don't give them, in this order: testing sections of `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING`; manifests (`package.json` scripts and dev dependencies, `pyproject.toml`, `go.mod`, `pom.xml` or Gradle, `Cargo.toml`) for the framework; test file patterns (`*.spec.*`, `*.test.*`, `test_*.py`, `*_test.go`, `tests/`, `__tests__/`); then the two or three newest tests per layer, for fixtures and helpers. Record each convention with where it came from, so the implementer can check it. If the repo has an OpenAPI or other schema, read it too and treat drift from the code as a divergence.
3. **List acceptance criteria and divergences.** Number the criteria (`AC-1` …). Compare each against the code and note every mismatch now, before designing around it.
4. **Design scenarios per criterion**, using [references/coverage-checklist.md](references/coverage-checklist.md) for the default cases and the ones the code's features trigger. Boundary values come first: they find the most defects per case.
5. **Build the API table** for every endpoint touched, with the checklist's default rows.
6. **Coverage matrix and self-check.** Map every criterion to its cases; a criterion with no case is a gap to fill or to list as an open question. Then confirm every case has an ID, priority, layer with reason, exact assertion, and a source tag.

## Handoff

`next:` the implement stage, or whoever writes the tests. Whoever writes the tests follows the reference test named for each layer. A test is done when it passes against a correct implementation and fails when the behavior it names is broken.
