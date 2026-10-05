---
name: tmux-orphaned-socket
description: Diagnose and recover from "error connecting to /tmp/tmux-*/default (No such file or directory)" when tmux ls or attach fails but sessions were working before. Use when a tmux socket has gone missing, especially after any /tmp cleanup, disk-space sweep, or agent-run cleanup script — never assume the sessions are lost before checking.
---

# Tmux Orphaned Socket

`tmux ls` failing with `error connecting to /tmp/tmux-<uid>/default (No such file or directory)`
does not mean the sessions are gone. A running tmux server keeps its windows alive in memory
even after its own socket file is deleted out from under it — deleting a Unix domain socket
file doesn't touch the process holding it open, it only blocks *new* connections. This is the
usual outcome of a `/tmp` cleanup (a cron sweep, an agent-run script, a manual `rm -rf /tmp/*`)
that didn't exclude `/tmp/tmux-*`.

## Diagnose, don't assume

1. Confirm the socket is actually missing, not just misnamed:
   `ls -la /tmp/tmux-$(id -u)/` — expect it empty, not absent: tmux itself recreates
   `/tmp/tmux-<uid>` (mode 0700) on its own next invocation, including the `tmux ls`/`attach`
   that surfaced the error, so by the time you're reading this the directory almost always
   exists again — an "absent" directory is essentially unreachable once any tmux command has
   run as that uid. `pam_systemd` creates `/run/user/<uid>`, not this directory, and
   `systemd-tmpfiles` manages `/tmp` broadly rather than per-uid tmux dirs specifically, so
   don't attribute the recreation to either of them.
2. Check whether the server process is still alive, and identify the server specifically —
   `ps aux | grep '[t]mux'` lists clients and the server indistinguishably:
   `ps -eo pid,ppid,cmd | grep '[t]mux'` and look for the process with no controlling terminal
   (`?` in a `ps -eo pid,tty,cmd` listing), often shown as `tmux: server`; exact presentation is
   tmux-version- and platform-dependent, so treat this as a strong hint, not a guarantee. Cross-
   check by connecting once (`tmux ls`) and then finding who holds the socket:
   `lsof /tmp/tmux-$(id -u)/default` or `fuser -v /tmp/tmux-$(id -u)/default`.
3. Check when the socket directory was recreated, to date the event:
   `stat /tmp/tmux-$(id -u)` — a `Birth` timestamp much later than the server's start time means
   the directory was deleted and silently recreated. `Birth` isn't always available (tmpfs and
   some filesystems omit it and print `-`); when it's missing, fall back to `stat -c '%Y'`
   (mtime) or the server's own start time (`ps -o lstart= -p <server-pid>`) for the same
   comparison.
4. Confirm live windows/panes under the orphaned server before deciding anything:
   `pstree -p <server-pid>` and `ps --ppid <server-pid>`. All panes under a surviving server
   process keep running regardless of whether their client is currently attached or detached —
   survival depends on the server process, not on client attachment. An already-attached
   client's terminal also stays usable, since its connection was established before the socket
   vanished; a detached session is not at any extra risk and should be checked with the same
   care as an attached one.
5. Rule out the routine suspects before blaming an ad hoc script: check whether
   `systemd-tmpfiles-clean.timer` actually ages `/tmp` with `systemd-tmpfiles --cat-config`
   (merges `/usr/lib/tmpfiles.d`, `/etc/tmpfiles.d`, and `/run/tmpfiles.d` in override order —
   checking only the vendor file under `/usr/lib/tmpfiles.d/tmp.conf` can miss an `/etc`
   override) — a bare `-` age field in the effective config means aging is disabled — and
   whether a known cleanup cron's schedule lines up with the timestamp from step 3.

## Recovery is a trade-off, not a fix

There is no way to make a running tmux server re-bind a socket that was deleted while it was
alive — stock tmux has no "recreate my socket" or "adopt an orphaned server" command. The
choice is:

- **Leave it running.** Already-attached panes keep working exactly as before. You lose the
  ability to `tmux ls`, attach a new client, or open new windows on that server — but nothing
  currently running is interrupted. Right default whenever any pane holds work you can't easily
  reproduce (an active agent session, a long build, an SSH tunnel).
- **Kill and restart.** Only way to regain `tmux ls`/attach/new-window. Kills every window on
  that server, including ones you didn't check. Never do this without first walking through the
  diagnosis steps above and confirming with whoever depends on those panes.

Default to leaving it running and reporting what's alive, unless the user has already confirmed
losing those panes is fine.

## Prevention

Any cleanup routine that touches `/tmp` broadly — cron job, agent-run script, disk-space
recovery — must exclude `/tmp/tmux-*` (and other live-process sockets: `/tmp/ssh-*`,
`/tmp/.X11-unix`, `/tmp/.ICE-unix`, etc.). A directory holding a live process's control socket
is not stale just because its files look old; staleness has to be judged by whether the owning
process still exists, not by file age alone.
