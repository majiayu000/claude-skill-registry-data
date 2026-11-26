---
name: local-services-tailnet
description: "Use when publishing a local service on the tailnet."
version: 1.0.0
author: Charles Ponti
license: MIT
metadata:
  author: ponti-studios
  category: Software Development
  tags:
    - services
    - background
    - tailscale
    - mcp
    - localhost
  hermes:
    tags: [services, background, tailscale, mcp, localhost]
    related_skills: [app-configuration]
---

# Local services and tailnet exposure

Run a local service as a daemon and publish it on the tailnet without breaking loopback consumers.

## When to use

- Starting an MCP server, dev server, or any long-lived HTTP service in the background.
- Exposing a local port on the tailnet with `tailscale serve`.
- A local service is "up" by `lsof` but `curl 127.0.0.1` returns 000.

## Procedure

### 1. Start the daemon (Hermes terminal tool)

The terminal tool rejects shell-level background wrappers (`nohup`/`disown`/`setsid`). Use the tool's own backgrounding and keep it alive across the session:

```
terminal(command="<cmd> > /tmp/<name>.log 2>&1", background=true, persist_on_release=true)
```

Then **poll** readiness; do not rely on a completion ping for a process that never exits:

```
sleep 15
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/<path>
tail -30 /tmp/<name>.log
```

First runs download packages; if checks fail, wait ~20s and check once more before declaring failure.

### 2. Bind on IPv4 loopback, not "localhost"

Many Node/Python servers default to `--host localhost`, which on macOS binds **IPv6 only** (`[::1]`). Consumers that use `127.0.0.1` (curl checks, Tailscale Serve, other local tools) then get connection refused even though `lsof` shows the port listening.

- Verify with `lsof -nP -iTCP:<port> -sTCP:LISTEN` — note whether it says `[::1]` or `127.0.0.1`.
- If IPv6-only and a 127.0.0.1 consumer is needed, restart with an explicit IPv4 bind: `--host 127.0.0.1` (or `0.0.0.0` only when LAN exposure is intended).
- When `curl 127.0.0.1` returns 000, also try `http://localhost:<port>` and `http://[::1]:<port>` before concluding the server is down.

### 3. Host-header / proxy gotcha

When a service sits behind a reverse proxy (Tailscale Serve forwards its own hostname), the service's Host validation may reject the request with 400 even though the backend is reachable. Allowlist the proxy hostname or disable the check:

- Playwright MCP: `--allowed-hosts '*'` (or the specific tailscale hostname).
- Hermes dashboard: `HERMES_DASHBOARD_PUBLIC_URL` / `dashboard.public_url`.
- Verify by curling both `http://127.0.0.1:<port>` (direct) and the published `https://<host>:<port>/` (proxied).

### 4. Publish on the tailnet (add-only)

```
tailscale serve status                                    # record existing mappings first
tailscale serve --bg --https=<port> http://127.0.0.1:<port>
tailscale serve status                                    # verify the new mapping
```

- Never `tailscale serve reset` and never remove/change an existing mapping — add only.
- Never enable Funnel; keep it tailnet-only.
- `tailscale serve status` shows the mapping even when the backend is down, so confirm the backend separately (step 2).
- If the CLI differs, check `tailscale serve --help`.

### 5. Verify published endpoint

```
curl -sk -o /dev/null -w "%{http_code}" https://<host>:<port>/
```

## Pitfalls

- **`nohup`/`disown`/`setsid` are rejected** by the terminal tool; use `background=true` + `persist_on_release=true` and poll.
- **A service "listening" on `[::1]` is not reachable on `127.0.0.1`.** Check the bind address in `lsof`, not just the port.
- **`curl … 000` does not prove the server is down** — it may be an IPv4/IPv6 or Host-header mismatch. Try localhost/::1 and a direct request.
- **tailscale serve does not validate the backend at setup time** — a successful "Serve started" with an unreachable backend gives a mapping that 502s. Verify the backend first.
- **First run downloads packages** — wait 15s, then 20s more before reporting failure.
- **Env vars are not inherited across terminal calls** — inline them on the launch command (`FOO=bar cmd …`), or the daemon starts without them.
- **Do not stop the daemon when finishing** unless asked; leave it running with `persist_on_release`.

## Verification checklist

- `lsof -nP -iTCP:<port> -sTCP:LISTEN` shows `127.0.0.1:<port>` (or intended bind).
- `curl` to the direct URL returns an HTTP code (not 000).
- `tailscale serve status` shows the new mapping.
- Published URL returns an HTTP code.
