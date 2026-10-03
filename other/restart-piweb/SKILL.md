---
name: restart-piweb
description: 重啟 Pi agent gateway、piweb host worker、Docker web app 與 Tailscale sidecar，並驗證 tailnet Serve 和真正的公開 Funnel。當使用者說「重啟 piweb / pi web」、網頁回傳 502、Tailscale host/serve 不正常、agent 或 worker 沒回覆，或輸入 /restart-piweb 時使用。特別防止 app 重建後 sidecar 留在 stale network namespace 的陷阱。
license: MIT
metadata:
  hermes:
    tags: [piweb, docker, tailscale, funnel, restart, systemd, discord]
---

# Restart piweb

## Just run it

```bash
bash ~/.hermes/skills/restart-piweb/scripts/restart.sh
```

Use for `/restart-piweb`, 「重啟 piweb / pi web」, HTTP 502, a dead web UI, or an agent/worker that
stops replying. The script starts the Pi agent gateway and restarts the host worker before
restarting the Docker web tier and Tailscale sidecar. It fails unless both tailnet Serve and the
actual public Funnel path return HTTP 200.

The skill lives in `~/.hermes/skills/restart-piweb`; `~/.claude/skills/restart-piweb` is a symlink to
it, so edit only the Hermes copy. `tests/run-tests.sh` covers the script's ordering and failure
handling.

## Live architecture

Project: `~/src/piweb`

| Piece | Role | Managed by |
|---|---|---|
| `pi-discord-gateway.service` | Runs the Pi agent gateway and Discord-facing agent process | `systemctl --user` |
| `piweb-worker.service` | Runs Pi jobs on the host so it can access host tools/files | `systemctl --user` |
| `piweb-app` | Node web/API tier bound to `127.0.0.1:8099` inside Docker | Docker Compose `app` |
| `piweb-ts` | Dedicated `piweb` Tailscale node; HTTPS Serve + public Funnel | Docker Compose `tailscale` |

The sidecar uses `network_mode: service:app`, so it shares the app container's network namespace.
Its Serve config proxies `https://piweb.crayfish-monitor.ts.net/` to
`http://127.0.0.1:8099`. Persistent Tailscale identity is under `~/src/piweb/ts-state/`.

## Restart order

The restart script must start both host-side services, not only the Docker frontend:

```bash
systemctl --user enable --now pi-discord-gateway.service
systemctl --user enable --now piweb-worker.service
systemctl --user restart piweb-worker.service
```

It verifies both units are active at the end. The gateway is started rather than restarted so an
invocation from Discord is not interrupted. `pi-discord-gateway.service` is the Pi agent;
`piweb-worker.service` handles queued piweb jobs. The Docker app alone is not a complete
piweb/agent restart.

## The rabbit hole: healthy containers, broken host

The failure seen on 2026-07-24 looked misleadingly healthy:

- `piweb-app` was running and logged `listening` on `127.0.0.1:8099`.
- `piweb-ts` was also running and `tailscale serve status` showed the correct proxy.
- Yet the site returned **HTTP 502**, and the sidecar could not connect to localhost.

Root cause: the app had been recreated while the old Tailscale sidecar stayed alive. Docker's
`network_mode: service:app` is effectively tied to that specific app container/network namespace.
The sidecar remained attached to the dead, stale network namespace while the replacement app
listened in a new one. Container status and Serve configuration therefore both looked correct.

The decisive check is from inside the sidecar:

```bash
docker exec piweb-ts sh -c 'wget -S -O /dev/null http://127.0.0.1:8099/'
```

If that says `Connection refused` while app logs say it is listening, recreate the sidecar **after**
the app:

```bash
cd ~/src/piweb
docker compose up -d --build --force-recreate app
docker compose up -d --force-recreate tailscale
```

Do not rely on `docker restart piweb-ts` after the app was recreated: force-recreation makes Compose
resolve and attach the current app namespace. This ordering is the core of the restart script.

## Verification traps

### MagicDNS can hide a broken Funnel

Running ordinary `curl https://piweb.crayfish-monitor.ts.net/` on a tailnet device resolves through
MagicDNS to the node's `100.x` address. That proves tailnet Serve, **not** public Funnel. Funnel can
still be broken while that curl returns 200.

To exercise real Funnel, query public DNS and pin curl to a public ingress IP:

```bash
dig +short @1.1.1.1 piweb.crayfish-monitor.ts.net A
curl --resolve piweb.crayfish-monitor.ts.net:443:<PUBLIC_IP> \
  https://piweb.crayfish-monitor.ts.net/
```

The script tests both paths. The public root should return 200 and render the token login page.

### Funnel may need tailscaled to reconnect

Applying `AllowFunnel` can make status immediately say `Funnel on` while public TLS still ends with
`unexpected eof`. Recreating/restarting `piweb-ts` re-establishes its ingress connection. Use a
public-DNS `--resolve` test rather than trusting status alone.

Seen again on 2026-07-28, right after a normal restart: worker active, both containers running,
sidecar→app loopback 200, tailnet Serve 200, `tailscale serve status` showing `Funnel on` — yet
the pinned public curl failed the TLS handshake (`TLS alert, decode error` →
`unexpected eof while reading`, `%{http_code}` = `000`). A single `docker compose restart tailscale`
plus ~20s fixed it; three consecutive public probes then returned 200.

The script now handles this itself: if the public probe fails it restarts the sidecar once, retries,
and then re-probes twice more to make sure Funnel is not flapping. Two rules matter here:

- `000` from curl is a **transport/TLS failure, not an HTTP status** — do not read it as "the app is
  down". The app tier is fine in this failure mode.
- Restarting (not recreating) `piweb-ts` is only correct when the app container was **not** recreated
  since. For a stale-netns 502 you still need the force-recreate ordering above; a plain restart
  would reattach to the dead namespace.

### First registration and containerboot timeout

On fresh state, `containerboot` gives interactive `tailscale up` only a **60-second timeout**.
Interactive browser login often loses that race: the container restarts, generates a new node key,
and the URL already opened becomes stale. Symptoms include a restart loop, `tailscale up failed:
signal: killed`, and no Serve config.

Use either:

1. `TS_AUTHKEY` in `.env` for first registration, then remove it after state persists; or
2. Run `tailscaled` directly against the same `ts-state`, complete `tailscale up --hostname=piweb`,
   then start the Compose sidecar.

## Manual diagnostics

```bash
systemctl --user status pi-discord-gateway.service piweb-worker.service
docker compose -f ~/src/piweb/docker-compose.yml ps
docker compose -f ~/src/piweb/docker-compose.yml logs --tail=50 app tailscale
docker exec piweb-ts tailscale status
docker exec piweb-ts tailscale serve status
journalctl --user -u piweb-worker.service -n 50 --no-pager
```

Do not reset `ts-state`, run `tailscale logout`, or expose app port 8099 on the host as a routine fix.
The loopback-only app is intentional: it protects trust in identity headers injected by Serve.
