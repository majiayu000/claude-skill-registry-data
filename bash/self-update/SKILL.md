---
name: self-update
description: Weekly self-maintenance for the team-lead — update Claude Code to the latest version and pull the latest ai-team-lead repo (skills, rules, registry, scripts), then propagate both to the fleet. Runs as Step 0 of /weekly-plan; also invoke ad hoc after a known Claude Code release or a big repo change.
user-invocable: true
---

# Self-Update (weekly)

Keep the team-lead current on two axes: the **Claude Code binary** and the **ai-team-lead repo** (your own skills/rules/registry + the fleet plugin). Both only take effect on a restart/respawn, so this skill also handles propagation to the fleet.

## When to run

- **Every week, at the start of the week** — this is Step 0 of `/weekly-plan`, so it happens each planning session.
- Ad hoc after a known Claude Code release, or after a big `ai-team-lead` change you want the fleet on.
- Prefer a moment when the fleet is between tasks — Step 4 respawns peers, which interrupts in-flight work.

## Steps

### 1. Claude Code version

```bash
before=$(claude --version)
claude update            # checks for updates and installs if behind
after=$(claude --version)
echo "Claude Code: $before -> $after"
```

- If `after` > `before`, the on-disk binary updated. **The running team-lead session keeps the OLD version until restarted** — but the team-lead can restart itself autonomously (Step 6, self-respawn), so no human step is needed. Peers keep their old version until respawned (Step 4).
- If unchanged, there's nothing to propagate for the version.

### 2. Pull the latest ai-team-lead

```bash
cd ~/dev/ai-team-lead
git status --porcelain           # the team-lead repo is a live worktree — check for WIP first
```

- **Clean** → `old=$(git rev-parse HEAD); git pull --ff-only origin main`.
- **Dirty** → commit or `git stash -u` your WIP first (per the working rules), pull, then restore. Never force. If it can't fast-forward, investigate before proceeding — don't paper over a diverged history.
- Review what changed so you know how your own behavior + the fleet's just shifted:
  ```bash
  git log --oneline "$old"..HEAD -- .claude/ plugin/ registry.yaml
  ```
  Call out any new/changed skills, rules, or registry entries in the report.

### 3. Reload skills/rules in this session

- Run `/reload-plugins` to pick up `plugin/team-lead-fleet/` changes without a full restart.
- Top-level `.claude/` skills + rules and `CLAUDE.md` are re-read on the next session start; note in the report if a full restart is needed to apply something.

### 4. Propagate to the fleet

Peers each run their own copy of the binary + the fleet plugin, so they need respawning to pick up changes. Respawned peers launch via the `claude` shell function → the updated binary + current plugin, automatically.

- **Claude Code version bumped** → full respawn onto the new binary:
  ```bash
  python3 .claude/skills/respawn-sessions/respawn.py --mode all --execute
  ```
  Checkpoint any peer mid-task first (graceful path in `/shutdown-session`) — don't kill in-flight work.
- **Only `plugin/team-lead-fleet/` changed** → **run `/ship-fleet`, not a respawn.** A respawn re-reads the
  version-keyed cache at `~/.claude/plugins/cache/`; if the version wasn't bumped that cache is stale, and the
  peer comes back on a fresh process running the same old rules. `/ship-fleet` bumps both manifests, refreshes
  the cache, reloads peers in place, and verifies from a peer's injected context rather than from yours.
- **Neither changed** → skip; nothing to propagate.

### 5. Report

One block back to Bryan:
- **Claude Code:** `<before> → <after>` (or "already current").
- **ai-team-lead:** N commits pulled; bullet any skill/rule/registry changes worth knowing.
- **Fleet:** respawned (which mode) / no respawn needed.
- **Pending on Bryan:** nothing for a routine update — the team-lead self-respawns (Step 6). Flag Bryan only if self-respawn is disabled/fails, or if a peer respawn needs his input.

### 6. Self-respawn onto the new binary (autonomous — only if Step 1 bumped the version)

The team-lead runs as a bare `claude --continue` process, so it can't revive itself directly. `self-respawn.sh` schedules a **detached** respawn (via `setsid`, so it survives the team-lead's own death), then kills self. The detached job waits for the old process to exit, then spawns a fresh team-lead into tmux session `team-lead` on the new binary, resuming this conversation via `--continue`.

**Do this LAST** — after the report (Step 5) is delivered and after the fleet respawn (Step 4), since it ends the current session. Discover your own claude PID via the parent-process walk (the top-level `…/bin/claude` ancestor, not the hive-mcp child), then:

```bash
bash .claude/skills/respawn-sessions/self-respawn.sh <team-lead-claude-pid>
```

(The script + full self-respawn how-to now live in the `respawn-sessions` skill — see its "Respawning yourself" section.)

- ~10–20s gap with no team-lead, then it's back in `tmux:team-lead`, same conversation, new binary, named "Team Lead". Reconnect via `tmux a -t team-lead` or Remote Control (it re-registers).
- No `-e DISCORD_STATE_DIR` — the team-lead keeps its own shell/direnv discord state (unlike peers).
- **Only self-respawn when the binary actually changed.** If Step 1 was a no-op, skip — don't churn the session for nothing.
- If a live human is mid-conversation with the team-lead, tell them it's about to happen (the `--continue` resume preserves context, but the ~15s gap + reconnect is visible). For a fully-autonomous run (cron/off-hours), just fire it.

## Cadence & wiring

- Reliable trigger is **Step 0 of `/weekly-plan`** (human present, week start, fleet usually idle) — this is deliberately NOT a fully-autonomous cron, because Step 4 respawns the fleet and wants a human around for mid-task peers.
- If Bryan wants the binary kept fresh mid-week too, a **version-check-only** loop is safe to schedule (Steps 1 + report, skip the fleet respawn): `/loop 3d run self-update version-check only`. Keep the disruptive propagation on the weekly, human-present run.

## What to avoid

- Don't `git pull` over uncommitted WIP — the team-lead repo is a live worktree; stash or commit first.
- Don't respawn peers mid-flight without checkpointing (graceful shutdown first).
- Don't assume the running team-lead is on the new version — it isn't until Bryan restarts it.
- Don't run the fleet respawn autonomously with no human present unless Bryan has explicitly opted in.
