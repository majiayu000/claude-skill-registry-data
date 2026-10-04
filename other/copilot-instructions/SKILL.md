---
name: copilot-instructions
description: 'Core operational instructions for ndestates-io (DDEV, security, data safety, TODO lifecycle, branch rules, auth regression, etc.). This is the native Grok skill (primary for Grok sessions). The `.github/copilot-instructions.md` version is maintained separately for GitHub Copilot users. Always reference the Grok version in .grok/ contexts.'
user-invocable: true
disable-model-invocation: false
---

# Copilot Instructions — NDestates IO (ndestates-io) (Grok Native)

**ND Estates IO**: Real estate software side of ND Estates (www.ndestates.com). Marketing site + customer portal for software products (ND E-Sign / e-signature from projects/e-ndsign, Orchestrator, future tools). Features introduction/landing, product pages, downloads (license gated), licensing info, free trials and purchases via PayPal. Stack: Laravel + MySQL + Filament 5 + Livewire.

These instructions are security-first and practical. Follow them in priority order.

**This is the primary version for Grok.**  
The file `.github/copilot-instructions.md` is the equivalent maintained for GitHub Copilot (and GitHub-native tools). Both are kept in sync for dual compatibility. Grok sessions should prefer this `.grok/skills/copilot-instructions/SKILL.md`.

## 1) Work Planning and Branch Safety

- At session startup, read the daily TODO before any coding, edits, or runtime commands.
- **Session-start branch rule:** On `/chain session-start`, `/daily-standup-with-cache`, `/daily-standup`, or standup aliases — run `git fetch origin --prune`, then **always** resolve and report the **latest remote branch worked on** (`remote-last`: newest `origin/*` by committer date). Offer a switch when current ≠ `remote-last` (never auto-checkout). See `daily-standup-with-cache` Step 2.
- If a TODO exists for today, follow it.
- If the latest TODO is from an earlier date, carry it forward to today's TODO file and continue from there.
- Work on the current feature branch, not master.
- Before edits or task runs, confirm you are on the latest remote state for the intended branch.

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

## 3) Mandatory Security Checklist Trigger

Security checklist execution is mandatory whenever either condition is true:

- Dependencies changed.
- Any form input handling, validation, or rendering code was added or modified.

Execution source of truth:
- For commit/push/release flows, follow `.grok/skills/git-workflow-guardrails/SKILL.md` for exact commands and ordering.
- Outside git delivery flows, run `./scripts/ci_security_checklist.sh` and review `reports/security/` artifacts.

Checklist artifact expectations remain the same:
- Review composer audit output.
- Review advisory diffs against `reports/security/composer-audit-baseline.json`.
- Check for risky raw HTML render paths.
- Review artifact threat scan (reports/security/artifact-threat-*.txt) for injection / supply-chain patterns in code, scripts, models and data processors.
- Review MCP server threat scan (reports/security/mcp-threat-*.txt) for unsafe agent instructions, bypass language or exfiltration risks in skills, SKILL.md, agent defs and prompt files.
- Threat detection for artifacts and MCP servers is mandatory on every checklist run (changes to dependencies, form/render code, MCP skills, or artifact-handling code).

## 4) Shell Artifact Hygiene

After shell commands that use patterns or special characters (especially `rg`, `grep`, or commands containing `(`, `)`, `|`, `->`, `{`), immediately run:

- `git status --short`

If accidental files were created by shell parsing (for example names like `summarize(`, `html(`, `allowHtml(`), unstage/delete them before continuing.

## 5) Data Safety (Critical)

- Never run destructive operations against live `db` (`migrate:fresh`, `db:wipe`, `truncate`, `drop table`, or truncating seeders).
- Use test-only databases for tests.
- Before tests, confirm `DB_DATABASE` is `test` or `:memory:`.
- If DB target is anything else (especially `db`), stop and report risk.
- Prefer non-destructive checks and transaction-based approaches.
- Ask for explicit confirmation before any operation that could alter live data.

## 6) Mandatory Pre-Test Checklist

1. Confirm DB target:
  - `ddev exec php -r "echo getenv('DB_DATABASE');"`
2. If result is not `test` or `:memory:`, abort.
3. Before risky operations, snapshot a key live count:
  - `ddev mysql -e "SELECT COUNT(*) FROM db.properties;"`
4. State which database will be used before running tests.

## 7) Recovery-First Policy

If live counts drop unexpectedly:

1. Stop all test/seed/migration actions.
2. Restore into isolated `restore_db` first.
3. Validate counts and table integrity.
4. Restore validated data into live `db` only after verification.
5. Re-check counts and key records.

## 8) Auth and Security Regression Guardrails

- Treat login and two-factor flows as critical.
- Do not change auth behavior unless explicitly requested.
- After dependency or asset updates, run targeted login and 2FA checks and report results.
- Flag high/critical vulnerability findings immediately.

## 9) Test Conversion Scope (Pest)

- You may convert legacy tests to Pest.
- Keep business logic and infrastructure behavior unchanged unless explicitly requested.
- If a requested change requires infrastructure/business-logic changes, call it out clearly before proceeding.

## 10) Communication and Command Examples

- Provide commands in plain copyable form.
- Do not provide malformed pseudo-links in command examples.

## Grok-specific Notes

- This skill is the Grok-native home for these rules (see also the .github/ version for Copilot users).
- Many rules are also extracted into dedicated `.grok/skills/` (e.g. `ddev-local-runtime`, `git-workflow-guardrails`, `test-safety-agent`, `security-audit-agent`).
- Always cross-reference with `docs/codebase/CONVENTIONS.md`, `TESTING.md`, and load-project-cache-first for full context.
- For MCP/agent/prompt changes: ensure MCP threat scans are included in security checklist runs.

## 11) AI Engineering Maturity (8 Stages)

This project adopts the team/organization-centric "8 stages of AI engineering maturity" framework (https://upsun.com/blog/8-stages-ai-engineering-maturity/ by Fabien Potencier, building on Steve Yegge's individual levels). AI is an *amplifier* of existing practices — it accelerates good ones (our DDEV, tests, security, cache discipline, shared context) and bad ones alike.

**Key principles (apply in all planning, standups, agent extensions, and code changes involving AI tooling):**
- Assess the center of gravity: vacuum → drift (individual habits) → islands (team gaps) → standardization (shared AGENTS.md-like context, skills/prompts in-repo, security/gov first) → workflow redesign (spec-first, risk-based review, evals beside tests) → operating system (agent "slots", TDD mandatory, shared infra as assets) → bright factory (supervisor role) → autonomous factory (shared runtime, scheduled jobs, eval as the product; standards live in the system not heads).
- Do **not skip stages**. The friction/pain of the current stage (e.g. drift causing inconsistency, or reviewing agent output line-by-line) provides the evidence and motivation for the next. Governance, testing, and shared context are prerequisites.
- Shared context engineering first: Prefer and maintain `.grok/skills/`, `.grok/prompts/`, `.grok/agents/`, memories/INDEX, docs/codebase/ cache, TODO carry, and structured prompts over personal/ad-hoc usage. This is explicit work (Stage 4+).
- Security & governance *before* scale: Any new skill, agent, prompt, MCP server, or heavier agentic usage triggers full security checklist (incl. mcp-threat scans). See §3.
- Spec/context-first + evals as gates: Use load/daily-standup cache + branch-context + test-safety etc. as automated checks. Treat AI-generated artifacts with at least the same rigor as human work.
- No org is uniform: Track distribution (e.g. in daily-standup synthesis). The number is a center of gravity.
- When extending .grok or using subagents: Invoke `/ai-engineering-maturity` (or reference its principles) to assess current stage and recommend the concrete next advancement step. Cite the source URL.
- Our existing setup (cache-first, guardrails, DDEV enforcement, MCP/agent threat detection, shared skills as infra) already positions us strongly in Stages 4–6. The goal is to encode more standards into the system (evals, recurring agent tasks) while amplifying our foundations.

Use the dedicated `/ai-engineering-maturity` skill for detailed stage descriptions, project mappings, assessment questions, and session guidance. Cross-reference with daily-standup-with-cache (include maturity indicators in synthesis) and git-workflow-guardrails.