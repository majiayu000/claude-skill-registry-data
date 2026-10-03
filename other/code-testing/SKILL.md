---
name: code-testing
description: "Designs test cases, then writes unit / in-process API tests or a test-case document. Load it first, before searching for code or specs or asking the user anything, when the user wants unit tests or test cases designed or written for a method, class, file, git changes, a PRD, pasted requirements or an OpenAPI / Swagger spec; it locates inputs and asks its own questions. Output: runnable tests; numbered cases with steps and expected results in a Markdown document, optional Word (.docx) export; or test-first failing tests with stubs. Trigger on 写单元测试 / 补测试 / 写测试用例 / 设计测试用例 / 列出用例 / 出用例文档 / Word 版用例 / 按接口文档写测试 / 测试先行 / TDD / 锁定当前行为 / write unit tests / generate test cases / characterization tests. Do NOT use, even though tests are mentioned, for: E2E or Playwright tests (端到端测试), coverage targets or coverage tooling / reports, reviewing test quality (use code-review-deep), deleting tests (use code-slimming), only running or debugging tests, flaky tests, load tests, building a feature (use code-vibe-workflow)."
---

# Code Testing

Design first, write second. The value of this skill is the design: every case comes from a named dimension, every expected result names its source, and the whole list is confirmed before a single test or document line is written. Typing the tests is the easy part.

In scope: unit tests, integration tests where the project already has the infrastructure, in-process API tests, and test-case documents. Out of scope: E2E / browser UI automation, load and performance testing, coverage-report-driven backfill, whole-module or whole-repo backfill.

## Modes

| Mode | Input | Output |
|---|---|---|
| **Code** | a method / class / file the user names; git changes (uncommitted, or a commit range); endpoints of an existing service | runnable tests |
| **Spec → Doc** | requirements: md / txt / docx / pdf, pasted text, OpenAPI | a Markdown test-case document; a `.docx` export on request |
| **Spec → Test-first** | requirements for behavior that does not exist yet | failing tests + minimal stubs |

Resolve the mode first:
- Requirements in, 用例 / 用例文档 / 测试用例表 wanted → **Spec → Doc**.
- Requirements plus an existing implementation, test code wanted → **Code**, with the requirements as the top oracle source.
- Requirements for behavior not implemented yet, or the user says 测试先行 / TDD / 先写测试 → **Spec → Test-first**.
- Still ambiguous → ask with the platform's interactive question tool (e.g. AskUserQuestion), recommended option first.

**Lock (Code mode only).** The default oracle is intent. Only when the user explicitly asks — 锁定当前行为 / 重构前兜底 / 先补保护网 / characterization tests — does the oracle become the implementation. Never switch on your own.

References (this skill's directory, read on demand):
- `references/test-design.md` — the 5 + 3 design dimensions and the technique behind each. **Read before drafting any case list.**
- `references/case-list.md` — the list format, oracle values, priorities, the confirmation round. **Read before presenting the list.**
- `references/quality-floor.md` — the rules every test and case must meet, whatever the project's habits. **Read before writing the first test or case.**
- `references/mode-code.md` — scope, oracle and Lock, existing tests, level, running. **Code mode.**
- `references/mode-requirements.md` — reading requirements and OpenAPI, coverage, the document, test-first stubs. **Both Spec modes.**
- `references/lang-java.md` · `lang-python.md` · `lang-go.md` · `lang-typescript.md` — detection, default stack, naming, boundary mocks, stubs, run commands. Read one per language in scope. Any other language: apply the same rules with the project's own tests as the reference, and say that no language guide applied.
- `assets/test-case-doc-template.md` — the Spec → Doc skeleton.

All user-facing questions, lists, documents and reports are in Chinese. Rules stay English.

Do NOT use this skill for: building a feature end to end (`code-vibe-workflow`, whose Phase 4 keeps its own test rules), reviewing the quality of existing tests (`code-review-deep` / `code-review-deep-zh`), deleting redundant or tautological tests (`code-slimming`), reading code (`code-read-deep-*`), converting an existing document to Word (`docx`), or anything on the out-of-scope list. A mixed request: decline the out-of-scope part in one or two sentences, then do the rest.

## Conventions

The project's existing tests beat the built-in style below; the quality floor applies either way and is never relaxed to match project habits. For documents, a test-case template the project already uses beats `assets/test-case-doc-template.md`.

Built-in style, only where the project has no precedent:
- Test name `method_scene_expected` in English, e.g. `redeem_pointsInsufficient_throwsInsufficientPoints`.
- A Chinese description of scene and expected result, in the language's slot — JUnit `@DisplayName`, the pytest docstring, the Go `t.Run` subtest name, the Vitest / Jest `it`. The `lang-*.md` file gives the exact mapping.
- The body in three parts marked `given` / `when` / `then`.
- Placement: the project's layout; none → the language default: Java `src/test/java`, Go `_test.go` beside the source, Python and TS `/tests`. Java and Go never go under `/tests` — their standard toolchains would not compile them there, or could not reach unexported code.
- A test file for the target already exists → append to it; otherwise create one.

## Step 1 — Scope

- **Code.** A named method, class or file: that target only; callers are read as oracle evidence, not tested. Git changes and endpoints: `references/mode-code.md`. Generated code (`DO NOT EDIT`, `@generated`, `Code generated by`, `*_pb2.py`, `**/generated/**`) is dropped and named in the report.
- **Spec.** The given document or text; for OpenAPI, all operations or the ones the user names.
- **Scope guard.** More than 20 source files, or more than 20 requirement items / operations: report the count and ask 继续 / 分批（约 10 个一批）/ 缩小范围. Batches run sequentially; no parallel subagents.

## Step 2 — Probe the project

Before designing, establish:
- the test framework, assertion and mock libraries, from the build files (`lang-*.md` lists the signals);
- test layout, naming and structure — read one to three existing tests near the target;
- existing tests for the target: scenarios already covered (→ 已有覆盖) and assertions the change makes stale (→ 需更新);
- integration test infrastructure — Testcontainers, an embedded DB, a test profile;
- a `.docs/` lifecycle directory, and any existing test-case documents (Spec → Doc).

No test infrastructure at all → prepare an infra proposal for Step 4 from the language file: default stack, placement, the exact build-file change. Touch no build file yet.

## Step 3 — Design

Walk `references/test-design.md`: the five core dimensions always, the three conditional ones when their triggers are present. Every case names its dimension; every dimension without a case gets a one-line reason (不适用 / 刻意不测).

Intent oracle: collect the intent evidence and draft the expected results **before** reading the implementation's branches; then read the implementation for missing branches and for mismatches. A mismatch is a ⚠ suspected defect, with evidence on both sides — the intent source, and `file:line`.

## Step 4 — Confirm, once, before any write

Present the case list from `references/case-list.md` in the terminal, with every pending item under it: ⚠ rulings, stale tests, 已有覆盖, 刻意不测, test-first entry points and stubs, the infra proposal, the document path and whether to also export `.docx`. Collect the decisions with the interactive question tool — recommended option first, at most four questions per call, several calls in a row when needed. Nothing is written until the round is complete. "全按推荐" collapses the questions; the list is still shown.

More than 30 cases for one target: confirm in priority batches — P0, then P1, then P2. The user may stop after any batch; writing starts after the last accepted one.

## Step 5 — Write

Only confirmed items.
- **Code / Test-first**: tests per the conventions above and the language file.
- **Spec → Doc**: fill `assets/test-case-doc-template.md` at the confirmed path. When the `.docx` export was accepted, generate it from the finished Markdown through the `docx` skill — same directory, same base name. The Markdown stays the source of truth. No `docx` skill on this host → deliver the Markdown and say the export was not produced.
- **Production code is never edited.** Two exceptions, both confirmed in Step 4: Test-first minimal stubs, and the build-file change of an accepted infra proposal. A testability gap is solved with test-side tooling or reported as 不可测 with the suggested seam — never with a refactor.

## Step 6 — Run (Code and Test-first)

Run only the new or modified test files (`lang-*.md` has the commands); the whole suite only when the user asks.

| Outcome | Action |
|---|---|
| The test's own fault — compile error in the test, setup, mock wiring, wrong assertion mechanics | Fix it; at most 3 rounds for the same failure, then stop and report |
| A ⚠ case the user ruled 按意图写 fails | Expected. It stays failing; the assertion is never weakened |
| A new intent / implementation mismatch shows up | Stop and ask: 按意图保留失败 / 改为按实现 / 删除该用例 |
| Lock mode, any failure | The test's fault — fix the test, never the code |
| Test-first, fails for the right reason — an assertion, the stub's not-implemented error, 404 for a missing route | Expected |
| Test-first, fails for the wrong reason (a compile error in the test code, an import, a fixture) or passes | Fix the test; one that passes before any implementation is reported as suspect |
| Nothing runnable | Say **未验证** and name what was missing. Never imply verification that did not happen |

## Step 7 — Report

Terminal, Chinese:
1. **Counts** — cases by dimension and by priority; files written.
2. **Run results** — per file, and which failures are the confirmed defects.
3. **⚠ Defects** kept failing, and mismatches found while running.
4. **Existing tests** — updated as 需更新, skipped as 已有覆盖.
5. **Production-side writes** — stubs and build-file changes, each with its path; none → say so.
6. **刻意不测 / 不可测** — with the reason or the suggested seam.
7. **未验证** — what could not run, and why.

Spec → Doc instead reports the document path(s), case counts, and the coverage-matrix gaps.

## Common Mistakes

- Writing a test, stub, document or build-file change before the confirmation round ends
- Copying the implementation's output into an assertion in intent mode — the test then certifies the bug
- Weakening, deleting or skipping an assertion to turn a red test green
- Refactoring production code to make it testable
- Mocking collaborators inside the module under test instead of the boundaries only
- A case that asserts only "no exception" or "not null"
- One test covering several behaviors
- Real clock, unseeded randomness, `sleep`, or network in a test
- Adding a test dependency or editing a build file without an accepted proposal
- Test-first: writing the implementation, or counting a compile error in the test code as "red"
- Switching to Lock without the user asking for it
- Rewriting existing tests that were not listed as 需更新
- Filling a requirement gap with an invented value instead of a 待确认
- Producing `.docx` or any other format nobody asked for
- Running `git commit`
