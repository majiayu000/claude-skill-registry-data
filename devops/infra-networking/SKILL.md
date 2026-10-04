---
name: infra-networking
description: Manage AICP's network surfaces — LocalAI on `localhost:8090` (host) → `:8080` (container), AICP own metrics on `:9101/metrics`, optional Grafana on `:3000` + Prometheus on `:9090`, MCP server stdio (no port), agent server `--agent <port>` (default no agent), planned LocalAI P2P cluster peering (Stage 4 reliability). Loads when the operator says "what ports does AICP use" / "expose LocalAI to fleet" / "firewall rules" / "set up cluster peering" / "AICP behind a reverse proxy" / "MCP not connecting".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# infra-networking

Manage AICP's network surfaces — port mappings, MCP transport, planned
P2P cluster peering, and reverse-proxy/firewall integration. AICP is
local-first by default (everything on `localhost`); fleet integration
extends to peer connections.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "what ports does AICP use", "expose LocalAI to fleet",
  "firewall rules", "set up cluster peering", "AICP behind a reverse
  proxy", "MCP not connecting"
- **Multi-machine setup**: extending AICP from single-host to fleet (per
  CLAUDE.md `## Infrastructure target` two-machine plan)
- **Security posture**: confirming what's exposed externally vs
  localhost-only

Do NOT load when:

- The concern is HTTPS cert management (load `infra-security`)
- The concern is application-layer routing (load `aicp/core/router.py`-related skills, e.g., `aicp-ops-runtime`)
- The concern is API contract design (load `infra-api`)

## Operations

### Operation 1 — Inventory ports and surfaces

**When**: pre-deploy audit or firewall configuration.

**Process**:

1. Build the canonical list (current AICP):
   - **8090** (host) → 8080 (container): LocalAI OpenAI-compatible API
     + `/metrics` + `/app/collections` (KB)
   - **9101**: AICP own Prometheus exporter (`aicp/core/prometheus.py`)
   - **9090** (optional): Prometheus server (when `make monitoring-up`)
   - **3000** (optional): Grafana (when `make monitoring-up`, admin/aicp)
   - MCP server: stdio transport (no port — bidirectional pipe via the
     MCP client invocation)
   - Agent server: `aicp --agent <port>` (operator-chosen, default not
     running)
2. For each: record exposed-on (`localhost`-only vs `0.0.0.0`), required
   inbound for fleet vs operator-only
3. Document in firewall config or operator runbook

**Quality bar**: by default, ALL surfaces should be `localhost`-only.
Exposing externally is a deliberate fleet/integration step.

### Operation 2 — Expose LocalAI for fleet access

**When**: fleet machines need to call this AICP's LocalAI inference API.

**Process**:

1. Edit `docker-compose.yaml` LocalAI port mapping:
   - From `127.0.0.1:8090:8080` (localhost-only)
   - To `0.0.0.0:8090:8080` (any-interface) OR `<lan-ip>:8090:8080`
     (specific interface — preferred)
2. Restart LocalAI: `docker compose restart localai`
3. Configure firewall (ufw / iptables / cloud SG) to allow port 8090
   from fleet IPs only — NEVER open to internet
4. Verify from fleet machine: `curl http://<host>:8090/v1/models`
5. Update fleet config (`config/fleet.yaml.template` → operator-specific
   `fleet.yaml`) to point at the new LAN-accessible LocalAI

**Quality bar**: NEVER expose 8090 to the public internet. LocalAI's
API has no auth; exposure invites abuse. Firewall to LAN/VPN only.

### Operation 3 — Set up LocalAI P2P cluster peering (planned, partial)

**When**: extending to multi-machine fleet with cross-host model load
balancing.

**Process**:

1. Per CLAUDE.md `## Infrastructure target`, the planned topology is
   "LocalAI peering: Cluster 1 ↔ Cluster 2 (load balance, failover)"
2. Status: marked PENDING in CLAUDE.md `## The Mission` Stage 4 ("partial:
   circuit breakers + DLQ + reliable profile shipped; cluster peering
   pending")
3. Implementation requires:
   - LocalAI's built-in P2P feature (libp2p-based)
   - Discovery mechanism (mDNS / static peer list / federated registry)
   - Per-peer health monitoring (`aicp_p2p_status` MCP tool exists but
     is now deprecated — use `aicp --observe`)
4. Document the cluster setup in `wiki/decisions/00_inbox/` before
   implementing

**Quality bar**: cluster peering is architecturally significant —
author the decision page BEFORE implementing.

### Operation 4 — Place AICP behind a reverse proxy

**When**: operator wants TLS termination or path-based routing in front
of LocalAI / AICP exporter.

**Process**:

1. Choose reverse proxy: Caddy (auto-TLS, simplest), Nginx (most
   flexible), Traefik (cloud-native)
2. Configure proxy to forward:
   - `https://<domain>/v1/*` → `http://localhost:8090`
   - `https://<domain>/metrics` → `http://localhost:9101/metrics`
   - `https://<domain>/grafana/*` → `http://localhost:3000` (with prefix
     stripping if needed)
3. After proxy is in place, restrict LocalAI to `localhost`-only (proxy
   handles external)
4. Add auth at the proxy layer (basic auth, mTLS, OAuth) — LocalAI has
   no native auth

**Quality bar**: TLS termination + auth at the proxy is the operator's
responsibility; AICP itself doesn't ship with these. Don't expose the
raw proxied LocalAI without auth.

### Operation 5 — Diagnose MCP connection failures

**When**: a Claude Code agent or other MCP client can't connect to AICP's MCP server.

**Process**:

1. AICP's MCP uses stdio transport — the client invokes `aicp --mcp`
   and reads/writes via stdin/stdout
2. Verify the client's MCP config points at the correct command:
   `aicp --mcp` (or the standalone `aicp-mcp` entry point)
3. Common failures:
   - `aicp` not in PATH → fix with absolute path or PATH update
   - Python venv not activated → MCP config needs to invoke through the venv
   - Permission denied → check executable bit
4. Test manually: `echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}' | aicp --mcp`
   should return a JSON response

**Quality bar**: MCP stdio transport has no port to firewall — connection
issues are almost always config (wrong command, wrong PATH, wrong venv).

## Gotchas

- **Detection**: agent recommends exposing LocalAI port 8090 to the public internet.
  **Rule**: NEVER expose 8090 publicly. LocalAI has no auth; exposure
  is an immediate abuse vector.
  **Reasoning**: any external reachable LocalAI becomes free GPU compute
  for whoever finds it; cost + abuse risk is severe.

- **Detection**: agent uses MCP stdio config without absolute path.
  **Rule**: MCP client configs should use absolute paths to the AICP
  binary (or full venv-activated invocation).
  **Reasoning**: MCP clients run `aicp --mcp` from their own working
  directory; PATH may not include AICP's venv.

- **Detection**: agent assumes AICP's metrics port (9101) is the same as Prometheus (9090).
  **Rule**: 9101 is AICP's OWN exporter; 9090 is the Prometheus SERVER
  (when monitoring-up). Different roles.
  **Reasoning**: Prometheus scrapes 9101 (and 8090's `/metrics` for
  LocalAI). They're producer + consumer, not duplicates.

- **Detection**: agent skips reverse proxy auth for LocalAI exposure.
  **Rule**: any external exposure must include auth at the proxy layer.
  **Reasoning**: LocalAI's lack of native auth means the proxy is the
  ONLY auth gate; skipping it leaves the inference API open.

- **Detection**: agent recommends cluster peering without checking CLAUDE.md status.
  **Rule**: per CLAUDE.md, cluster peering is PENDING. Don't promise it
  exists today.
  **Reasoning**: setting expectations correctly avoids operator confusion;
  the partial-Stage-4 status should be transparent.

## Reference exemplars

- `docker-compose.yaml` — port mappings, GPU passthrough config
- `aicp/core/prometheus.py` — `:9101/metrics` exporter
- `aicp/agent/server.py` — agent server (operator-chosen port via
  `aicp --agent <port>`)
- `config/fleet.yaml.template` — fleet config template (cluster peering)
- CLAUDE.md `## Infrastructure target` — planned multi-machine topology

## Domain context

AICP is local-first by default — everything on `localhost`. Fleet rollout
extends carefully: LocalAI exposed to LAN only, AICP exporter exposed
to Prometheus on LAN, agent server activated per-host. The MCP server
uses stdio (no port), avoiding network-level concerns at that layer.
TLS + auth are operator-supplied via reverse proxy when external
exposure is needed.

## Related skills

| Skill | When to use |
|-------|-------------|
| `infra-security` | When the concern is the security posture of exposed surfaces |
| `infra-monitoring` | When setting up Prometheus/Grafana scraping |
| `aicp-ops-runtime` | When diagnosing live network state via `--check` / `--observe` |
| `config-deploy` | When the deploy profile selects different network config |
| `foundation-docker` | When changing the Docker network config |
