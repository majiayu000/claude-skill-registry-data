---
name: onboard
description: Creates or updates a repo's CLAUDE.md by exploring the code and adding the standard workflow sections (git/PR rules, changes that require human review, non-obvious context). Use whenever the user is starting in a new repo, says "set up the CLAUDE.md", "onboard this repo", "there's no CLAUDE.md here", or asks to complete or improve an existing CLAUDE.md — or in Spanish "armá el CLAUDE.md", "iniciá este repo", "falta el CLAUDE.md acá". Also run it before the first time `plan` runs in a repo that has no CLAUDE.md yet.
---

# Build the repo's CLAUDE.md

Produce a `CLAUDE.md` that combines two things: what you discover by reading the repo, and
the fixed sections the `plan` -> `ship` -> `watch` flow needs.

If a `CLAUDE.md` already exists, **do not overwrite it**: fill in what's missing and flag
what's stale.

## 0. Preflight the setup

Before anything, check the tooling the flow needs:

```bash
preflight.sh
```

(The plugin bundles this script and puts its `bin/` on your `PATH`, so call it by name.) Run
it with the sandbox off if you use Claude Code's sandbox (it calls `gh`). It reports any
missing piece (`gh` not installed or not logged in, no `jq`, no git remote) with the fix for
each. If something required is missing, tell the user and stop until it's sorted — the rest of
the flow just fails on `gh` otherwise.

## 1. Explore (what you discover on your own)

Refresh first so you read the real state, not a stale checkout: `git fetch origin` (updates
every remote branch). Then read, don't guess:

- Build manifests: `go.mod`, `pom.xml`, `build.gradle`, `package.json`, `Makefile`,
  `Taskfile.yml`. The real build, test, and lint commands come from here.
- CI: `.github/workflows/`. **The commands CI runs are the source of truth** for how this
  repo builds and tests; they win over whatever the README says.
- `README.md`, `CONTRIBUTING.md`, `docker-compose.yml`, `Dockerfile`, k8s charts.
- `git log --oneline -50` to infer the real commit-message format, not the documented one.
- `git branch -r` to see which branch work actually targets (this is the PR base branch
  that `ship` will read back).
- Package/module layout: the **rule** of organization, not the list of folders.
- Config: where env vars come from and how a new one is added.

Rule: if a command couldn't be confirmed by reading something, don't invent it. Leave it as
`{{fill-in}}` and tell the user which ones are pending.

## 2. Ask (what isn't in the code)

These three can't be deduced from the repo and are what make the file worth having. Ask them
together, in one message, with a tentative proposal for each:

1. **PR base branch** and branch-naming convention.
2. **Which changes require human review** in *this* service. Propose a starting point based
   on what you saw (migrations, contracts with other services, auth, running workflows, data
   deletion) and ask them to add or remove.
3. **Historical quirks**: odd decisions the code doesn't explain. Ask directly: "is there
   anything in this repo that would surprise someone new?"

If the user doesn't want to answer now, leave those sections with a visible `{{fill-in}}`. A
marked gap beats an invented fact.

## 3. Write

File structure, in this order:

1. What this service is (2-3 lines), stack, infra
2. Commands (build, tests, lint, local dependencies)
3. Git and PRs (base branch, naming, commit format, PR body)
4. Code conventions (errors, logging, config, tests, structure, prohibitions)
5. **Changes that require human review**
6. How we work (plan first, don't refactor out of scope, ask when in doubt)
7. Context that isn't in the code

Writing criteria:

- **Target: under 150 lines.** This file enters context every session; if it grows, move a
  section to another file and reference it with `@path/to/file.md`.
- Every line must change the agent's behavior. If it's true but changes nothing, cut it.
- Write explicit prohibitions, not just recommendations. "Don't add dependencies without
  asking" is worth more than "use dependencies judiciously".
- Nothing task-specific. That goes in `docs/plans/`, not here.

## 4. Leave the repo ready

```bash
mkdir -p docs/plans
```

If the repo uses GitHub Copilot review, check that `.github/copilot-instructions.md` exists;
if not, offer to create it.

### Make the repo self-configuring (offer this)

So the flow runs without anyone editing their personal/global settings, offer to seed the
repo's committed `.claude/settings.json` with what the flow needs. **Merge** into it if it
already exists — never clobber existing keys or arrays.

```json
{
  "permissions": {
    "allow": ["Bash(git:*)", "Bash(gh:*)", "<the repo's build/test/lint/run commands>"],
    "deny": ["Bash(git push --force:*)", "Bash(git reset --hard:*)", "Bash(gh pr merge:*)"]
  },
  "sandbox": {
    "excludedCommands": ["git", "gh"]
  }
}
```

- The `allow` list is git/gh **plus this repo's platform-specific commands** — the ones you
  found in step 1 (`Bash(go test:*)`, `Bash(mvn:*)`, `Bash(npm run build:*)`, `Bash(gradle:*)`,
  etc.). Don't guess the stack: use what step 1 read, and **ask the user** which commands they
  run often that should never prompt (build, test, lint, run). A Go repo and a Java or JS repo
  get different lists.
- `excludedCommands` runs git/gh outside the sandbox — that fixes both the `gh` TLS failure
  inside the sandbox and git being unable to write, and because they run outside, the flow
  needs no user-level network knob.

Say two things before writing it: it's **committed**, so teammates inherit the same sandbox
exclusion in this repo (they can override it in their own `.claude/settings.local.json`); and
the sandbox's writable area is the folder Claude Code launched in, so it should be started from
inside the repo.

If the repo runs lint/format/tests through a Claude Code hook, put the real command (from step
1) in that same `.claude/settings.json`. Don't invent a hook that isn't there.

## 5. Close

Report in a few lines: what you discovered on your own, what's left as `{{fill-in}}`, and the
user's answers you folded in. Suggest testing the file with the first `plan` run, which is
where you notice if something's missing.

---

*Convention: `{{like-this}}` marks a value to replace. `<>` is avoided because it breaks skill parsing.*
