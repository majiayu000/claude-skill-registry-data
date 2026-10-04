---
name: init-repo
description: >-
  Get this repo's Shipyard config from zero (or partially done) to genuinely usable: write
  `.shipyard/config.json` (shared, tracked) and `.shipyard/config.local.json` (personal,
  gitignored), retire any leftover `SY_*` variables from a legacy `env` block, then prove it live
  with the same preflight check every other command runs. Asks only for what is actually missing,
  so a teammate joining an already-configured repo is a short exchange, not a full interview.
argument-hint: "[optional tracker override]"
disable-model-invocation: true
---

Turn an unconfigured or partially-configured repo into one where `/sy:plan`, `/sy:spec`, `/sy:ship`, and `/sy:spike` all pass preflight (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md`) on the first real try. Never writes code; never touches the tracker's actual issues.

$ARGUMENTS

## 1. Read what already exists

Read the resolved configuration and the layer each value came from, with the `show_config` tool (tool names resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`):

```
show_config {}
```

Anything already resolved from the `repo-committed` layer is **shared, committed config** — never re-ask for it, never overwrite it without saying so first. This is what makes the common case fast: a teammate joining a repo someone already configured has almost everything already answered, and this run is short.

### 1b. Retire a legacy `env` block, if one is still there

Shipyard used to be configured through the `env` block of `.claude/settings.json`. If either settings file still carries `SY_*` keys, there is no converter to run — the move is by hand, and the validator writes the worklist:

```
validate_config {}
```

It names, per variable, the retired name that is still set and the config key it now resolves to, plus any `SY_*` name no setting answers to at all (a typo, or something stale). Move each value into the file step 5 would put it in, then unset the variable and delete the key from the `env` block: a retired variable left set is a hard validation failure rather than an override, because two live resolution paths for one key is exactly what this replaced. Two exceptions to where a value lands: a credential stays in the environment and never enters a config file at all, and a genuinely per-person value (an account email, a machine-specific worktree root) goes down into `.shipyard/config.local.json` rather than the shared file. `docs/configuration.md` carries the full retired-name-to-key table.

## 2. Resolve the tracker

If `tracker` already resolves from a config layer or `$ARGUMENTS` names one, use it. Otherwise ask via `AskUserQuestion` which supported tracker this repo uses (the options and their meaning are `${CLAUDE_PLUGIN_ROOT}/skills/tracker/CONTRACT.md`'s to name, not this file's) — a genuine fork with no reasonable default (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`).

Load `${CLAUDE_PLUGIN_ROOT}/skills/tracker/<tracker>/ADAPTER.md`'s configuration/preflight section to learn, for the chosen tracker only: its required config keys, which values are secrets that stay in the environment, and the one-time CLI login it needs outside Shipyard's config. That adapter's `config-map.json` declares the same split machine-readably. This file stays tracker-agnostic in its own prose — the concrete var names and meanings live only in the adapter, exactly per `CONTRIBUTING.md`'s seam rule.

## 3. Check the one-time CLI login first

Before asking for anything else, check the adapter's one-time login **live**, not by presence: the loaded `ADAPTER.md` names the check (e.g. an auth-status command) and the login command that fixes it. This step cannot be automated — it is an interactive, per-person login this skill has no business running on the user's behalf — so a missing login stops the run right here with a single `## Action needed` block naming the exact command to run, then re-run `/sy:init-repo`. Continuing the interview before this is fixed only produces config that still cannot pass preflight.

## 4. Interview only for what is missing

For each of the adapter's required config keys, and the five canonical column names (`columns.backlog`, `columns.ready`, `columns.in_progress`, `columns.in_review`, `columns.done` — shared across trackers, matching the real names on this tracker's board or workflow) not already resolved in step 1, ask directly in conversation — this is data entry, not a multiple-choice fork, so plain prompts, not `AskUserQuestion`. State plainly which values are shared (safe to commit) and which are secret (never committed) before asking, so the user is not surprised later by where an answer lands.

The user may not recall a board's exact column spelling. Once the identifiers that only they know (project/board key or number) are answered, discover the board's actual lifecycle values via a subagent scoped to exactly that tracker and project/board — never run open-ended discovery queries in this session — and present the discovered names for the user to confirm rather than asking them to type a spelling from memory.

Separately, and only if `worktree.root` still resolves from `derived-default`, ask once whether they want ship worktrees in the default sibling `<repo>-worktrees/` directory beside the repo or a different directory (e.g. a shared `~/worktrees`). This is optional, not part of the required-keys interview above — skip silently on "default is fine" or no answer. If they name a directory, resolve it to an absolute path (expand `~`, resolve anything relative against the repo root) before writing it: a literal `~` in a config value is not expanded by any later shell that consumes it. If the directory is one they intend to share across multiple repos, mention once, briefly, that worktrees for identically named branches in different repos would then collide under that one root — the default per-repo sibling directory avoids this.

## 5. Write, split by secrecy and portability

- Shared, portable, non-secret values (`tracker`, the five column names, and every adapter key the loaded `ADAPTER.md` does not call out as a credential) merge into `.shipyard/config.json`. Create the file if absent, include the `$schema` key so editors validate it, and preserve every existing key rather than overwriting.
- Machine-specific and per-person non-secret values (a resolved `worktree.root`, an account email) merge into `.shipyard/config.local.json` — **never** the shared file. Neither is a secret, but both differ per person; committing one breaks preflight for every teammate whose home directory or account differs. Ensure `.shipyard/config.local.json` is gitignored.
- **Secrets never go in either file.** A credential belongs in the environment, where `sy_tools/guards/secret_guard.py` covers it and no `cat` of a committed file can burn it into transcript history. The resolver refuses a config layer containing a credential-shaped key. Tell the user plainly which value this is and where to export it. Matches `docs/configuration.md`.
- If the repo's `.claude/settings.json` has no `enabledPlugins` entry for this plugin yet, this is the very first setup for the repo, not a teammate joining one already configured: mention, as a single optional aside, the project-scope install path in `docs/installation.md` so the rest of the team gets it for free on clone — never run a plugin-install command silently on the user's behalf, the same boundary `docs/installation.md` already states.

## 6. Prove it live

Run every presence check, then the adapter's real preflight read with the cache forced past — the config just changed, so a cache hit would be stale by construction — which also records success, so the very next command gets the cached fast path:

```
validate_config {}          # every presence check, naming key and layer
preflight {"force": true}   # the adapter's own live read, run now rather than answered from the cache
```

`preflight` runs the adapter's live check and records it in one call — there is no separate record step to remember here, and `force` is what makes it read rather than trust the entry the pre-edit config left behind (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md`).

A failure here is the same `## Action needed` shape as step 3 — name the exact thing that is still wrong (per the adapter's own error text) and stop; do not report success on unverified config.

## 7. Report

Close with a status update: which file(s) were written, the tracker confirmed live, and — as a single optional aside, never a gate — a nudge toward `/sy:plan` or `/sy:spec` next.
