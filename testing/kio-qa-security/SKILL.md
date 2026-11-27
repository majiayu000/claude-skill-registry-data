---
name: kio-qa-security
description: "Kio QA, Testing, Code Review & Security hub. Use for: 4-quadrant test case matrices; unit tests (Vitest/Jest, Pytest, Go, PHPUnit) with disciplined mocking; TDD red-green-refactor; systematic debugging and root-cause tracing (flaky tests, test pollution, race conditions); evidence-based 'done' verification; deep review of risky diffs (blast radius, adversarial interrogation, solution arena, make-recurring-bugs-impossible); security review, OWASP checks, anti-bot form defense, Semgrep and CodeQL SAST with SARIF; Playwright E2E and responsive visual QA (375/768/1440)."
license: MIT
metadata:
  author: Kio System / Toan Pham
  version: 3.0.0
---

# 🧪 Kio QA, Code Review & Security (`kio-qa-security`)

The router for Kio's testing, review and security work. Knowledge lives in `references/`; this file only points the way and holds the mandatory quality gates.

`KIO_QA_ROOT` = this skill's install directory (e.g. `~/.claude/skills/kio-qa-security`).

## ⚙️ How to work

1. **Read the project's rules first** (`CLAUDE.md`, `AGENTS.md`, test commands in `package.json` / `pyproject.toml` / `Makefile`). Use the test framework the project already uses; do not add a new one.
2. **Pick one primary reference** from the [routing table](#-routing-table) and follow its process.
3. **Never report done without running it.** Every conclusion carries the command that ran and its result (exit code, pass/fail counts, report path).
4. **MANDATORY reads (open the file before you answer, not from memory):** security review or pre-merge review → `references/security-review.md`; Semgrep/CodeQL scan → `references/codeql/SKILL.md` and the workflow it names; a bug you cannot explain → `references/tdd-debugging/root-cause-tracing.md`; a risky or > 300-line diff → `references/deep-review/blast-radius.md`; UI/E2E checks → `references/playwright-e2e.md`. In the answer, name the reference you followed.

## 🧭 Routing table

| Task | Open | Notes |
|---|---|---|
| Build a test case matrix, write unit tests | `references/unit-testing-and-test-cases.md` | 4 quadrants: happy path, boundaries, edge cases, failure/security; Vitest, Pytest, Go templates |
| Work test-first, prove "done" | `references/tdd-debugging/README.md` | Red → Green → Refactor; Zero-False-Completion gate |
| Hard bug, find the root cause | `references/tdd-debugging/root-cause-tracing.md` | No fix without a root cause; stop after 3 failed attempts |
| Flaky tests from timing / races | `references/tdd-debugging/condition-based-waiting.md` | Example: `condition-based-waiting-example.ts` |
| One test pollutes another's state | `scripts/find-polluter.sh` | Bisects to the polluting test |
| Harden after a fix | `references/tdd-debugging/defense-in-depth.md` | Validate at every layer the data crosses |
| Write good tests, avoid anti-patterns | `references/tdd-debugging/writing-good-tests.md` | Never mock the unit under test |
| A change might break something elsewhere | `references/deep-review/blast-radius.md` | Prove it with code that runs |
| Large diff (> 300 lines) needs challenge | `references/deep-review/interrogate.md` | Adversarial review |
| Compare several solutions in parallel | `references/deep-review/arena.md` | |
| A bug keeps coming back | `references/deep-review/correct.md` | Make it impossible |
| Security review, 5-layer checklist, form anti-bot | `references/security-review.md` | Two-stage review, sign-off (MIT, Kio) |
| Semgrep / CodeQL SAST | `references/codeql/SKILL.md` → `workflows/` (CC BY-SA 4.0, Trail of Bits) | Scripts in `references/codeql/scripts/`, rules in `references/codeql/references/` |
| E2E tests, responsive screenshots | `references/playwright-e2e.md` | 375 / 768 / 1440 px, 1:1 against the design |

## 🔀 Selection rules for overlaps

| Need | Start at | Switch when |
|---|---|---|
| "Write tests for this function" | `unit-testing-and-test-cases.md` | New feature with no code yet → `tdd-debugging/README.md` (test first) |
| "Tests fail" | `tdd-debugging/root-cause-tracing.md` | Random failures → `condition-based-waiting.md`; only fails in the full suite → `find-polluter.sh` |
| Review a PR | `security-review.md` (two-stage + 5 layers) | Large diff or shared API → `deep-review/blast-radius.md`, `interrogate.md` |
| "Any vulnerabilities?" | `codeql/SKILL.md` | Automated scan → Semgrep first (fast), CodeQL for deep taint tracking |
| UI differs from the design | `playwright-e2e.md` | The bug is in UI code → `kio-frontend-craft` |

## 🧩 Workflows

| Job | Order |
|---|---|
| New feature | `unit-testing-and-test-cases.md` (matrix) → `tdd-debugging/README.md` (TDD) → `playwright-e2e.md` (if UI) → sign-off |
| Bug fix | `root-cause-tracing.md` → failing test that reproduces it → fix → `defense-in-depth.md` → `deep-review/correct.md` if it recurred |
| Before merging a big change | `deep-review/blast-radius.md` → `security-review.md` → `codeql/SKILL.md` (Semgrep) → full test suite |
| Pre-release security audit | `security-review.md` → `codeql/SKILL.md` → `workflows/scan-workflow.md` (Semgrep) → `workflows/build-database.md` + `run-analysis.md` (CodeQL) → `merge_sarif.py` |

Writing code belongs to `kio-frontend-craft` / `kio-backend-cloud`; planning to `kio-core-delivery`.

## 🛡️ Mandatory quality gates

1. **No "done" without a real run:** quote the command, exit code 0, 0 failing tests. Without evidence, say it is unverified.
2. **Every new feature has tests** for the happy path, boundaries, edge cases and failures.
3. **No fix without a root cause.** After 3 failed attempts, stop and revisit the hypothesis.
4. **Never mock the unit under test;** mock only external effects (network, time, filesystem, paid services).
5. **Never disable, skip or delete tests to get green.**
6. **Measure the blast radius** before merging architecture or shared-API changes.
7. **1:1 visual match** when a design exists (HTML/PDF/image): Playwright screenshots at 3 sizes; wrong colours, layout or fonts are rejected.
8. **Security:** run SAST with `--metrics=off`; never send a client's code to outside services without permission.
9. **Language:** answer in the language of the user's request (an English prompt gets an English answer), even when skill documents are written in another language.

## 📦 What's included

- `references/` — the documents in the table above (`tdd-debugging/`, `deep-review/`, `codeql/`).
- `scripts/find-polluter.sh`; `references/codeql/scripts/` (build log, database discovery, query suites, SARIF merge) with tests: `python3 -m pytest references/codeql/scripts`.
- `evals/tdd-pressure/` — scenarios checking the skill keeps TDD discipline under deadline pressure.
- `THIRD_PARTY_NOTICES.md` — credits and licenses for the open-source sources Kio uses; keep it when redistributing.
