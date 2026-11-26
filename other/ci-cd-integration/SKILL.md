---
name: ci-cd-integration
description: Guide for agents to help users integrate NightVision DAST scanning into CI/CD pipelines. Use when setting up security scans in GitHub Actions, GitLab CI, Azure DevOps, Jenkins, BitBucket, or JFrog pipelines, configuring NightVision tokens, creating targets, running scans, exporting results as SARIF/CSV, or detecting API breaking changes.
allowed-tools: Bash
---

# NightVision CI/CD Integration

Use this skill when helping users add NightVision security scanning to their CI/CD pipelines. NightVision is a white-box-assisted DAST tool that finds exploitable vulnerabilities in web applications and REST APIs. It combines Source Intelligence (reads source code to extract OpenAPI specs) with dynamic scanning (ZAP + Nuclei engines), and traces vulnerabilities back to exact source code locations (Code Traceback).

## Agent workflow

When a user asks to set up NightVision in their pipeline:

1. **Check prerequisites** — verify the NightVision CLI is available (`nightvision --help`). If not installed, see the Installation section below.
2. **Examine the repo** — look for existing CI configs (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`) to understand the CI platform and existing pipeline structure
3. **Ask the user** what you can't determine from the repo:
   - Target URL (staging/production endpoint to scan)
   - Target type — web app or API?
   - Does the app require authentication to scan?
   - What language is the backend? (needed for Source Intelligence)
   - Have they already created a NightVision project, target, and token?
4. **Tell the user what they must do locally** — some steps require interactive browser sessions that the agent cannot perform (see Prerequisites below)
5. **Generate the pipeline config** — adapt the patterns below and the platform-specific examples in [references/ci-platforms.md](references/ci-platforms.md) to the user's repo, substituting their target name, language, app startup method, and CI platform conventions

**Related skills:** Use `scan-configuration` for detailed target/auth setup, `source-intelligence` for spec extraction details, `scan-triage` for interpreting results.

## Pipeline structure

Every NightVision CI pipeline follows this pattern:

```
1. Install the NightVision CLI
2. Extract API spec from source code (API targets only)
3. Start the application (private/local targets only)
4. Run the scan (CLI polls until completion, ~5-15 min)
5. Export results (SARIF / CSV / GitLab DAST)
6. Upload to CI platform (GitHub Security, GitLab DAST, Azure Boards, Jenkins Warnings)
```

## Prerequisites the user must complete

These steps require interactive sessions (browser login, GUI) that the agent cannot perform. Instruct the user to run these locally before the pipeline will work.

**1. Create an API token** — requires browser-based login:
```bash
nightvision login
nightvision token create                          # no expiry
nightvision token create --expiry-date 2026-12-31 # with expiry
```
Tokens can also be created in the NightVision web UI: Profile > Settings > Tokens. The user must store the token as a CI secret named `NIGHTVISION_TOKEN`.

**2. Record authentication** (if the target requires login) — Playwright recording opens a browser:
```bash
nightvision auth playwright create my-auth https://myapp.example.com
# A Chrome window opens — user completes login, then closes the window
```
For API key / bearer token auth, the agent can help construct the command:
```bash
nightvision auth headers create my-auth \
  -H "Authorization: Bearer <token>"
```

**3. Create the target** — the agent can help with this if `NIGHTVISION_TOKEN` is available:
```bash
# Web target
nightvision target create my-web-app https://staging.example.com --type WEB -p my-project

# API target with local spec
nightvision target create my-api https://api.example.com --type API -p my-project \
  --spec-file openapi-spec.yml

# API target with remote spec URL
nightvision target create my-api https://api.example.com --type API -p my-project \
  --spec-url https://api.example.com/docs/openapi.json

# Idempotent create-or-update (useful in pipelines)
nightvision target create my-api $URL --type API -p my-project --spec-file spec.yml \
  || nightvision target update my-api -p my-project --spec-file spec.yml
```

## Installation (in the pipeline)

```bash
# Linux Intel (standard for most CI runners)
curl -L https://downloads.nightvision.net/binaries/latest/nightvision_latest_linux_amd64.tar.gz | tar -xz
sudo mv nightvision /usr/local/bin/
```

For Linux ARM runners, substitute `linux_arm64` in the URL.

## Environment variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `NIGHTVISION_TOKEN` | Yes | API token (store as CI secret) |
| `NIGHTVISION_API_URL` | No | API endpoint (default: `https://api.nightviz.ai/api/v1/`) |

This API default applies to CLI 0.26.0 and later. Earlier releases default to `https://api.nightvision.net/api/v1/`; upgrade before configuring a `nightviz.ai` API host.

All config keys accept env vars with the `NIGHTVISION_` prefix (hyphens become underscores).

## CLI output format

Most `list` and `get` commands default to text output. Use `--format json` (or `-F json`) for machine-parseable output, or `--format table` for tabular display.

## Source Intelligence (spec extraction from source code)

For API targets, extract OpenAPI specs from source with Source Intelligence. Supports C#, Go, Java, JavaScript/TypeScript, PHP, Python and Ruby; project roots and languages are detected automatically, so `--lang` is only needed to restrict a run.

```bash
# Extract and upload to a target
nightvision openapi extract . -t my-api -p my-project

# Extract without a target (e.g. for a spec diff)
nightvision openapi extract . -o openapi-spec.yml --no-target

# Compare specs for breaking changes (useful in PR checks)
nightvision openapi diff old-spec.yml new-spec.yml
```

**Important CI pattern — extraction fallback:** Extraction exits non-zero when it finds no routes, for example on an unsupported framework, and also when the spec was written but the upload failed. Fall back to a backup spec only when no spec was written, keep `openapi-spec.diagnostics.json` as a build artifact, and print why the fallback was taken.
```bash
if ! nightvision openapi extract . -t $TARGET; then
  if [ -e openapi-spec.yml ]; then
    echo "Spec extracted but the upload failed; keeping openapi-spec.yml"
  else
    echo "Source Intelligence produced no spec; see openapi-spec.diagnostics.json"
    cp backup-openapi-spec.yml openapi-spec.yml
  fi
fi
```

### Code Traceback

When Source Intelligence generates the spec, it annotates endpoints with file paths and line numbers. Vulnerabilities found during scanning trace back to exact source locations. This powers the file/line links in GitHub Security Alerts, Azure Boards work items, and similar CI integrations.

## Running scans

```bash
# Basic scan
nightvision scan my-target -p my-project

# Authenticated scan: gate on the login first, so a broken login fails the job
# instead of producing a quiet, mostly-public scan
nightvision scan my-target -p my-project --auth my-auth --login-check
nightvision scan my-target -p my-project --auth my-auth

# Unauthenticated (explicit, skip any stored credentials)
nightvision scan my-target -p my-project --no-auth

# Extended duration (default 30 min, max 480 min / 8 hours); use 120 for web apps
nightvision scan my-target -p my-project --max-duration-minutes 120

# Engine selection
nightvision scan my-target -p my-project --no-nuclei   # ZAP only
nightvision scan my-target -p my-project --no-zap      # Nuclei only

# Verbose logging (recommended for CI debugging)
nightvision scan my-target -p my-project --verbose
```

### Capturing the scan ID

In CI (non-interactive), the CLI prints the scan ID as the first line of stdout. Use this pattern:

```bash
nightvision scan $TARGET --auth $AUTH > scan-results.txt
SCAN_ID=$(head -n 1 scan-results.txt)
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Scan completed successfully (`SUCCEEDED`). Vulnerabilities may still have been found. |
| 1 | Scan failed (`FAILED`, `ABORTED`, `TIMED_OUT`), or other error. |

**Exit code 0 does not mean "no vulnerabilities."** Use export commands to inspect findings.

On failure (exit code 1), the CLI prints a status-specific error message:
- **TIMED_OUT** — includes the configured `--max-duration-minutes` value and suggests increasing it
- **ABORTED** — indicates the scan was aborted (by user or system)
- **FAILED** — includes a link to the dashboard for investigation

When the API provides a failure reason, it is included in the error message and displayed in the TUI dashboard.

### Private / internal targets (Smart Proxy)

NightVision's Smart Proxy automatically tunnels scan traffic through the CLI when the target is not publicly reachable (localhost, Docker, Kubernetes, corporate networks). No configuration needed — it's built into the CLI.

Use `--force-private-scan` to force tunneling when the target appears publicly accessible but isn't from the scanner's perspective.

## Exporting results

```bash
# SARIF with Code Traceback (API targets — provide the spec used for the scan)
nightvision export sarif -s "$SCAN_ID" --swagger-file openapi-spec.yml -o results.sarif

# SARIF without Code Traceback (WEB targets, or when no spec is available)
nightvision export sarif -s "$SCAN_ID" -o results.sarif

# CSV (for reports, spreadsheets, custom processing)
nightvision export csv -s "$SCAN_ID" -o results.csv

# GitLab DAST report (for the GitLab Vulnerability dashboard)
nightvision export gitlab -s "$SCAN_ID" --swagger-file openapi-spec.yml -o gl-dast-report.json

# Jira tickets (one per finding; severity sets priority; status changes sync back to findings)
# --jira-token is a classic user API token. For an Atlassian service-account token
# (always scoped), pass --jira-cloud-id <id> instead of --base-url (scopes: read:jira-work, write:jira-work).
nightvision export jira -s "$SCAN_ID" --project-key SEC \
  --base-url https://your-org.atlassian.net --user-email you@example.com --jira-token "$JIRA_TOKEN"
```

`--swagger-file` is optional. When provided, SARIF output includes Code Traceback source annotations (file paths and line numbers linking findings to source code). When omitted, the SARIF is still valid but won't contain source locations. Always provide `--swagger-file` for API targets when the spec is available.

## Failing the build on findings (the merge gate)

Uploading SARIF surfaces findings but does not stop a merge. To block a merge on serious, unresolved findings, count them and exit non-zero. The scan's own exit code cannot do this: exit 0 means the scan ran, not that it was clean (see Exit codes).

Filter the SARIF to the findings that should block, then count what is left:

```bash
# Keep only open critical and high findings: drop lower severities, and drop
# anything already triaged away (resolved, false positive, won't fix).
nightvision export sarif -s "$SCAN_ID" --openapi-file openapi-spec.yml \
  --exclude-severity info,low,medium,unknown,unspecified \
  --exclude-resolution resolved,false_positive,wont_fix \
  -o gate.sarif

COUNT=$(jq '[.runs[].results[]] | length' gate.sarif)
echo "Open critical/high findings: $COUNT"
if [ "$COUNT" -gt 0 ]; then
  echo "NightVision gate failed: $COUNT open critical/high finding(s). See the Security tab or the NightVision dashboard."
  exit 1
fi
```

Points that matter:

- **Export the full SARIF for the Security tab, and a separate filtered copy for the gate.** Upload the unfiltered `results.sarif` so developers still see every finding; count `gate.sarif` to decide pass or fail. Do not gate on the file you uploaded, or lower-severity findings vanish from the dashboard.
- **`--exclude-resolution` is what makes the gate livable.** Once AppSec marks a finding false positive or accepts the risk in NightVision, it stops failing the build, with no code change and no inline-suppression file to maintain. Keep `resolved,false_positive,wont_fix` excluded so a triaged finding does not re-break the pipeline.
- **Set the bar deliberately.** Excluding `info,low,medium,unknown,unspecified` leaves critical and high. To gate on high and above only, that is already the line; to include medium, drop `medium` from the exclude list.
- **`jq` counts `.runs[].results[]`** across every run in the file, so it is correct whether the scan produced one run or several. If `jq` is not on the runner, `grep -c '"ruleId"' gate.sarif` is a rough fallback, but install `jq` for an exact count.

### Blocking a merge when app code changed but no scan ran

The gate above assumes a scan ran. The other half, a PR that changes application code and merges with no scan at all, is enforced by the CI platform, not the CLI: make the scan job a **required status check** and trigger it on the paths that hold app code, so the check must run and pass before merge.

GitHub Actions example:

```yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - 'api/**'
      - '!**/*.md'
```

Then mark the job's check required in branch protection (Settings > Branches > Branch protection rule > Require status checks to pass). A PR that touches those paths cannot merge until the scan job succeeds, and the gate step above makes "succeeds" mean "no open critical/high findings." A PR that touches none of them skips the scan, so docs-only and config-only changes are not blocked.

GitLab's equivalent is a `rules:` clause keyed on `changes:` plus a protected-branch merge check; the pattern is the same, path-trigger the scan and require it.

The NightVision Claude Code plugin ships a Stop hook that nudges the agent to run `ship-check` when app code changed without a scan. That hook is a reminder on the developer's machine; this required check is the enforcement in CI. Use both: the hook catches it early, the check catches it at the gate.

## CI platform quick reference

See [references/ci-platforms.md](references/ci-platforms.md) for complete, copy-pasteable pipeline configs.

| Platform | Results surface | Upload mechanism |
|----------|----------------|-----------------|
| GitHub Actions | Security tab (Code Scanning) | `github/codeql-action/upload-sarif@v3` (needs `permissions: contents: read, security-events: write`) |
| GitLab CI | Vulnerability dashboard | `nightvision export gitlab`, `artifacts.reports.dast` |
| Azure DevOps | Azure Boards work items | `sarif-manager azure create-work-items` |
| Jenkins | Warnings Next Generation | `recordIssues tool: sarif(pattern: 'results.sarif')` |
| BitBucket | Pipeline artifacts | SARIF as artifact |
| JFrog | Evidence on Docker packages | `jf evd create` with SARIF predicate |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "login authentication token has expired" | Token expired or invalid | `nightvision token create`, update CI secret |
| "API is unreachable" | Network/firewall issue | Check `NIGHTVISION_API_URL`, network connectivity |
| "SSL certificate error" | TLS verification failed | Fix certs, or `--skip-tls-verify` (not for production) |
| Scan `TIMED_OUT` | Exceeded max duration | CLI error message shows the current limit; increase `--max-duration-minutes` (up to 480) |
| Scan `ABORTED` | Scan was cancelled by user or system | Check the failure reason in the CLI output or dashboard |
| Scan `FAILED` | Engine error or target unreachable | CLI error includes a dashboard link; also use `--verbose` and verify target is up |
| 401 Unauthorized during scan | Auth credentials expired | Re-record authentication locally |
| "Repository not found" in checkout | `permissions` block missing `contents: read` | Add `contents: read` alongside `security-events: write` in the workflow permissions |
