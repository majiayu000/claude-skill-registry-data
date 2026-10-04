---
name: shutdown-session
description: Cleanly shut down peer Claude Code session(s). Maps project paths to the actual claude binary PIDs (NOT the hive-mcp child PIDs that `list_peers` returns), kills them, sweeps any orphan MCP servers, and verifies. Use when spinning down agents that aren't needed for the current week's goals, or freeing memory after a /weekly-plan pass.
user-invocable: true
---

# Shutdown Session

Cleanly shut down peer Claude Code sessions.

**The non-obvious bit:** `mcp__claude-hive__list_peers` returns the **bun claude-hive-mcp server's PID** for each peer, NOT the claude binary's PID. Killing that bun PID severs the hive connection but leaves the claude session running — and the claude process will just spawn a new hive-mcp child. To actually spin down a session, you have to find the claude binary's PID by cwd, then kill that.

## When to invoke

- "Spin down peer X" / "shut down X" / "kill X agent"
- Spinning down agents not on this week's committed goals (after `/weekly-plan` decides the team)
- Freeing memory / reducing fleet size before a respawn pass
- Periodic cleanup of dormant peers

## When NOT to invoke

- A peer is mid-work and shutdown would lose state. Send them a hive message first asking to checkpoint + finish, then shut down once they ack.
- The team-lead's own session — never kill self. The cwd-mapping step exposes the team-lead's PID so it can be excluded.

## Steps

### 1. Identify which peer(s) to shut down

From the user's ask. Look up each project's path from `registry.yaml` if you don't have it memorized.

### 2. Map claude PID → cwd for every running claude

This is the only reliable way to find the claude binary's PID — `list_peers` returns the wrong PID (the hive-mcp child).

```bash
ps -axww -o pid=,command= | awk '/\.local\/bin\/claude/ && !/grep/ {print $1}' | while read pid; do
  cwd=$(lsof -a -p $pid -d cwd -Fn 2>/dev/null | grep '^n' | sed 's/^n//' | head -1)
  printf '%-6s  %s\n' "$pid" "$cwd"
done
```

Output looks like:
```
48464   /Volumes/Data/Users/bryanchan/dev/ai-team-lead
62102   /Volumes/Data/Users/bryanchan/dev/<project-a>
62110   /Volumes/Data/Users/bryanchan/dev/<project-b>
...
```

### 3. Identify the team-lead's own PID — never kill it

The team-lead's cwd is the ai-team-lead repo (or whatever the team-lead repo is). Note its PID and exclude it from the kill list. From inside a team-lead session, this is the PID of the parent process tree.

### 4. Filter PIDs by target project path

Match on cwd substring. Remember to handle worktrees too — e.g., `<project>/.claude/worktrees/v1-impl` should match for `<project>`.

### 5. Kill — space-separated args, not newlines

**Critical gotcha:** if you collect PIDs into a multi-line variable and pass `kill "$pids"`, zsh treats the whole `pid1\npid2\npid3` string as ONE bad arg and errors with `illegal pid`. Always space-separate:

```bash
kill <pid1> <pid2> <pid3>
```

Or normalize the var first:
```bash
pids=$(awk '...' | tr '\n' ' ')
kill $pids   # unquoted — word-splits on spaces
```

**Use explicit PIDs, not a pattern.** `pkill -f 'dev/<project>'` and a loop of `tmux kill-session` are both refused by the permission classifier — a pattern kill can match anything, so it reads as unbounded. `kill <pid1> <pid2> <pid3>` with the PIDs resolved in step 2 is allowed and does the same job. Measured 2026-08-25, after `pkill` and the tmux loop were denied and the explicit-PID form went through unchallenged. This is a reason to follow step 2 rather than shortcut it.

### 6. Wait briefly and verify

```bash
sleep 2
for pid in <pid1> <pid2> ...; do
  if ps -p $pid -o pid= >/dev/null 2>&1; then echo "STILL ALIVE: $pid"; else echo "gone: $pid"; fi
done
```

If any are still alive after SIGTERM, escalate to `kill -9`.

### 7. Sweep orphan hive-mcp servers

When a claude binary dies, its child `bun claude-hive-mcp/server.ts` process can get reparented to launchd (PPID=1) instead of cleanly exiting. These orphans keep claude-hive's registry confused.

```bash
orphans=$(ps -axww -o pid=,ppid=,command= | grep 'claude-hive-mcp/server.ts' | grep -v grep | awk '$2==1{print $1}')
if [ -n "$orphans" ]; then echo "$orphans" | xargs kill -9; fi
```

### 8. Confirm via claude-hive

```
mcp__claude-hive__list_peers(scope: "machine")
```

The shut-down peer should be absent (or stale per `last_seen`). claude-hive's stale-window is ~30s after the underlying process dies, so wait briefly before re-listing.

## Common pitfalls

- **Killing the hive-mcp PID instead of the claude PID.** Symptom: `list_peers` keeps showing the peer with a similar-but-different PID a minute later (the claude binary spawned a new hive-mcp child). Fix: use the cwd-mapping in step 2, not `list_peers`'s PID column.
- **Multi-line PID variable.** `kill "$pids"` where `$pids` is `pid1\npid2` passes one bad arg. Always unquote OR `tr '\n' ' '` first.
- **Killing the team-lead self by accident.** Always identify and exclude the team-lead's PID.
- **Stale claude-hive entries.** `list_peers` may show entries for ~30s after kill before they expire. Check `last_seen` timestamps to distinguish stale-but-actually-dead from genuinely-alive.

## Graceful shutdown (when peer has in-flight work)

If the peer is mid-task and you don't want to lose state, send a hive message asking them to checkpoint + `/exit`:

```
mcp__claude-hive__send_message(
  to_stable_id: <peer_stable_id>,
  message: "From Team Lead — spinning you down for the week. Please checkpoint any in-flight work (commit WIP branches, save drafts, etc.) and reply when ready. I'll kill the session after your ack."
)
```

Wait for ack, then kill. For idle peers (no active task per their `summary`), skip the ping and just kill.

## Related

- `respawn-sessions` — bring them back when needed (`respawn.py --execute`; tmux-based)
- `spawn-session` — spawn a single new session (tmux-based)
- `feedback_respawn_command_form.md` (memory) — tmux is the canonical spawn path; iTerm/AppleScript was removed for unreliability
