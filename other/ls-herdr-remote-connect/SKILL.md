---
name: ls-herdr-remote-connect
description: "Connect Herdr machines and SSH tunnels, deploy missing Herdr, translate master configuration, and perform idle-first upgrades and restart/reconnect workflows. Start with ls-herdr-task-routing."
metadata:
  version: "1.0"
  compatibility: "Authenticated OpenSSH routes; Linux/macOS or WSL2; official Herdr Unix binaries."
---

# Herdr remote operations

Read the master first if needed:
[ls-herdr-task-routing](localsetup://package/ls-herdr-task-routing/SKILL.md)

Inspect `localsetup herdr remote --help`. Bind one exact saved machine or user-named SSH
target and an explicit remote session. Local inherited pane IDs do not identify
remote panes.

## Connect or deploy

For an already requested deployment, the full lifecycle is one tool operation:

```bash
localsetup herdr --state-dir "$task_state" remote deploy <ssh-alias> \
  --session <remote-session> --apply
```

Use `remote upgrade` for the complete upgrade/restart/reconnect path. Omit
`--apply` or use `--dry-run` to inspect the operation without mutation. These
switches express dispatch intent; they do not grant user authority. Resolve
the alias, session, and existing absolute `task_state` from the actual task.

Resolve effective SSH settings, existing approved master connection, account,
jump hosts, remote installation owner, session, and socket. Reuse authentication
and host-key policy. Do not copy a master's socket path blindly, enable agent
forwarding globally, or silently change SSH settings to bypass authentication.

If Herdr is ready, qualify the connection and complete the requested work.
If it is missing and deployment was not requested, offer deployment once with
the exact target and the install/configure/start/connect outcome. If deployment
was requested, reuse that authority and continue. Do not add a second consent
step for each command or retry within the unchanged approved operation.

The lifecycle helper fills upstream's noninteractive setup gap with a narrow
authenticated SSH bootstrap: verified official artifact, targeted backup,
atomic activation, native server start, profile registration, and connection
verification. Do not overwrite a package-manager-owned binary or invent a
native `--yes` option. Native machine forwarding is for an already prepared
server; it does not install or restart it.

Apply the owning dependency/release verification policy for a newly selected
artifact and reuse applicable evidence. Integrity and compatibility checks run
as part of the operation; they are not extra consent prompts.

## Match the master appropriately

Translate the effective master's supported portable UI/theme and session
preferences. Keep local keybindings for remote attach unless the user requested
server keybindings. Resolve shell, working directories, and integration paths
on the target. Preserve unrelated remote configuration and validate the staged
configuration before activation.

Never copy connection profiles, credentials, arbitrary executable commands,
machine paths, experimental settings, or security settings as a convenience.
Report a required unsupported setting instead of silently claiming parity.
Named sessions share global configuration: include every affected session in
the operation's impact assessment.

## Upgrade, restart, and reconnect

Use the reviewed stable release and owning install mechanism. Preserve targeted
binary/configuration rollback before replacement. Prefer configuration reload
when sufficient; reconnecting a client is different from restarting the server.

Full server restart stops pane processes. Proceed automatically only after
idle-first checks establish it will not interrupt work. If active or unknown
work would be affected, present one concrete decision covering those sessions.
Do not enable experimental live handoff by default or promise process survival.
Verify the running endpoint after restart, not just the binary on disk.

On lost mutation responses, reconcile files, process identity, and endpoint
state read-only before any further action. Never automatically replay an
uncertain deployment, stop, or restart. For deploy/upgrade, preserve the returned `operation_id`;
its phase and recovery receipts are under the existing task state directory in
`remote-operations/<operation_id>.json`. Read that record before resuming.
Roll back a proven failed activation
within its existing authority; retain an uncertain outcome for reconciliation.

## Tunnels

Use native saved-machine forwarding where supported. For published raw API
methods without a CLI wrapper, use a task-owned SSH Unix-socket relay after
resolving the real remote socket. Custom socket overrides need explicit
resolution; Herdr has no documented socket-discovery endpoint.

Bind TCP forwarding to loopback by default. Track ownership and connection
identity, and close only owned forwarding processes. Do not terminate an
unrelated master connection, expose a listener publicly, or create a second
remote-control service.
