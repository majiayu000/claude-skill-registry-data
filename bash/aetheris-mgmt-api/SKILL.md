---
name: aetheris-mgmt-api
category: How Milo works
blurb: The operations reference for the Aetheris server — how Milo inspects, restarts, and diagnoses its own home without SSH.
example: Check the health of the services on Aetheris.
---
# Aetheris Management API

Operational reference for the lightweight management API on oracle-aetheris. Use this skill whenever Milo needs to inspect, restart, or diagnose services on the Aetheris box without SSH.

## Access

- **Endpoint:** `https://mgmt.nrupalakolkar.com`
- **Auth:** header `X-Mgmt-Token` with the token stored in Milo's global memory.
- **Transport:** Cloudflare Tunnel `c12afde0` -> `http://localhost:9090` on the box.
- **Server:** Python `http.server` process, systemd unit `aetheris-mgmt.service`, env file `/etc/aetheris-mgmt.env` (chmod 600, root-owned).

## Endpoints

### Unauthenticated
| Method | Path | Returns |
|--------|------|---------|
| GET | `/health` | `{"status":"ok"}` — liveness only |

### Authenticated (require X-Mgmt-Token)
| Method | Path | Returns |
|--------|------|---------|
| GET | `/status` | Service states (systemd + docker), disk, memory |
| GET | `/docker-ps` | All containers with status and ports |
| GET | `/nginx-config` | Current Nginx `default.conf` content |
| GET | `/logs/aetheris` | Last 50 lines of aetheris-core logs (journalctl or docker) |
| GET | `/logs/ollama` | Last 50 lines of Ollama logs |
| POST | `/restart/{service}` | Restart a service. Allowed: `aetheris-core`, `cloudflared`, `bee`, `ollama`, `nginx`. Tries systemd first, falls back to docker. |
| POST | `/docker-compose-up` | Runs `docker compose up -d` in `/opt/aetheris` (timeout 120s) |
| POST | `/ollama-models` | Lists installed Ollama models |

## Usage from Milo (sandbox_exec)

```bash
# Read status
curl -s -H "X-Mgmt-Token: $TOKEN" "https://mgmt.nrupalakolkar.com/status"

# Restart Ollama
curl -s -X POST -H "X-Mgmt-Token: $TOKEN" "https://mgmt.nrupalakolkar.com/restart/ollama"

# Check Nginx config
curl -s -H "X-Mgmt-Token: $TOKEN" "https://mgmt.nrupalakolkar.com/nginx-config"
```

The token is retrieved from Milo's stored memory at runtime. Never hardcode it in scripts or commit it to repos.

## Extending the API

To add new endpoints, edit `/opt/aetheris-mgmt/mgmt.py` on the box (via opencode/SSH) and restart:
```bash
sudo systemctl restart aetheris-mgmt
```

Keep the same patterns: token check via `_auth()`, JSON response via `_json()`, subprocess via `_run()`. New POST endpoints that mutate state should be added to the `allowed` list explicitly.

## Security posture

1. **Localhost-only listener** — `127.0.0.1:9090`, unreachable from the internet except via Cloudflare Tunnel.
2. **Token-gated** — shared secret in header, not basic auth (avoids browser credential caching).
3. **Allowlist for restarts** — only named services can be restarted; arbitrary command execution is not exposed.
4. **No shell exec endpoint** — by design. If arbitrary commands are needed, Nrupal runs them via opencode/SSH.

## Troubleshooting

- **502 from mgmt.nrupalakolkar.com:** The mgmt service is down. SSH to box: `sudo systemctl restart aetheris-mgmt`.
- **403 Forbidden:** Wrong or missing token. Check `/etc/aetheris-mgmt.env` on the box.
- **Health returns ok but status returns 501:** Token not set in env file. Check `MGMT_TOKEN` is populated.
- **Tunnel not routing:** Verify ingress entry exists: `mgmt.nrupalakolkar.com -> http://localhost:9090` in Cloudflare tunnel config.
