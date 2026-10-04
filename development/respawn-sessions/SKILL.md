---
name: respawn-sessions
description: Respawn Bryan's long-running Claude Code sessions in detached tmux sessions. Four modes — `missing` (default, fill gaps), `plugin` (kill+respawn anyone lacking the fleet plugin), `all` (kill+respawn every registry entry), `running` (kill+respawn what is actually up, at its own cwd — the mode to use after a /login account switch). Auto-accepts dev-channel permission dialogs and sweeps orphan claude-hive servers. Also holds `self-respawn.sh` for the team-lead to cycle its own session (which the modes never kill) onto a new binary/plugin/settings.
---

# Respawn Sessions

Re-open Bryan's long-running Claude Code sessions as detached tmux sessions. One command for any of these scenarios:

- After a Mac reboot — fill gaps in the running set.
- After a plugin/marketplace update — push every session onto the new plugin set.
- "Respawn everything" — full fleet reset.

Attach to any session with `tmux a -t <session>` when you want a pane visible.

## Modes

| Mode | What it does |
|------|--------------|
| `missing` (default) | For each `respawn: true` project: spawn a fresh session ONLY if no claude is currently running with that project's `path` as cwd. Skips everything that's already up. **Safe.** |
| `plugin` | Kill+respawn any running session whose argv includes neither install key of the canonical fleet plugin (`plugin:claude-workspaces@claude-workspaces`, or the pre-rename `plugin:live-feedback@claude-live-feedback`). Use after enabling/upgrading a plugin globally. **Team Lead (self) is never killed**; if it lacks the plugin, the script flags it for manual restart. |
| `all` | Kill+respawn every `respawn: true` session. Use as a full fleet reset. **Team Lead (self) is never killed.** |
| `running` | Kill+respawn every session that is **actually running, at its own cwd**, ignoring the registry. **This is the account-switch mode** — use it after Bryan runs `/login`. **Team Lead (self) is never killed.** |

### After a `/login`, the mode is `running` — not `all`

`--mode all` respawns what the registry *says* should be up, at the registry's canonical path. After an account switch you need the opposite: every session that is *actually* up has to cycle, or it keeps the old account's MCP handshakes. `all` gets this wrong in two specific ways, and both bit on 2026-09-01:

- **It skips `respawn: false` sessions.** Workspaces is marked `respawn: false` and was 51% of that day's burn — the single most important session to move, silently excluded.
- **It relocates a worktree session to the registry path.** The ClientOrg Project Beta peer came back at `~/dev/project-alpha` on an unrelated branch, resuming a different conversation, and looked completely healthy doing it.

**The failure mode to watch for in yourself is patching those two symptoms by hand** — reaching for a raw `tmux new-session` for the session the mode skipped, and another for the one it misplaced. That is how both peers came up with no `CW_AGENT_NAME` and mute on the board. One `--mode running --execute` does the whole job.


**Every mode takes `--only <substr>`, repeatable.** It restricts the mode to targets whose display name or path matches, case-insensitively — so a subset respawn is `--mode missing --only workspaces --only <second-project> --execute`, not a reason to write your own loop. A mode is not all-or-nothing, and on 2026-08-30 assuming it was cost the fleet two extra restarts. Full flag list: `respawn.py --help`.

## Per-peer DISCORD_STATE_DIR scoping (automatic)

Each spawned tmux session gets `DISCORD_STATE_DIR` set explicitly via `tmux new-session -e DISCORD_STATE_DIR=…`, so the peer doesn't inherit the team-lead's discord state. Two destinations:

- **Peer has its own `.claude/discord/access.json`** (e.g., octoturtle with a family-bot) → that peer's local state dir is used.
- **Peer doesn't** → a shared `~/.config/team-lead/no-discord/` state is used. The dir contains an empty allowlist and no `.env`, so the discord plugin loads but doesn't connect (no token) and the peer isn't subscribed to any channel.

Why this matters: without the per-session override, every peer inherits the team-lead's `DISCORD_STATE_DIR` from the team-lead's shell env (set by direnv). All peers then share the team-lead's bot + access.json + channel subscriptions. A single Discord post to the team-lead's channel fans out to every peer. The `-e` flag is critical — `new-session` ignores client env if the tmux server is already running, so just `export`ing the var in the parent shell doesn't help.

Encoded in `respawn.py`'s `discord_state_dir_for(path)` + `spawn_session_tmux`.

## Every session needs a name, and a nameless one fails silently

`CW_AGENT_NAME` — and `FEEDBACK_AGENT_NAME`, which carries the same value for the pre-rename spelling — is what gives a session an identity on a claude-workspaces board. It comes from `session_name` in `registry.yaml`, and `spawn_session_tmux` passes both via `tmux new-session -e`.

**Without it, a session reads the board perfectly and writes nothing.** It connects, it attaches, it receives every comment event as it arrives. Every write — a comment, a status note, a filed task — is refused with `author-required`, because an unnamed session collapses into the shared "agent" category and a category is not an author.

That asymmetry is the whole hazard. There is no crash, no red banner, no missing tool. From the inside the session looks healthy and stays busy; from the outside it is a peer that hears everything the user says and answers none of it. On 2026-08-30 all eight tmux peers ran that way, and it surfaced only because the user asked one of them directly whether it was still connected.

### Check it before trusting a cycled fleet

```bash
for s in $(tmux ls -F '#{session_name}'); do
  printf '%-22s ' "$s"; tmux show-environment -t "$s" CW_AGENT_NAME 2>&1 | head -1
done
```

Every line should print `CW_AGENT_NAME=<the registry session_name>`. A line reading `unknown variable` is a mute peer. It cannot be repaired in place — the value is read at startup, so the fix is always a relaunch: `--mode missing --only <name> --execute`.

**Ask a suspected session to post something, not to read something.** Reading was never the broken half, so "I can see the board" is not evidence either way.

### Hand-rolling a spawn drops it

This is how it happened. An account cycle was run with a hand-written `tmux new-session` loop instead of this script, because of a wrong belief that the script could not do a subset. The loop carried `DISCORD_STATE_DIR` across and dropped both name variables — a third spawn path with none of the script's accumulated knowledge in it. All eight sessions came up mute.

**Use `respawn.py` for any spawn, including a single session and including an account switch.** A spawn line has more load-bearing detail than it looks: the two name variables, `DISCORD_STATE_DIR` scoped per peer, `--continue` only where a transcript exists and never where `fresh_start: true`, and home-path resolution so a worktree session resumes its own transcript. A loop written from memory reproduces whatever the docs discuss at length and silently drops whatever lives in a docstring — which is not the same ranking as what matters.

If you must hand-roll one anyway, copy the `-e` flags out of `spawn_session_tmux` verbatim rather than writing them from memory, then run the check above before calling the cycle done.

## There are TWO spawn paths, and only one of them gets updated

`respawn.py` spawns every peer. `self-respawn.sh` spawns the team-lead, because the team-lead runs as a
bare `claude --continue` and cannot be killed by the modes above. **They carry their launch env
independently, and a variable added to one does not appear in the other.**

Measured 2026-09-17. claude-workspaces 0.1.182 moved the end-of-turn note route under the board and made
the Stop hook read that board from the launch env — `readWorkspaceId` consults `CW_WORKSPACE_ID` then
`FEEDBACK_WORKSPACE_ID` and has no third fallback. `respawn.py` was updated and passes it for every peer.
`self-respawn.sh` was not, so the team-lead came back carrying `CW_AGENT_NAME` and no board, and its hook
exited 0 posting nothing on every turn for weeks. One record in 24 hours across a night of continuous work.

- **The failure is silent on both sides.** The hook exits 0 by design so it can never block a turn, and a
  session posting nothing looks exactly like a session having quiet turns. Nothing distinguishes them from
  outside; reading the session's own env is the only check that answers it.
- **The session it misses is the one coordinating the others.** A structural fix that covers everything
  spawned one way cannot reach the thing spawned the other way, and here that is the team-lead.
- **When you add anything to `spawn_session_tmux`, add it to `self-respawn.sh` in the same change.** Read
  the value from `registry.yaml` rather than hardcoding it, so the two paths cannot drift to different
  answers. `TL_WORKSPACE` is the worked example.
- **Verify from inside a real session, not from the script.** `printenv CW_WORKSPACE_ID` in the running
  team-lead is the check; the script reading correctly proves only what the next spawn will do.

**Expect this to recur.** The trend is toward more per-session configuration, and each new variable breaks
in exactly this place — the path nobody remembered was a second path.

## Misplaced session home

A session's **home** is the directory whose transcript `--continue` resumes. Normally
that is the registry `path`. When a peer is started in a git worktree, its transcript
lives under the worktree's encoding instead, and the two disagree.

`[misplaced]` in the dry-run output means exactly that: the session is alive somewhere
other than its registry path, and the script is respawning it **where it is**, because
that is the only cwd whose `--continue` restores the work it is holding. Respawning at
the registry path instead would resume a different, older conversation and the peer
would come back looking healthy while holding none of its context.

- **This is correct behaviour, not an error.** Do not "fix" it by pointing the respawn
  at the registry path.
- **It reproduces on every respawn** until the transcript is migrated from the worktree
  encoding to the registry-path encoding. Until then the peer's home is the worktree.
- **A worktree is temporary; the registry path is the agent's home.** Migrate when the
  branch work is finished, then the warning stops.

`--at <path>` is the deliberate form of the same thing — see below.

## Reviving a session at an explicit path: `--at`

```bash
python3 respawn.py --at ~/dev/some-project/worktrees/feature-x --execute
```

Repeatable. Takes an explicit cwd, spawns there whether or not anything is currently
running at that path, and whether or not the registry knows the path at all. Anything
alive there is cycled first.

The gap it fills: `--mode running` can only cycle a session that is **alive**, and
`--mode missing` spawns at the **registry** path. So when a worktree session dies —
a reboot, a crash — neither mode brings it back where it lived, and `missing` mode
quietly resumes the wrong conversation. Added 2026-09-04 after a reboot killed a
worktree session mid-benchmark and the only way back looked like a hand-rolled tmux
spawn, which is the thing this script exists to prevent.

It goes through the full spawn path, so the identity env, the scoped Discord state
dir, dialog dismissal and the orphan-MCP sweep all still apply.

## Spawning on a second account: `--account-dir`

```bash
python3 respawn.py --mode running --only <name> --account-dir <folder> --execute
```

Sets `CLAUDE_CONFIG_DIR=<folder>` for each spawn, so the session runs on the
subscription account logged in to that folder. Combine it with any mode, `--only` or
`--at`.

- **Build the folder with `scripts/account_dir.py <folder> --execute`.** It links the
  shared parts of `~/.claude` (settings, plugins, transcripts and memory, skills) into
  the folder and seeds the folder's own `.claude.json` without the main login's
  account record.
- **Someone runs `/login` in the folder once**, as
  `CLAUDE_CONFIG_DIR=<folder> claude`. The script refuses a folder with no login
  recorded, since a session spawned there would sit at a login prompt.
- **Spell the folder the same way every time.** The Keychain entry holding the login
  is keyed to the exact path string. The script canonicalizes to the realpath, and
  `account_dir.py` prints the command to log in with that spelling.
- **A spawn without the flag uses the default login.** So `--mode running` without
  `--account-dir` moves a session on a spare account back to the main one.

## What `--execute` actually does

Beyond spawning the tmux sessions, when something gets spawned the script also:

1. **Polls each new tmux pane for known startup dialogs** and sends Enter to dismiss them — covers the dev-channel approval dialog (`--dangerously-load-development-channels`), the MCP-server approval dialog, and the resume-from-summary auto-compact dialog. Polls every 3s for up to ~75s; multiple Enters per pane are sent if dialogs chain.
2. **Sweeps orphan `claude-hive-mcp/server.ts` processes** (re-parented to PID 1 / launchd) left behind by killed claudes. Without this, new claude sessions can't register with claude-hive cleanly — the hive registry would still show the old PIDs.

Pass `--no-auto-accept` to skip both post-spawn steps and walk through the panes by hand.

## Safety: dry-run by default

The script is **dry-run by default**. A bare invocation prints what it would do (which projects are already running, which would be killed, which would be spawned) and exits without touching anything. To actually execute you must pass `--execute`.

```bash
# Safe preview:
python3 respawn.py
python3 respawn.py --mode plugin
python3 respawn.py --mode all

# Actually do it:
python3 respawn.py --execute                   # missing (default)
python3 respawn.py --mode plugin --execute     # upgrade plugin-less sessions
python3 respawn.py --mode all --execute        # full fleet reset

# Skip post-spawn dialog acceptance + cleanup (rare — usually you want it):
python3 respawn.py --execute --no-auto-accept

# Help:
python3 respawn.py --help
```

## How to invoke

### Manually (from a team-lead session)

```bash
python3 /Users/bryanchan/dev/ai-team-lead/.claude/skills/respawn-sessions/respawn.py --mode all --execute
```

### Via the skill

If you have this skill loaded, say "respawn my sessions" or "respawn all agents." Team Lead will pick the right mode based on intent — `all` for "respawn all," `plugin` for "the plugin isn't loaded everywhere," `missing` for default fill-gap.

### Attaching to a session

```bash
tmux a -t <session-name>      # e.g. tmux a -t my-project
tmux ls                        # list all live tmux sessions
```

Session names are derived from the registry's `session_name` field, lowercased with spaces replaced by hyphens (e.g., `"My Project"` → `my-project`).

## Team Lead self-protection

The script walks the parent process chain to identify the team-lead's own claude PID and **never kills it**, in any mode. If `--mode plugin` finds the team-lead lacks the plugin, it prints a flag — but you don't need a human to restart the team-lead: use `self-respawn.sh` (next section) to cycle your own session autonomously.

If the parent-walk fails to find a claude PID (`get_self_pid()` returns None), `--mode all` and `--mode plugin` abort with a non-zero exit code rather than risk killing the team-lead.

## Respawning yourself (the team-lead)

Because the modes above never kill self, the team-lead can't ride an `--mode all/plugin` respawn onto a new binary, plugin, or `~/.claude/settings.json` change. Use **`self-respawn.sh`** — it cycles your own session autonomously, no human step:

```bash
# Discover your own claude PID first: the top-level …/bin/claude ancestor
# (NOT the hive-mcp child), via the parent-process walk — same logic as
# respawn.py's get_self_pid. Then:
bash .claude/skills/respawn-sessions/self-respawn.sh <team-lead-claude-pid>
```

**How it works:** the team-lead runs as a bare `claude --continue` process and can't revive itself directly (a dying process can't respawn itself, and a detached spawn needs a pty). The script schedules a **detached** respawn via `setsid` — so it survives the team-lead's own death — then kills self. The detached job waits for the old process to exit, then spawns a fresh team-lead into tmux session `team-lead` on the **current** binary + plugin set, resuming this very conversation via `--continue`, and auto-accepts the startup dialogs (dev-channel / MCP / resume-from-summary → this is what compacts you).

- **~10–20s gap** with no team-lead, then back in `tmux:team-lead`, same conversation (compacted), named "Team Lead". Reconnect via `tmux a -t team-lead` or Remote Control — it re-registers on the hive.
- **Do this LAST** — it ends the current session. Deliver any report and finish any in-flight handoff first.
- **No `-e DISCORD_STATE_DIR`** — the team-lead keeps its own shell/direnv discord state (unlike peers, which get an explicit override to prevent channel fan-out).
- **Tell a live human first** if one's mid-conversation — the `--continue` preserves context, but the ~15s gap + reconnect is visible. For a fully-autonomous/off-hours run, just fire it.
- **Use it to pick up:** a new Claude Code binary (`/self-update` Step 6), the fleet plugin, or any user-scope settings change that only applies on restart.

### Hard-won invariants — do not "simplify" these away

Learned the expensive way (2026-07-11): the first version used `setsid`, **which does not exist on macOS**. The detach failed with `setsid: command not found`, but the script fell through and killed self anyway — the team-lead went down for **~16 hours** with no revival path, until a human noticed and a peer hand-restarted it.

1. **Detach via `python3 -c 'os.setsid()'`, never `setsid(1)`.** macOS has no `setsid` binary. `nohup … & disown` alone is *not* sufficient — it only ignores SIGHUP, it does not escape the dying process's group.
2. **Never kill self until the detached job proves it armed.** The job's first act is to `touch` a sentinel; the script blocks on that sentinel and **ABORTs (leaving the team-lead alive)** if it never appears. A failed detach must cost nothing.

If you see `ABORT: respawn job never armed`, that is the guard working — the team-lead is still up and nothing was lost. Read `/tmp/tl-selfrespawn.log` and fix the cause; do not bypass the guard.

**The general rule:** any script that kills its own caller must *prove the revival path is live* before pulling the trigger — and you must test it against a dummy victim (with side-effects stubbed) before ever aiming it at yourself.

## How to add or remove a project from the respawn list

Edit `registry.yaml` and add (or remove) two fields on the project's entry:

```yaml
projects:
  example-project:
    type: personal
    path: ~/dev/example-project
    repo: fryanpan/example-project
    respawn: true              # ← include in respawn
    session_name: "Example"    # ← tmux session name (optional; defaults to humanized key)
    docs:
      ...
```

`respawn: true` is required. `session_name` is optional — if missing, the script uses a Title-Cased version of the registry key. `repo` is **optional**: omit it for a local-only folder (no git repo — e.g. a synced Google Drive subfolder). respawn.py never runs git regardless, so a local-only project respawns exactly like a repo-backed one; only `path` + `respawn: true` are needed.

No need to redeploy the script — the next respawn pass picks up the new registry contents automatically.

## How it parses registry.yaml

Minimal regex parser (~30 lines), no PyYAML dependency. Handles the registry's specific structure (2-space project keys, 4-space scalar fields). Ignores nested blocks like `docs:`, `linear:`, `notion:`.

## Why `zsh -ic` (and not bare `claude`)

Bryan's `claude` is a zsh **function** (defined in `~/.zshrc`), not an alias. The function injects the canonical channel + dev-plugin flags before forwarding to `/Users/bryanchan/.local/bin/claude`. Bare `claude` from a non-interactive shell skips the function entirely.

The script invokes `tmux new-session -d -s <name> -c <path> /bin/zsh -ic "claude --continue"` so the interactive zsh sources `~/.zshrc` and the function applies. Don't try to inline the channel flags in `claude_invocation` — the function will append its own copy and you'll see duplicates in argv.

## Bootstrapping requirements

For each project to actually have a session to resume:

- The project's `path` must exist as a directory.
- The project must have at least one prior Claude Code conversation in that directory (so `claude --continue` finds something to resume). For brand-new projects, the script falls back to plain `claude` (per `feedback_first_time_spawn.md`).

The script logs `[skip]` for any registry entry whose `path` doesn't exist on disk and continues.

## Failure modes and how to debug

- **`claude` command not found in pane:** the inline `zsh -ic` should source `~/.zshrc`. If your `claude` shell function isn't there, or `~/.local/bin` isn't on `PATH`, fix the rc file. Verify with `tmux capture-pane -t <session> -p` after spawn.
- **Dialog wasn't dismissed:** the auto-accept polls the pane via `tmux capture-pane -p` and sends `Enter` when it sees one of `DIALOG_PATTERNS` (`Resume from summary`, `I am using this for local development`, `Use this and all future MCP servers`, `Enter to confirm`). If a new dialog wording doesn't match, add it to the pattern list. As a workaround: `tmux send-keys -t <session> Enter` manually.
- **Wrong session resumed:** `claude --continue` resumes the most recent conversation in the cwd. If you accidentally started a fresh session in that cwd at any point, it's now the "most recent." Fix: attach with `tmux a -t <name>`, run `/resume` in-session, pick the right one, exit, and the next respawn will grab it.
- **tmux session name collision:** `spawn_session_tmux` calls `tmux kill-session -t <name>` before creating, so the spawn is idempotent. If you see "session not found" warnings on first run, that's normal — the kill is best-effort.

## Common scenarios

### "I just enabled a new plugin globally and want every agent to pick it up"

```bash
python3 respawn.py --mode plugin --execute
```

If team-lead itself lacks the plugin, the script flags it. Restart team-lead with `/exit` then `claude --continue`.

### "I rebooted my Mac and want my fleet back"

```bash
python3 respawn.py --execute
```

(`missing` mode — only spawns gaps, doesn't disturb anything that's already up.)

### "Something's weird — full reset"

```bash
python3 respawn.py --mode all --execute
```

Kills + respawns everything. Team Lead is preserved; restart manually if needed.
