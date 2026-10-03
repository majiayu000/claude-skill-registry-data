---
name: tailscale-serve-setup
description: Manage Tailscale serve (reverse proxy on tailnet) and TLS certificate generation.
---

# Tailscale Serve + Cert Setup

Manage Tailscale `serve` (reverse proxy on tailnet) and TLS certificate generation.

## When to use
- User wants to expose a local service on the tailnet via HTTPS
- User wants to change Tailscale hostname / DNS name
- User needs Tailscale-managed TLS certificates for local services

## Steps

### 1. Check current hostname and DNS name
```bash
# Get current DNS name — this is what cert/serve commands need
tailscale status --json 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
s = d.get('Self', {})
print('HostName:', s.get('HostName'))
print('DNSNames:', s.get('DNSNames', []))
"
```

### 2. Change hostname (optional)
```bash
sudo tailscale set --hostname=<new-name>
# Wait for DNS to propagate
sleep 5
tailscale status 2>&1
```

**⚠️ Important:** After changing hostname, the **Tailnet domain may also change** (e.g. from `tail465b60.ts.net` to `crayfish-monitor.ts.net`). Always re-check `DNSNames` before generating certs or re-adding serve.

### 3. Generate TLS certificate
```bash
# Domain MUST be the actual Tailnet FQDN — NOT .local or any other suffix
sudo tailscale cert <hostname>.<tailnet-domain>
# Example: sudo tailscale cert aya.crayfish-monitor.ts.net
```

**Gotchas:**
- Must use the exact Tailnet FQDN (e.g. `aya.crayfish-monitor.ts.net`), NOT `<hostname>.local`
- Tailscale will return a 500 error if the domain doesn't match the DNSNames
- Certificates are written to `/var/lib/tailscale/certs/<hostname>.<domain>.crt` and `.key`

### 4. Configure serve — Use `--set-path` (Tailscale v1.98+ only command)

**Preferred for Tailscale v1.98+:** Use incremental `--set-path` to add routes and `off` to remove them.

```bash
# Add a new route
sudo tailscale serve --bg --set-path /<subpath> http://localhost:<port>/

# Remove an existing route
sudo tailscale serve --https=443 --set-path=<oldpath> off
```

**Example - Add SearXNG at /search (port 8081):**
```bash
sudo tailscale serve --bg --set-path /search http://localhost:8081/
```

**Example - Remove old / route:**
```bash
sudo tailscale serve --https=443 --set-path=/ off
```

**⚠️ `--json` format is NOT supported in Tailscale v1.98.1** — it returns `flag provided but not defined: -json`.

**⚠️ `set-config --all <file>` has a CLI bug in v1.98.1** — it errors with "must specify filename" even when filename is provided. Use `--set-path` + `off` instead.

**Verify:**
```bash
sudo tailscale serve status
sudo tailscale serve status --json  # detailed
```

**If you need to reset and start fresh:**
```bash
sudo tailscale serve reset
sudo tailscale serve --bg --set-path /search http://localhost:8081/
sudo tailscale serve --bg --set-path /stock http://localhost:8501/
```

## Management commands
| Action | Command |
|---|---|
| View serve config | `sudo tailscale serve status` |
| View as JSON | `sudo tailscale serve status --json` |
| Remove all serve rules | `sudo tailscale serve reset` |
| Remove specific rule | `sudo tailscale serve off <path>` |
| Generate cert | `sudo tailscale cert <fqdn>` |
| Check hostname | `tailscale status` |
| Change hostname | `sudo tailscale set --hostname=<name>` |

## ⚠️ Known Pitfalls

- **Domain format:** `tailscale cert` requires the exact Tailnet FQDN, never `.local` or custom domains
- **Domain changes:** Changing hostname can change the entire Tailnet domain (e.g. from `tail465b60.ts.net` to `crayfish-monitor.ts.net`). Always re-check DNSNames after hostname change.
- **Serve reset:** After domain change, old serve config may reference the old domain — run `serve reset` before re-adding rules.
- **Port conflicts:** If the target port is already bound by another service (e.g. Docker), either change the serve port or stop the conflicting service.
- **Background serve:** Use `--bg` flag to run serve in the background (recommended for server setups).
- **Certificate path:** Certs go to `/var/lib/tailscale/certs/` — may need `sudo` to read.
- **--json is broken:** Current Tailscale CLI version rejects standard JSON config format. Use incremental `--set-path` approach instead.
- **Overwrite behavior:** `tailscale serve --bg <root>` replaces ALL routes. Use `--set-path` to add subpaths without overwriting.
- **curl from localhost needs SNI:** When testing Tailscale serve via curl from the same machine, use `--resolve "hostname:443:100.x.x.x"` to provide SNI. Without it, TLS handshake fails with `no SNI ServerName`.

## Related: Streamlit apps behind subpath

When deploying Streamlit apps via Tailscale serve on a subpath (e.g. `/stock`), the app returns a **blank page** because it can't load static resources from the wrong base path.

**Fix:** Add `--server.baseUrlPath=<subpath>` to the Streamlit command.

```bash
# Wrong (blank page on /stock)
streamlit run app.py --server.address 0.0.0.0

# Correct (static resources load properly on /stock)
streamlit run app.py --server.address 0.0.0.0 --server.baseUrlPath=/stock
```

## Related: SearXNG path

SearXNG serves at **root path `/`**, NOT at `/searxng`. Tailscale must proxy to `http://localhost:8081/` (not `/searxng`). Accessing `/searxng` returns **404**.