---
name: restart-power-monitor
description: 重啟 Strix Halo Power Monitor 電源監控服務與 Tailscale 旁路容器（sidecar）。當使用者要求重啟服務、Tailscale 網址無法載入、度數與電費計算異常、網頁 WebSockets 連線失敗或斷線，或是使用 /restart-power-monitor 時。此技能會依序重構並重新部署後端服務、重新建立 Tailscale 代理容器、自動偵測並修復 Tailscale 的離線與網路故障，最後進行端對端 API 及外網 HTTPS 驗證。
license: MIT
metadata:
  hermes:
    tags: [power-monitor, tailscale, docker, restart, amdgpu, telemetry]
---

# Restart Strix Halo Power Monitor

Use this skill when the Strix Halo Power Monitor web app or its Tailscale endpoint is unhealthy, non-responsive, or when the user explicitly requests `/restart-power-monitor` or "重啟 power-monitor / 電源監控 / 電費監控服務".

## Just run it

Run the automated restart and diagnostic script on the host:

```bash
bash ~/.hermes/restart-power-monitor/scripts/restart.sh
```

The script automatically performs the following actions:
1. Rebuilds and restarts the `power-monitor` container (FastAPI + WebSocket backend).
2. Force-recreates the `tailscale` container (sharing network namespace with the backend).
3. Verifies local API responsiveness at `http://localhost:8085/api/stats` with a 30-second retry window.
4. Validates the Tailscale node status and resolves transient offline states (auto-restarting container if network is reported down).
5. Tests the public HTTPS endpoint `https://power.crayfish-monitor.ts.net/` to verify SSL reverse-proxying and Funnel reachability.

## Live Architecture

| Piece | What | Managed by | Location |
| --- | --- | --- | --- |
| **Backend & UI** | FastAPI + SQLite database + HTML templates | Docker Compose service `power-monitor` (Port `8085:8000`) | [main.py](file:///home/chihmin/src/power-monitor/main.py) |
| **Tailscale Sidecar** | Tailscale node providing SSL HTTPS + Funnel on `power.crayfish-monitor.ts.net` | Docker Compose service `tailscale` (`network_mode: service:power-monitor`) | [ts-entrypoint.sh](file:///home/chihmin/src/power-monitor/ts-entrypoint.sh) |

> [!IMPORTANT]
> Because the `tailscale` sidecar uses `network_mode: service:power-monitor`, any recreation of the `power-monitor` container invalidates the old network namespace. You **MUST** recreate/restart the `tailscale` container as well. Do not restart them individually via simple `docker restart`.

## Manual Troubleshooting

If the script fails, follow these steps to manually diagnose the service:

### A. Inspect Logs
```bash
# Check FastAPI backend logs
docker compose -f ~/src/power-monitor/docker-compose.yml logs power-monitor

# Check Tailscale sidecar and proxy logs
docker compose -f ~/src/power-monitor/docker-compose.yml logs tailscale
```

### B. Verify Tailscale Status inside Container
If the public FQDN doesn't resolve, check if the Tailscale daemon inside the container is authenticated:
```bash
docker exec power-monitor-ts tailscale --socket=/tmp/tailscaled.sock status
```
If it shows "Tailscale cannot connect because the network is down", run:
```bash
docker compose -f ~/src/power-monitor/docker-compose.yml restart tailscale
```

### C. Manual Deploy
If Compose configuration changes:
```bash
cd ~/src/power-monitor
docker compose up -d --build power-monitor
docker compose up -d --force-recreate tailscale
```
