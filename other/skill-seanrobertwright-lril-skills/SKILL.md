---
name: port-authhority
description: >
  Manage Docker port conflicts during local development. Detects and resolves port collisions
  between Docker containers, docker compose services, and host processes.
  Use when: deploying containers, running docker compose, debugging port binding errors,
  seeing "address already in use", managing port mappings, or working with Docker Desktop.
  Keywords: docker, container, port, port conflict, docker compose, docker-compose, deploy,
  port mapping, port binding, address already in use, EADDRINUSE, bind, listen.
allowed-tools:
  - Bash
  - Edit
---

# Port Authhority

Detect, diagnose, and resolve port conflicts between Docker containers, compose services, and host processes.

## Prerequisites

This skill requires Python 3.8+ with `docker` and `pyyaml` packages. If missing, install them:

```bash
pip install docker pyyaml
```

## Workflow

### Phase 1: Scan

Run the port scanner script from the skill's `scripts/` directory:

```bash
python "<skill-directory>/scripts/port_scanner.py" [--path /optional/compose/dir]
```

The `--path` argument defaults to the current working directory. The script outputs JSON to stdout.

Parse the JSON output. Present a formatted report to the developer:

**Containers table:** Show each running container's name, image, state, and port mappings.

**Host ports table:** Show each listening host process with port, protocol, PID, and process name.

**Compose services:** If a compose file was found, show declared services and their port mappings, noting which are running and which are not.

### Phase 2: Analyze & Report

If the `conflicts` array in the JSON output is non-empty, present each conflict:

- **What:** Which port, which protocol, which parties are involved
- **Why:** Explain the impact (container won't start, traffic routed to wrong service, etc.)
- **Fix:** The suggested alternative port from the `suggestion` field

Refer to `references/common-ports.md` for context on well-known ports. For example, if port 5432 is conflicting, mention that it's typically PostgreSQL.

If no conflicts exist, confirm all clear and show the summary counts.

### Phase 3: Fix (with confirmation)

For each conflict, propose a specific fix action. **Always ask the developer before applying any change.** Possible actions:

- **Edit compose file:** Change the host port in the `ports:` mapping (e.g., `"3000:3000"` → `"3001:3000"`)
- **Restart container:** Stop the conflicting container and restart with a different host port
- **Kill host process:** Offer to kill a host process occupying the port (show PID and process name)

After applying any fix, re-run the scan to verify the conflict is resolved.

### Error Handling

- **Docker not running:** Tell the developer to start Docker. Offer to re-scan.
- **Docker not installed:** Skip Docker checks. Still scan host ports for a partial report.
- **Python not available:** Fall back to inline commands: `docker ps --format json` and `docker port <id>`.
- **Permission denied:** Suggest running with elevated privileges for full host port visibility.
- **No compose file found:** Skip compose analysis. Report only running containers and host ports.
