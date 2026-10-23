---
name: zap-baseline
description: "Configures and runs OWASP ZAP baseline scanning: `zap-baseline.py` Docker-packaged spider + passive scan suitable for CI gating; supports `-t target_url` + `-r html_report` + `-c config_file` rule customization (INFO/IGNORE/FAIL warnings) and Ajax spider via `-j` for JS-heavy SPAs; `zap-full-scan.py` active companion for staging. Covers authenticated scans end to end as a reference - ZAP Context, auth methods (form/JSON/script/browser), session management, verification strategy, OAuth/bearer injection, context XML export for `-n` - plus DAST cadence planning (PR-blocking passive baseline, nightly ZAP full + nuclei active layer, baseline-finding ratchet for legacy apps). Use when the user runs OWASP ZAP for pre-prod web app DAST, needs coverage of routes behind a login wall, or is designing a team's DAST rollout cadence."
---

# zap-baseline

## Overview

Per [zaproxy.org/docs/docker/baseline-scan/][zap-base]:

[zap-base]: https://www.zaproxy.org/docs/docker/baseline-scan/

> "The ZAP Baseline scan is a script that is available in the ZAP
> Docker images. It runs the ZAP spider against the specified
> target for (by default) 1 minute and then waits for the passive
> scanning to complete before reporting the results."

The baseline scan is **passive only** - non-intrusive, safe for
production. The companion `zap-full-scan.py` adds active scanning
(injection probes, XSS payloads) and is **NOT** safe for
production; reserve for staging.

## When to use

- The repo deploys a web app + needs pre-prod DAST gate.
- A CI workflow needs a non-intrusive scan that's safe to point at
  a deployed staging environment.
- The team uses OWASP ZAP (de facto OSS DAST) over commercial
  alternatives.
- The app's interesting routes sit behind a login wall
  ([references/auth.md](references/auth.md)).
- The team is designing its DAST rollout cadence from scratch
  ([references/cadence.md](references/cadence.md)).

## Step 1 - Install

ZAP baseline runs from the official Docker image - no host install
needed. Per [zap-base][zap-base]:

```bash
docker pull ghcr.io/zaproxy/zaproxy:stable
```

Image variants:

| Tag | Use |
|---|---|
| `:stable` | Production-grade; pin in CI |
| `:weekly` | Latest features; for evaluation |
| `:bare` | Headless minimal; smallest |

## Step 2 - First baseline scan

Per [zap-base][zap-base] (verbatim):

```bash
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
    -t https://www.example.com -r testreport.html
```

The `-v $(pwd):/zap/wrk/:rw` mount makes the report writable to the
host directory. The report file lands at `./testreport.html` after
the scan.

## Step 3 - Common flags

Per [zap-base][zap-base]:

| Flag | Use |
|---|---|
| `-t URL` | Target URL (required) |
| `-r FILE` | HTML report output |
| `-w FILE` | Markdown report |
| `-x FILE` | XML report |
| `-J FILE` | JSON report (for finding triage) |
| `-c FILE` | Config file: rule INFO/IGNORE/FAIL behavior |
| `-P PORT` | Specify ZAP listen port |
| `-j` | Use Ajax spider in addition to traditional spider (JS-heavy apps) |
| `-m MINS` | Spider duration in minutes (default 1) |
| `-d` | Show debug messages |
| `-I` | Don't return failure on warning (gate softly) |
| `-n CONTEXT_FILE` | Authenticated scan context file |

## Step 4 - Authenticated scans

For apps requiring login, export a ZAP context file from the GUI
(Sites → right-click → Export Context). The context file encodes:

- Auth method (form / script / HTTP / OAuth)
- Login URL + creds (referenced env vars; never hardcode)
- Session-management strategy
- Logged-in / logged-out indicators

Building that context from scratch - choosing the auth method, wiring
session management, calibrating verification indicators, CSRF and
OAuth/bearer handling - is walked end to end in
[references/auth.md](references/auth.md). Then:

```bash
docker run -v $(pwd):/zap/wrk/:rw \
  -e ZAP_AUTH_USERNAME=$USER \
  -e ZAP_AUTH_PASSWORD=$PASS \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://app.example.com -n /zap/wrk/context.xml -J report.json
```

## Step 5 - Active scan companion (`zap-full-scan.py`)

For staging-only deeper analysis:

```bash
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t https://staging.example.com -J report.json
```

`zap-full-scan.py` triggers active payloads (SQLi probes, XSS,
SSRF). **NEVER point at production** - risk of data corruption +
generates audit-log noise.

## Step 6 - False-positive triage (MANDATORY)

Per [zap-base][zap-base], rule customization via `-c config_file`
where each line is `<rule_id>\t<INFO|WARN|IGNORE|FAIL>\t<URL_pattern>`:

Example `zap-config.tsv`:

```
10049	IGNORE	*	# Cookie No HttpOnly: legacy session cookie; tracked in JIRA-1234
40012	WARN	https://app.example.com/admin/*	# XSS: legacy admin pages; not exposed to users
10063	FAIL	*	# Permissions Policy: must be set on all responses
```

Three suppression layers:

| Mechanism | Example | When to use |
|---|---|---|
| Per-rule config TSV | `<rule_id>\tIGNORE\t*` | Rule disabled globally |
| Per-URL pattern | `<rule_id>\tWARN\thttps://app/admin/*` | Rule downgraded for known-old code path |
| Context exclusion | `<exclude_from_context>` in context XML | Whole URL trees out of scope |
| `-I` flag | `zap-baseline.py -I ...` | Soft gate: warns but exits 0 |

**Justification template (mandatory in config):**

```
# Rule 10049 (Cookie No HttpOnly)
# Suppressed: 2026-05-15 by alice@example.com
# Reason: legacy session cookie; tracked in JIRA-1234; expires 2026-09-15
# Re-review-date: 2026-09-15
10049	IGNORE	*
```

Cadence: every quarter, audit the config TSV - every IGNORE entry
should have an Re-review-date. Past-due entries are removed +
re-evaluated.

## Step 7 - Output formats for cross-tool triage

```bash
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://app.example.com -J zap-report.json
```

The JSON report feeds cross-tool aggregation.
For SARIF output (GitHub Code Scanning), use a converter (zap-sarif
container action).

## Step 8 - CI integration

GitHub Actions:

```yaml
jobs:
  zap-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: zaproxy/action-baseline@v0.13.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-J zap-report.json'
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: zap-report, path: zap-report.json }
```

The official `zaproxy/action-baseline` action wraps the Docker
invocation. Auto-creates a GitHub Issue on failure.

Designing the full team cadence around this job - PR-blocking passive
baseline, nightly ZAP full + nuclei active layer, the baseline-finding
ratchet for legacy apps, dedup, and coverage measurement - is in
[references/cadence.md](references/cadence.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Run `zap-full-scan.py` against production | Active payloads pollute / damage data | Staging-only (Step 5) |
| Skip `-J` JSON output | Can't feed finding triage; report is HTML-only | Always pass `-J` (Step 7) |
| Ignore Ajax spider for SPAs | Missing routes; coverage gap | Add `-j` flag (Step 3) |
| Hardcode credentials in context file | Secrets leak in repo | Reference env vars (Step 4) |
| Suppress without `# Re-review-date` | Permanent debt | Required template (Step 6) |

## Limitations

- Baseline is passive only; full-scan needed for active probes
  but is not safe in production.
- Spider duration default 1 min may miss deep-routes apps;
  increase via `-m` (Step 3).
- ZAP scans single-target only; for multi-app fleet, run per-app
  + aggregate via cross-tool triage.
- Authentication setup via context file is fragile - 
  apps with complex login flows often need custom ZAP scripts
  ([references/auth.md](references/auth.md)).

## References

- [zap-base][zap-base] - official baseline scan documentation
- zaproxy.org/docs/docker - full Docker docs
- github.com/zaproxy/action-baseline - official GHA action
- Authenticated-scan setup (context, auth methods, session management,
  verification): [references/auth.md](references/auth.md)
- Layered DAST cadence (PR baseline → nightly active, ratchet, dedup):
  [references/cadence.md](references/cadence.md)
- `nuclei-dast` - sister DAST tool (template-driven scanning)
