---
name: SSH Exec
description: Run shell commands on remote hosts via SSH, and transfer files via SCP. Allowlist-gated.
requires:
  bins:
    - ssh
    - scp
  env:
    - SSH_EXEC_ALLOWED_HOSTS
---

# SSH Exec

Execute commands on remote Linux hosts through the system `ssh` client. Uses
key-based auth only (`BatchMode=yes` — no interactive password prompts). Hosts
must be explicitly allowlisted.

## Use when

- "Restart nginx on `prod01`"
- "Tail `/var/log/syslog` on `home-server`"
- Pushing / pulling a file to/from a known host
- Kate driving ops on other machines you administer

## Do not use when

- Persistent interactive sessions — use `tmux-remote`
- Containers on *this* host — use `docker-api`
- Arbitrary / untrusted hosts — allowlist is mandatory

## Tools

- `status` — allowlist + bin versions
- `exec` — `host`, `command`; optional `timeout_secs` (default 30, max 600), `identity_file`
- `scp_upload` — `host`, `local_path`, `remote_path`
- `scp_download` — `host`, `remote_path`, `local_path`

## Env

| Var | Required | Notes |
|-----|----------|-------|
| `SSH_EXEC_ALLOWED_HOSTS` | yes | comma-separated `user@host` or `~/.ssh/config` alias |
| `SSH_EXEC_ALLOW_WRITES` | for `scp_upload` | must be `"true"` |
| `SSH_EXEC_TIMEOUT_SECS` | no | default 30 |
| `SSH_BIN` / `SCP_BIN` | no | override binaries |

## Safety

- Non-allowlisted host → `-32041 host not allowed`
- `StrictHostKeyChecking=accept-new` — first connect auto-adds host key; subsequent changes fail
- `BatchMode=yes` — password-protected keys without agent will fail. Use `ssh-agent` or unencrypted deploy keys
- Writes gated: upload requires `SSH_EXEC_ALLOW_WRITES=true`. Download is read-only, ungated
- `stdout` truncated at 16 KB, `stderr` at 8 KB
