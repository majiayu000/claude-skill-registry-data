---
name: paseo-profiles
description: Copy paseo agent profiles (Architect, Engineer, Reviewer, Writer…) from one machine to another by merging them into the target's ~/.paseo/config.json, over ssh, idempotently. Use when the user wants to export/import/sync/clone paseo agent profiles between hosts, set up paseo agent profiles on a new or freshly installed machine, or roll the same profile set across a fleet. paseo itself has no profile export/import command — `paseo agent` manages running agents, not profile templates.
---

# paseo-profiles

Move **agent profiles** — the templates that pair a name, provider, model, mode, and thinking level
(“Software Engineer” = claude / claude-opus-5 / bypassPermissions / xhigh) — between machines.

paseo has no command for this. The profiles are a JSON array at `daemon.agentProfiles` in
`~/.paseo/config.json`, authored by hand in a paseo client UI (desktop, mobile, or the daemon's
own web UI) and reachable from no CLI.

## Why not just scp config.json

That same file holds **host-specific** settings: `daemon.listen`, `daemon.relay.enabled`,
`daemon.cors`, and any password hash written by `paseo daemon set-password`. Copying the file
wholesale flips those on the target. `~/.paseo/server-id`, `cli-client-id` and `daemon-keypair.json`
are per-host identity and must never be copied either. So this is a **key-scoped merge**, not a file copy.

## Usage

One command does the whole round trip:

```bash
~/.claude/skills/paseo-profiles/scripts/paseo-profiles.py push dev-server-frank-lume
```

Multiple hosts are just more arguments; one host failing doesn't abort the rest.

```bash
paseo-profiles.py push host-a host-b host-c --dry-run   # report only, write nothing
```

Always offer `--dry-run` first when the target already has profiles of its own.

The halves are also usable separately, for an air-gapped or reviewed transfer:

```bash
paseo-profiles.py export -o profiles.json     # on the source
paseo-profiles.py import profiles.json        # on the target (also reads stdin)
```

Other flags: `--config PATH` (default `~/.paseo/config.json`), `--no-reload`.
`paseo-profiles.py selftest` checks the merge logic.

## What it carries

| Key path | How |
|---|---|
| `daemon.agentProfiles` | merged element-wise |
| `daemon.mcp.injectIntoAgents` | scalar overwrite |
| `daemon.browserTools.enabled` | scalar overwrite |
| `agents.providers.omp.enabled` | scalar overwrite |

Every other key in the target is read, left alone, and written back verbatim.

## Merge rules

Per incoming profile: **id match** → replace in place; else **name match** under a different id →
replace that slot, incoming id wins (importing “Software Engineer” must not leave two of them); else
**append**. Profiles only the target has are never deleted. Re-running is a no-op — it prints
`no changes` and skips the write and reload entirely.

## Reference

[`references/config-and-merge.md`](references/config-and-merge.md) covers the profile fields on
disk, the export envelope and its versioning, how each incoming profile resolves, the atomic write,
and how the reload report is read. Reach for it when a merge did something unexpected, when adding
a key to the synced set, when changing the envelope version, or when a reload reports a path back.

## Safety

Backs up to `config.json.bak-<UTC>` before the first write, writes via a temp file at mode `0600`
then `os.replace` (atomic; the file holds secrets on some hosts). A missing target config is created
rather than treated as an error.

## Gotchas

- **`paseo` is not on the non-interactive ssh PATH on every host.** `ssh host 'paseo …'` can fail
  with *not found* while `ssh host 'zsh -lc paseo'` works. Use an absolute path —
  `~/.local/share/mise/shims/paseo` on hosts running the npm CLI, `/opt/homebrew/bin/paseo` on any
  still on Paseo.app. The script resolves this itself, in that order.
- **A stopped daemon is fine.** Reload is best-effort; a stopped daemon reads the config at next
  start, and the script says so instead of failing.
- After writing, it reads `paseo daemon reload --json` and reports honestly — including when the
  edit will be ignored because a launch-time flag outranks the file. See the reference.
- Profiles land regardless of whether the target has that provider installed. A Codex profile on a
  host without Codex shows as unavailable — a gap on that host, not a transfer failure.
- `push` stages the script at `/tmp/paseo-profiles-$(id -u).py` on the remote and runs it with
  `python3`, so the target needs python3 on its ssh PATH (macOS with CLT or mise: yes).
