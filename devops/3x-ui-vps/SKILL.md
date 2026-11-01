---
name: 3x-ui-vps
description: Deploy and manage 3X-UI on a root-managed Ubuntu or Debian VPS using Docker Compose, nginx, ACME certificates, SSH panel tunneling, UFW hardening, and Xray VLESS over XHTTP behind nginx. Use when the user explicitly wants to install 3X-UI from scratch, lock the panel and subscription server to 127.0.0.1, open an SSH tunnel to the panel, create or repair a VLESS inbound behind nginx on public 443, add extra clients to an existing inbound, or run safe OS and container updates.
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - python3
        - ssh
---

# 3X-UI VPS

Deploy 3X-UI on a VPS with the panel and subscription server bound to loopback, `ufw` allowing only SSH/HTTP/HTTPS, nginx on public `80/443`, and one `VLESS + XHTTP` transport routed through nginx.

This skill is manual-first because it mutates remote infrastructure. Invoke it only when the user explicitly asks to deploy, repair, harden, or update a VPS.

## Hard rule

- All server-side configuration must be executed only through the bundled scripts in this skill.
- Do not create or edit remote configs manually over SSH, do not run ad-hoc heredocs on the server, and do not "quick-fix" nginx, Docker, ACME, or 3X-UI by hand.
- Read-only inspection commands are allowed for diagnosis.
- If a script fails because the host is in an unexpected state, stop changing the server, patch the relevant script locally in this skill, and rerun the script.
- The manual fallback in this skill is for the 3X-UI panel UI only. It is not permission to mutate server files manually.

## Inputs

Collect these before doing any work:

- `ssh target` for the VPS, preferably `root@host`
- optional plain-text SSH password if the host is password-auth only
- public domain pointed at the VPS
- optional ACME email
- panel admin username and password
- optional local tunnel port

Assume Ubuntu or Debian with `apt`. Do not use this skill on other distributions without adapting the Docker repository setup first.

The operator workstation and the target VPS also need outbound internet access for Docker downloads, ACME issuance, and panel API calls.

## Preflight

Before changing the host, confirm these assumptions:

- the domain already resolves to the VPS from the server side, not only from the operator workstation
- the operator knows whether SSH access is key-based or password-based
- if the host already has a certificate for the same domain, reruns must reuse it instead of treating `acme.sh` "Domains not changed" as a hard failure
- if panel tunneling starts failing with immediate SSH disconnects after several quick attempts, stop parallel retries, wait briefly, and retry one connection at a time

## Workflow

### 1. Fresh deploy

Use [`scripts/bootstrap-host.sh`](scripts/bootstrap-host.sh).

Example:

```bash
./scripts/bootstrap-host.sh \
  --host root@example-vps \
  --ssh-password 'host-password' \
  --domain assets.example.com \
  --panel-username admin \
  --panel-password 'panel-secret'
```

Default shape:

- 3X-UI runs via Docker Compose under `/opt/3x-ui`
- Docker is installed on Ubuntu and Debian hosts through `get.docker.com`
- container keeps `network_mode: host`
- data lives under `3x-ui-data/db/`
- certificates live under `3x-ui-data/cert/`
- panel must bind to `127.0.0.1:<panel_port>`
- subscription server must bind to `127.0.0.1:2096`
- panel admin username and password must be applied during deploy
- the script must resolve the public domain on the server itself with `dig` before ACME issuance
- nginx terminates TLS on public `443`
- nginx returns `401` for unmatched traffic
- nginx proxies only the configured Xray secret path to the local backend port with `grpc_pass`
- `ufw` must allow only SSH, HTTP, and HTTPS from the internet

After deploy, verify:

```bash
ssh <target> 'ss -ltnp | egrep ":2053 |:2096 |:1234 "'
ssh <target> 'docker compose -f /opt/3x-ui/docker-compose.yml ps'
ssh <target> 'curl -I http://127.0.0.1:2053/'
ssh <target> 'ufw status numbered'
```

Read [`references/architecture.md`](references/architecture.md) if you need the full topology or nginx routing rationale.

### 2. Panel access

Use [`scripts/open-panel-tunnel.sh`](scripts/open-panel-tunnel.sh) and keep the panel SSH-only.

Default tunnel:

```bash
./scripts/open-panel-tunnel.sh --host root@example-vps --ssh-password 'host-password' --local-port 12053 --panel-port 2053
```

Then open `http://127.0.0.1:12053`.

If the tunnel fails with an immediate SSH disconnect, avoid parallel SSH sessions to the same host for a short period and retry the tunnel as a single connection after a brief pause.

Do not publish the panel in nginx. If the operator later wants a public panel, treat that as a separate hardening decision.

### 3. Quick inbound bootstrap

Use [`scripts/bootstrap-inbound.py`](scripts/bootstrap-inbound.py) against the tunneled panel URL.

Important detail:

- public client transport is `TLS` because nginx terminates TLS on `443`
- backend Xray inbound behind nginx stays plain `XHTTP` on loopback
- the inbound path must match the nginx secret path

Preferred flow:

```bash
python3 scripts/bootstrap-inbound.py \
  --panel-url http://127.0.0.1:12053 \
  --username admin \
  --password 'secret' \
  --public-domain assets.example.com \
  --backend-port 1234 \
  --path /xhttp-keep-this-secret
```

The script prefers API automation but always prints a manual fallback checklist. Use [`references/manual-bootstrap.md`](references/manual-bootstrap.md) if API endpoints drift or the panel UI has changed.
That fallback is UI-only. If server-side behavior needs to change, update the bundled scripts first and rerun them.

### 4. Add another client to an existing inbound

Use [`scripts/add-inbound-client.py`](scripts/add-inbound-client.py) against the tunneled panel URL.

This workflow is for adding one more client to an already working inbound without changing nginx, ports, or the existing secret path.

Preferred flow:

```bash
python3 scripts/add-inbound-client.py \
  --panel-url http://127.0.0.1:12053 \
  --username admin \
  --password 'secret' \
  --inbound-id 1
```

Behavior:

- the script logs in to 3X-UI through the panel tunnel
- loads the existing inbound
- appends one more VLESS client to `settings.clients`
- keeps the existing public domain and XHTTP path from that inbound
- updates the same inbound instead of creating a second parallel inbound
- prints a ready-to-import `vless://` client URL

If `--inbound-id` is omitted, the script may auto-select the inbound only when the panel has exactly one inbound. Otherwise require the operator to pass the inbound ID explicitly.

### 5. Updates

Use [`scripts/update-stack.sh`](scripts/update-stack.sh).

The update workflow must stay conservative:

```bash
./scripts/update-stack.sh --host root@example-vps --ssh-password 'host-password'
```

This runs:

- `apt update`
- `apt upgrade`
- `docker compose pull`
- `docker compose up -d`
- reapply panel loopback bind
- reapply subscription loopback bind on `2096`
- reapply `ufw` rules for SSH, HTTP, and HTTPS only

Do not switch this skill to `apt full-upgrade` unless the user explicitly asks for it.

## Fast troubleshooting

Use these checks before assuming the deploy is broken:

- `ssh <target> 'ss -ltnp | egrep ":2053 |:2096 |:1234 |:443 |:80 "'`
- `ssh <target> 'docker compose -f /opt/3x-ui/docker-compose.yml ps'`
- `ssh <target> 'curl -I http://127.0.0.1:2053/'`
- `ssh <target> 'cat /opt/3x-ui/bootstrap.env'`
- local tunnel check: `lsof -nP -iTCP:12053 -sTCP:LISTEN`

Interpretation:

- `127.0.0.1:2053` and `127.0.0.1:2096` mean panel and sub server are correctly isolated
- `127.0.0.1:1234` means the Xray backend inbound exists
- public `0.0.0.0:80` and `0.0.0.0:443` should belong to nginx
- `curl -I http://127.0.0.1:2053/` returning `404` is acceptable and proves the panel is responding
- `https://<domain>/` returning `401` is the expected nginx default for unmatched traffic

## Decision rules

- Prefer the bundled scripts over retyping long shell sessions.
- Treat the bundled scripts as the only writable interface to the server state.
- If deployment or update fails, fix the script or add a new script in this skill. Do not repair the server manually.
- If the operator provides a plain-text SSH password, pass it through to the bundled script with `--ssh-password` instead of wrapping SSH manually.
- Keep Docker installation simple and consistent by using `curl -fsSL https://get.docker.com -o get-docker.sh` followed by `sh ./get-docker.sh`.
- Resolve the public domain from the server itself with `dig`, not from the operator workstation, before relying on DNS results.
- Keep the panel on `127.0.0.1`; verify with `ss -ltnp`.
- Keep the subscription server on `127.0.0.1:2096`; verify with `ss -ltnp`.
- Keep nginx responsible for public `80/443`.
- Keep the Xray backend on a separate loopback port such as `127.0.0.1:1234`.
- Reuse the exact same secret path in nginx and the inbound config.
- When the operator asks for another client, prefer adding it to the existing inbound instead of creating a second inbound with duplicate transport settings.
- Keep `nginx` default responses normal HTTP `401`, not `444`, so browsers receive a valid error page.
- Keep `ufw` active and restricted to SSH, HTTP, and HTTPS ingress only.
- On current 3X-UI images, prefer `/app/x-ui setting ...`; the `x-ui` wrapper may not apply panel settings correctly inside the container.
- If this 3X-UI version exposes an extra subscription listener, set `subListen=127.0.0.1` and verify that `2096` is not public.
- If 3X-UI API calls fail, stop guessing and use the manual fallback.

## Script inventory

- [`scripts/bootstrap-host.sh`](scripts/bootstrap-host.sh): install host packages, Docker, nginx, ACME, Compose stack, and nginx config
- [`scripts/ssh-with-password.sh`](scripts/ssh-with-password.sh): wrapper for `ssh` with optional plain-text password support
- [`scripts/open-panel-tunnel.sh`](scripts/open-panel-tunnel.sh): open an SSH local port forward to the loopback-bound panel
- [`scripts/bootstrap-inbound.py`](scripts/bootstrap-inbound.py): log in to 3X-UI and create one VLESS client plus inbound
- [`scripts/add-inbound-client.py`](scripts/add-inbound-client.py): log in to 3X-UI, load an existing inbound, append one more client, and print the new `vless://` URL
- [`scripts/update-stack.sh`](scripts/update-stack.sh): run safe package and container updates remotely
- [`scripts/repair-existing-xhttp.py`](scripts/repair-existing-xhttp.py): switch an existing native 3X-UI XHTTP inbound to CDN-compatible `packet-up` mode with HTTP/2 ALPN
- [`scripts/rename-transport-hosts.py`](scripts/rename-transport-hosts.py): migrate public transport hostnames to neutral aliases while retaining the old names during rollout
- [`scripts/set-reality-camouflage.py`](scripts/set-reality-camouflage.py): change the target and advertised server name of an existing Reality inbound
- [`scripts/rotate-shared-subscription-id.py`](scripts/rotate-shared-subscription-id.py): assign one fresh subscription ID to several clients to avoid stale client-side subscription entries
- [`scripts/install-short-subscription.py`](scripts/install-short-subscription.py): expose an existing static subscription at a short nginx URL for clients and QR codes
- [`scripts/install-direct-subscription-host.py`](scripts/install-direct-subscription-host.py): expose a static subscription through a dedicated DNS-only HTTPS hostname when CDN access is unreliable
- [`scripts/optimize-shadowrocket-transports.py`](scripts/optimize-shadowrocket-transports.py): add direct WS/XHTTP routes and conservative Hysteria settings for Shadowrocket on unreliable mobile networks

## References

- [`references/architecture.md`](references/architecture.md): deploy topology and nginx behavior
- [`references/manual-bootstrap.md`](references/manual-bootstrap.md): panel UI fallback steps and field mapping
