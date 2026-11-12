---
name: thrum
description:
  "Multi-agent coordination via messaging, groups, and shared context. Use when
  agents need to communicate, delegate work, or coordinate across worktrees."
# source: claude-plugin/skills/thrum/SKILL.md
---

## Thrum - Git-Backed Multi-Agent Coordination (Messaging, Groups, Shared Context)

Run `thrum prime` for full session context (auto-injected by the SessionStart
hook; also fires on post-compact resume). PreCompact is not registered — use
`$thrum:thrum-compact` to save a snapshot before deliberately compacting.

If the prime output was truncated, run `thrum prime --to-file` (if --to-file is
an unknown flag, run plain `thrum prime` once and read its output fully) ONCE
and read that file page by page; never re-run `thrum prime` to page through it.

### Quick Command Reference

#### Messaging

```bash
thrum send --to @name --body-file msg.md           # Direct message (body from file)
thrum send --to @name1 --to @name2 --body-file msg.md   # Multiple explicit recipients (repeatable --to)
thrum reply <msg-id> --body-file reply.md          # Reply (same audience; NO --to — recipient comes from the message)
thrum inbox                              List messages (never marks them read)
thrum inbox --unread                     Unread only (never marks them read)
thrum message search "<term>"            Pro: full-text search — use instead of paging; stale unread sorts last (Free: thrum inbox --unread --from @<sender>)
thrum sent                               List messages you sent
thrum sent --unread                      Sent messages with unread recipients
thrum message read --all --force         Mark ALL unread as read (run `read --all` alone first — dry run)
thrum wait                               Block until message arrives (30s timeout)
thrum wait --timeout 120s                Custom timeout (duration)
```

**No reply to a pure acknowledgement.** Do not reply to a message that only
thanks, acknowledges, confirms receipt or signs off ("thanks", "ok", "got it",
"acknowledged", an emoji): mark it read with `thrum message read <id>`. Reply
only when it asks a question, gives a task, reports a result you must act on, or
you have new information. A dispatch the sender is waiting on still gets its
status reply.

One-to-many fan-out (`--broadcast`, `@everyone`, role-based mentions/groups) was
removed by design (P0 ruling); do not restore it. Name every recipient
explicitly with repeatable `--to @name`, or address a scoped agent-type group.

#### Agents

```bash
thrum quickstart --name <agent-name> --role R --module M --intent "..."   Register + start session
thrum worktree create <name> --name <agent> --role R --module M    Create worktree + register agent
                                                                   (then run `thrum tmux launch <name>` to start runtime)
thrum worktree setup <name> --name <agent> --role R --module M     Alias for worktree create
thrum whoami                                          Show identity
thrum team                                            List active agents
thrum ping @name                                      Check if agent online
thrum who-has <file>                                  Who's editing a file
```

#### Role Templates

```bash
thrum roles list                         List templates + matching agents
thrum roles deploy                       Re-render preambles from templates
thrum roles deploy --agent foo           Deploy for specific agent
thrum roles deploy --dry-run             Preview without writing
```

#### Sessions & Context

```bash
thrum session start                      Start session
thrum session end                        End session
thrum session set-intent "..."           Update work description
thrum state set --kind <k> --scope <s> --value '<json>'   Upsert your personal state
thrum state list                         List your state entries
thrum queue list [--assigned <agent>]    List your committed-work bundles (rows show assignees; --assigned filters)
thrum overview                           Combined status + team + inbox
$thrum:thrum-update-project                    Guided project state update (only the coordinator responsible for this repo's project state)
$thrum:thrum-load-context                      Restore session after compaction (runs thrum prime)
```

#### Tmux Sessions (Recommended)

```bash
thrum tmux start                     Launch agent session (create+launch+prime+attach)
thrum tmux status                    Show managed sessions with state
thrum tmux connect                   Attach to running session (interactive picker)
thrum tmux restart <name>            Restart session with context snapshot
thrum tmux kill <name>               Tear down session
thrum tmux create <session> --name <n> --role <r> --module <m> --cwd <path>   Create + register agent
thrum tmux quickstart <session> --name <n> --role <r> --module <m> --cwd <path>   Alias for tmux create
thrum tmux launch <session> [--runtime <r>]   Start runtime in session (REQUIRED after `tmux create`)
```

#### Monitor Jobs

Load the `thrum:using-monitors` skill before you start, change or stop a
monitor.

```bash
thrum monitor start --name <n> --match <re> --to @agent [--schedule "<cron>"] [--notify-on-success] -- <cmd> [args...]
thrum monitor list [--all]           List monitor jobs (running; --all adds stopped)
thrum monitor show <name>            Show job details
thrum monitor logs <name>            Recent matched lines
thrum monitor update <name>          Change match, schedule, target or debounce in place
thrum monitor stop <name>            Stop a monitor job
thrum monitor delete <name>          Remove a job and free its name
thrum monitor restart <name>         Restart a stopped job
```

Reminders, periodic script checks and delivery verification: see the
`using-monitors` skill.

#### Daemon & Sync

```bash
thrum daemon start                       Start daemon
thrum daemon stop                        Stop daemon
thrum daemon status                      Daemon health
thrum sync force                         Force immediate sync
thrum sync status                        Sync state
```

#### Utility

```bash
thrum init                               Initialize thrum in repo (also starts the daemon)
thrum prime                              Full session context
thrum prime --json                       Machine-readable output
thrum <cmd> --help                       Detailed command usage
```

### When to Use Thrum

| Thrum                                    | TaskList/SendMessage       | Neither                       |
| ---------------------------------------- | -------------------------- | ----------------------------- |
| Cross-worktree messaging                 | Same-session task tracking | Single-agent, no coordination |
| Persistent messages (survive compaction) | Ephemeral task lists       | Temporary scratch notes       |
| Non-tmux listener fallback               | Inline progress tracking   | Simple linear execution       |
| Multi-machine sync via git               | Local to conversation      | No persistence needed         |

**Decision test:** "Do messages need to survive session restart or reach agents
in other worktrees?" YES = Thrum.

**Thrum + TaskList coexist:** Use TaskList for immediate session work. Use Thrum
for cross-session/cross-worktree coordination messages.

### Message Delivery

#### Tmux Sessions (Recommended)

When running in a tmux-managed session, messages are delivered directly to your
pane via daemon nudge — zero token cost, no background sub-agent needed. See
[TMUX_SESSIONS.md](resources/TMUX_SESSIONS.md). Check `thrum inbox --unread` at
natural breakpoints; never spawn a background listener.

#### Listener Pattern (Fallback)

Use the background message listener only when tmux pane delivery is unavailable.
It calls `thrum wait` (blocking) and returns when messages arrive. See
[LISTENER_PATTERN.md](resources/LISTENER_PATTERN.md).

#### Context Management

- `thrum prime` gathers identity, team, inbox, git context, sync health
- SessionStart hook auto-runs `thrum prime` on session start (including
  post-compact resume)
- PreCompact is NOT registered — run `$thrum:thrum-compact` to save a restart
  snapshot deliberately before compacting
- **After compaction:** resume from the Resume Plan in the injected
  `# Previous Session Context`; check your personal state with
  `thrum state list` and your committed work with `thrum queue list`
- Agent identity persists across sessions; read it with `thrum whoami`, never by
  opening the file

### Resources

| Resource                                             | Content                                      |
| ---------------------------------------------------- | -------------------------------------------- |
| [TMUX_SESSIONS.md](resources/TMUX_SESSIONS.md)       | Tmux-managed session setup and commands      |
| [BOUNDARIES.md](resources/BOUNDARIES.md)             | Thrum vs TaskList/SendMessage decision guide |
| [MESSAGING.md](resources/MESSAGING.md)               | Protocol patterns, context management        |
| [ANTI_PATTERNS.md](resources/ANTI_PATTERNS.md)       | Common mistakes and how to avoid them        |
| [LISTENER_PATTERN.md](resources/LISTENER_PATTERN.md) | Background message listener template         |
| [CLI_REFERENCE.md](resources/CLI_REFERENCE.md)       | Complete command syntax reference            |
| [IDENTITY.md](resources/IDENTITY.md)                 | Agent identity and multi-worktree patterns   |
| [WORKTREES.md](resources/WORKTREES.md)               | Multi-worktree coordination                  |

Run `thrum <command> --help` for any command's full usage.
