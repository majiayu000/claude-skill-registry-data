---
name: using-tmux-ssh
description: "Use when about to ssh to a host, run a command on a VM or remote box, start a long test or build on another machine, inspect a remote log, or recover after an ssh connection dropped or a remote command timed out. Use tmux-ssh for remote commands, saved-watch resume, and concurrent observation."
---

# Running Remote Commands With tmux-ssh

`tmux-ssh` drives one persistent SSH login per host in a local tmux pane.
Use it for every command on another machine or VM, short or long, including
remote tests, builds, and log reads. Use `--read` and `--status` to observe;
never use plain SSH polling or Monitor loops.

## Resolve the bundled executable

Resolve `resources/tmux-ssh` relative to the active `using-tmux-ssh` skill
folder supplied by your runtime. Set `TMUX_SSH` to that absolute executable
path, then read its live help:

```bash
TMUX_SSH='/absolute/path/to/using-tmux-ssh/resources/tmux-ssh'
"$TMUX_SSH" --help
```

The runtime's loaded plugin root contains
`skills/using-tmux-ssh/resources/tmux-ssh` for Claude, Codex, Cursor, and Muse;
OpenCode contains `assets/skills/using-tmux-ssh/resources/tmux-ssh`. Locate the
root from the active skill's path rather than assuming plugin root environment
variables are set in an interactive shell. Nothing else from Thrum is
required; local `tmux` and `ssh` must be installed.

## Usage

The examples below invoke the resolved executable through `"$TMUX_SSH"`. `HOST` is an
SSH config alias or `user@host`.

```bash
"$TMUX_SSH" HOST                                  # connect if needed; print status
"$TMUX_SSH" HOST 'uname -a'                        # finite command; return its exit code
"$TMUX_SSH" HOST --timeout 900 'make test'          # bounded observation, in seconds
"$TMUX_SSH" HOST --resume --timeout 900            # continue the saved watch; never resend
"$TMUX_SSH" HOST --status                          # session and recorded state
"$TMUX_SSH" HOST --read --settle                    # screen; usable during another call
"$TMUX_SSH" HOST --abort                           # deliberately interrupt and clear the watch
"$TMUX_SSH" HOST --kill                            # close SSH and clear saved state

"$TMUX_SSH" HOST --send 'top'                      # interactive program
"$TMUX_SSH" HOST --read
"$TMUX_SSH" HOST --send --key C-c

"$TMUX_SSH" HOST "tmux new -d -s JOB 'long-command >job.log 2>&1'"
```

Run mode waits for a command that ends. For editors, REPLs, attached tmux,
and other programs that stay open, use `--send`/`--read`. Run mode refuses
obvious interactive commands with code 2; use `--force-run` only deliberately.
`--send` types into the current program and refuses a dead session rather
than reconnecting and losing interactive state.

Quote remote commands locally so variables expand on the intended machine.
They execute in the remote login shell, which may be zsh; invoke `bash` for
Bash syntax. For long or complex content, transfer a script using `scp` or
`rsync` with the same connection options, then run a short command through
`tmux-ssh`. The wrapper transports commands, not files.

## Rules

- **One command per host session.** Mutating calls share a local per-host lock
  and wait up to 30 seconds by default. `--read` and `--status` observe without
  that lock. Coordinate drivers across machines or different `TMUX_SSH_DIR`
  values; these do not provide a global lock.
- **One local tmux session per `TMUX_SSH_DIR`.** The session is named
  `ts_<host>_<8 hex of a hash of the canonical TMUX_SSH_DIR>` on tmux socket
  `tmux-ssh`, so drivers with different state dirs never share, reuse, or kill
  each other's session. The session records its dir in the tmux option
  `@tmux_ssh_dir` (tmux >= 2.9 is required for these options; older tmux is
  refused with a clear error before any session is touched). Every verb that
  touches a session (`--attach`, `--status`, `--read`, `--send`, `--resume`,
  run/ensure, `--kill`, `--abort`) refuses with exit 125 and changes nothing on
  a session recorded for another dir; the message names both dirs. A dir with
  no session of its own is never refused for clearing its own stale watch or
  input guard with `--kill`/`--abort`. A pre-upgrade session named plain
  `ts_<host>` is adopted only by a dir whose saved state names it; each adopter
  is recorded in `@tmux_ssh_dirs`, and if more than one dir has adopted it the
  session is ambiguous: `--kill`, `--abort` and the typing verbs refuse for all
  of them (`--status`, `--read`, `--attach` still work). Confirm which dir owns
  the running command, then kill that tmux session by hand
  (`tmux -L tmux-ssh kill-session -t =NAME`) or let the command end. The first
  adopter cannot see a sibling that has not yet touched the session. Run from the
  owning `TMUX_SSH_DIR`, or kill by hand as above.
- **Resume observation, never resubmit a queued or visible command.** Code 124
  ends the wait; the command may still be running or waiting for input. Use
  `--read`, then `--resume`, which retains the watch and never sends the command
  again. Resume reuses the original timeout unless overridden. Other run calls
  refuse while a watch remains.
- **Interrupt deliberately.** `--interrupt-on-timeout` sends Ctrl-C when the
  wait expires. `--abort` sends Ctrl-C and clears the watch; code 0 reports a
  ready/finished/gone session, code 1 means the shell did not answer. Inspect
  `--read` before further input. An abort receipt does not prove job success.
- **Give long jobs an independent remote lifecycle.** Use detached remote
  tmux, retaining the job name and logs. An ordinary call can reconnect a dead
  SSH session, but a drop during foreground execution leaves completion unknown
  and may terminate that command. Check the job and its results before deciding
  to retry. `--kill` closes SSH; it does not stop an independent remote job.
- **Interpret the diagnostic and completion evidence.** Remote command exit
  codes are passed through and can overlap wrapper codes. Wrapper code 124 is
  a wait timeout; 125 is refusal or 'completion unknown', so it alone cannot
  prove nothing ran; 2 is a usage error; 3 means input state UNKNOWN after a
  failed keystroke, dropped send, or failed watch persistence. Code 3 guards
  later typing until `--kill`; `--read`, `--status`, and `--resume` still work.
  Do not blindly retry unknown completion or input, or kill another driver's
  session or lock merely because it looks stuck.

## Connection options and pool leases

Obtain the key, known-hosts file, target address, and actual remote OS hostname
from the current lease. Keep these values outside the skill.

```bash
TMUX_SSH_OPTS='-i /path/to/lease-key -o IdentitiesOnly=yes -o UserKnownHostsFile=/path/to/lease-known-hosts -o StrictHostKeyChecking=yes' \
TMUX_SSH_EXPECT_HOST='<remote-os-hostname>' \
"$TMUX_SSH" user@<lease-address> 'uname -a'
```

Host-key checking: `tmux-ssh` adds `-o StrictHostKeyChecking=accept-new` only
when `TMUX_SSH_OPTS` names no `StrictHostKeyChecking` option and `ssh -G <host>`
reports SSH's built-in default (`ask`). A value you set in `TMUX_SSH_OPTS` or in
`~/.ssh/config` (`yes`, `no`, `accept-new`) always wins, so a host alias with
`StrictHostKeyChecking yes` stays strict. If the `ssh -G` probe fails or times
out, nothing is added and SSH's own default applies. The probe is killed after
`TMUX_SSH_PROBE_TIMEOUT` seconds (default 5; a non-integer or `0` means 5).
Residual: an explicit `StrictHostKeyChecking ask` in `~/.ssh/config` looks
identical to the built-in default in `ssh -G` output, so it also gets
`accept-new`; put `-o StrictHostKeyChecking=ask` in `TMUX_SSH_OPTS` to keep it.

Options precede built-in defaults, so SSH's first `-o` wins. Allowed characters
are letters, digits, spaces, and `- _ . / = : , @ ~ + %`; paths cannot contain
spaces. A live session retains its original options: deliberately close it
with `--kill` before changing them. `--help`, `--status`, and `--kill` work
with invalid options. `--expect-host` overrides `TMUX_SSH_EXPECT_HOST` and
matches short/FQDN hostname forms case-insensitively; the SSH alias need not
match the OS hostname.

## Execution identity checks

SSH is the pane's own process; a dropped connection leaves a dead pane, not a
local shell. Run mode checks a live SSH pane, probes the recorded hostname,
and wraps execution with a hostname check. Interactive input checks the live
SSH pane because a program may own stdin. These checks catch mistaken targets;
they are not an adversarial security boundary. Remote targets reporting the
local hostname are refused; explicit `localhost`/`127.0.0.1` aliases permit
intentional local use.
