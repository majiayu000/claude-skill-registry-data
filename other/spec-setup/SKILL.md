---
name: spec-setup
description: >
  One-time discovery that teaches the spec-driven-dev pipeline how THIS project works, and saves
  the answers to .spec-driven.yml — project layout (single repo, monorepo, or multiple repos),
  issue tracker, base branch, PR target, branch naming, commit style, and the lint/typecheck/test/
  build/dev commands. Use when the user says "set up spec-driven", "configure the pipeline",
  "spec-setup", "change our branch rules", or when any other spec-* skill finds no
  .spec-driven.yml. Detects everything it can from the repos first and only asks about what is
  ambiguous. Writes config only — never changes code, branches, or commits.
license: MIT
---

# spec-setup

Learn this project's rules once, save them, and let every other `spec-*` skill reuse them. Team
rules live in a config file the team can review and change — never in the skills themselves.

## Where the config lives

`.spec-driven.yml`, found by walking up from the current directory (stop at the home folder). The
first one found wins.

| Layout | Put the file in | Share it? |
|---|---|---|
| `single` | the repo root | Commit it — the whole team gets the same rules |
| `monorepo` | the repo root | Commit it |
| `multi-repo` | the shared parent folder of the repos (usually not itself a git repo) | Personal by default; offer to also commit a copy into the repo the team treats as "home" |

A multi-repo config only applies inside the repos it lists. If the current repo sits under that
folder but isn't listed, treat it as having no config (ask whether to add it).

## Step 1 — Detect before asking

Read, don't guess. Collect a draft of every field in `references/config-template.yml`:

1. **Layout.**
   - Inside a git repo with workspace markers (`pnpm-workspace.yaml`, `workspaces` in
     `package.json`, `turbo.json`, `nx.json`, `lerna.json`, `go.work`, `[workspace]` in
     `Cargo.toml`, several `apps/*`/`packages/*`/`services/*` with their own manifests) →
     `monorepo`; list the packages.
   - Not inside a git repo, but sibling folders are git repos → candidate `multi-repo`. Group them
     by remote owner (`git remote get-url origin`) and show the groups — the user picks which repos
     belong together. Never assume every folder in the parent belongs. Always also ask whether
     repos in **other folders** belong (e.g. `~/clients/billing`). Check each path is a git repo,
     and store paths inside the workspace as relative and paths outside it as absolute.
   - The repos of one workspace can live in unrelated places (`/Projects/frontend`,
     `~/Work/backend`, `/srv/database`). Put the config in their shared parent folder, or in
     `~/.spec-driven/<name>/` when that parent would be the home folder or `/`. Then record it in
     `~/.spec-driven/workspaces.json` (`{"<config path>": ["<repo path>", …]}`) so every repo can
     find it.
   - The user can override the detected layout. If they choose `multi-repo` from inside one repo,
     the workspace folder defaults to that repo's parent, with the current repo pre-selected. If
     they choose `monorepo`, ask for the package folders. Never write a `multi-repo` config with
     no repos.
   - Otherwise → `single`.
2. **Existing written rules.** `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, PR templates,
   `.github/workflows`. Anything stated there is a strong default — quote it back to the user.
3. **Tracker.** Ticket keys in recent branch names and commit subjects (`STP-123`, `#45`,
   `ENG-91`), Jira/Linear links in PR templates or docs, whether GitHub Issues are enabled
   (`gh repo view --json hasIssuesEnabled`).
4. **Git, per repo.** Default branch (`git symbolic-ref refs/remotes/origin/HEAD` or
   `gh repo view --json defaultBranchRef`); integration branches (`staging`, `develop`,
   `pre-prod`); which branch recent PRs targeted (`gh pr list --state merged --limit 20 --json
   baseRefName`); the pattern of the last ~20 remote branch names; the commit style from
   `git log -30 --format=%s`.
5. **Commands, per repo/package.** `package.json` scripts plus the lockfile's package manager,
   `Makefile`, `pyproject.toml`/`tox.ini`, `Cargo.toml`, `go.mod`, `composer.json`, CI workflow
   steps (CI is often the most truthful source). Dev URL from the dev script, `.env.example`, or
   framework defaults.

6. **Models per tier.** Write the `models:` block from the template. Ask which models the user
   has for each tool they installed, only if they want to tune it: the Claude defaults (haiku /
   sonnet / opus) work as-is, and `default` is safe for the rest.
7. **After approval.** Ask whether an approved spec should stop after each stage (`stop`), or
   run implement → verify → checkpoint in one go (`run-through`), stopping at any failure and never
   pushing. Store it as `pipeline.after_approval`.

## Step 2 — Confirm in one round

Show the draft as a short table grouped by layout, tracker, git, commands, and specs location.
Mark each value **detected** (with where it came from) or **guess**. Then ask only about guesses
and conflicts — in one message, not a drip of questions. Typical ones:

- "Your repos default to `master`, but recent PRs targeted `staging`. Cut work from `staging`?"
- "Recent branches are bare ticket IDs (`STP-282`). Keep that, or use `fix/STP-282-short-slug`?"
- "These 6 repos share the `acme` GitHub org. Do they form one workspace for the pipeline?"
- "Where should specs live — this folder's `specs/`, or inside one repo so they go through PRs?"

If the user says "just use the defaults", accept the detected values and the template defaults
for the rest.

## Step 3 — Write and report

1. Write `.spec-driven.yml` using `references/config-template.yml` as the shape. Keep its
   comments; drop fields that don't apply (e.g. `repos:` for `single`). Per-repo values only go
   under `repos:` where they differ from the top level.
2. If it's inside a repo, tell the user it's meant to be committed (so teammates get the same
   rules) — don't commit it yourself.
3. If `npx` is available, run `npx -y @benjaminthomas/spec-driven-dev doctor` from the config's folder. It checks
   that every branch, folder, and `npm run` script in the file really exists. Fix anything it
   reports before finishing.
4. Report: the file path, a one-line summary per section, and "re-run spec-setup any time these
   change".

## Updating

Re-running `spec-setup` with an existing config: load it, re-detect, and show only what changed or
looks stale (a branch that no longer exists, a script that was renamed). Never silently overwrite
a value the user set by hand.

## Boundaries

- Writes `.spec-driven.yml` and nothing else. No branches, commits, pushes, installs, or code.
- Never put secrets, tokens, or credentials in the config.
- A value in the config beats a detected value. If the config looks wrong mid-run (a base
  branch that doesn't exist), the other skills stop and point back here rather than overriding it.
