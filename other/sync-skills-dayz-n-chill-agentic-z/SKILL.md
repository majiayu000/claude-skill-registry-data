---
name: sync-skills
description: "Links every skill in this repo's skills/ and .claude/skills/ into each agent CLI's home skills folder (Codex and Gemini by default, Claude Code on request, or any agent in agents.json) so all of them see the same slash commands, and removes those links with --unlink. Use when you have just cloned the repo, added, removed or renamed a skill, or moved the repo."
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\<other>\`. For first-time bootstrap from a fresh clone (before any harness is loaded), run the literal command `python .claude\skills\sync-skills\sync.py` from the repo root.

# /sync-skills

The bootstrap. **Links, not copies.** The single source of truth is `<repo>/skills/` plus the repo-only skills in `<repo>/.claude/skills/`; this skill creates symlinks (or junctions on Windows) in each agent CLI's home so every agent discovers the same slash commands. Nothing is copied, no skill content lives outside the repo, and editing a skill in the repo is instantly live in every agent.

The reason the agent home dirs are involved at all: Claude Code loads the repo's `skills/` (as the plugin) and `.claude/skills/` directly, but the others do not. Codex reads `.agents/skills/` in the repo and `~/.agents/skills/`. Gemini reads `.gemini/skills/` or `.agents/skills/` in the workspace and `~/.gemini/skills/` or `~/.agents/skills/` in the home folder. The links bridge that gap without duplicating files.

## Claude Code is left out by default

`~/.claude/skills/` is Claude Code's personal skills folder, which it loads in every project, not just this repo. Inside this repo Claude Code already loads `skills/` and `.claude/skills/` directly, so a link there adds nothing here and has two side effects:

- Every `/dayz-*` skill becomes available in every Claude Code project on this machine.
- If the Agentic-Z plugin is also installed, each skill shows up twice: once from the plugin (`agentic-z:dayz-build-pbo`) and once from the link (`dayz-build-pbo`).

So the `claude` entry in `agents.json` has `"default": false`, and a plain run links only Codex and Gemini. To make the skills global in Claude Code on purpose (for example without the plugin, so other projects can reach `~/.claude/skills/_shared/`), name it: `python "<skill-dir>\sync.py" --agents claude`.

Links made by an earlier version, which linked Claude Code by default, stay until you remove them: `python "<skill-dir>\sync.py" --unlink --agents claude`. That removes only links pointing into this checkout's `skills/` or `.claude/skills/`; links to other clones, real folders and the repo's own skill folders are left alone. Add `--dry-run` first to see the list.

## When to run it

- **Right after cloning the repo**, as step two, before doing real work. None of the slash commands work in Codex or Gemini until this runs (Claude Code loads the repo's `skills/` and `.claude/skills/` directly; Codex and Gemini do not read those folders).
- **After adding a new skill** to `skills/` or `.claude/skills/`.
- **After deleting a skill** — orphan links pointing at it get pruned, even when git left the folder behind holding only an ignored `__pycache__`.
- **After moving the repo** to a different path. Links still pointing at the old location are reported as `[FOREIGN]`; rerun with `--force` to retarget them.
- **To undo it** (before deleting the clone, or to stop the duplicate Claude Code skills): run with `--unlink`.

## How to run

```cmd
python "<skill-dir>\sync.py"
```

Optional flags:

```cmd
python "<skill-dir>\sync.py" --agents claude codex     # exactly these agents (naming claude opts it in)
python "<skill-dir>\sync.py" --skip gemini             # the default set minus Gemini
python "<skill-dir>\sync.py" --dry-run                 # preview, no writes
python "<skill-dir>\sync.py" --force                   # take over links that point at another clone
python "<skill-dir>\sync.py" --unlink --agents claude  # remove this checkout's links instead of making them
```

`--unlink` uses the same agent selection as a normal run (Codex and Gemini unless `--agents` says otherwise) and honours `--dry-run`.

## Where the per-agent skills folders live

Resolved from `agents.json`. Defaults:

| Agent  | Env var(s) checked first                | Default path |
|--------|------------------------------------------|--------------|
| Claude (only with `--agents claude`) | `CLAUDE_CONFIG_DIR` | `~/.claude/skills` |
| Codex  | none (`CODEX_HOME` does not move skills) | `~/.agents/skills` |
| Gemini | `GEMINI_CLI_HOME` (skills then live in `$GEMINI_CLI_HOME/.gemini/skills`) | `~/.gemini/skills` |

When `GEMINI_CLI_HOME` is unset, Gemini also reads `~/.agents/skills/`, so after a full run it finds each skill there and in `~/.gemini/skills/`; the `.agents` copy wins. Both are links to the same folder, so they never differ. With `GEMINI_CLI_HOME` set, Gemini reads `$GEMINI_CLI_HOME/.agents/skills/` instead, so this overlap does not apply.

To support a new agent later, append an entry to `.claude/skills/sync-skills/agents.json` — no code change needed. Each entry needs a unique `"name"` and a non-empty `"default_home"`; `"env_home_vars"` (a list, default `[]`), `"env_home_subdir"` (default none) and `"skills_subdir"` (default `"skills"`) are optional. Add `"default": false` to an entry to sync it only when it is named in `--agents`.

## What it does, per skill, per agent

For every folder under `skills/<name>/` or `.claude/skills/<name>/` containing `SKILL.md`, plus `skills/_shared/`. `_shared/` is not a skill, but the skills refer to the shared reference docs and helpers in it, so it is linked alongside them. Other folders starting with `_` are skipped.

| Existing state in `<home>/skills/<name>` | Action |
|---|---|
| Link already points at the repo skill | `[OK]` no-op |
| Link points at a different path inside this checkout's `skills/` or `.claude/skills/` (stale) | `[REFRESH]` retarget to the right skill. If the new link cannot be made, the old one is put back and the line reads `[FAILED] <name>: <error>; previous link to <path> restored` |
| Link points anywhere else (another clone, a git worktree under `.claude/worktrees/`, or the repo's old location) | `[FOREIGN]` left alone and counted as skipped; with `--force` it is retargeted (`[REFRESH]`) |
| Path doesn't exist | `[LINK]` create new link |
| Real folder, not a link | `[SKIP]` warn — don't clobber user-installed skills |
| Orphan link in target dir, points into this checkout's `skills/` or `.claude/skills/` at a folder that is gone or has no `SKILL.md` (for example a deleted skill whose `__pycache__` survived), other than `_shared` | `[PRUNE]` remove the link; the repo folder itself is not touched |

Ownership is decided against this checkout's `skills/` and `.claude/skills/` folders, not the repo root. A worktree under `<repo>/.claude/worktrees/` is another checkout with its own sessions, so its links count as foreign.

Link targets are compared after normalising separators and, on Windows, case (`os.path.normcase`), so `C:\Repo` and `c:\repo` count as the same place.

## Output

One line per skill per agent, then a summary. Example (trimmed). `<N>` is the number of skill folders plus `_shared`; the summary counts are made up for illustration, and yours depend on what each agent home already holds:

```
Repo skills: <N>  (<repo>\skills, <repo>\.claude\skills)
  - _shared
  - agentic-z-update
  ...

[codex] C:\Users\you\.agents\skills
  [OK]      _shared
  [LINK]    dayz-new-skill  (junction)
  [FOREIGN] dayz-preflight: points at D:\old-clone\skills\dayz-preflight; rerun with --force to take ownership
  ...

[gemini] C:\Users\you\.gemini\skills
  ...

Summary
          linked: 2
              ok: 95
       refreshed: 0
         skipped: 1
          pruned: 0
          failed: 0
```

With `--dry-run` the header reads `Summary (DRY-RUN: nothing was changed)` and the rows that would change something are labelled `would link`, `would refresh`, `would prune` (and `would unlink` with `--unlink`), so a preview cannot be mistaken for a real run.

With `--unlink` each removed link prints as `[UNLINK]  <name>` and the summary has only `unlinked` and `failed`.

Exits 1 if any link operation (including an unlink) failed or an agent's skills folder could not be created (printed as `[FAILED] cannot create <dir>: <error>`; that agent is skipped and the others still run), and 2 if `agents.json` is missing or malformed (a duplicate `"name"`, a missing or empty `"default_home"`, an `"env_home_vars"` that is not a list of variable names, an empty `"skills_subdir"`, or a `"default"` that is not `true` or `false`; the error names the field and the agents that break it), `--agents`/`--skip` names an unknown agent, or the repo has neither a `skills/` nor a `.claude/skills/` folder.

## Steps

1. Run `python "<skill-dir>\sync.py"` (no args = every agent except Claude Code; add `--agents claude` only if you want the skills global in Claude Code).
2. Read the per-agent output. Confirm the skill counts match what's in `skills/` and `.claude/skills/`.
3. Reload each agent session so it picks up the new entries:
   - **Claude Code** (only if you linked or unlinked it): restart the CLI / reopen the chat.
   - **Codex:** restart.
   - **Gemini CLI:** `/skills reload`, then `/skills list` will show them.

## Do not

- Don't edit skills inside `<home>/skills/<name>/` — those are links into the repo. Edit them in `<repo>/skills/<name>/` (or `<repo>/.claude/skills/<name>/` for the repo-only ones) and changes are live everywhere.
- Don't commit anything outside the repo. The agent home dirs are out-of-tree.
- Don't bother running with elevation just to get symlinks instead of junctions on Windows. They behave identically for skill discovery.
