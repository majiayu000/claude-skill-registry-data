---
name: implement
description: >-
  Use when the user asks to execute an existing task plan's Solution under TDD —
  RED → GREEN → REFACTOR → CHECK per AGENTS.md. Requires a written plan under
  the `tasks` role. Do NOT trigger on planning, review, or unrelated failing
  tests.
---

<!-- GENERATED FROM framework/atoms/implement.md via scripts/generate-skill-composites.ts — DO NOT EDIT BY HAND -->

# Task: Implement Plan Under TDD

## Overview

Execute the `## Solution` section of an existing task plan strictly under the TDD cycle defined in AGENTS.md: write a failing test (RED), write the minimal code that makes it pass (GREEN), improve without changing behaviour (REFACTOR), then run the project check (CHECK). Do not advance to the next iteration until CHECK is green; never edit a failing test to make it pass; never silence lint/format errors.

## Context

<context>
The user has already produced a plan. The plan file is resolved through the `tasks` role in AGENTS.md and contains a `## Solution` section enumerating the concrete steps to implement. This skill is the Implement Phase of the canonical task lifecycle and is consumed by the `ship` composite as its second phase. The phase BEFORE this one writes the plan; the phase AFTER reviews the diff.
</context>

## Rules & Constraints

<rules>
1. **Plan is authoritative**: re-read the plan file from disk before each iteration. The `## Solution` section drives scope; deviations are forbidden.
2. **TDD strictly**: per AGENTS.md "TDD Flow" — RED → GREEN → REFACTOR → CHECK. Skipping any phase (especially the failing-test RED step) is forbidden.
3. **Never edit tests to pass**: when a test fails, fix the source — not the test. Do not add swallowing, skips, `.todo`/`xfail`, or wider mocks to silence a failure.
4. **No lint/format suppression**: `// deno-lint-ignore`, `eslint-disable`, `# noqa`, etc. are forbidden unless the rule itself is genuinely wrong (rare). If CHECK reports a lint failure, fix the code, not the rule.
5. **Scope discipline**: changes are limited to those required by the plan's `## Solution`. Out-of-scope discoveries (pre-existing failing tests, formatter drift on untouched files, missing `deno.lock`, dependency updates, README polish) are surfaced as "out-of-scope findings" in chat — NOT folded into this commit. Silently fixing them turns a no-op task into an unrequested cleanup.
6. **Stop on second-fix-failure**: per AGENTS.md "Diagnosing Failures", emit a STOP-ANALYSIS REPORT after a second failed fix attempt on the same root cause and STOP — do not keep iterating.
7. **Planning**: use a task management tool (e.g. `todo_write`, `todowrite`, `Task`) to track the Solution's steps and each RED/GREEN/REFACTOR/CHECK iteration.
8. **No-op handling**: if re-reading the plan and examining the codebase shows the requested feature is already satisfied, STOP without making any source-code changes and surface "Solution turns out to be a no-op — nothing to implement."
9. **Decision gate (above class/method)**: if a Solution step surfaces a decision ABOVE the class/method line that the approved plan has NOT already settled — a business rule, an architectural choice, a public interface or data shape, a new dependency, a key technical trade-off — STOP, surface it to the human as options + trade-offs + a recommendation, and WAIT for their call before writing that code. Do NOT self-select a default and proceed. Choices at or below class/method granularity (local naming, private helpers, test layout) are yours to make without asking. The human's gate is the decision, never the diff.
</rules>

## Instructions

<step_by_step>

1. **Re-read the Task File**
   - Read the user-provided task file from disk (do NOT rely on memory). If the user gives only an identifier, resolve the `tasks` role from AGENTS.md and locate the matching task there. The user MUST provide either a path or an unambiguous task identifier; if it is missing, ask once.
   - Extract the `## Solution` section. The implementation steps listed there are authoritative.
   - Re-plan the todo list with the Solution's concrete steps. One todo item per RED/GREEN/REFACTOR/CHECK iteration is acceptable, but ensure every Solution bullet is represented.

2. **Determine the Project Check Command**
   - Priority: AGENTS.md / CLAUDE.md documented check command → manifest detection (`deno.json`/`deno.jsonc` → `deno task check`; `package.json` → `npm run check`/`test`/`lint`; `Makefile` `check` target → `make check`; `pyproject.toml` → `pytest` / `ruff check .`; `go.mod` → `go vet ./... && go test ./...`) → "no automated checks configured".
   - MUST NOT run a stack-specific command when its manifest is absent (any `deno *` creates `deno.lock`, any `npm *` resolves dependencies, etc.). Pre-flight artifacts in the working tree after verification are a bug.
   - **Baseline record**: run the project's test suite ONCE on the code without your change and write the ids of the failing tests to a file in a scratch dir outside the repository. This is the session's record of what was red before your change; later steps classify failures against it instead of rerunning the suite. **The record never holds up the work**: run it in a separate tree of the unchanged code (`git worktree add <scratch-dir> HEAD`), in the background, with its output in a file, and start RED in the working tree right away. Rules for that one run:
     - First check in seconds that the suite can start — a collect-only or dry-run mode, or one small test module. If it cannot — collection or import errors, a missing dependency — make it runnable, then start the record. The record is taken once, on an environment that runs.
     - Point the separate tree at the working tree's environment (the same interpreter, virtualenv or installed dependencies, by absolute path) instead of building a new one. Then confirm the separate tree tests its OWN code: when the project is installed into that environment in development (editable) mode, the environment resolves the project's package to the working tree, and the record silently measures your change. Put the separate tree first on the import or module path and check once where the package is loaded from.
     - No fail-fast flags (`-x`, `--exitfirst`, `--bail`, `--failfast`): a run stopped at the first failure records one failure and forces another run. Where the runner can, let it continue past collection errors.
     - Wait for the record only when you need it: when your own test run would collide with the background run (a fixed port, a shared database or file), and in step 5. Until then keep writing the test and the code.
     - Green suite → an empty record. No test command → no record. Remove the separate tree after step 5.

3. **TDD Loop (per Solution step)**
   - **RED**: write a single failing test for the new/changed behaviour. Run the project test command (or the focused test if the runner supports it). It MUST fail with a message that points at the missing functionality. A test that passes immediately is not RED — revise the test until it fails for the right reason.
   - **GREEN**: write the minimal production code that makes the failing test pass. Do NOT add features or speculative code paths beyond what the test demands.
   - **REFACTOR**: improve names, structure, duplication, and tests without changing observable behaviour. Re-run the tests after each refactor — they MUST still pass. If refactor breaks a test, STOP and decide: is the test wrong, or did the refactor change behaviour? Revert the refactor if behaviour drifted.
   - **CHECK**: run the project check command from step 2. When its test suite takes more than about a minute, run between steps the format and lint part plus the tests that cover this step — the new test and the test modules of the code you changed — and leave the whole suite to step 5. It MUST pass, apart from tests on the baseline record. If it fails:
     - **Within Solution scope**: fix the root cause. Do NOT disable lint rules or silence formatter output. On a second fix attempt that also fails, STOP and emit STOP-ANALYSIS REPORT per AGENTS.md "Diagnosing Failures".
     - **Pre-existing / out-of-scope**: surface as "out-of-scope finding"; do NOT fix here.
     - **Classify a failing test from the baseline record (step 2)**, not by another run of the suite. On the record → pre-existing. Not on the record → caused by your change until shown otherwise: fix it and rerun that test alone. Only when the record cannot tell — no record was taken, it is not in yet, or the test looks flaky — run that one test, not the suite, on the parent revision as the next bullet says.
   - **Looking at the code without your change** (is this failure pre-existing? does the new test fail on the original source? lint or type-check output before vs after): run it in a separate tree — `git worktree add <scratch-dir> HEAD`, then `git worktree remove` it when done — or read one file with `git show HEAD:<path>`. **Never take your uncommitted work out of the working tree to do it** — no `git stash` in any form, no `git checkout -- <path>`, `git restore` or `git reset` of the files you changed. A session cut off before the work is put back leaves the working tree empty, and the finished change is lost.

4. **Repeat per Solution step**
   - After CHECK is green for the current Solution step, return to RED for the next step. Update the todo list status.
   - When all Solution steps are implemented and CHECK is green, proceed to the final step.

5. **Final Verification**
   - Run the project check command one last time on the full project (not just the changed file). It MUST exit 0, or fail only on tests in the baseline record (step 2) — list those as out-of-scope findings. A failure off the record is yours: fix it, then rerun the tests that failed and the modules covering the fix, not the whole suite.
   - Keep the baseline record file until the session ends: a review in the same session reads it instead of running the suite on the parent.
   - Confirm `git status` is non-empty (otherwise the Solution was a no-op — surface that and STOP).
   - Confirm no scope creep: every changed file maps to a Solution bullet.

6. **6. **TOTAL STOP**
   - Narrate the result UPWARD, not as a diff. Report: (a) which requirements / Solution steps are now satisfied; (b) the class/method structure you produced or changed — names, responsibilities, and how they relate — in prose the human can follow WITHOUT reading the code; (c) every above-class/method decision you made or surfaced (or "none — purely local"); (d) the final check result. The human must be able to accept the work from this summary alone; reading the diff is optional, never required.**

</step_by_step>

## Verification

<verification>
- [ ] Plan file re-read from disk; Solution section drove the implementation scope.
- [ ] Every Solution step went through RED → GREEN → REFACTOR → CHECK.
- [ ] No test was edited to make a failing assertion pass.
- [ ] No lint/format suppression added (no `// deno-lint-ignore`, `eslint-disable`, `# noqa`, etc.).
- [ ] Final project check exits 0 on the whole project, or fails only on tests in the baseline record.
- [ ] The whole suite ran once on the unchanged code, in a separate tree in the background while the work went on (the baseline record), and once at the end; failures were classified from the record, and the parent revision ran only single tests the record could not explain.
- [ ] `git status` is non-empty AND every changed file maps to a Solution bullet.
- [ ] Out-of-scope findings surfaced separately and NOT folded into this work.
- [ ] STOP-ANALYSIS REPORT emitted on second-fix-failure (if any).
- [ ] Final summary narrates requirements + class/method structure (names, responsibilities, relationships) in prose; the human can accept WITHOUT reading code, and the diff is framed as optional.
- [ ] Every above-class/method decision was surfaced to the human and approved before coding (or none arose); none was silently self-selected.
</verification>
