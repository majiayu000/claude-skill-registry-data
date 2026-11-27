---
name: onboard-project
description: "Set up an existing repo for Claude: short CLAUDE.md, safe settings, verify skill. Use when a repo has no CLAUDE.md or .claude folder."
---

# Onboard a project

Goal: any future Claude session in this repo knows what it is, how to check its work, and what
not to touch, without reading the whole codebase. Deliver it as one PR.

## 1. Learn the repo (read, don't guess)

- `README*`, `package.json` / `pyproject.toml` scripts and dependencies, `.node-version`,
  framework configs (`nuxt.config.*`, `vite.config.*`, `wrangler.*`, `firebase.json`,
  `docker-compose.yml`), `.github/workflows/*`, existing `CLAUDE.md` / `AGENTS.md` / `.claude/`.
- `git log --format=%s -20` for commit style.
- For a large or unfamiliar repo, map it with an Explore subagent first.

## 2. Hygiene check (report, fix only what is safe)

- Tracked files that should not be: `git ls-files | grep -E '(^|/)(\.env(\..*)?|node_modules/|dist/|\.output/)'`
  (`.env.example` is fine). Untrack them in the PR with `git rm --cached` and fix `.gitignore`.
  If a tracked env file holds a real secret, tell yskills to rotate it: removing it from git
  does not remove it from history.
- Secrets in frontend env vars (`VITE_*`, `NUXT_PUBLIC_*`) are public; flag any that guard
  something (admin PINs, API keys that are not meant to be public).

## 3. Write the files

**`CLAUDE.md`** (under ~60 lines; see `templates/CLAUDE.md`): what the project is in two lines,
layout, the commands that matter, project rules (security model, language of docs and UI,
deploy target), and how UI changes are verified. Only facts a session could not cheaply
rediscover; no generic advice that the global setup already gives.

**`.claude/settings.json`** (see `templates/settings.json`):
- `permissions.allow` for the repo's own safe scripts (test, build, typecheck, lint, verify).
- `permissions.deny` for reading or editing real env files.
- Per-project plugins this repo uses, added with
  `claude plugin install <id> --scope project` (writes `enabledPlugins`). Common signals below;
  for anything else use the `toolbox` skill:

  | Signal in the repo | Plugin |
  |---|---|
  | `wrangler.toml` / `wrangler.jsonc` | `cloudflare@claude-plugins-official` |
  | `firebase` dependency or `firebase.json` | `firebase@claude-plugins-official` |
  | `stripe` dependency | `stripe@claude-plugins-official` |
  | `@sentry/*` dependency | `sentry@claude-plugins-official` |
  | `posthog-js` / `posthog-node` dependency | `posthog@claude-plugins-official` |
  | `@supabase/*` dependency | `supabase@claude-plugins-official` |
  | `vercel.json` | `vercel@claude-plugins-official` |

**`.claude/skills/verify/SKILL.md`**: the exact commands CI runs, in order, from the repo root,
plus repo-specific review questions. If there is no CI, add a `verify` npm script and a minimal
`.github/workflows/ci.yml` that runs it on pull requests.

Add `.shots/` to `.gitignore`.

**HQ row, no page of its own**: an existing project gets the same view as a new one in the Claude
Setup HQ Artifact (`operator` skill, Dashboard bullet), never a page of its own. From what the repo
shows (README, open PRs and issues, `PROGRESS.md` or `PLAN.md` if present, recent commits) write a short
plan of 3-5 phases with goals, then write the `projects/<id>` row and the `<id>-` prefixed `phases`
and `team` rows into HQ exactly as that bullet says. Add the day-one rows (operator skill, step 3): `work/<session>` per running thread, and for a repo
meant to earn the first euro list in `you[]`. Before the first new slice of a repo meant to earn,
run the demand probe: `product-lens` Mode 1 on one page, `docs/demand-probe.md` (who pays, where
they are, three signals, go or no-go). Note in the repo's `PROGRESS.md` (create it if
missing) that HQ carries the project, so every later session updates the same rows.

## 4. Prove it and ship

Cold-start check: a fresh session must answer "what is this and what is next" from CLAUDE.md, PROGRESS.md and PLAN.md within three reads. If it can't, fix those files before the PR.

Run the verify steps you wrote; they must pass on the current main (if main is already red, say
what fails and keep the skill honest about it). Open a PR titled
`chore(claude): set up Claude for <project>` listing what was added and every hygiene finding.
