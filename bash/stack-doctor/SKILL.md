---
name: stack-doctor
description: Read-only health check of the local dev environment — Docker daemon identity, port allocation vs docs/ports.md, Node/pnpm toolchain, container and service health. Use when the stack misbehaves, ports collide, containers act oddly, or before starting environment work.
---

# Stack Doctor

Diagnose the dev environment without changing it. **Read-only** — report findings
and hand the user exact fix commands; never restart, delete, or reconfigure
anything yourself (see Verify Environment Before Theorizing in `AGENTS.md`).

Run the check script first, then interpret:

```bash
.claude/skills/stack-doctor/scripts/check.sh
```

## What the results mean

- **Environment**: the script detects devcontainer vs host. Inside the agent
  devcontainer there is no docker CLI and services are reached via
  `host.docker.internal` — that is normal, not a failure.
- **Docker daemon**: on the host, Docker Desktop is THE daemon; the native
  `dockerd` was deliberately disabled after a split-brain incident. Confirm
  server identity with `docker info`; WSL can legitimately use the `default`
  context for Docker Desktop. Flag an active native daemon or unreachable server.
- **Ports**: expected listeners come from `docs/ports.md` (single source of
  truth). A missing web-app port usually just means that dev server isn't
  running — only flag it if the user expected it up. A port held by an
  unexpected process is the real finding: name the process.
- **Toolchain**: expect Node 24.x and the `packageManager` pnpm pin from root `package.json` via corepack. Mismatches
  cause subtle lockfile and build skew.
- **WSL2 memory**: low MemTotal means `.wslconfig` limits — a host-side file the
  user must edit from Windows (`%UserProfile%\.wslconfig`), then `wsl --shutdown`.

## Report format

One line per check: `PASS` / `WARN` / `FAIL` with a plain-language sentence.
Finish with a numbered list of host-side actions the user must take themselves
(container rebuilds, `.wslconfig` edits, daemon toggles) — clearly separated from
anything that needs no action.
