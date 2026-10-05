---
name: caddy-https-reverse-proxy
description: >-
  Deploy Caddy (no Docker) on a remote Linux host to expose a local HTTP
  backend as trusted HTTPS, prioritizing first-party domain + Let's Encrypt
  (HTTP-01), with DuckDNS DNS-01 fallback, low-bandwidth binary transfer
  fallback, verification, and rollback.
---

# Caddy HTTPS Reverse Proxy (Domain-First)

Use this skill to deploy or repair a production-style HTTPS reverse proxy on
a remote Linux server where backend API is only HTTP (for example
`127.0.0.1:39080`).

Default policy:
1. Prefer user-owned domain first (for example `api.example.com`).
2. Use DuckDNS only as fallback when no usable own-domain is available.

## When To Use
Use this skill when the user asks to:
1. Add trusted HTTPS in front of an existing HTTP backend.
2. Configure Caddy without Docker.
3. Use their own domain with Let's Encrypt automatic certificate issuance.
4. Fallback to DuckDNS DNS-01 when own-domain path is unavailable.
5. Prepare a backend endpoint consumable by browser frontends (for example
   GitHub Pages).

## Required User Inputs
Collect and confirm these values before execution:
1. `ssh_host`: target SSH host (IP or domain).
2. `ssh_user`: remote SSH user.
3. `domain`: target HTTPS domain (prefer user-owned domain, for example
   `api.ackingliu.top`).
4. `backend_upstream`: backend HTTP upstream (default `127.0.0.1:39080`).
5. `contact_email`: ACME email (use a real mailbox when possible).

Optional but useful:
1. `public_ip`: expected public IP of target server.
2. `ssh_port`: default `22`.
3. `use_local_download_upload`: `true` when remote network is unstable.
4. `disable_http3`: `true` to force only `h1/h2`.

DuckDNS fallback only:
1. `duckdns_domain`: DuckDNS hostname (for example `sfapi.duckdns.org`).
2. `duckdns_token`: DuckDNS token for DNS challenge.

## Preconditions
1. `domain` resolves to the target public IP.
2. Inbound `80/tcp` and `443/tcp` are reachable.
3. Backend service will bind loopback (`127.0.0.1`) instead of `0.0.0.0`.
4. Remote user has `sudo` privilege.

## Security Rules
1. Never hardcode token directly in `Caddyfile`.
2. If DuckDNS mode is used, store token in root-only env file:
   - `/etc/caddy/caddy.env` with mode `600`.
3. Do not run Caddy with `--environ` in systemd ExecStart, to avoid leaking
   env vars into logs.
4. Do not expose backend upstream port publicly.
5. If switching from DuckDNS to own domain, remove stale DuckDNS env/drop-in.

## Deployment Workflow

### Step 1: Select deployment mode
Choose one mode before execution:
1. `domain-first` (default and preferred):
   - Use user-owned domain.
   - Use standard Caddy + Let's Encrypt (`http-01`).
   - No DNS plugin and no token file needed.
2. `duckdns-fallback`:
   - Use only when user has no usable own domain or explicitly requests it.
   - Use Let's Encrypt DNS-01 via `dns.providers.duckdns`.

### Step 2: Preflight checks
Run on remote:
1. `hostname && whoami && date`
2. `sudo -n true` (or explicit sudo check)
3. `dig +short A <domain>`
4. `sudo ss -lntup | grep -E '(:80|:443|:39080|:22)' || true`

If `public_ip` is provided and DNS does not match it, stop and ask user to fix
DNS first.

### Step 3: Install baseline packages
On remote:
1. `sudo apt-get update -y`
2. `sudo apt-get install -y caddy curl ca-certificates`

### Step 4: Configure Caddyfile (domain-first preferred)
Create `/etc/caddy/Caddyfile`:

```caddyfile
{
    email admin@example.com
    servers {
        protocols h1 h2
    }
}

api.example.com {
    @health path /_caddy_health
    respond @health "ok" 200

    reverse_proxy 127.0.0.1:39080
}
```

Replace:
1. email with `contact_email`
2. site address with `domain`
3. upstream with `backend_upstream`
4. if `disable_http3` is `false`, you may remove `servers { protocols h1 h2 }`

### Step 5: DuckDNS fallback path (only when needed)
Requirement: module `dns.providers.duckdns` must exist.

Preferred download URL:
`https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com/caddy-dns/duckdns`

Two supported methods:
1. Remote direct download:
   - download to `/tmp/caddy-custom`
2. Local download + upload fallback (recommended when remote bandwidth is poor):
   - download locally
   - `scp` upload to `/tmp/caddy-custom` on remote

Then on remote:
1. `chmod +x /tmp/caddy-custom`
2. `/tmp/caddy-custom list-modules | grep dns.providers.duckdns`
3. backup existing binary:
   - `sudo cp /usr/bin/caddy /usr/bin/caddy.bak.<timestamp>`
4. replace:
   - `sudo install -m 755 /tmp/caddy-custom /usr/bin/caddy`
5. verify:
   - `caddy version`
   - `caddy list-modules | grep dns.providers.duckdns`

Then configure token and systemd environment:
Create env file:
1. `/etc/caddy/caddy.env`
2. content:
   - `DUCKDNS_TOKEN=<duckdns_token>`
3. permission:
   - `chmod 600 /etc/caddy/caddy.env`
   - `chown root:root /etc/caddy/caddy.env`

Create/overwrite drop-in:
1. `/etc/systemd/system/caddy.service.d/env.conf`
2. content:
   - `[Service]`
   - `EnvironmentFile=/etc/caddy/caddy.env`
   - `ExecStart=`
   - `ExecStart=/usr/bin/caddy run --config /etc/caddy/Caddyfile`

DuckDNS mode Caddyfile template:

```caddyfile
{
    email admin@example.com
    servers {
        protocols h1 h2
    }
}

sfapi.duckdns.org {
    tls {
        dns duckdns {env.DUCKDNS_TOKEN}
        resolvers 1.1.1.1 8.8.8.8
    }

    @health path /_caddy_health
    respond @health "ok" 200

    reverse_proxy 127.0.0.1:39080
}
```

Replace:
1. email with `contact_email`
2. site address with `domain`
3. upstream with `backend_upstream`

### Step 6: Validate and restart
On remote:
1. `sudo caddy validate --config /etc/caddy/Caddyfile`
2. `sudo systemctl daemon-reload`
3. `sudo systemctl restart caddy`
4. `sudo systemctl status caddy --no-pager -l`
5. `sudo journalctl -u caddy -n 120 --no-pager -l`

Expected success signal:
1. log contains challenge flow matching selected mode:
   - domain-first: usually `challenge_type":"http-01"` (or `tls-alpn-01`)
   - duckdns-fallback: `challenge_type":"dns-01"`
2. log contains certificate obtained message
3. listeners include `:80` and `:443`

### Step 7: End-to-end verification
Verify from remote and local client:
1. `curl -I http://<domain>/_caddy_health` -> `308` redirect to HTTPS
2. `curl -I https://<domain>/_caddy_health` -> `200`
3. certificate check:
   - `echo | openssl s_client -connect <domain>:443 -servername <domain> 2>/dev/null | openssl x509 -noout -issuer -subject -dates`

If backend is not started yet, `/_caddy_health` must still return `200` by Caddy.

### Step 8: Cleanup stale fallback config (when domain-first is selected)
If machine previously used DuckDNS mode:
1. remove `/etc/systemd/system/caddy.service.d/env.conf` if present.
2. remove `/etc/caddy/caddy.env` if present.
3. `sudo systemctl daemon-reload`
4. `sudo systemctl restart caddy`

## Firewall and Cloud-Network Notes
If certificate issuance fails:
1. In domain-first mode, confirm inbound `80/443` are reachable from internet.
2. Check cloud security group allows inbound 80/443 from `0.0.0.0/0`.
3. Check host firewall order so explicit allow for 80/443 is effective.
4. Recheck domain A/AAAA record accuracy.
5. If network path for HTTP challenge is unstable, switch to DuckDNS DNS-01.

## Common Failure Patterns
1. Browser still warns:
   - stale cert; verify with `openssl s_client` and clear CDN/proxy assumptions.
2. `502` from Caddy:
   - backend not running on configured `backend_upstream`.
3. `dns.providers.duckdns` missing in DuckDNS mode:
   - wrong Caddy binary, reinstall plugin-enabled binary.
4. DNS challenge fails in DuckDNS mode:
   - invalid token, wrong domain, or DNS propagation delay.
5. TLS internal errors from some clients:
   - verify client-side proxy/VPN interference and compare direct network path.

## Rollback
If deployment must be reverted:
1. restore old binary:
   - `sudo cp /usr/bin/caddy.bak.<timestamp> /usr/bin/caddy`
2. restore prior `/etc/caddy/Caddyfile` from backup.
3. remove drop-in/env only if needed:
   - `/etc/systemd/system/caddy.service.d/env.conf`
   - `/etc/caddy/caddy.env`
4. `sudo systemctl daemon-reload && sudo systemctl restart caddy`

## Output Contract
When finishing this skill, report:
1. selected mode: `domain-first` or `duckdns-fallback`.
2. final public HTTPS URL.
3. cert issuer + validity dates.
4. upstream target (`backend_upstream`) configured.
5. Caddy version and whether DuckDNS module is required/installed.
6. files created/changed:
   - `/etc/caddy/Caddyfile`
   - `/etc/caddy/caddy.env` (DuckDNS mode only)
   - `/etc/systemd/system/caddy.service.d/env.conf` (DuckDNS mode only)
   - `/usr/bin/caddy` (plus backup path)
