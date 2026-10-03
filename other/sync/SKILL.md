---
name: sync
description: Pull latest changes from remote and report status
type: shipping
version: v0.6
---

# Sync

Invoke as `$sync`.

Pull the latest changes from the remote repository and report status.

## Process

1. Check current state:
   - Run `git status` to check for uncommitted changes.
   - If there are uncommitted changes, stash them first, pull, then pop the stash. Warn the user about the stash.
2. Pull from remote:
   - Run `git pull --rebase origin <current-branch>`.
   - If rebase conflicts occur, abort the rebase, try `git pull --no-rebase` instead, and report any merge conflicts for the user to resolve.
3. Check for outstanding work:
   - Check if `tasks/roadmap.md` exists for the full plan, and `tasks/todo.md` for the current phase.
   - If `tasks/todo.md` exists, read it and look for unchecked items (`- [ ]`).
   - If there are incomplete items, summarise: which phase is current, what the next step is, and how many steps/phases remain.
   - If `tasks/manual-todo.md` exists, count unchecked manual tasks and include in the summary.
   - If `tasks/record-todo.md` or `tasks/recurring-todo.md` exists, count unchecked advisory items and include those counts separately. Do not treat them as active plan steps.
   - If all items are checked, report that the plan is complete.
   - If neither file exists, note that there is no active plan.
4. Check provisioned agent config:
   - If `CLAUDE.md` or `AGENTS.md` contains `<!-- provision-agentic-config vX.Y -->`, extract the version.
   - Read the canonical `provision-agentic-config` skill from the first existing path in this order (base skills install project-local, so the project roots come first):
     1. `.codex/skills/provision-agentic-config/SKILL.md`
     2. `.claude/skills/provision-agentic-config/SKILL.md`
      3. `packs/base/codex/provision-agentic-config/SKILL.md` in the current repo, when present
      4. `packs/base/claude/provision-agentic-config/SKILL.md` in the current repo, when present
   - Extract the `version:` field from the canonical skill's YAML frontmatter.
   - Extract the canonical provisioned blocks from the same skill:
     - `CLAUDE.md`: the fenced block under `Required Claude Block` or the section that says "The Claude block to insert into `./CLAUDE.md`".
     - `AGENTS.md`: the fenced block under `Required AGENTS Block` or the section that says "The AGENTS block to insert into `./AGENTS.md`".
   - Compare each existing project file against its corresponding canonical block after normalizing line endings and trimming only leading/trailing whitespace around the block. Do not ignore changed bullets, headings, command examples, or policy text.
   - If the installed skill version is newer than the provisioned version in either file, warn: `⚠ CLAUDE.md provisioned with vX.Y but provision-agentic-config is at vX.Y — consider re-running $provision-agentic-config`
   - If the version comment is missing from `CLAUDE.md` or `AGENTS.md`, note: `ℹ No provision version found in CLAUDE.md/AGENTS.md — run $provision-agentic-config to add version tracking`
   - If a project file has the current version comment but the provisioned block content differs from the canonical block, warn: `⚠ CLAUDE.md provisioned block differs from the canonical provision-agentic-config vX.Y block — re-run $provision-agentic-config`
   - If a canonical block cannot be extracted, fall back to the version-only check and note: `ℹ Could not extract canonical provision-agentic-config block; checked version comment only`
   - If none of the canonical skill files exists, skip this check silently.
   - Always report the local canonical source path used and its `version:` field when this check runs.
5. Check skill-install drift (track-latest):
   - Project-local pack/skill installs under `.claude/skills` and `.codex/skills` are managed copies stamped with `.agentic-skills-managed`, which now records `source_version` and `source_sha`. When canonical sources in the `agentic-skills` checkout move ahead, the installed copies fall behind.
   - Resolve the `agentic-skills` checkout from any install marker's `source=` path (the parent above `.../packs/..` or `.../base/..` is the repo root). If no managed install exists or the checkout cannot be resolved, skip this check silently.
   - Run `scripts/pack.sh doctor` from the project root using that checkout (read-only; it never mutates installs).
   - Fold any `stale` skills into the Report status block and surface the exact refresh command the doctor itself reported (the context-aware dual hint). Prefer `npx skillpacks refresh` when the resolved managing source is the published npx `skillpacks` package (the marker `source=` path has no `.git`); use `scripts/pack.sh refresh` run from the resolved source-checkout root otherwise. Report `unknown` skills as "run the doctor-reported refresh command to enable drift tracking" with the same npx-vs-checkout choice, and leave `pinned` skills noted as frozen. Do not print a bare `scripts/pack.sh refresh`, which will not resolve from a non-checkout project directory.
   - Must not mutate. Plain `$sync` only warns; it never runs `refresh`, re-copies, or otherwise changes installs. Direct the user to the doctor-reported refresh command — `npx skillpacks refresh` for installs managed by the published npx package, or `scripts/pack.sh refresh` run from the source checkout (or enable auto-refresh) — for the actual update.
6. Resolve GitHub freshness preference:
   - Use the user-local machine-wide preference file at `~/.agentic-skills/preferences.json`.
   - Read `sync.github_freshness_check`, whose only allowed values are `"ask"`, `"always"`, and `"never"`.
   - If the file or key is missing, ask the user once which default to remember:
     - Always check GitHub during sync
     - Never check GitHub during sync
     - Ask each time
   - Create `~/.agentic-skills/preferences.json` if needed and save the selected value as:
     ```json
     {
       "sync": {
         "github_freshness_check": "ask"
       }
     }
     ```
   - If the value is `"always"`, check GitHub remote freshness automatically.
   - If the value is `"never"`, skip GitHub freshness checks and report that local canonical `provision-agentic-config` was used without a GitHub check.
   - If the value is `"ask"`, ask before checking GitHub for this sync.
   - Treat malformed JSON or an unsupported value as missing preference and ask again before writing one of the allowed values.
7. Optional GitHub freshness check:
   - Only run this check when the resolved preference or explicit user approval says to check GitHub.
   - Compare the local `agentic-skills` checkout against `origin/HEAD` using non-mutating commands such as `git remote get-url origin`, `git rev-parse HEAD`, `git rev-parse origin/HEAD`, and, when remote freshness is explicitly enabled, `git fetch --dry-run` or an equivalent non-mutating freshness probe.
   - Report the local checkout commit, remote URL, local `origin/HEAD` commit if available, and whether the local checkout appears behind the remote.
   - Do not pull, fast-forward, rebase, install, or mutate the checkout from plain `$sync`.
   - If a GitHub check shows the local checkout is stale, recommend an explicit update — update the `agentic-skills` checkout (e.g. `git pull --ff-only`) or bump the `skillpacks` package, then run `npx skillpacks refresh` — without performing it from plain `$sync`.
8. Report status:
   - Branch name
   - Commits pulled (if any) — show short log of new commits
   - Whether stashed changes were re-applied
   - Any conflicts that need manual resolution
   - Current `git status`
   - **Agent config drift** — provisioning version, local canonical source path/version, and canonical block match/drift status for `CLAUDE.md` and `AGENTS.md`, if checked
   - **Skill-install drift** — any `stale` project skill installs (with `vOld → vNew`), `unknown` installs needing a refresh to enable tracking, and the doctor-reported refresh command (`npx skillpacks refresh`, or `scripts/pack.sh refresh` from a source checkout); report "all installs current" when none are stale, or skip the line when no managed installs exist
   - **GitHub freshness** — preference value, whether GitHub was checked, and the local checkout/remote status; when skipped, say local canonical was used
   - **Outstanding work** — summary from step 3 (next step, current phase, remaining work, pending manual tasks) or "No active plan"
   - **Advisory tasks** — pending record/recurring counts, if those files exist
9. Post-sync actions:
   a) Check if `sync.md` exists at the project root.
   b) **If `sync.md` exists** — parse and execute it:
      - Read `sync.md` and identify sections by H2 headings.
      - **Dependencies** (aliases: "Deps", "Dependency Management"): Execute shell commands in fenced code blocks. Report output briefly.
      - **Conflict Resolution** (aliases: "Conflicts"): If the pull introduced merge conflicts (from step 2), apply the guidance in this section. If no conflicts, skip silently.
      - **Custom** (aliases: "Project-Specific", "Scripts", "Setup"): Execute shell commands in fenced code blocks in order. Report output briefly.
      - **Notifications** (aliases: "Awareness", "Alerts", "Watch"): For each bullet, check if the mentioned file/directory was modified in pulled commits (`git diff --name-only` against pre-pull HEAD). If any match, print a prominent alert.
      - Unrecognised headings: skip with a note.
      - Report a summary of all post-sync actions taken.
   c) **If `sync.md` does not exist** — suggest creating one:
      - Analyse the project to detect: package manager (look for lockfiles), common scripts (package.json, Makefile, Justfile), config templates (.env.example, docker-compose.yml).
      - Present a suggested `sync.md` following the format below.
      - Ask: "Would you like me to create this `sync.md`?"
      - **Only create the file if the user approves.**

## sync.md format

The `sync.md` file lives at the project root. H2 sections are categories. Shell commands go in fenced code blocks; prose guidance goes in bullet points.

```markdown
# Post-Sync Actions

## Dependencies

```sh
npm install
```

## Conflict Resolution

- Always accept theirs for `package-lock.json`

## Custom

```sh
npm run codegen
```

## Notifications

- `.env.example` — check for new environment variables
- `CLAUDE.md` — review if project conventions were updated
```

## Constraints

- Do not force-push or rewrite history.
- Do not auto-resolve merge conflicts — report them and let the user decide. However, if `sync.md` has a Conflict Resolution section, follow its guidance for the specific files/patterns it covers.
- If stash pop fails due to conflicts, leave the stash intact and report it.
- Post-sync commands from `sync.md` run in the project root directory.
- If any post-sync command fails, report the error and continue with remaining actions.
- Never auto-create `sync.md` without explicit user approval.
- Do not execute commented-out sections (`<!-- ... -->`).
- Plain `$sync` must not update the `agentic-skills` checkout, pull from GitHub for the local canonical source, or reinstall skills. The explicit update flow is the user's own checkout/package update (e.g. `git pull --ff-only`) followed by `npx skillpacks refresh`, run only after confirmation.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
