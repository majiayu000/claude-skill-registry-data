---
name: spawn-cc-remote
description: Spawn a detached interactive `claude --remote-control` session locally and return the claude.ai/code session URL. Use when the user wants to pair a Claude Code session from claude.ai/code web, their phone, or another machine. Trigger phrases — "spawn cc remote", "new remote-control session", "give me a web URL for CC", "/spawn-cc-remote".
---

# spawn-cc-remote

## Purpose
Start another local Claude Code session with Remote Control enabled,
detached from the current shell, and return the `claude.ai/code/session_...`
URL the user can open from any browser or phone. The spawned process
keeps running after the current CC session ends.

## Why a skill (not just a command)
`claude --remote-control` is a TUI. Run from inside another CC session
via the `Bash` tool, it has no TTY → falls into `--print` mode → exits
demanding a prompt. This skill wraps `script(1)` to provide a
pseudo-TTY so the spawned claude boots interactive anyway.

## Inputs
- Optional `name` argument → session name (also names the log file).
- Default name: `rc-<unix-ts>`.

## Steps
1. Run `bash bin/spawn-cc-remote.sh [name]`.
2. Script prints four `key=value` lines on success:
   - `url=https://claude.ai/code/session_...`
   - `name=<session-name>`
   - `pid=<pid-of-claude-process>`
   - `log=/tmp/cc-rc-<name>.log`
3. Surface the `url` to the user as a clickable line. Also report the
   pid so they can kill it later.
4. If the script prints `FAILED:` and a log tail, surface the failure
   verbatim — don't retry blindly. Common causes:
   - `claude` CLI not in PATH for non-login shells.
   - User not authenticated (run `claude /login` once manually first).
   - Working directory denied by workspace-trust prompt — answer yes
     once in a real terminal, then this skill will work.

## Cleanup
- `kill <pid>` or `pkill -f "claude --remote-control <name>"`.
- Log files at `/tmp/cc-rc-<name>.log` persist until reboot. Safe to
  delete after the remote session ends.

## Caveats / known
- Spawned session inherits the **current working directory** of the
  caller. If you want it rooted elsewhere, `cd` first or pass the dir
  through the calling shell.
- Hooks/MCP servers configured in `.claude/settings.json` load in the
  spawned session normally — Semgrep / IDE-extension warnings are
  non-blocking.
- Spawning two sessions with the same `name` will collide in the log
  file. Either pass a unique name or let the timestamp default fire.

## Verification
After surfacing the URL, optionally run:
```
ps -o pid,ppid,etime,command -p <pid>
```
to confirm the process is alive. Three-process chain expected:
`zsh → script → claude`.
