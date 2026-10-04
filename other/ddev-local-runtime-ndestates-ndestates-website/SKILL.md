---
name: ddev-local-runtime
description: 'Mandatory rule that all local project commands for the ndestates-io repository run inside the DDEV runtime, not on the host shell. Apply when about to run php, composer, artisan, npm, node, python3, pip, mysql, pest, phpunit, or any project tooling locally.'
user-invocable: true
disable-model-invocation: false
---

# DDEV is the local runtime — host shell is not supported

## 2) DDEV Runtime Rules

### 2.0) Hard rule: All local commands run via DDEV (mandatory)

When working locally on this repository, all project commands MUST be executed inside the DDEV runtime. The host shell is not a supported execution environment for project work.

- Use `ddev exec <command>` for any command that touches application code, dependencies, the database, or runtime tooling.
- Use the dedicated DDEV wrappers when available: `ddev php`, `ddev composer`, `ddev artisan`, `ddev mysql`, `ddev npm`, `ddev yarn`, `ddev pnpm`, `ddev xdebug`, `ddev exec python3`, `ddev exec doctl`.
- Do NOT run `php`, `composer`, `artisan`, `npm`, `node`, `python3`, `pip`, `mysql`, or `doctl` directly on the host. If a host-only invocation is unavoidable (e.g. `git`, `gh`, `docker` for image build/push, repo-wide `find`/`grep`), state why before running it.
- If DDEV is not running, follow section 2.1 (start it) before issuing any project command.
- For tests, prefer `ddev exec ./vendor/bin/pest` / `ddev exec php artisan test` over host invocations. Database tests must target the DDEV `db` service or `:memory:` per section 6.
- For Python tooling, see "Python Environment Rule (Inside DDEV)" below — `ddev exec python3 ...` is the only supported path.
- The only project command exempt from DDEV is the DDEV control surface itself: `ddev start`, `ddev stop`, `ddev status`, `ddev describe`, `ddev restart`, `ddev import-db`, `ddev export-db`.

Rationale: keeps the local toolchain, PHP/Python versions, extensions, env vars, and DB engine identical to CI and production-adjacent environments. Bypassing DDEV produces drift bugs that don't reproduce on the server.

### 2.1) DDEV lifecycle

- Check DDEV status before running project commands.
- If DDEV is not running:
  1. Run `git status --short` and treat it as a baseline.
  2. Run `ddev start`.
  3. Run `git status --short` again and compare.
  4. If startup created file changes, report them and ask whether to keep or discard before continuing.
- Keep DDEV running for the session unless the user asks to stop it.
- At session end, when stopping DDEV, ensure tomorrow's TODO file exists. If it does not exist, create it before or immediately after `ddev stop`.
- Assume `ddev start` can change tracked files (hooks, dependency updates, migrations, asset publishing). Do not include those side effects in commits unless explicitly requested.

### Session Lifecycle Checklist

Startup (mandatory):
- Find the latest `TODO-YYYY-MM-DD.md` file in `TODO/` (or `TODO/archive/` if needed).
- If today's TODO file is missing, create `TODO/TODO-<today>.md` by carrying forward open items from the latest TODO.
- Read today's TODO and state the active work items before proceeding.

Shutdown (mandatory when user asks to stop DDEV):
- Compute tomorrow's date and check for `TODO/TODO-<tomorrow>.md`.
- If missing, create `TODO/TODO-<tomorrow>.md` with carried-forward open items and a short "next session" section.
- Run `ddev stop` only after confirming tomorrow's TODO exists.

### Python Environment Rule (Inside DDEV)

- Treat Python tooling as running inside the DDEV runtime for this repo.
- Prefer `ddev exec python3 ...` and `ddev exec pip ...` over host Python/venv commands.
- Do not rely on host venv activation (for example `source .venv/bin/activate`) unless the user explicitly asks for host-only execution.
- When running Python scripts in this project, default to:
  - `ddev exec python3 scripts/<script>.py ...`
  - `ddev exec python3 -m pip install -r requirements-python.txt`

## Copilot execution notes

# DDEV is the local runtime — host shell is not supported

The full DDEV local runtime rules and command table are contained in this SKILL.md (originally sourced from the project's .github/skills/ for dual compatibility). Follow the mandatory DDEV wrappers, pre-flight, allowed host exceptions, and Python rules exactly as documented in the body of this file.

## Grok notes
- This is non-negotiable per `.github/copilot-instructions.md` §2.
- Use `.github/prompts/load-project-cache-first.prompt.md` to absorb CONVENTIONS/TESTING before running project cmds.
- Only host cmds allowed: ddev control, git/gh, doctl/aws, docker (for prod images), read-only rg/grep/find.
- For Python: always `ddev exec python3 scripts/...` or pip via ddev.
- Before any project cmd: `ddev status`; if down, baseline git status, start, recheck.
- Tests: always via ddev + confirm test DB.

State reason and ask if you must ever deviate. Default: prefix with ddev.
