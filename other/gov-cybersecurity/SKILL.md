---
name: gov-cybersecurity
description: CVE vulnerability lookup via NIST NVD, CISA KEV, EPSS scores, and MITRE ATT&CK. 7 tools for real-time cybersecurity intelligence.
homepage: https://github.com/martc03/gov-mcp-servers
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["mcporter"]}}}
---

# Government Cybersecurity Vulnerability Intel

Real-time vulnerability intelligence from 4 authoritative sources — no API keys required.

## Setup

Connect to the remote MCP server:

```bash
mcporter add gov-cyber --url https://cybersecurity-vuln-mcp.apify.actor/mcp --transport streamable-http
```

Or add directly to your OpenClaw MCP config (`~/.openclaw/mcp.json`):

```json
{
  "servers": {
    "gov-cyber": {
      "url": "https://cybersecurity-vuln-mcp.apify.actor/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Available Tools

### `vuln_lookup_cve`
Look up a CVE by ID and get enriched intelligence from all 4 sources in a single call — NVD details (CVSS score, description, references), CISA KEV active exploitation status, EPSS exploitation probability, and MITRE ATT&CK techniques.

```
Look up CVE-2021-44228
```

Example output: CRITICAL 10.0, EPSS 94.4%, KEV=YES, ATT&CK: T1190/T1203/T1595.002

### `vuln_search`
Search the NIST National Vulnerability Database by keyword, severity, and date range.

```
Search NVD for "apache log4j" critical vulnerabilities
```

Parameters: `keyword`, `severity` (LOW/MEDIUM/HIGH/CRITICAL), `pubStartDate`, `pubEndDate`, `limit`

### `vuln_kev_latest`
Get recently added entries from the CISA Known Exploited Vulnerabilities catalog — confirmed actively exploited in the wild.

```
Show KEV entries added in the last 7 days
```

Parameters: `days` (1-365, default 7), `limit`

### `vuln_kev_due_soon`
Get CISA KEV vulnerabilities with upcoming remediation deadlines. Federal agencies must patch by the due date.

```
Show KEV vulnerabilities due within 14 days
```

Parameters: `days` (1-90, default 14), `limit`

### `vuln_epss_top`
Get CVEs with the highest EPSS exploitation probability scores. A score of 0.9 = 90% chance of exploitation in the next 30 days.

```
Show CVEs with EPSS score above 0.9
```

Parameters: `threshold` (0-1, default 0.5), `limit`

### `vuln_trending`
Get recently published critical and high severity CVEs. Stay on top of emerging threats.

```
Show trending critical CVEs from the last 3 days
```

Parameters: `days` (1-30, default 3), `severity`, `limit`

### `vuln_by_vendor`
Search CVEs for a specific vendor/product with KEV cross-referencing for actively exploited vulns.

```
Show Microsoft Windows vulnerabilities
```

Parameters: `vendor` (required), `product` (optional), `limit`

## Data Sources

- **NIST NVD 2.0** — National Vulnerability Database (CVE details, CVSS scores)
- **CISA KEV** — Known Exploited Vulnerabilities catalog
- **FIRST.org EPSS** — Exploitation Prediction Scoring System
- **MITRE ATT&CK** — Adversary techniques and tactics (172 CVEs mapped to 42 techniques)

## Use Cases

- Vulnerability triage and prioritization
- Compliance tracking (CISA KEV deadlines)
- Vendor risk assessments
- Threat intelligence briefings
- Patch management decisions

All data from free US government APIs. Zero cost. No API keys required.
