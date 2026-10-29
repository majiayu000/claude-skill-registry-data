---
name: verify
description: Run and fix the software-factory verification gate (scripts/verify.sh) from the repo root — format, build, config-JSON and oxlint-plugin guards, typecheck, lint, knip, tests with coverage thresholds and the coverage ratchet, the stub eval, and the shell-script tests. Use before every commit or push, when asked to "run verify", "run the checks", "make CI green", when a CI `ci` job fails, when the coverage ratchet complains, or when running the pipeline integration tests.
---

# Verify

Run every command from the repo root. Tests only resolve from there.

## Which path to run

| When                                        | Command                           |
| ------------------------------------------- | --------------------------------- |
| Before every commit (fast loop)             | `bash scripts/verify.sh --no-e2e` |
| Before you push (adds the coverage ratchet) | `bash scripts/verify.sh`          |
| Pipeline integration suites (on demand)     | `npm run test:integration`        |

The factory's own CHECK phase runs `bash scripts/verify.sh --no-e2e` in the build worktree (`packages/core/src/checkers/index.ts`).

## What `scripts/verify.sh` runs, in order

1. `npm ci`
2. `npm run format:check` (Prettier, includes Markdown)
3. `npm run build` (`tsc -b`)
4. `npm run adr:index -- --check` — the ADR index table in `docs/adr/README.md` must match the ADR files
5. `bash scripts/check-config-json.sh` — no JSON may exist under `packages/config/src` or `dist` (#716)
6. `bash scripts/check-oxlint-plugin-version.sh` — `@oxlint/plugins` must match `oxlint` exactly (#795)
7. `npm run typecheck`
8. `npm run lint` — Oxlint, type-aware, `--deny-warnings`
9. `npm run knip` — dead code and unused dependencies
10. Tests:
    - full path: `npm run test` (Vitest with coverage thresholds), then `npm run coverage-ratchet`
    - `--no-e2e`: `npm run test` (Vitest with coverage thresholds), no ratchet
    - after the tests, `npm run slowest-tests` prints the 5 slowest files and `npm run test-budget` compares the test-step wall-clock time against `TEST_BUDGET_SECONDS` in `scripts/test-budget.ts` (450s; override for one run with `FACTORY_TEST_BUDGET_SECONDS`). It prints `test-budget: PASS` within budget, a warning plus the slowest files when over locally, and fails verify in CI (`CI` set, e.g. `CI=true`) with `test-budget: FAIL` plus the slowest files
11. `npm run eval -- --stub`
12. Shell-script tests: `auto-merge-sweep`, `filter-green-prs`, `repo-merge-settings`, `repo-about`, `repo-issue-optics`, `ruleset-copilot-review`, `launchd/install-sweep-plist`, `publish-workspaces` (guards the publish list `scripts/publish-workspaces.txt` against the workspace graph)

CI (`.github/workflows/ci.yml`) runs the same checks as the full path, split into parallel jobs: `static` (format, build, guards, typecheck, lint, knip) and `test (1/3)`…`test (3/3)` (Vitest shards that write blob reports with raw coverage and no thresholds, via `FACTORY_COVERAGE_SHARD=1`). The required `ci` job fails unless all of them succeeded, then merges the shard reports (`vitest --merge-reports`) and enforces the coverage thresholds, the ratchet, and the stub eval on the merged result. A red `ci` names the failing job; read that job's log. CI also runs `scripts/quickstart-smoke.sh` in a separate job. It does not run the `install-sweep-plist` test.

## Coverage gate and ratchet

- Thresholds live in `vitest.config.ts`: one global set plus one set per package. Read the file for the current numbers.
- A drop below any threshold fails `npm run test`. Add tests. Never lower a threshold.
- `npm run coverage-ratchet` fails when measured coverage beats a threshold by more than 2 points (`DEFAULT_RATCHET_SLACK`). Raise that threshold to the suggested value it prints, in the same PR.
- `packages/core/src/types/**` and `packages/core/src/test-support/**` are excluded from coverage.

## Max-lines guard

No lintable file may exceed 500 lines. Tests count, and so do blank lines and comments. The limit is set in `oxlint.config.ts` and enforced by `npm run lint` (step 8). `scripts/max-lines-config.test.ts` enforces it again in the test step.

`max-lines-baseline.json` grandfathers files that were already over the limit. It is a flat JSON object that maps a repo-relative path to the line count recorded when the file was grandfathered. That count is the file's own ceiling, so the file may shrink but never grow. Never add a new entry and never raise a count. CI enforces this; see [Human override](#human-override).

### New file over 500 lines

Lint fails with `File has too many lines`, and the test step fails because the file is not baselined. Split the file by responsibility into colocated modules of 500 lines or fewer. Keep `.js` import extensions, and split the colocated tests the same way. Do not add the file to the baseline.

### Baseline file grew

Lint fails for the file, and the test step reports it grew past its recorded ceiling. Move code out, or split the file, until it is at or under its recorded count. Never raise the number.

### Baseline file shrank or was deleted

The test step names the file in a `remove it from max-lines-baseline.json` message. Delete its line from `max-lines-baseline.json` so the default 500 ceiling applies again.

### Human override

The CI `static` job's "Max-lines baseline guard" step diffs `max-lines-baseline.json` against the PR base. It fails on a raised count or a new entry.

Only a human may approve one, by applying the `max-lines:override` label to the PR. Then re-run the failed `static` job (or push), because a label change does not re-trigger CI. A label applied by a bot or app identity, or by a login in the `FACTORY_BOT_LOGINS` repo variable, does not count. Lowering or removing entries never needs the label.

Agents must never apply the label, never raise a count themselves, and never compact unrelated code to fit. They split the file, or ask a human for the label in the PR body or park comment.

Local `verify.sh` does not enforce this.

## Integration tests

`*.integration.test.ts` files (real git worktrees, whole plan → build → check → ship cycles) are excluded from both verify paths. They run nightly in `.github/workflows/nightly-integration.yml` (07:00 UTC). Run them with `npm run test:integration` when you touch `packages/core/src/phases/` or worktree handling.

`npm run mutation` (Stryker) runs on demand only. It is not part of `scripts/verify.sh` and CI does not run it (#805).

## Fixing common failures

| Failing step                              | Fix                                                                                                                                       |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `format:check`                            | `npm run format`, then re-run.                                                                                                            |
| `adr:index --check`                       | `npm run adr:index`, commit the README change. If it names an unparseable ADR, fix that file's `# ADR-NNNN:` heading or `- Status:` line. |
| `check-config-json`                       | Move the data into `packages/config/src/defaults.ts` as typed TS. Delete the JSON file.                                                   |
| `check-oxlint-plugin…`                    | Bump `oxlint` and `@oxlint/plugins` to the same version in `package.json`, then `npm install`.                                            |
| `lint`                                    | Fix the code. Warnings fail the build too.                                                                                                |
| `lint` / test: `max-lines`                | See [Max-lines guard](#max-lines-guard).                                                                                                  |
| `knip`                                    | Delete the unused export, file, or dependency.                                                                                            |
| `test` threshold                          | Add tests for the uncovered lines the report names.                                                                                       |
| `coverage-ratchet`                        | Raise the named threshold in `vitest.config.ts` to the suggested value.                                                                   |
| `eval --stub`                             | See the `run-evals` skill.                                                                                                                |
| Tests pass in root, fail inside a package | Expected. Run from the repo root. Do not change `packages/core/package.json`'s `test` script.                                             |
