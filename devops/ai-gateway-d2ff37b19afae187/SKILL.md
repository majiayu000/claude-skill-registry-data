---
name: ai-gateway
description: Debug and troubleshoot ettametta's AI Gateway — the load-balancing reverse proxy for remote GPU worker nodes. Use when node routing fails, health checks stall, provisioning breaks, or inference requests time out.
---
# AI Gateway Debugging

The AI Gateway (port 8133) is a FastAPI reverse proxy that load-balances inference requests across remote GPU worker nodes with model-aware routing.

## Quick Diagnostics

```bash
# Cluster health + node telemetry
curl http://localhost:8133/health

# Via nginx proxy
curl http://localhost:8000/ai-gateway/health

# Check gateway container
docker compose ps ai-gateway
docker compose logs --tail=50 ai-gateway

# Check registered nodes
docker compose exec ai-gateway cat /workspace/gateway_state.db 2>/dev/null
```

## Architecture

### Core: `src/engines/remote_ai_setup/gateway.py`

FastAPI app ("AI Cluster Gateway") that acts as a load-balancing reverse proxy.

**Node Registry:** SQLite-backed (`/workspace/gateway_state.db`) with tables for `jobs` and `nodes`. Nodes seeded from `AI_NODES` env var (comma-separated URLs).

**Health Loop:** Background async task polls every node's `/health` every 10 seconds, tracking:
- Online/offline status
- Busy state
- Currently loaded model

**Smart Routing** (`select_best_node`):
1. Prefer a node that already has the requested model loaded
2. Fall back to any idle node
3. Fall back to any online node

**Catch-All Proxy** (`POST /{path:path}`):
- Extracts `model` or `model_key` from request body
- Infers model from path keywords (`hunyuan`, `animatediff`, `generate`)
- Routes to best available node
- Stores `job_id` mappings for status/download routing

**Provisioning** (`POST /nodes/provision`):
- Accepts IP + SSH key (passed via `/dev/shm`, never persisted)
- Deploys worker via `deploy_to_gpu_server.sh`

### Key Files

| File | Purpose |
|------|---------|
| `src/engines/remote_ai_setup/gateway.py` | Core gateway — routing, health, provisioning |
| `infra/docker/gatekeeper.Dockerfile` | Container definition (Python 3.10-slim, fastapi, uvicorn, httpx) |
| `infra/docker/nginx.conf` | Nginx proxy: `/ai-gateway/` → `http://ai-gateway:8133` |
| `apps/dashboard/src/lib/config.ts` | Frontend: `AI_GATEWAY_URL` = `{host}/ai-gateway` |

### Docker Compose Config

Service: `ai-gateway`, built from `gatekeeper.Dockerfile`, port `8133:8133`, mounts `src/engines/remote_ai_setup` into `/app`, volume `gateway_data` for `/workspace`.

Env vars: `AI_NODES`, `INTERNAL_API_TOKEN`, `AI_CLUSTER_SECRET`.

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | None | Cluster health + node telemetry |
| `/status/{job_id}` | GET | None | Proxied job status lookup |
| `/pulse` | POST | `X-Worker-Token` | Worker heartbeat sink |
| `/register` | POST | `X-Admin-Token` | Register a new node |
| `/nodes` | POST | `X-Admin-Token` | Register a new node (alias) |
| `/nodes/{url}` | DELETE | `X-Admin-Token` | Remove a node |
| `/nodes/provision` | POST | `X-Admin-Token` | SSH-deploy a new GPU worker |
| `/{path:path}` | POST | None | Catch-all proxy with model-aware routing |

## Common Issues

### All nodes offline
```bash
curl -s http://localhost:8133/health | jq '.nodes'
```
Check if `AI_NODES` env var is set:
```bash
docker compose exec ai-gateway env | grep AI_NODES
```

### Requests routing to busy node
`select_best_node` prefers model-loaded nodes even if busy, as a last resort. Check node states:
```bash
curl -s http://localhost:8133/health | jq '.nodes[] | {url, online, busy, model}'
```

### Model not found on any node
If no node has the requested model loaded and all are busy, the request fails. Solutions:
- Add more nodes
- Wait for a node to finish
- Pre-load models on nodes

### Provisioning fails
SSH key is passed via `/dev/shm` (memory-backed tmpfs). Check:
- SSH key is valid
- Target IP is reachable from the gateway container
- `deploy_to_gpu_server.sh` exists and is executable

### SQLite state corrupted
Gateway state is in `/workspace/gateway_state.db`. Volume-mounted, survives restarts. If corrupted:
```bash
docker compose exec ai-gateway rm /workspace/gateway_state.db
docker compose restart ai-gateway
```

### Job status returns wrong node
Job-to-node mapping is stored in SQLite. If gateway restarts during a job, the mapping is preserved (volume). But if the node also restarts, the job is lost.

### Nginx 502 on /ai-gateway/
Check gateway container:
```bash
docker compose ps ai-gateway
docker compose exec ai-gateway curl -s http://localhost:8133/health
```

## Worker Heartbeat

Workers send `POST /pulse` with `X-Worker-Token` header. Gateway tracks:
- Worker URL
- Online/busy status
- Current model
- Last seen timestamp

If a worker misses 3 heartbeats (~30s), it's marked offline.

## Debugging Checklist

1. Gateway up? `curl http://localhost:8133/health`
2. Nodes registered? Check `AI_NODES` env
3. Nodes online? `curl /health | jq '.nodes'`
4. Nginx proxy working? `curl http://localhost:8000/ai-gateway/health`
5. SQLite intact? `ls -la gateway_data/gateway_state.db`
6. Auth tokens set? `INTERNAL_API_TOKEN`, `AI_CLUSTER_SECRET`
7. Provisioning: SSH key valid, target reachable
