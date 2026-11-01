---
name: dayz-record-correction
description: "Turns the user's correction of how the mod team built something into a written rule with good and bad examples, confirms it, and saves it where every agent follows it. Use whenever the user corrects the team's code, config, structure or behavior, or says \"remember this\" or \"always/never do X\"."
argument-hint: "[what the user corrected]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-record-correction

The user's corrections are how the team learns. Nothing is written without their yes.

This is a meta-skill that edits rule files, not DayZ content, so like `/dayz-scope-mod` it does not gate on `/dayz-preflight`. The Tier 2 rules it adds to live in `skills/_shared/dayz-conventions.md` and its topic files in `skills/_shared/conventions/`; read the relevant section there before drafting so the new rule matches what is already written.

## 1. Find the repo, then draft the rule

First find where this skill really lives, because every path below is relative to that Agentic-Z repo root, not to the current project. `/sync-skills` exposes the skill through a link (a junction on Windows) under `~/.claude/skills/`, and the harness reports the link path as the base directory, so resolve the link before deciding anything:

```cmd
python "<skill-dir>\check.py" root "<skill-dir>"
```

It follows symlinks and junctions and prints JSON with `kind` (`clone`, `plugin` or `unknown`), the resolved path, the repo `root` and any `missing` required files. Exit 0 means a usable clone or a plugin install; exit 2 means stop and ask the user where their Agentic-Z repo is, and write nothing until they answer. What it checks:

- Under `~/.claude/plugins/cache/` (for example `C:\Users\<you>\.claude\plugins\cache\...`): a plugin install.
- Ending in `\skills\dayz-record-correction`: a clone. The repo root is two levels up (the folder that holds `skills\`), and it must hold both `skills\_shared\dayz-conventions.md` and `.claude\CLAUDE.md`. If either is missing, the command lists it under `missing` and exits 2. A copy (not a link) in `~/.claude/skills/`, where two levels up is `~/.claude`, is reported as `unknown` and also exits 2.

Then draft:

```
Rule: <one sentence, in the user's words>
Why: <one line>
Good: <a short example>
Bad: <the version the user corrected>
Tier: 1 | 2 | 3 (<file>)
```

Pick the tier by scope:

- **Tier 1**: how any agent works in this repo, DayZ or not (reporting, tooling, file locations). Goes in `.claude/CLAUDE.md`, `AGENTS.md` and `GEMINI.md`, all three with the same text.
- **Tier 2**: true for all DayZ work (Enforce Script style, config patterns, asset rules). Goes in `skills/_shared/dayz-conventions.md` if every DayZ agent needs it, otherwise in the matching topic file under `skills/_shared/conventions/` (config, assets, scripts, ui, server).
- **Tier 3**: about one kind of work. Goes in that agent's file under `agents/` or the matching knowledge pack under `skills/_shared/`.

Once you have picked a tier, search all three tiers for a rule that overlaps: Grep the key words across `.claude/CLAUDE.md`, `skills/_shared/dayz-conventions.md`, `skills/_shared/conventions/*.md`, `agents/*.md` and `skills/_shared/**/*.md` (the knowledge packs live in subfolders such as `_shared/enscript/`), all under the `root` the command above printed. In a plugin install, Grep the plugin's own copies of those files and also the `## Agentic-Z rules` section of the current project's `CLAUDE.md`, `AGENTS.md` and `GEMINI.md`, because step 3 writes plugin rules there. An earlier correction on the same topic lives there, and it counts as an overlapping rule like any other:

- An overlapping rule in the right tier: propose an edit to that rule instead of a new one.
- An overlapping rule in the wrong tier (for example a DayZ-wide rule sitting in one agent's file): propose moving it to the right tier and merging the correction into it, so the rule lives in one place.
- Overlapping rules in two tiers: propose merging them into the one tier that fits.

## 2. Ask the user

Show the draft and ask for yes, a change, or no. Keep it short.

## 3. Write it (only after yes)

In a clone, record a baseline before you edit anything (step 3b compares against it). The repo checks can already fail before your edit, and without a baseline every pre-existing failure looks like yours. The checks need pytest once: `python -m pip install pytest`.

```cmd
python "<skill-dir>\check.py" baseline --root "<repo root>"
```

It runs the full test suite and `docs-sync --check` once and saves the failing test ids and wiki problems, with the resolved repo root and the time it was made, to `record-correction-baseline.json` in the system temp folder (pass `--out <file>` to choose another path). The same command works in cmd, PowerShell and Git Bash. A check that crashes or exits non-zero without listing anything (a pytest internal error, a docs-sync traceback) is saved as a failure too, never as a pass.

**It takes several minutes** (about 5 on this repo, almost all of it pytest). It prints `running pytest ...` and `running docs-sync --check ...` to stderr as it goes, and stops any check that runs past `--timeout` seconds (default 1200) and records it as a failure. Run it in the background (the Bash or PowerShell tool's `run_in_background`) and wait for it to finish, or in the foreground with the tool's timeout set to 600000 ms. The default 2-minute shell timeout kills it. If a foreground run is killed, run it again in the background. Do not edit until it has printed `baseline saved to ...`.

- In a clone, edit the file the tier names under that repo root, even when the session was started in another project. Keep the edit small and in the file's existing style.
- In a clone, if the edit changes the length of `skills\_shared\dayz-conventions.md` or a topic file under `skills\_shared\conventions\`, or adds, renames or removes an agent or skill, run `/docs-sync` so the React wiki under `wiki\src\` still states the right line counts, names and numbers (`--apply` rewrites wrong counts; names need a hand edit). Otherwise the Stop hook reports wiki problems at the end of the session.
- In a plugin install, the plugin's files are replaced on every update. Write the rule under a `## Agentic-Z rules` heading in whichever of the project's `CLAUDE.md`, `AGENTS.md` and `GEMINI.md` exist, with the same text in each, and say that's why. For a Tier 1 rule, create any of the three that are missing, so Claude Code, Codex and Gemini all see it. For a Tier 2 or Tier 3 rule, create all three the same way when none of them exists.

## 3b. Check it (clones only)

Compare against the baseline from step 3. Like `baseline`, it takes several minutes: run it in the background or with a 600000 ms shell timeout.

```cmd
python "<skill-dir>\check.py" compare --root "<repo root>"
```

It reads the baseline from the same temp file (pass `--baseline <file>` if you used `--out`), runs the same two checks from the repo root (`python -m pytest -q .claude skills scripts/dev hooks` and `python .claude/skills/docs-sync/sync.py --check`), prints each `NEW` failure and each one that was `fixed`, and exits 1 only when something is new. Exit 2 means the baseline cannot be trusted, and nothing is compared: the file is missing or unreadable, it was made for another repo root (another clone), it is older than `--max-age-hours` (default 12, so a baseline from an earlier session is refused), or it was written by an older `check.py` without a root and time. Run `baseline` again (before editing, or after reverting your edit) before trusting any result. Wiki problems are matched without their line numbers, so a shifted line is not counted as new, and they are compared as counts, so a second copy of a problem the file already had is reported as new. Failures already in the baseline are not yours: report them, never revert for them. The root `pytest.ini` skips `.claude/worktrees/`, where Claude Code keeps full copies of the repo for its worktree sessions, so the run sees only this checkout.

An edit to an agent file or a rules file can break the repo tests (for example `test_route.py` checks the agent list against `rules.json`). If `compare` reports a new failure, fix the problem or revert the edit, then run `compare` again. A new wiki problem after a rules-file edit usually means `/docs-sync` still needs to run (step 3).

## 4. Say what changed

One line: the rule and the file it went into. When `/docs-sync` ran, also name the wiki file it updated, for example `wiki\src\content\guide.md`. In a clone, add the result of step 3b: no new failures, or each new one and whether you fixed or reverted it, plus the count of failures that were already in the baseline.
