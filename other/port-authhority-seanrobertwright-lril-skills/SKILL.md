---
name: port-authhority
description: >
  Diagnose and resolve port conflicts during local development. Triggers when a developer
  hits "address already in use" or EADDRINUSE errors, when a Docker container or docker compose
  service fails to start due to a port binding collision, or when multiple dev servers (React,
  Vite, Django, Rails) compete for the same port. Also useful when the developer wants to see
  which processes are listening on which ports, needs to free up a specific port, or wants to
  audit port mappings before deploying containers. Handles Docker Desktop, native Docker Engine,
  and plain host-process conflicts across Linux, macOS, and Windows (including WSL).
allowed-tools:
  - Bash
  - Edit
---

# Port Authhority

Detect, diagnose, and resolve port conflicts between Docker containers, compose services, and host processes.

## Prerequisites

Python 3.8+ with `docker` and `pyyaml` packages. Install if missing:

```bash
pip install docker pyyaml
```

## Workflow

### Phase 1: Scan

Run the port scanner to collect a cross-platform snapshot of all port usage:

```bash
python "<skill-directory>/scripts/port_scanner.py" [--path /optional/compose/dir]
```

The `--path` argument defaults to the current working directory and controls where to look for compose files.

The script outputs JSON with this structure:

```json
{
  "platform": "linux | darwin | windows",
  "docker_desktop": true,
  "containers": [
    {"id": "abc123", "name": "my-api", "image": "node:18", "state": "running",
     "ports": [{"host_port": 3000, "container_port": 3000, "protocol": "tcp", "bind_address": "0.0.0.0"}]}
  ],
  "compose_services": [
    {"service": "web", "image": "nginx", "ports": [{"host_port": 8080, "container_port": 80, "protocol": "tcp", "bind_address": "0.0.0.0"}],
     "compose_file": "/project/docker-compose.yml"}
  ],
  "host_ports": [
    {"port": 5432, "protocol": "tcp", "pid": 1234, "process": "postgres", "bind_address": "127.0.0.1"}
  ],
  "conflicts": [
    {"type": "container-host", "port": 3000, "protocol": "tcp",
     "parties": ["container:my-api", "process:node(PID 9876)"],
     "suggestion": "Use port 3001 (available)"}
  ],
  "summary": {"total_ports": 12, "conflicts": 1, "containers": 3}
}
```

Parse the JSON and present a formatted report:

- **Containers table:** Name, image, state, and host:container port mappings.
- **Host ports table:** Port, protocol, PID, and process name for each listener.
- **Compose services:** Declared services and their port mappings, noting which are already running.

### Phase 2: Analyze

If the `conflicts` array is non-empty, present each conflict with three parts:

- **What:** The port number, protocol, and which parties collide (e.g., container vs host process).
- **Why it matters:** A container trying to bind a taken port will fail to start entirely. Two containers on the same host port means traffic reaches only one of them. A compose service conflicting with a local database means `docker compose up` will error out partway through.
- **Fix:** The suggested alternative port from the `suggestion` field.

Conflict types the scanner detects:
- `container-host` -- a running container's host port collides with a host process.
- `container-container` -- two containers map to the same host port.
- `compose-pending` -- a compose file declares a port that is already taken, so `docker compose up` would fail.

Use `references/common-ports.md` for context on well-known ports. For example, if port 5432 is conflicting, mention it is typically PostgreSQL. If port 3000 is taken, note it is commonly used by React, Rails, and Express dev servers, so the developer may have a forgotten dev server running.

If no conflicts exist, confirm all clear and show the summary counts.

### Phase 3: Fix (with confirmation)

**Always ask the developer before applying any change.** Propose one fix per conflict:

- **Edit compose file:** Change the host port in the `ports:` mapping (e.g., `"3000:3000"` to `"3001:3000"`). Only the host side changes; the container-side port stays the same so the app inside the container is unaffected.
- **Stop or restart a container:** Stop the conflicting container, then restart it with a different `-p` host port.
- **Kill a host process:** Offer to kill the process occupying the port. Show the PID and process name so the developer can make an informed decision. Warn if the process looks like a database or system service -- killing those has side effects.

After applying any fix, re-run the scanner to verify the conflict is resolved. This catch-and-verify loop prevents partial fixes.

### Common Scenarios

- **"address already in use" on `docker compose up`:** A local dev server or database is already on that port. Scan, identify the host process, and either stop it or remap the compose port.
- **Multiple dev servers on port 3000:** React, Rails, and Express all default to 3000. Scan host ports to find the culprit process and suggest incrementing (3001, 3002).
- **Database port collision:** A dockerized PostgreSQL on 5432 conflicts with a locally installed PostgreSQL. Remap the container to 5433 so both coexist.
- **Port works on one machine but not another:** Different bind addresses (127.0.0.1 vs 0.0.0.0) or Docker Desktop vs native Engine behave differently. The scanner's `bind_address` and `docker_desktop` fields help diagnose this.

## Error Handling

- **Docker not running:** Tell the developer to start Docker Desktop or the Docker daemon. Offer to re-scan afterward. On Linux, suggest `sudo systemctl start docker`.
- **Docker not installed:** Skip container checks entirely. Still scan host ports to provide a partial but useful report.
- **Python not available:** Fall back to inline commands: `docker ps --format json` for containers and `docker port <id>` for mappings. Use `ss -tlnp` (Linux), `lsof -iTCP -sTCP:LISTEN -P -n` (macOS), or `netstat -ano` (Windows) for host ports.
- **Permission denied on host port scan:** Some systems require elevated privileges for full port visibility. Suggest `sudo` on Linux/macOS. On Windows, run the terminal as Administrator.
- **No compose file found:** Skip compose analysis. Report only running containers and host ports -- the scan is still valuable without compose context.
- **`docker` or `pyyaml` Python packages missing:** The scanner gracefully degrades. Without `docker`, it skips container enumeration. Without `pyyaml`, it skips compose parsing. Both cases still produce valid JSON.
