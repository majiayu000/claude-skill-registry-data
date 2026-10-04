---
name: github-expert
description: GitHub operations expert for the Calculadora-BMC repo — branches, commits, PRs, CI workflows, review flow, labels/board, and merge policy. Use when creating or reviewing PRs, diagnosing red CI, managing branches/releases, triaging issues, or when the user invokes /github-expert or asks "how do we do X on GitHub" in this repo.
---

# GitHub Expert — Calculadora BMC

Operational guide for all GitHub work on `matiasportugau-ui/Calculadora-BMC` (default branch: `main`).

## Tooling

- **Claude Code on the web / remote sessions:** use the GitHub MCP tools (`mcp__github__*`) for PRs, comments, CI status, and logs. `gh` CLI is NOT available there.
- **Local sessions:** `gh` CLI works if installed; MCP tools are the fallback.
- Never call the GitHub REST API directly with tokens from `.env`.

## Branch & commit conventions

- Branch names: `feat/...`, `fix/...`, `chore/...`, `docs/...` (or the session-designated `claude/*` branch). Never commit directly to `main`.
- Commit messages: concise, **English**, `type:` prefix — `feat`, `fix`, `refactor`, `docs`, `chore`. Scope in parentheses is common: `feat(ci): ...`, `fix(deps): ...`.
- If a branch's PR was already **merged**, never stack new commits on it — restart the branch from `origin/main` and open a new PR.

## PR workflow (Definition of Done — `docs/team/AGILE.md` §3)

1. `npm run gate:local` green (lint + test + test:api). For large UI/build changes: `npm run gate:local:full` (adds build).
2. Fill the PR template (`.github/PULL_REQUEST_TEMPLATE.md`): **Qué cambia**, `Closes #`, **Tipo** checkbox, DoD checklist, **Notas para el reviewer**.
3. **PR > 500 LOC adds → DRAFT obligatorio** and split into atomic commits before marking ready (branch protection can't enforce this; we do).
4. If the change alters behavior, append a line under "Cambios recientes" in `docs/team/PROJECT-STATE.md` in the same PR.
5. Bot/agent-created PRs always start as **draft**.

## CI — what runs and when

`ci.yml` ("CI — Panelin Calculadora BMC") on push + PR:

| Job | What it does |
|-----|--------------|
| `validate` | `npm test` (offline suite) + build |
| `lint` | ESLint on `src/` |
| `env-drift` | `.env.example` vs config drift check |
| `smoke` | Prod smoke (push to `main` only; MATRIZ CSV is the critical check) |
| `channels_pipeline` / `voice_health` / `knowledge_antenna` | Channel + voice + KB health checks |

Other notable workflows:

- `deploy-calc-api.yml` / `deploy-vercel.yml` — Cloud Run (`panelin-calc`, us-central1) and Vercel deploys.
- `catalog-diff.yml` — Catalog ↔ MATRIZ diff; upserts a PR comment, fails on regression/S1.
- `codeql.yml`, `dependency-review.yml` — security gates.
- `gemini-*.yml` — Gemini review/triage bots (dispatch, review, scheduled triage).
- `smoke-prod-scheduled.yml` — scheduled prod smoke; failures open/refresh an auto-managed tracking issue.
- `wa-canonical-cutover.yml` — dispatchable WA migrate/flip/soak.
- `labels-sync.yml` — label catalogue is code-managed; don't hand-edit labels in the UI.

### Red CI playbook

1. Identify the failing job (`pull_request_read` / `actions_get`), then pull job logs (`get_job_logs`, `failed_only: true`).
2. Reproduce locally: `npm run gate:local` (or the specific script the job runs).
3. Native `midi` build failures on Linux → missing ALSA headers (`libasound2-dev`); CI installs them, local containers may not.
4. Disk precheck false-fails on cloud FS → `BMC_DISK_PRECHECK_SKIP=1`.
5. Fix → commit → push; CI re-runs automatically. Use `actions_run_trigger` only for dispatchable workflows.
6. Several re-kicks with no progress → stop and report the diagnosis instead of looping.

## Issues & board

- Backlog lives in GitHub Issues / Project **BMC Dev**; offline mirror `docs/team/BACKLOG.md`; board rules `docs/team/AGILE.md`.
- Priority labels: `priority:P0` (drop everything) → `priority:P1` → lower. Surface P0/P1 first in any triage.
- Search for duplicates before opening an issue; set `state_reason` when closing.

## Guardrails

- `npm audit fix --force` is **forbidden** without explicit approval (it has broken Vite here).
- Secrets only in `.env` / Secret Manager — never in code, workflow files, or PR bodies.
- Never force-push `main`; force-with-lease on feature branches only when rebasing your own unshared work.
- Be frugal with bot comments on PRs — comment only when it genuinely adds signal.

## Language

Respond in **Spanish** when the user writes in Spanish. Commands, file paths, and technical terms stay in English.
