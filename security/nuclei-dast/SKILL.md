---
name: nuclei-dast
description: "Installs and runs ProjectDiscovery Nuclei template-based HTTP scanning: selects templates via `-t {path}` and `-tags`/`-severity` filters, controls request rate with `-rl`, emits JSONL output via `-j` for cross-tool finding aggregation, authors custom YAML matchers for app-specific checks, and gates CI on severity thresholds. Use when the team runs Nuclei alongside ZAP for template-driven DAST coverage, needs fuzzing-style probes beyond ZAP passive scan, or wants to operationalize community CVE templates in a pipeline."
metadata:
  keywords: "nuclei, dast, templates, cve, security, jsonl, ci"
  version: "1.3.9"
---

# nuclei-dast

## Overview

Per [docs.projectdiscovery.io/tools/nuclei/overview][nuclei-overview]:

> "Nuclei is a fast and customisable vulnerability scanner powered by simple
> YAML-based templates."

[nuclei-overview]: https://docs.projectdiscovery.io/tools/nuclei/overview

Each template is a YAML file defining a request plus matchers that decide whether
the response is a finding. The community library ships 6,500+ templates for CVEs,
misconfigurations, exposed panels, and default credentials; custom templates add
app-specific checks. Run it alongside ZAP - ZAP crawls for broad coverage, Nuclei
adds deep template-driven CVE checks - and feed both into cross-tool triage.

## When to use

- The repo needs CVE-specific or misconfiguration checks beyond ZAP passive scan.
- A CI pipeline should gate on `critical`/`high` template matches without active
  spider coverage.
- The team maintains custom YAML templates for proprietary endpoints.
- Nuclei output must be unified with ZAP findings via cross-tool aggregation.

## Step 1 - Install

Per [docs.projectdiscovery.io/tools/nuclei/install][nuclei-install]:

[nuclei-install]: https://docs.projectdiscovery.io/tools/nuclei/install

**Go (recommended for CI):**

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

Requires the latest Go toolchain version.

**Homebrew (macOS/Linux):**

```bash
brew install nuclei
```

**Docker:**

```bash
docker pull projectdiscovery/nuclei:latest
```

**Precompiled binary:** download from
[github.com/projectdiscovery/nuclei/releases](https://github.com/projectdiscovery/nuclei/releases)
and place on `PATH`.

After install, update the default template library:

```bash
nuclei -update-templates
```

## Step 2 - First scan

Per [docs.projectdiscovery.io/tools/nuclei/running][nuclei-running]:

[nuclei-running]: https://docs.projectdiscovery.io/tools/nuclei/running

```bash
nuclei -u https://staging.example.com -j -o nuclei-report.jsonl
```

`-j` writes JSONL output; `-o` names the file. Each line is one finding, ready
for cross-tool aggregation. The default template set is applied; DOS-capable
templates are excluded from the default run (see Step 6).

## Step 3 - Common flags

Per [nuclei-running][nuclei-running]. The flags used in most scans:

| Flag | Default | Use |
|---|---|---|
| `-u <url>` | (required) | Single target URL or host |
| `-t <path>` | community templates | Template file or directory |
| `-tags <tag,...>` | - | Run only templates with matching tags |
| `-severity <level,...>` | - | Filter by `info`, `low`, `medium`, `high`, `critical` |
| `-rl <int>` | 150 | Max requests per second |
| `-j` / `-jsonl` | off | JSONL output (feeds triager) |
| `-o <file>` | stdout | Output file path |
| `-validate` | off | Syntax-check templates without running |

Full flag reference (target lists, exclusions, concurrency, timeouts, SARIF,
debug): [references/flags.md](references/flags.md).

Per [nuclei-running][nuclei-running], `-rl` caps request rate regardless of the
`-c` and `-bs` concurrency settings.

## Step 4 - Severity filtering and CI gating

Run only `high` and `critical` templates for a fast CI gate:

```bash
nuclei -u https://staging.example.com \
  -severity high,critical \
  -rl 50 \
  -j -o nuclei-critical.jsonl
```

Then count findings and gate:

```bash
count=$(wc -l < nuclei-critical.jsonl)
if [ "$count" -gt 0 ]; then
  echo "FAIL: $count critical/high findings" >&2
  exit 1
fi
```

For a softer gate (fail on `critical` only, warn on `high`):

```bash
nuclei -u https://staging.example.com -severity critical -j -o nuclei-crit.jsonl
nuclei -u https://staging.example.com -severity high    -j -o nuclei-high.jsonl
```

Run both, fail CI on any line in `nuclei-crit.jsonl`, log `nuclei-high.jsonl`
as advisory.

## Step 5 - Template selection

Per [docs.projectdiscovery.io/templates/introduction][template-intro] and
[docs.projectdiscovery.io/templates/structure][template-struct]:

[template-intro]: https://docs.projectdiscovery.io/templates/introduction
[template-struct]: https://docs.projectdiscovery.io/templates/structure

Community templates are organized by tag. Common tags include `cve`, `rce`,
`sqli`, `xss`, `misconfig`, `exposure`, `default-login`.

Run all CVE templates:

```bash
nuclei -u https://staging.example.com -tags cve -j -o nuclei-cves.jsonl
```

Run a specific template file:

```bash
nuclei -u https://staging.example.com -t nuclei-templates/cves/2024/CVE-2024-1234.yaml
```

Run all templates in a local directory:

```bash
nuclei -u https://staging.example.com -t ./custom-templates/ -j -o nuclei-custom.jsonl
```

List templates that would run without executing:

```bash
nuclei -tl -tags misconfig -severity high,critical
```

## Step 6 - Custom YAML templates

Per [template-struct][template-struct], every template requires: a unique `id`,
an `info` block, and at least one protocol request with matchers.

Minimal HTTP template:

```yaml
id: custom-debug-endpoint

info:
  name: Debug Endpoint Exposed
  author: your-team
  severity: high
  description: "Detects an exposed /debug endpoint returning sensitive runtime info."
  tags: exposure,custom

http:
  - method: GET
    path:
      - "{{BaseURL}}/debug"
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      - type: word
        words:
          - "goroutine"
          - "heap"
        condition: or
```

Matcher types per [template-intro][template-intro]:

| Type | Matches against |
|---|---|
| `word` | Response body or headers contain literal string(s) |
| `regex` | Response body matches a regular expression |
| `status` | HTTP response status code |
| `dsl` | Boolean expression using Nuclei DSL functions |

Validate before running:

```bash
nuclei -t ./custom-templates/custom-debug-endpoint.yaml -validate
```

## Step 7 - JSONL output for cross-tool triage

Each JSONL line represents one match. Key fields:

```json
{
  "template-id": "cve-2024-1234",
  "info": { "name": "...", "severity": "high", "tags": ["cve"] },
  "host": "https://staging.example.com",
  "matched-at": "https://staging.example.com/vulnerable-path",
  "timestamp": "2026-06-04T12:00:00Z"
}
```

Feed the JSONL to cross-tool aggregation:

```bash
nuclei -u https://staging.example.com -j -o nuclei-report.jsonl
# aggregate nuclei-report.jsonl alongside zap-report.json
```

For SARIF output (GitHub Code Scanning):

```bash
nuclei -u https://staging.example.com -se nuclei.sarif
```

## Step 8 - Rate limiting and responsible use

Per [nuclei-running][nuclei-running], the default rate is 150 req/s. Nuclei
generates several thousand requests when the full template set runs against a
single target. Per the [Nuclei FAQ][nuclei-faq]:

[nuclei-faq]: https://docs.projectdiscovery.io/tools/nuclei/faq

> "After detecting a security issue we always recommend that you validate it a
> second time before reporting it." Use `-debug` to confirm the matcher fired
> against the expected response content.

DOS-capable templates are tagged and excluded from default scans. To run them
explicitly (staging only, never production):

```bash
nuclei -u https://staging.example.com -tags dos -rl 5
```

Default-safe limits for shared infrastructure:

```bash
nuclei -u https://staging.example.com -rl 30 -c 10 -bs 10
```

**Only scan targets you are authorized to test.** Nuclei is an active probe
tool; running it against a target without authorization may violate computer
abuse laws.

## Step 9 - CI integration

Install Nuclei, update templates, run a severity-gated scan, then fail the job on
any finding:

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -update-templates
nuclei -u "$STAGING_URL" -severity high,critical -rl 50 -j -o nuclei-report.jsonl
[ "$(wc -l < nuclei-report.jsonl)" -eq 0 ]
```

Full GitHub Actions workflow (checkout, artifact upload, SARIF upload to Code
Scanning): [references/ci-integration.md](references/ci-integration.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Run all templates against production | Active probes may trigger WAF blocks, corrupt data, or run DOS-tagged templates | Staging only; use `-etags dos` on shared envs |
| Skip `-j` / `-jsonl` output | Findings are stdout-only; can't feed the finding-triage step | Always pass `-j -o <file>` (Step 7) |
| Skip `-rl` in CI on shared infra | Default 150 req/s spikes load on shared staging | Set `-rl 30` or lower (Step 8) |
| Run `-validate` only, skip a real scan | Syntax passes but matchers may produce no output | Always run a real scan against a known-vulnerable target to confirm match |
| Suppress findings without a tracked justification | Invisible risk debt | Use an IGNORE list with date + ticket, same pattern as ZAP config TSV (see `zap-baseline` Step 6) |
| Treat `info` severity as noise | `info` templates surface exposed panels, paths, and tech stack - useful for reconnaissance hardening | Route `info` findings to finding triage, not direct suppression |

## Limitations

- Nuclei is active: every template sends at least one HTTP request. It is not
  safe to run the full template set against production.
- Template coverage is only as current as the last `nuclei -update-templates`;
  pin template versions in CI to avoid scan variance between runs.
- Matchers are per-template; a misconfigured custom template silently returns
  no findings. Always `-validate` and smoke-test against a known-vulnerable
  endpoint before trusting zero-finding output.
- Nuclei does not spider the target; it probes specific paths defined in
  templates. Use alongside ZAP for crawl-based coverage.
- `-rl` controls outbound rate but not the total request count; large template
  sets against a slow target may run for tens of minutes.

## References

- [nuclei-overview][nuclei-overview] - official Nuclei overview
- [nuclei-install][nuclei-install] - installation methods
- [nuclei-running][nuclei-running] - CLI flags reference (rate limiting, output, filters)
- [template-intro][template-intro] - template introduction and matcher types
- [template-struct][template-struct] - YAML template structure and info block fields
- [nuclei-faq][nuclei-faq] - validation and responsible use guidance
- github.com/projectdiscovery/nuclei-templates - community template library
- `zap-baseline` - companion passive DAST scanner
- `zap-baseline` cadence reference - layered DAST cadence (baseline + nightly active + nuclei)
