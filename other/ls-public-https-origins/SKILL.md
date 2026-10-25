---
name: ls-public-https-origins
description: "Migrates HTTP network clients to public DNS and verified HTTPS, with protected Unix socket origins and bounded TLS passthrough for isolated containers. Use when local clients bypass TLS, origins expose plaintext ports, or HTTP proxies break public endpoint compatibility."
license: MIT
compatibility: "Python 3.12+; Linux for Unix socket publication. Service changes require the owning administrator. LocalSetup is optional."
metadata:
  version: "1.0"
---

# Public HTTPS and protected origins

**Purpose:** Preserve one public HTTPS identity from local and remote clients,
including S3 signatures, while removing plaintext HTTP network hops.

## Scope and prerequisites

Use for transport migration after the application works. This complements
service-specific administration; it does not own mail account resets, DNS zone
administration, secrets management, or a blanket server hardening exercise.
Read [the migration notes](references/migration.md) only for the selected path.
Scripts use Python's standard library and run without LocalSetup or Envman.
Use the host's existing secret manager and privileged terminal workflow when
present. Existing task authorization covers ordinary reversible steps.

## Workflow

1. **Observe once.** Identify the actual service owner, configured client URLs,
   listeners, proxy headers, certificates, container routes and proxy variables.
   Record only secret-free facts in durable documentation; keep raw evidence in
   ignored private state. Never dump container environments or credentials.
2. **Choose the minimum change.** Every HTTP network client uses a public DNS
   HTTPS URL with certificate and hostname verification. Prefer native TLS.
   Where unavailable, put the origin on a protected Unix socket behind the TLS
   frontend. HTTP messages over local IPC are not a plaintext TCP origin.
3. **Preserve recovery.** Capture the exact owning configuration and required
   consistent data with the host's maintained encrypted backup workflow before
   overwriting it. Preserve images, volumes, users, ownership and unrelated work.
   Identify the stop condition and recovery action before activation.
4. **Prepare and apply.** Update client endpoints, public Host/SNI identity,
   health checks and SDK path style. Remove plaintext port publications and
   proxy inheritance. Use existing TLS ingress and service instances. Render
   only parameters, never embed credentials. For isolated outbound clients use
   the optional gateway below; for local socket exposure use the socket helper.
5. **Verify the real path.** From both host and actual client namespace, check
   CA/hostname verification, authenticated application access and an object
   digest. Inspect effective listeners, generated unit arguments, environment
   variable names, routes and socket permissions. Confirm that service restart
   recreates and republishes its socket. Reuse evidence for unchanged layers.
6. **Finish.** Update owning documentation and record limits. Keep buckets
   private unless public access is requested. Use verified, expiring HTTPS
   downloads for authorized private artifacts. Never roll back silently to HTTP.

## Included tools

Resolve paths relative to this skill directory; run `--help` before invocation.

- `python3 scripts/public_https.py https://storage.example.com` validates the
  endpoint form. It does not perform DNS or TLS verification; actual requests
  must use the platform default CA store and verify the public hostname.
- `python3 scripts/tls_gateway.py --allow-host storage.example.com
  --listen 10.66.0.2 --source-cidr 10.66.0.0/24` relays bounded TLS records to
  public IPv4 port 443 after exact SNI and source-subnet checks. Clients retain
  certificate verification. It is not an HTTP CONNECT proxy and holds no keys.
- `python3 scripts/socket_bridge.py --config /etc/origins/storage.json` requires
  root and a root-owned private config. The source socket and proxy data
  directory must share a filesystem. See the example and systemd templates in
  `assets/`. Prefer native shared socket mounts when available.

## Fail closed

Reject IP URL literals, local-only hostnames, non-HTTPS URLs, URL credentials,
non-443 endpoints and TLS verification bypasses. Do not print signed query
strings. A gateway is a transport allowlist, not a replacement for application
authentication or origin authorization. Encrypted ClientHello without visible
approved SNI is unsupported and rejected; do not add a plaintext fallback.

## Portability

The skill format follows Agent Skills. Linux root, systemd and a compatible
reverse proxy are required only for the optional socket bridge deployment.
The gateway requires Python 3.12+, public DNS and allowed public IPv4 egress.
No installation, listener, service restart, key creation or remote write occurs
merely from loading this skill. See the release-specific integration record in
[compatibility](references/compatibility.md).
