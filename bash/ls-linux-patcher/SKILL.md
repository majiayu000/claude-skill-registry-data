---
name: ls-linux-patcher
description: Create safe Linux server patching and Docker update plans. Use when the user asks to update, patch, or upgrade Linux servers, check maintenance readiness, plan package updates, plan Docker Compose refreshes, or coordinate multi-host maintenance. The bundled helper is plan-only; PatchMon API execution is unavailable until a tested Python client is added.
metadata:
  version: "1.1"
compatibility: "Python 3.12+ for scripts/patch_cli.py; ssh is required to run generated commands manually. The bundled CLI never executes remote patching commands."
---

# Linux Patcher

Linux Patcher helps plan package and Docker maintenance for Linux hosts. It emits auditable commands for an operator or agent to review and run manually. It does not query PatchMon, open SSH sessions, run package managers, or update containers.

## Current Capability

- `status`: print supported and unavailable modes.
- `auto`: describe the unavailable PatchMon/Python API workflow and give a safe fallback.
- `host-only`: plan package update checks for one host.
- `host-full`: plan package checks plus Docker Compose refresh checks for one host.
- `multiple`: read a local host list and emit one combined plan.
- `--json`: emit machine-readable plan output.

All CLI modes are plan-only. `--dry-run` on `auto` is accepted for compatibility, but it does not change behavior because no execution mode exists in this shipped helper.

## Quick Start

Run commands from the skill directory:

```bash
python scripts/patch_cli.py status
python scripts/patch_cli.py auto --dry-run
python scripts/patch_cli.py host-only admin@webserver.example.com
python scripts/patch_cli.py host-full admin@app.example.com /opt/docker
python scripts/patch_cli.py multiple ./hosts.conf
```

Example `hosts.conf`:

```text
admin@webserver.example.com
docker@app.example.com,/opt/docker
```

For structured output:

```bash
python scripts/patch_cli.py --json host-only admin@webserver.example.com
```

## Safety Rules

- Review every generated command before running it.
- Confirm the maintenance window, backups, rollback path, and service owner.
- Use SSH key authentication; do not store passwords in this skill.
- Avoid unrestricted passwordless sudo.
- Prefer a dedicated maintenance user with narrowly scoped sudo access.
- Test on staging or one low-risk host before broad rollout.
- Reboots are not automated; schedule them separately when kernel updates require them.

## Target Host Requirements

- SSH server reachable from the control machine.
- Package manager available on the host: `apt`, `dnf`, `yum`, or `zypper`.
- Passwordless sudo only for the exact commands your organization has approved.
- Docker and Docker Compose only when using a Docker refresh plan.
- PatchMon agents are optional for monitoring. This skill does not query PatchMon directly.

## Minimal Sudo Guidance

Do not copy a universal sudoers block blindly. Generate the plan first, identify the exact commands your host will need, then create a narrow `/etc/sudoers.d/` entry for a dedicated user.

Sudoers rules that include arguments are command-line-specific. Verify the executable path on the target host and choose its matching readiness command: `apt update`, `dnf check-update`, `yum check-update`, or `zypper list-updates`. Do not grant every alternative merely because the planner can recognize them.

Example pattern:

```sudoers
# Replace patchbot and command paths for the target distribution.
patchbot ALL=(root) NOPASSWD: /usr/bin/apt update
patchbot ALL=(root) NOPASSWD: /usr/bin/apt upgrade
patchbot ALL=(root) NOPASSWD: /usr/bin/apt autoremove
patchbot ALL=(root) NOPASSWD: /usr/bin/docker compose pull
patchbot ALL=(root) NOPASSWD: /usr/bin/docker compose up
```

Validate with:

```bash
sudo visudo -c -f /etc/sudoers.d/linux-patcher
ssh patchbot@host 'sudo -n -l -- /usr/bin/apt update'
```

The remote `sudo -n -l` command lists whether that exact path and argument vector is authorized; it does not execute `apt update`. It proves only that one readiness command is listed. Each later update, upgrade, autoremove, or Docker command still needs its own reviewed rule, and the operator must separately confirm backups, the maintenance window, and service readiness.

## PatchMon

PatchMon can remain useful as a dashboard for host update state, but this skill only provides a guidance stub for PatchMon automation:

```bash
python scripts/patch_cli.py auto
```

The command reports that PatchMon automatic execution is unavailable in the current framework and points users to `host-only`, `host-full`, or `multiple` plan generation. Add a tested Python API client before documenting any live PatchMon querying or credentials file contract.

## Manual Workflow

1. Run `python scripts/patch_cli.py status` to confirm available modes.
2. Generate a plan with `host-only`, `host-full`, or `multiple`.
3. Review commands for the target distribution and service risk.
4. Confirm maintenance window, backups, and rollback.
5. Run approved commands manually or through your platform's terminal tool.
6. Check package logs, container health, and reboot requirements.

## References

- `references/overview.md`: concise operator overview.
- `references/setup.md`: secure setup and validation steps.
- `references/workflows.md`: current plan-only workflows.
- `references/patchmon-setup.md`: PatchMon dashboard notes and unavailable API boundary.
- `references/patchmon-security-and-distributions.md`: security and distribution notes.
- `references/contributing.md`: contribution and test guidance.
