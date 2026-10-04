---
name: update-all
description: Run the self-maintaining update for the whole agent stack (jcode fork rebase, skills sync, tools, configs, manifest) and then reload so the new list is live. Use when asked to "update everything", "update all", "self-update", "keep the stack fresh", or to run the high-level maintenance workflow. Invokes ~/.jcode/bin/update-all.sh and verifies the result.
version: 1.0.0
---

# update-all — self-maintaining stack update

The user wants the entire agent stack updated in one shot, keeping our custom
features on top, then having the fresh skill list take effect immediately, and
finally proving the update worked. Do ALL of the following, in order.

## Custom changes layered on top of upstream

Everything below is our own work, applied on top of base upstream, and is what
`update-all` deliberately preserves (and re-applies after every rebase). If any
of it is ever missing after an update, that is a bug in the updater, not a
deliberate revert.

### jcode fork — `local/turn-end-gate` (PremModhaOfficial/jcode, ahead of 1jehuang/jcode)

Commits carried on top of upstream `master`:

- `65fcb341b` **feat(hooks): opt-in turn_end_gate for external orchestrator continuation**
  Adds an opt-in `turn_end_gate` hook so an external orchestrator (babysitter)
  can drive continuation: instead of jcode ending the turn and waiting for a
  Stop hook that never comes, it yields control at the end of a turn and lets
  the orchestrator resume it. Controlled via `[hooks]` config; off by default.
- `afc3bac81` **fix(hooks): drop stale turn-end gate followup after loop cap**
  Removes a stale follow-up that would fire after the orchestration loop cap,
  so the gate does not linger or double-yield when the loop is already bounded.
- `e974ae785` **feat(update): honor JCODE_NO_AUTO_UPDATE in background check for all builds**
  Makes `JCODE_NO_AUTO_UPDATE` the universal kill switch: the self-dev path
  (`should_spawn_background_update_check`) now skips the background update
  check entirely when the env var is set, matching the release path
  (`should_auto_update`). With `JCODE_NO_AUTO_UPDATE=1` set in
  `~/.config/fish/conf.d/jcode.env.fish` and
  `~/.config/environment.d/10-jcode.conf`, jcode never auto-updates its
  binary — `update-all` is the only gate that updates it.

The updater's `update_jcode` step rebases this branch onto latest upstream
`master` and force-pushes it to the fork, so the commits above sit directly
on top of whatever the base upstream is at update time.

### Hook — `babysitter-gate.sh` (`~/.jcode/hooks/`, source in dotfiles)

The turn_end_gate bridge that actually invokes the babysitter orchestrator.
Ships as a hook file so the `turn_end_gate` feature in the fork has something to
call. Opt-in (commented out by default in `~/.jcode/config.toml`).

### Regenerated skill — `babysit` (`~/.agents/skills/babysit/`)

Re-synced from upstream `a5c-ai/babysitter`, then regenerated with our jcode
adaptation appended:

- `SDK_VERSION=latest`
- `{{harness}}` → `pi`
- Appends the **"jcode harness note"**: jcode does not implement Claude Code's
  Stop/PreToolUse hook protocol, so babysitter runs in non-hook-driven
  continuation mode — keep driving the loop inside the current turn rather than
  yielding and waiting for a Stop hook that never comes.

### Configs (dotfiles → live)

- `~/.jcode/config.toml` — jcode config incl. `[hooks]` (`turn_end_gate` opt-in)
- `~/.jcode/hooks/herdr-agent-state.sh` — reports agent state to herdr (observer hooks)
- `~/.jcode/hooks/babysitter-gate.sh` — turn_end_gate bridge (above)
- `~/.config/herdr/plugins/config/pickr/config.toml` — herdr-pickr (tuicr/hunk/delta/browser)
- `.a5c/processes/` + `~/.a5c/processes/` — babysitter processes, incl.
  `jcode-turn-gate.js`

### Health check after an update

After running the updater, confirm these survive (the skill's Verify section
checks the first two):

- fork branch `local/turn-end-gate` still exists with the 2 commits above
  (`gh api repos/PremModhaOfficial/jcode/branches/local/turn-end-gate`)
- `babysit/SKILL.md` still contains the "jcode harness note"
- `~/.jcode/hooks/babysitter-gate.sh` and `herdr-agent-state.sh` are present

## 0. Read the checklist (ledger of what was done before)

This skill keeps a living ledger at `<skill-dir>/CHECKLIST.md` — every run
appends a table of each step (jcode fetch/rebase/push/build, skill syncs,
tools, configs, manifest, dotfiles) with `done`/`fail` status and a summary.

Read it first:

```bash
cat <skill-dir>/CHECKLIST.md   # ~/.jcode/skills/update-all/CHECKLIST.md
```

Note any previously-failed steps. If a prior run shows a `fail` for a step you
can fix (e.g. dotfiles pull, a skill sync), fix it during this run and confirm
it flips to `done` in the new ledger entry.

## 1. Run the updater

Run the updater **from dotfiles only** — the sole canonical copy of the script
lives in the dotfiles repo at `~/dotfiles/jcode/update-all.sh`. There is no
duplicate bundled in this skill folder; do not copy it anywhere else.

```bash
cd ~/dotfiles && ./jcode/update-all.sh
```

Always execute it from within the dotfiles working tree (`cd ~/dotfiles` first)
so its dotfiles pull/commit/push step operates on the correct repo and branch.

It performs, in order:

1. **jcode core** — fetches upstream (`1jehuang/jcode`), rebases our fork branch
   `local/turn-end-gate` (the babysitter turn-end-gate feature) onto upstream
   `master`, force-pushes it to our fork `PremModhaOfficial/jcode`, and builds.
2. **Skills** — pulls ponytail/caveman, tiger-style, tuicr, babysitter, herdr
   into `~/.jcode/updater-src`; re-syncs them into `~/.agents/skills`;
   regenerates `babysit` with our jcode adaptation (harness=pi).
3. **Tools** — mise herdr@latest, herdr-pickr plugin, babysitter SDK probe,
   gopls.
4. **Configs** — installs dotfiles configs live (jcode config + hooks, pickr
   config, babysitter processes).
5. **Manifest** — regenerates `~/.agents/skills/README.md` (skill → source →
   commit).
6. **Dotfiles auto-commit + push** — the updater ALWAYS does this at the end:
   - pulls `~/dotfiles` (ff-only) so remote changes are merged in first
   - stages only owned paths (`jcode/`, pickr config, `babysitter/`) — never
     `git add -A`, which would sweep in unrelated edits and nested git repos
   - commits as `update-all: sync configs/skills/updater` (allow-empty, so a
     no-change run still records the update)
   - pushes to `origin` (branch `wrk`)
   This keeps dotfiles (the source of truth for configs, the updater, and this
   skill) current on GitHub after every single run. No manual git needed.
   ```bash
   # equivalent manual check:
   cd ~/dotfiles && git log --oneline -3 && git status
   ```

Use a long timeout (the first run clones skill sources and may rebuild jcode;
subsequent runs are fast). If it fails, read the tail of
`~/.jcode/logs/update-all.log` and fix the specific step before proceeding.

## 2. Reload so the new list is live

After the updater succeeds, make the fresh skill list take effect in the
current session:

```bash
# jcode: reload all skills (this agent)
jcode skills reload-all   # or use the skill_manage reload_all equivalent
```

If jcode core itself was rebuilt, tell the user to run `jcode self-dev --reload`
(or restart jcode) so the new binary with the `turn_end_gate` feature is active.

## 3. Verify and report

Confirm the update actually landed:

- Check the manifest exists and count the skills:
  `head -5 ~/.agents/skills/README.md`
- Confirm the custom bits survived: `local/turn-end-gate` is still on the fork
  (`gh api repos/PremModhaOfficial/jcode/branches/local/turn-end-gate`),
  `babysit` still carries the "jcode harness note", `babysitter-gate.sh` is in
  `~/.jcode/hooks/`.
- Check the log tail: `tail -10 ~/.jcode/logs/update-all.log`.

Then give the user a short summary:

```
Updated: <jcode core? skills? tools? configs?> 
Skills now: <N> (from <manifest>)
Custom bits preserved: turn-end-gate on fork ✓, babysit harness=pi ✓, babysitter-gate ✓
Log: ~/.jcode/logs/update-all.log
Next: <anything needing a restart, or ready to work>
```

## Notes

- The only copy of the updater is `~/dotfiles/jcode/update-all.sh` (canonical,
  versioned in dotfiles). Run it only from `~/dotfiles`; it is never duplicated
  into this skill folder or `~/.jcode/bin`.
- Our custom things are preserved every run: `local/turn-end-gate` jcode
  branch, babysitter-gate hook, babysitter processes, pickr config, herdr
  hook, and any skill with no upstream source.
- Use `--dry-run` first if the user wants to preview.
