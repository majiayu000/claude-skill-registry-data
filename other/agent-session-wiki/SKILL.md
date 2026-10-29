---
name: agent-session-wiki
description: Operate the cross-machine agent-session archive (prateek/wiki-agent-sessions) — find past sessions from any host, run or troubleshoot the hourly sync launch agent and daily wiki-ingest Orca automation, check fleet health, and migrate the ingest role. Use when asked to find a session from another machine, check why session sync is failing or stale, review SKIPPED.md quarantines, wire agentsview to the archive, or ingest archived sessions into the wiki.
---

# Agent Session Wiki

Use this playbook to search, operate, and troubleshoot the cross-machine
archive. Each machine mirrors its raw sessions hourly to
`~/code/github.com/prateek/wiki-agent-sessions` and pushes them under
`sessions/<host>/...` in their native layouts. One designated host ingests the
archive into `wiki/` each day.

Personal and homelab machines hold the full archive. Work machines use a
sparse, blobless clone containing their own `sessions/<alias>/`, `health/`,
and agent config directories. Work clones omit other hosts' transcripts and
the distilled `wiki/`; they still push their own sessions in full. The
repository `AGENTS.md` defines its layout, ownership, clone shapes, consumer
matrix, automation definitions, and expected hosts. The repository's
`session-sync` skill is the automation's failure playbook.

## Find sessions

Choose the source that matches the session format and search goal:

- **QMD** searches indexed archive text quickly. Setup creates the named
  `wiki-agent-sessions` lexical index, and each successful hourly sync updates
  it. Search without embedding or model downloads:

  ```sh
  qmd --index wiki-agent-sessions search '"Roux Home"' -c agent-session-history -n 10
  qmd --index wiki-agent-sessions get '#<docid>:<line>:<count>'
  ```

  The index contains main Claude transcripts and history, Claude memories, pi
  sessions, cursor agent transcripts, and the distilled wiki. It omits
  subagent transcripts, cursor databases, and raw Codex rollouts. Use
  agentsview for Codex. Keeping these out makes the lexical index useful and
  bounded instead of duplicating large tool and image payloads.
- **agentsview** searches Claude, Codex, and cursor `projects/` data. The
  dotfiles-managed `~/.agentsview/config.toml` generates `[[session_sources]]`
  entries for each other host in the clone and labels them by machine. Browse
  in the UI or run `agentsview session list --format json`, then filter by
  `machine`. A new host appears after the next sync or `chezmoi apply`; both
  regenerate entries and restart the daemon. Cross-host entries exist only on
  full-clone hosts. Work clones contain only their own sessions and no `wiki/`,
  so use a full-clone host for cross-host lookups.
- **obsidian-wiki** builds a topic-search index for one host directory:

  ```sh
  obsidian-wiki sessions-build --claude-dir ~/code/github.com/prateek/wiki-agent-sessions/sessions/<host>/claude
  obsidian-wiki sessions-query "that auth bug with the retry loop"
  ```
- **pi sessions** are available in the archive and wiki, with no agentsview
  parser. Search `sessions/<host>/pi/sessions/` with `grep`, or ingest using
  `PI_HISTORY_PATH`.
- **cursor database snapshots** are retained as raw data. Open
  `chats/store.db` with `sqlite3` when needed.

## Ingest sessions manually

The daily automation ingests sessions on the designated host. To ingest one
host manually, run this from the archive clone:

```sh
cd ~/code/github.com/prateek/wiki-agent-sessions
.agents/skills/session-sync/scripts/with-repo-lock zsh -c '
  CLAUDE_HISTORY_PATH=$PWD/sessions/<host>/claude claude -p "/wiki-history-ingest claude"'
```

Commit only `wiki/` paths and include the archive HEAD SHA in the commit
message. The manifest in `wiki/` deduplicates sources already ingested.

## Check archive and automation health

Start with local run state at
`${XDG_STATE_HOME:-~/.local/state}/wiki-agent-sessions/latest.json`. It records
the phase, exit code, and next step; timestamped logs are beside it. Then
inspect the relevant signal:

- **Host sync:** each host updates `health/<host>.json` during sync, at least
  every ~20 hours. The daily ingest fails loudly when an expected host's
  heartbeat is older than 26 hours. On the ingest host, inspect
  `orca automations runs`.
- **Wiki freshness:** each sync warns to stdout and `latest.json` when the
  newest `wiki/` commit is older than 48 hours. This is a second signal for a
  stalled ingest host.
- **Hourly sync launch agent:** inspect
  `launchctl print gui/$(id -u)/com.prateek.wiki-sessions-sync`. Its log is
  `~/.local/state/dotfiles/wiki-sessions-sync/sync.log`. The Raycast
  "Launchd Monitor" extension watches the same label.
- **Ingest automation:** list with `orca automations list --json`; inspect run
  history with `orca automations runs --id <id> --json`.
- **Clone shape:** run
  `scripts/agent-sessions/reconcile-wiki-clone --check ...` from dotfiles.
  Check mode reports cone, `blob:none` filter, and stray paths outside the
  cone without changing them. The apply-time verify step runs the same check.
  Without `--check`, the command repairs drift. The bootstrap script invokes
  repair only when machine, clone, app, wrapper, QMD, launchd, or agentsview
  inputs change.

## Troubleshoot sync and clone failures

| Signal | Cause and next action |
|---|---|
| Sync exit 3 | The host alias is missing. `chezmoi apply` renders `~/.config/wiki-agent-sessions/config.toml` from `wiki_host_alias` in machines.toml. |
| Sync exit 4 | Dirty paths exist outside this host's archive. Treat them as someone's WIP; never reset them. Resolve by hand. |
| Sync exit 5 | Push failed three times. The next hourly run retries; if failures persist, check SSH and network in the log. |
| Sync exit 6 | Rebase conflict. Per-host paths make this unlikely; suspect two machines share an alias. The machines.toml uniqueness test guards against that. |
| Sync exit 7 | Raw sync and push succeeded, but the derived QMD index is stale. Inspect the launchd log, verify `qmd --version`, then run `qmd --index wiki-agent-sessions update`. |
| Exit 75 | A live sync or ingest holds the repo lock. Wait for it to finish. |
| No new log entries at the top of the hour | Check `launchctl print gui/$(id -u)/com.prateek.wiki-sessions-sync`. If it is not loaded, bootstrap it with `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.prateek.wiki-sessions-sync.plist`. |
| New host absent from agentsview | Restart with `agentsview serve --background --replace`, or wait for the next sync/apply. Entries regenerate from the clone glob. |
| `SKIPPED.md` grew | Sources over 90 MB or otherwise quarantined were skipped. Review whether to split or ignore them. |
| Ingest automation unregistered | On a fresh ingest host, or when Orca was installed later, run `~/dotfiles/scripts/agent-sessions/register-wiki-automations --enable --ingest`. The run_onchange script does not refire on its own. |
| `sessions/` contains only this host | This is expected on a sparse work clone. Other hosts live on GitHub and full-clone machines. |
| Apply says the ingest owner resolves `agent_session_wiki_sparse` | Ingest reads every host. Move `agent_session_wiki_ingest` to a full-clone host's layer. |
| Ingest audit says the clone is sparse | Widen the ingest host clone, then run `chezmoi apply` or `reconcile-wiki-clone ... --full`. |
| `reconcile-wiki-clone` exits 5 | The helper refused to change the clone because of local changes outside the cone, an active Git operation, or a remote without partial-clone support. Read its output, resolve the condition by hand, and rerun the printed command. |
| Apply warns that the repo is locked (exit 75) | A sync or ingest holds the lock. Clone shape was left alone; rerun the printed command later. |
| Work-machine agentsview still shows other hosts | It was indexed before the clone became sparse. `agentsview prune` cannot target one machine. Stop the daemon, then in `~/.agentsview/sessions.db` run the cleanup below, vacuum, and restart the daemon. |

For the agentsview cleanup, enable foreign keys and delete the machine's rows
from all three tables so cascades and FTS triggers run:

```sql
PRAGMA foreign_keys=ON;
DELETE FROM sessions WHERE machine='<alias>';
DELETE FROM project_identity_observations WHERE machine='<alias>';
DELETE FROM worktree_project_mappings WHERE machine='<alias>';
VACUUM;
```

Restart with `agentsview serve --background --replace`.

## Onboard a machine

1. Add `wiki_host_alias = "<alias>"` under the machine's
   `[machines.host.<hostname>]` layer in machines.toml. The alias must be
   unique and non-empty; `just test-python -p test_machines.py` checks both.
   The machine type must set `agent_session_wiki = true`.
2. Run `chezmoi apply` on that machine. It clones the repo in the machine
   type's shape (sparse for work), renders the alias and named QMD configs,
   builds the lexical index, loads the hourly sync launch agent, and wires
   agentsview.
3. After the first successful sync, add the alias to `health/expected-hosts`
   in the wiki repo so the daily audit covers the machine.

## Move the ingest role

1. Move `agent_session_wiki_ingest = true` to the new host's
   `[machines.host.*]` layer in machines.toml. Exactly one host may own it;
   `just test-python -p test_machines.py` enforces this. The new host needs the
   full archive, not `agent_session_wiki_sparse`; bootstrap refuses a sparse
   ingest host.
2. Run `chezmoi apply` on both hosts. The old host disables its ingest
   automation, and the new host registers it.
3. Expect some delta re-ingest: obsidian-wiki's manifest keys sources by
   absolute path. Identical clone paths and `$HOME` minimize the delta, while
   manifest-tracked pages deduplicate by page identity.

## Ownership boundaries

- Never write to another host's `sessions/<host>/` or `health/<host>.json`;
  each host owns only its own.
- Never edit `~/.agentsview/config.toml` repo entries by hand. The modify
  template and sync script own them.
- Keep `wiki-agent-sessions` lexical: do not run `qmd embed`; the managed index
  and hourly wrapper use `qmd update` only.
- The `obsidian-wiki@prateek-local` plugin ships disabled. Repositories opt in
  through `.claude/settings.json` or `.codex/config.toml`. Never run global
  `obsidian-wiki setup`: it writes skills into `~/.claude/skills` and
  `~/.agents/skills`, which the dotfiles plugin architecture forbids.
