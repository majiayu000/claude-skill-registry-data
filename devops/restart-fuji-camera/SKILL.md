---
name: restart-fuji-camera
description: 重啟 Fuji Camera 相機 App（Docker 部署）並驗證有起來。當使用者說「重啟 fuji / fuji camera / 相機 app / 底片相機」、Discord 回報網頁打不開 / 上傳沒反應 / 照片一直卡在處理中、或 /restart-fuji-camera 時使用。會重啟 host 的 fuji-gen.service（GPU 生圖）、docker compose 的 app + tailscale sidecar，然後驗證 https://fuji-camera.crayfish-monitor.ts.net/ 有沒有通、回報佇列狀態。
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fuji-camera, camera, flux, docker, tailscale, systemd, restart, discord]
---

# Restart Fuji Camera

Use when the Fuji Camera app needs restarting — page won't load, uploads do nothing, photos
stuck, or the user says「重啟 fuji / 相機 app / 底片相機」.

## Just run it

```bash
bash ~/.hermes/skills/restart-fuji-camera/scripts/restart.sh
```

Idempotent. It restarts the host GPU gen service + the docker stack (app + tailscale), then
verifies `https://fuji-camera.crayfish-monitor.ts.net/` returns 200. When passcode-gated, the
root still returns 200 and renders the login page so browsers and embedded webviews do not treat it
as an HTTP error.

## Architecture — this is a Docker deployment (GPU stays on the host)

Project: `~/src/fuji_camera` (see its `CLAUDE.md`). Three moving parts:

| Piece | What | Managed by |
|-------|------|-----------|
| `fuji-gen.service` | HOST generation service — FLUX.2 底片風 on the **GPU**, HTTP bytes on `:7863` | `systemctl --user` |
| `fuji-camera-app` (docker) | FastAPI web + picture pool, **no GPU/torch**; calls the gen service over `host.docker.internal:7863` | docker compose |
| `fuji-camera-ts` (docker) | `tailscale/tailscale` sidecar (own node **fuji-camera**); serves `https://fuji-camera.<tailnet>.ts.net` → app | docker compose |

The docker stack is defined by `docker-compose.yml` and wrapped by the systemd unit
`fuji-camera-docker.service`. The app talks **bytes over HTTP** to the host gen service, so no
shared filesystem — the container is portable.

## How to launch / start / stop this service

Everything lives in `~/src/fuji_camera`. Config is in `.env` (gitignored):

```dotenv
FUJI_PASSCODES=8345,2233,2345    # one gallery per passcode; empty = no gate
TS_AUTHKEY=                      # only for the FIRST node registration (see below)
```

**Normal launch / relaunch** (node already registered — ts-state exists):

```bash
# 1. host GPU service (FLUX.2 底片風 on :7863) — enable once, it stays on/boots
systemctl --user enable --now fuji-gen.service
curl -s localhost:7863/health                        # {"ready": true}

# 2. the app + Tailscale sidecar (systemd unit just wraps `docker compose`)
systemctl --user enable --now fuji-camera-docker.service   # = docker compose up -d
#    stop: systemctl --user stop fuji-camera-docker.service # = docker compose down
#    or directly: cd ~/src/fuji_camera && docker compose up -d

# 3. verify
curl -s -o /dev/null -w "%{http_code}\n" https://fuji-camera.crayfish-monitor.ts.net/   # 200 (app or passcode login page) = up
```

`fuji-gen.service` + `fuji-camera-docker.service` (systemd `--user`, linger on) and the containers
(`restart=unless-stopped`) all start on boot; Tailscale state persists in `ts-state/` so no re-login.

**First-time / fresh-box registration** — the `fuji-camera` node isn't in `ts-state` yet, so put a
Tailscale auth key in `.env` (`TS_AUTHKEY=tskey-auth-...` from the admin console) before the first
`docker compose up -d`. It registers the node once, then the key is no longer needed (remove it).
Alternatively register interactively: run `tailscaled` in the sidecar, `tailscale up`, open the
printed login URL. To make it **public**: set `AllowFunnel` true in `ts-serve.json` (+ enable Funnel
in the tailnet ACL) — then guard it with `FUJI_PASSCODES`.

**Add / change a passcode**: edit `FUJI_PASSCODES` in `.env` → `docker compose up -d` (recreates the
app with the new env). Each passcode is an isolated gallery; existing photos belong to the first
passcode's group.

## Notes / troubleshooting

- Restart order matters: **app first, then the ts sidecar** (it shares the app's netns) — the
  script already does `docker restart fuji-camera-app` then `fuji-camera-ts`.
- **Public login root must be HTTP 200, not 401.** The login HTML is a normal page, not an HTTP
  authentication challenge; returning 401 can make browser/webview clients display an error instead
  of the passcode form. Keep `/api/*` unauthenticated responses at 401, but return the login page
  with 200 for non-API paths.
- Logs: `docker compose logs --tail=40` (in `~/src/fuji_camera`), `journalctl --user -u fuji-gen -n 40 --no-pager`.
- **Frontend edits (`static/index.html`) are live on refresh** — no restart needed. Restart only for
  `server.py` / `gen_service.py` changes (rebuild the image for `server.py`: `docker compose up -d --build`).
- The old host-only path (`fuji-camera.service` on `:8090` + `aya.*` serve) is **retired/disabled**;
  the live deployment is the Docker one above.
- Make it public on the internet: set `AllowFunnel` true in `ts-serve.json` (+ enable Funnel in the
  tailnet ACL).
