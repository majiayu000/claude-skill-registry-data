---
name: "speckit-tests"
description: "Turn the feature spec's requirements and acceptance scenarios into failing tests BEFORE implementation (the red-first gate). Runs between /speckit-tasks and /speckit-implement."
argument-hint: "Optional scope filter (e.g. a user story or FR range)"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "speckit-demo"
  source: "ported from speckit-demo, adapted to blastradius conventions"
user-invocable: true
disable-model-invocation: false
model: opus
---


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Convert the active feature's functional requirements and acceptance scenarios into
**executable, currently-failing tests** so that `/speckit-implement` starts from red.
Concrete failing-test context beats advisory "please do TDD" prose — this command
produces artifacts, not intentions.

## Operating Constraints

- **Writes tests only.** This command MUST NOT create or modify production source.
  If a test needs a helper, the helper lives next to the spec file.
- **Real assertions, no placeholders.** Every test asserts the concrete expected
  behavior from the spec (return shapes, thrown errors, counters, ordering). No
  `it.todo`, no empty bodies, no assertions on placeholder values.
- **House test conventions** (constitution II): Jest, colocated `foo.spec.ts`
  next to the source it covers; app-level integration tests in the app's `test/`;
  cross-app in `e2e/`. Temp dirs via `mkdtemp`, cleaned in `afterEach`. Suite
  stays fast and deterministic. End-to-end flows are Playwright, in the app's
  `*-e2e` project.
- **Plain test titles** (project rule): describe the behavior, nothing else — no
  FR tokens, ticket codes, or other prefixes in titles.
- **No internal identifiers in the source but one** (Constitution II): not in
  test titles, not in prose comments, not in non-test code — no bare `FR-003`,
  no Jira key, no task id, no spec or feature-directory number. They name things
  that live outside the repo and rot when the ticket moves or the numbering
  changes. The one exception is the trace line: a test file may carry a
  whole-line comment `// @traces 010-FR-016` (one or more `<feature>-FR-<n>`
  ids and nothing else, on or above the tests it covers), which
  `trace-matrix.mjs` reads. Anything else on that line, an SC id included,
  makes the matrix skip it. The completion report's FR → test table and
  `tasks.md` carry the mapping too.
- **A comment must earn its line.** Write one only where the code cannot say it
  itself: why a non-obvious choice was made, a constraint from outside the file,
  a trap the next reader would otherwise re-introduce. Never restate what the
  next line already says, never label a test with its own title, never leave a
  section banner, a step number, or a note addressed to this run rather than to
  a future reader. A test whose title and assertions are clear needs no comment
  at all — that is the normal case, not the exception.

## Execution Steps

### 1. Initialize

Run `python3 .specify/scripts/python/check_prerequisites.py --json --paths-only` from
repo root and parse FEATURE_DIR. Read `spec.md` (required — STOP and point to
`/speckit-specify` if missing) and, when present, `plan.md` + `tasks.md` for file
layout and naming decisions.

### 2. Inventory the requirements

From `spec.md` collect: every `FR-###`, each user story's acceptance scenarios, and
edge cases. Apply the user's scope filter if given. For each item, decide the
concrete observable behavior to assert — taking contract details from `contracts/`
and `data-model.md` when they exist.

### 3. Write the failing tests

Colocate each spec file with the source it will cover per plan.md's structure
(`foo.ts` / `foo.spec.ts`, even when `foo.ts` does not exist yet). Keep titles
plain; track which FR each test verifies for the report table.

### 4. Verify RED

Run the affected workspace's tests (`npm run test -w apps/<name>`); run it into a log and read only the exit code, the summary and the failures (AGENTS.md "Agent replies": `tail -n 40`, then `grep -nE '✕|●|FAIL|Error'` on a failure). Required outcome:

- every **new** test FAILS (red), because the behavior does not exist yet;
- every **pre-existing** test still PASSES (you broke nothing by adding files).

If a new test passes before any implementation, one of two things is true — handle
explicitly, never shrug it off:

- the behavior already exists → mark the FR as already-covered in your report and
  keep the test (it becomes a regression guard);
- the test is vacuous → rewrite it until it fails for the right reason.

Report a table: FR → test file → RED/GREEN(pre-existing).

### 4b. Adversarial pass (when the user asks, or in `/speckit-auto`)

Invoke the `test-adversary` subagent (Agent tool, `subagent_type:
test-adversary`) with `FEATURE_DIR` and the public surface the spec defines —
route paths, exported functions, contract schemas. It sees the spec and the
contract and nothing else, and writes the tests you are least likely to: the
empty input, the value one past the cap, the same call twice, every "MUST NOT"
attempted. Its tests land in the working tree next to yours and go red with
them. Its report is not shown to the user; add its table to yours in step 5.

### 5. Handoff (do NOT commit at red)

Leave the red tests in the working tree, run `/speckit-implement` next, and commit
each implementation slice **together with the tests it turns green** (working
agreement: short semantic commits per logical chunk). State this explicitly in your
completion report, including:

- how many tests were written, and the FR coverage count;
- the red/green table from Step 4;
- next command: `/speckit-implement`.

## Project Constitution Gate: No Bloated Code (NON-NEGOTIABLE)

<!-- project-local addition (constitution v1.0.0) — re-apply after `specify integration upgrade` -->

motor-fix Constitution Principle I applies to everything this skill produces:

- Tests cover real behavior and contracts — no padding suites for coverage
  numbers, no speculative fixtures, no helper layers with one call site.
- Roughly one focused test per stated behavior, sized like the neighboring
  `*.spec.ts`; scratch checks are never promoted to permanent tests.
- Complexity that cannot be justified against a current, concrete requirement
  is cut — not deferred to review.

Full text: `.specify/memory/constitution.md`.

## Done When

- [ ] Every FR has at least one test asserting concrete behavior from the spec
- [ ] Tests were seen failing, with the failing count quoted — a test passing before implementation is not red-first
- [ ] No production source created or modified
- [ ] Titles plain, no internal identifier in the file outside a whole-line `// @traces <feature>-FR-<n>` comment, and no comment that restates its own code

