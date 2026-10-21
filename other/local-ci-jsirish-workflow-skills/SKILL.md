---
name: local-ci
description: Run the project's test/lint checks locally (PHPUnit, PHPCS, PHPStan, npm, ruff/pytest, shellcheck, .local-ci.json) and report PASS/WARN/FAIL. Use for "run local CI", "run the checks before a PR", "run ci", "check before opening a PR", "run the tests", "does it pass", or verifying before merge.
---

# Local CI

LLM review (`/code-review`, `pr-review-toolkit`) reasons about code but **never executes a test suite**. This skill fills that gap: it detects which check configs a project has and runs the matching checks, the same canonical set `silverstripe/gha-ci` runs in CI — PHPUnit, PHPCS, PHPStan, the npm scripts, and (for Python) ruff + pytest. It also covers shell projects that have adopted shellcheck (via `.shellcheckrc`) and, via a project-committed `.local-ci.json`, any custom entrypoint a project's real CI actually runs.

It is the executable counterpart to review, not a replacement. Run it, then feed the summary into the review. By default it auto-fixes (phpcbf, eslint --fix, ruff --fix; skip with `--no-fix`), then reports PASS/WARN/FAIL/SKIP per check. It replaces per-project `tests.sh` scripts and is self-contained: it bundles `scripts/local-ci.sh`.

## When to use

- After writing a feature, before opening a PR.
- As the test pass alongside `/code-review` or `pr-review-toolkit` — run this first, then review with the results in hand.
- Before `/merge-pr`, to confirm the branch is green locally.

Cadence: `feature-dev` → **`/local-ci`** → push → `/code-review` or `/pr-review-toolkit` → `/merge-pr` → `/handoff`.

## What it runs (gating by config presence)

**Every check is WARN-by-default** — a no-flag run never blocks (`exit 0`), it just surfaces
findings in the SUMMARY. Pass `--strict` to escalate the whole run to FAIL, or a scoped
`--strict-build` / `--strict-lint` to escalate just that category. The one exception is a
**broken local-ci setup** (malformed `.local-ci.json`) — that's always a hard FAIL, `--strict`
or not, because it isn't a finding to review, it's local-ci itself failing to run.

| Check | Fires when present | Command |
|---|---|---|
| composer validate | `composer.json` present | `composer validate --strict` (genuine errors: WARN; FAIL with `--strict`. `--strict`-only cosmetic warnings always WARN) |
| composer install | `vendor/` missing or `--fresh-deps` | `composer install` (else `--dry-run` resolve check) (WARN; FAIL with `--strict`) |
| dev/build | `vendor/bin/sake` (SilverStripe) | `sake dev/build flush=1` (WARN; FAIL with `--strict-build` or `--strict`) |
| PHPUnit | `phpunit.xml` / `.dist` | `vendor/bin/phpunit` (config present but binary missing → WARN, not silently skipped; test failures → WARN, FAIL with `--strict`). Under DDEV, runs with `SS_DATABASE_USERNAME=root SS_DATABASE_PASSWORD=root` for just this invocation — DDEV's default `db` user can't `CREATE DATABASE` for SilverStripe's per-run `ss_tmpdb_*` temp DB, which otherwise fails every PHPUnit run before a test executes. Never written to `.env`; the app's own runtime DB access is untouched. |
| PHPCS | `phpcs.xml` / `.dist` | `phpcbf` (auto-fix) → `phpcs --standard=…` (config present but binary missing → WARN, not silently skipped; findings → WARN, FAIL with `--strict-lint` or `--strict`) |
| PHPStan | `phpstan.neon` / `.dist` | `vendor/bin/phpstan analyse` (config present but binary missing → WARN, not silently skipped; findings → WARN, FAIL with `--strict-lint` or `--strict`) |
| JS lint | `package.json` lint script or eslint config | `eslint --fix` → `npm run lint` (findings → WARN, FAIL with `--strict-lint` or `--strict`) |
| JS build | `package.json` build script | `npm run build` (WARN; FAIL with `--strict`) |
| JS test | `package.json` test script | `npm test` (npm placeholder script is skipped) (WARN; FAIL with `--strict`) |
| Python lint | `[tool.ruff]` in `pyproject.toml`, `ruff.toml`/`.ruff.toml`, or a ruff hook in `.pre-commit-config.yaml` | Interpreter/binary resolution prefers a project-local venv (`$VIRTUAL_ENV`, else `./.venv`, else `./venv`) over a global `ruff` or `python3 -m ruff`, so a project's pinned version isn't silently shadowed by an older/newer global install → `ruff check --fix` → `ruff check` (config present but ruff not resolvable → WARN, not silently skipped; findings → WARN, FAIL with `--strict`) |
| Python test | pytest resolvable (same venv-first resolution as ruff above) + tests present | `pytest -q` with cwd forced onto `PYTHONPATH` (no tests found → SKIP; **tests found but pytest not resolvable → WARN, not silently skipped**; failures → WARN, FAIL with `--strict`) |
| Behat | `behat.yml` | **opt-in** via `--with-behat` (needs a browser/driver) (WARN; FAIL with `--strict`) |
| Shellcheck | `*.sh` files present (tracked or untracked-but-not-ignored) and `.shellcheckrc` exists, or forced via `--with-shellcheck` | `shellcheck` over every matching file (dialect autodetected per-file from its shebang; adopted-but-missing-binary → WARN). Deliberately config-only, like the Python lint row below — no "shell-only project" auto-adopt, since shellcheck's default sensitivity would otherwise swamp a project's very first run with no escape hatch (findings → WARN; FAIL with `--strict`) |
| Custom checks | `.local-ci.json` at the project root | Runs each declared command as its own check (`jq` missing → WARN; malformed file or a check missing `"run"` → **always FAIL**, regardless of `--strict`; a declared check's own failure → WARN, FAIL with `--strict`) |

The legacy `phpmd` / `phploc` / `pdepend` / `phpdox` tools some old `tests.sh` scripts ran are intentionally **not** included — no project CI actually runs them.

### Custom checks (`.local-ci.json`)

For a project whose real CI isn't shaped like any of the language drivers above — e.g. a pure-shell repo that also runs `jq`-based manifest validation or its own test harness — commit a `.local-ci.json` at the project root:

```json
{
  "checks": [
    { "label": "manifest validation", "run": "jq -e '.name' plugin.json >/dev/null" },
    { "label": "hook tests", "run": "sh tests/run.sh" }
  ]
}
```

Each entry becomes its own `custom[<dir>]: <label>` row in the SUMMARY, executed via `bash -c` and recorded PASS/WARN (FAIL with `--strict`) like any other check. **Trust model:** this is identical to local-ci already running a project's own npm/composer scripts — it executes commands the project itself authored and committed. Requires `jq` on the host to parse the file; if `jq` is missing, this driver WARNs instead of silently skipping. A malformed `.local-ci.json` (not valid JSON, or a check missing `"run"`) is a **broken setup, not a finding** — it always FAILs, `--strict` or not. Custom checks run regardless of `--no-fix` — same as PHPUnit/npm test/pytest above; only the auto-fixer sub-steps (phpcbf / eslint --fix / ruff --fix) are gated by that flag.

## How to run

From the project root:

```bash
bash <path-to-skill>/scripts/local-ci.sh
```

Options:

- `--dry-run` — detect checks and print what *would* run; execute nothing. Use this first on an unfamiliar project to see the plan before anything mutates files or the DB.
- `--no-fix` — report only; do not run phpcbf / eslint --fix / ruff --fix.
- `--no-build` — skip the SilverStripe `sake dev/build` step.
- `--strict` — escalate **every** check to FAIL on a non-zero exit, restoring hard-gating for the whole run in one flag. Implies `--strict-build` and `--strict-lint`. Use when you want the same hard gate GHA enforces, or before a push you want a real pass/fail on.
- `--strict-build` — treat a failing `sake dev/build` as FAIL rather than WARN, without escalating anything else. A subset of `--strict`.
- `--strict-lint` — treat failing phpcs/phpstan/eslint as FAIL rather than WARN, without escalating anything else. A subset of `--strict`.
- `--fresh-deps` — force a real `composer install` even when `vendor/` exists. Mirrors GHA's clean-install behaviour; slower and mutates `vendor/`. Use before a PR to verify a clean dependency resolution.
- `--with-behat` — also run Behat (off by default; it needs a browser + chromedriver).
- `--with-shellcheck` — force shellcheck even without a `.shellcheckrc`.
- `DIR …` — one or more dirs to scan. Default: the current dir plus the common
  sub-package dirs `frontend/ client/ backend/ app/` when they exist (handles
  monorepo layouts).

### Execution context

When a project has `.ddev/config.yaml`, **PHP** checks run via `ddev exec` and **composer** via `ddev composer` (the DDEV wrapper handles container mounts correctly). **JS and Python** checks always run on the host — DDEV web containers rarely carry the node/python toolchain. No flag needed; detection is automatic.

> **Note:** `ddev exec` always runs from the container's fixed working directory (`/var/www/html`), so a per-dir `cd` before invoking a PHP check doesn't reach the container on its own. **PHP-under-DDEV is fully supported only at the project root, or a `vendor/` live checkout nested under it (below)** - any other per-dir PHP sub-package (a monorepo `backend/`/`app/` dir, for instance) has no DDEV routing and silently runs bare-metal against whatever host PHP toolchain is installed; scan those from the project root for reliable results, or expect bare-metal execution if you scan them directly.
>
> For a PHP dir that sits *nested* under a different project's DDEV root (e.g. a SilverStripe module developed as a live git checkout inside that project's `vendor/` tree, rather than a plain composer-installed package): when the scanned dir is its own git checkout (has its own `.git`) sitting under a `vendor/` path, local-ci checks specifically the directory enclosing the *nearest* `vendor/` segment (not the leftmost, so a path with an unrelated earlier `vendor/` component still resolves to the real boundary) for `.ddev/config.yaml` - not a general ancestor walk - and if found, routes PHP/composer checks through `ddev exec -p <enclosing-project-name> -d /var/www/html/<relpath-from-root>` instead of falling back to a bare-metal toolchain. Both `-p` and the absolute container path are required, not just convenience: `ddev exec` resolves which project to target by walking up from the *invoking shell's* cwd to the nearest `.ddev/config.yaml`, not from `-d`'s value - and every check here runs from inside the nested dir itself. If that dir has its own `.ddev/config.yaml`, an unpinned `ddev exec -d <relpath>` would silently target *that* project's own separate container instead of the enclosing one (confirmed against a real nested-ddev fixture: without `-p` it started the wrong container; with `-p` it correctly targeted the enclosing project even when invoked from inside the nested dir). A candidate root only counts if it also has its own `composer.json` or `composer.lock` - a coincidentally-named `vendor/` directory that isn't actually a composer vendor boundary is left alone. This check runs *before* checking whether the nested dir has its own `.ddev/config.yaml` - **a deliberate choice, not an oversight**: the point of scanning a nested `vendor/` checkout is to test it *as integrated into the enclosing project* (its real dependencies, DB, PHP version), not the module's own separate standalone environment. If the module's own `.ddev/config.yaml` pins a different PHP version than the enclosing project, checks now run under the enclosing project's version - this is expected; local-ci records a WARN (`possible PHP-version mismatch`) whenever it routes this way and the nested dir also has its own `.ddev/config.yaml`, so the tradeoff is a visible runtime signal rather than a silent choice. Run the module's own test suite from its own separate checkout (not as a `vendor/` subdir scan) if you want its standalone environment instead. This does not by itself prevent a nested module's own `composer.json` from pulling in a `require-dev` package whose post-install script assumes it's a project root (e.g. a test-scaffold recipe) - that risk exists regardless of ddev vs bare metal, and local-ci flags it with a WARN on the module's first install rather than silently letting it happen. Pass the nested dir as an explicit `DIR` argument to scan it (see Options above); scanning only the project root does not also check its nested `vendor/` live checkouts. In this nested case, PHP tool invocations (`sake`, `phpunit`, `phpcs`, `phpcbf`, `phpstan`, `behat`) resolve against the *enclosing* project's `vendor/bin` rather than the nested checkout's own - as `/var/www/html/vendor/bin/<tool>` inside the container, since the nested checkout's own `vendor/` (if it has one, from a standalone composer install) is disconnected from the DDEV database and would otherwise fail with connection errors.

## Reading the result

The script ends with a `SUMMARY` block listing every check as PASS / FAIL / WARN / SKIP, then an `AUTO-FIX CHANGES` section (`git diff --stat`) showing any files a fixer mutated.

**A default (no-flag) run exits `0` even when real checks find real problems** — findings report WARN, not FAIL, unless escalated with `--strict` (or a scoped `--strict-build` / `--strict-lint`). The only thing that FAILs by default is a broken local-ci setup itself (a malformed `.local-ci.json`). **Read the SUMMARY text, not just the exit code** — a clean exit code no longer means a clean SUMMARY. Any automation that only checks the exit code will silently treat a WARN-covered failure as clean. The closing line reflects this too: `Result: all checks passed.` only when the SUMMARY has no WARN or FAIL rows; a WARN-only run instead prints `Result: no FAILs, but findings are WARN — read the SUMMARY above`.

A `composer install` or `npm install` failure (WARN by default) also short-circuits the checks that depend on it for that dir (dev/build, phpunit, phpcs, phpstan; or JS lint/build/test) — those show up as an explicit `SKIP …(install did not succeed)` row rather than silently vanishing from the SUMMARY.

When augmenting a review:
1. Run `local-ci.sh` and capture the summary.
2. If auto-fixes changed files, review that diff — those are real edits to your working tree.
3. Carry FAIL/WARN items into the review as concrete findings the LLM pass can then explain or contextualise. WARN is not a green gate for "done" — investigate it — even though it doesn't block a push.
4. Before a merge or a push you want a hard guarantee on, re-run with `--strict`.

## Status marker and the git-push gate

Every non-dry run writes a one-line marker to `<git-dir>/local-ci-status`:

```
sha=<HEAD-at-run> result=<PASS|FAIL|WARN|NONE> ts=<epoch>
```

`scripts/git-push-gate.sh` is a Claude Code `PreToolUse` (Bash) hook that consumes the marker and blocks `git push` only when the last recorded run **FAILed**, or a recorded **PASS** is stale or not an ancestor of HEAD. A PASS is valid at HEAD, or at an ancestor of HEAD for 4 hours (covers the run-ci, commit, push flow). A **missing marker** (no local-ci run recorded) and a **WARN** result both **allow the push** — WARN still isn't a green gate for "done" (investigate before declaring done), but it no longer blocks the push itself; a marker being missing means CI was never run against this repo, which shouldn't be able to trap a push behind a check that was never kicked off. The marker is stamped per repo: a run against one repo never green-lights another, and runs where nothing executed record `NONE`, not `PASS`.

Since every check is WARN-by-default, a **default run's marker is `PASS` or `WARN` — never `FAIL`** (only a broken `.local-ci.json` setup, or `--strict`/`-build`/`-lint`, can produce a FAIL marker). In practice this means the push gate is opt-in gating too: run without flags to see where things stand without risking a blocked push, or run with `--strict` when you want a marker that can actually block.

The command is parsed with a shell tokenizer, not a regex, so quoted `-C` paths, paths with spaces, `git -c <cfg>` options, multiple pushes in one compound command, and strings that merely mention "git push" are handled correctly. It also tracks a preceding `cd <dir>` (including `~`/`$VAR` expansion and `-C`/`--work-tree` composed onto it) as the effective directory for a later bare `git push`, and trusts a not-yet-existing target that was the destination of an earlier `mkdir`, `git clone`, or `git worktree add` in the same command (`mkdir foo && cd foo && git push`) - see the script's own header comment for the full set of tracked patterns and documented edge cases. Known fail-open cases, by design: `jq` or `python3` missing, and git aliases that expand to push. Do not treat the gate as a security boundary; it is a workflow guard.

Register it in `~/.claude/settings.json` under `hooks.PreToolUse` (matcher `Bash`):

```json
{ "type": "command", "command": "/path/to/skills/local-ci/scripts/git-push-gate.sh" }
```

Bypass for an investigated, genuinely benign case: prefix the push with `SKIP_CI_GATE=1`.

## Notes

- **Behavior change:** every check used to hard-FAIL (non-zero exit) by default except phpcs/phpstan/JS-lint/dev-build. As of this change, **all checks are WARN-by-default** and a no-flag run exits `0` even with real failures. Any script or CI wrapper that invoked `local-ci.sh` and relied on a non-zero exit in default (no-flag) mode needs `--strict` added to preserve the old behavior.
- **`composer validate` and `composer install --dry-run` run automatically** on every PHP project — these are the same checks GHA performs implicitly when building the environment. If `vendor/` is missing, a real install runs instead. Use `--fresh-deps` for a full clean-install mirror.
- `composer validate` runs with `--strict`, which also surfaces recommendation-level warnings (loose version constraints, a stray `version` field, etc.), not just real problems (malformed json, out-of-sync lock) — and both share the same non-zero exit code. If `--strict` fails, the script re-checks with a plain (non-strict) `composer validate`: still non-zero means a genuine problem and records WARN (FAIL with `--strict`); exit 0 means the only issue was a --strict-only warning, which always records WARN. WARN surfaces in the SUMMARY and no longer blocks `git push` via the push gate (see below), but is still worth investigating before declaring the change done.
- `dev/build` failure is WARN by default because phpunit can sometimes self-bootstrap from its own bootstrap file. Pass `--strict-build` (or `--strict`) to make it a hard gate.
- The script never commits. Auto-fixes are left in the working tree for you to review and commit.
- A project with no recognised configs reports "nothing to run" rather than erroring. A project that *does* have a recognised config (composer.json, package.json, a Python marker file, `*.sh` sources, or `.local-ci.json`) but where a specific driver still records nothing for it gets its own named WARN (`<PREFIX>[<dir>]: config recognised but nothing was recorded for this driver`) instead of silently vanishing — this is checked per directory and driver, not just "was the whole run's SUMMARY empty," so it isn't masked by other dirs/drivers in the same scan legitimately producing output. Every driver's own "recognised, but genuinely nothing to check" states (e.g. a package.json with no lint/build/test script, or a Python project that hasn't adopted ruff and has no tests) are recorded as their own SKIP rather than silence, precisely so this WARN is reserved for real gaps and doesn't false-alarm on ordinary projects.
