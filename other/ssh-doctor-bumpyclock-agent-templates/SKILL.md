---
name: ssh-doctor
description: Diagnose macOS SSH failures, Remote Login, pre-auth closes, and stale sessions.
disable-model-invocation: true
---

# SSH diagnosis

Keep diagnosis read-only unless the user requests repair.
Do not change Remote Login, restart sshd, terminate sessions, or transfer credentials during diagnosis.
Keep secrets, full environments, and unrelated configuration out of output.

## Select evidence

Compare loopback and remote behavior to locate the failure.
A loopback failure suggests sshd, launchd, or local configuration.
A remote-only failure suggests the listener, network, or firewall.
Treat these as hypotheses until evidence supports the cause.

Use only the checks needed for the current symptom:

- Remote Login status: `sudo systemsetup -getremotelogin`.
- Service status: `sudo launchctl print system/com.openssh.sshd`.
- Port listener: `sudo lsof -nP -iTCP:22 -sTCP:LISTEN`.
- Loopback reachability: `nc -vz 127.0.0.1 22`.
- Effective configuration: `sudo sshd -T`, restricted to relevant access and listener fields.
- Recent errors: targeted `log show` queries for sshd and launchd.
- Session ownership: `ps` and `lsof` for the suspected process IDs.

For a connection probe, use `RequestTTY=no` and `RemoteCommand=none`.
Use `BatchMode=yes` when an unattended password prompt could block.
Respect the user's authentication method for interactive diagnosis.

A pre-auth close with launchd error `67: Too many processes` can indicate exhausted service instances.
Check service counts and session ownership before attributing the failure to stale sessions.
Do not assume that a process owned by PID 1 is inactive.

For remote-only failures, inspect the relevant interface and firewall state.
Do not change firewall policy as a diagnostic probe.

## Repair and completion

For authorized service repair, read [repair safeguards](references/repair.md).
Report the supported cause, observed evidence, and remaining uncertainty.
Reuse valid probes rather than repeat the baseline after unrelated steps.
Stop when the cause is explained or the next check requires unavailable access or new authority.
