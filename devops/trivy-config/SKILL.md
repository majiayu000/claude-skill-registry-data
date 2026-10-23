---
name: trivy-config
description: "Runs Trivy's misconfiguration scanner (`trivy config`) against IaC directories to detect security issues across Terraform, CloudFormation, Kubernetes manifests, Helm charts, Dockerfiles, and Azure ARM templates - installs Trivy, scans with severity gating via `--exit-code`, suppresses findings via `.trivyignore` / `.trivyignore.yaml` or inline annotations, extends built-in checks with custom Rego policies, and emits SARIF for GitHub Code Scanning. Trivy is the tfsec successor - the forward path from tfsec per Aqua Security's own migration guidance - and the legacy tfsec workflow (install, custom YAML rules, ignore annotations, migration steps) is kept in references/tfsec-legacy.md. Use when adopting a consolidated IaC scanner for new projects, migrating away from tfsec (or still operating a Terraform-only tfsec stack), or scanning mixed IaC stacks with a single tool."
metadata:
  keywords: "trivy, iac, misconfiguration, terraform, kubernetes, dockerfile, helm, cloudformation, rego, sarif, security"
  version: "1.1.18"
---

# trivy-config

## Overview

[mc]: https://trivy.dev/latest/docs/scanner/misconfiguration/
[inst]: https://trivy.dev/docs/latest/getting-started/installation/
[cli]: https://trivy.dev/latest/docs/references/configuration/cli/trivy_config/
[custom]: https://trivy.dev/latest/docs/scanner/misconfiguration/custom/
[filter]: https://trivy.dev/latest/docs/configuration/filtering/
[report]: https://trivy.dev/latest/docs/configuration/reporting/
[checks]: https://github.com/aquasecurity/trivy-checks
[tfsec]: references/tfsec-legacy.md

Trivy is Aqua Security's consolidated misconfiguration scanner (`trivy
config`) and the forward path from tfsec. Per the
[tfsec legacy reference][tfsec], [trivy.dev misconfiguration docs][mc], and
Aqua's own documentation, new projects should evaluate Trivy first; tfsec's
checks ship inside Trivy under `trivy config`.

## Pinned versions

Bump these together when updating; they are the only version-sensitive
tokens in this skill. GitHub release assets are version-stamped, so the
RPM URL in Step 1 pins a tag rather than using `latest/download`.

| Component | Pin | Used in |
|---|---|---|
| Trivy | v0.72.0 (latest as of 2026-06-30) | Step 1 install |
| `aquasecurity/trivy-action` | 0.31.0 | CI workflow (Step 7) |
| `actions/checkout` | v5 | CI workflow (Step 7) |
| `github/codeql-action/upload-sarif` | v3 | CI workflow (Step 7) |

## Step 1 - Install

Per [trivy.dev installation docs][inst]:

```bash
# macOS
brew install trivy

# Docker (no local install)
docker run --rm -v $(pwd):/workspace aquasec/trivy config /workspace
```

Debian / Ubuntu and RHEL / Fedora hosts can also install Trivy from the
project's apt repository or a release `.rpm` package (pin the tag from the
Pinned versions section above), per [inst]. Both add a system package
source and need root, so bake them into the runner image or config
management rather than running them from a scan session. In CI, use the
pinned `aquasecurity/trivy-action` from Step 7 instead.

Verify: `trivy --version`.

## Step 2 - First scan

Per [cli reference][cli], `trivy config` accepts a path (file or
directory). Trivy auto-detects IaC types - Terraform, CloudFormation,
Kubernetes manifests, Helm charts, Dockerfiles, and Azure ARM templates
can all coexist in the same directory per [mc docs][mc].

```bash
# Scan the current directory (all IaC types)
trivy config .

# Scan a specific subdirectory
trivy config ./infra/

# Show only HIGH and CRITICAL findings
trivy config --severity HIGH,CRITICAL .

# Fail CI when any finding is found (exit code 1)
trivy config --exit-code 1 --severity HIGH,CRITICAL .

# Include passed checks alongside failures
trivy config --include-non-failures .
```

Built-in checks are distributed as an OPA bundle at
`ghcr.io/aquasecurity/trivy-checks` (per [checks repo][checks]).
Trivy caches the bundle locally and refreshes every 24 hours. An
embedded fallback is included in the binary for air-gapped environments.

## Step 3 - Severity gating

Per [cli reference][cli], `--exit-code` and `--severity` are the two
levers for CI gating:

| Flag | Purpose | Example |
|------|---------|---------|
| `--exit-code int` | Exit code when findings match | `--exit-code 1` |
| `--severity strings` | Comma-separated severity filter | `HIGH,CRITICAL` |

Pattern: gate hard on `CRITICAL` first; expand to `HIGH` after the
team has reviewed the initial finding set.

```bash
# Hard fail on CRITICAL only (bootstrap phase)
trivy config --exit-code 1 --severity CRITICAL .

# Ratchet: add HIGH once existing findings are triaged
trivy config --exit-code 1 --severity HIGH,CRITICAL .
```

## Step 4 - Output formats

Per [trivy.dev reporting docs][report], `--format` accepts:

| Value | Use case |
|-------|---------|
| `table` (default) | Human-readable terminal output |
| `json` | Machine-parseable; pipe to `jq` |
| `sarif` | GitHub Code Scanning / SARIF 2.1.0 |
| `template` | Custom templates (JUnit, ASFF, HTML via `contrib/`) |

```bash
# JSON for parsing / badge generation
trivy config --format json --output trivy.json .

# SARIF for GitHub Code Scanning
trivy config --format sarif --output trivy.sarif .

# JUnit XML for CI test reporting
trivy config --format template \
  --template "@contrib/junit.tpl" \
  --output trivy-junit.xml .
```

## Step 5 - Suppressing findings

Per [trivy.dev filtering docs][filter]:

### .trivyignore (check-ID list)

```
# .trivyignore
# Suppress a specific misconfig check
AVD-DS-0002

# Suppress a CVE alongside a misconfig in the same file
CVE-2018-14618
```

### .trivyignore.yaml (structured suppression)

Per [filter docs][filter], the YAML variant supports scoped expiring
suppressions:

```yaml
# .trivyignore.yaml
misconfigurations:
  - id: AVD-DS-0001
  - id: AVD-DS-0002
    paths:
      - "infra/legacy/Dockerfile"
    statement: "Legacy image; migration tracked in JIRA-4321"
    expired_at: "2026-12-31"
```

Run with: `trivy config --ignorefile ./.trivyignore.yaml .`

Per [cli reference][cli], `--ignorefile` defaults to `.trivyignore` and
accepts an alternate path.

### Rego-based ignore policy

Per [filter docs][filter], pass `--ignore-policy` with a Rego file that
contains a `trivy` package and an `ignore` rule:

```rego
# ignore_legacy.rego
package trivy

default ignore = false

ignore {
    input.Type == "terraform"
    input.Namespace == "user.legacy"
}
```

```bash
trivy config --ignore-policy ignore_legacy.rego .
```

## Step 6 - Custom Rego policies

Per [trivy.dev custom checks docs][custom], pass custom policies with
`--config-check` and scope them with `--namespaces`:

```bash
trivy config \
  --config-check ./policies/ \
  --namespaces user \
  ./infra/
```

Per [custom docs][custom], the `--namespaces` value (here: `user`) must
match the first segment of the package path. For a full policy file
(METADATA block + `deny` rule) and the list of supported
`input.selector` types, see
[references/trivy-config.md](references/trivy-config.md).

## Step 7 - CI integration (GitHub Actions)

Per [trivy.dev reporting docs][report], SARIF output integrates directly
with GitHub Code Scanning. For the full GitHub Actions workflow (with
`security-events: write`, the pinned `trivy-action`, and an
`if: always()` SARIF upload so findings surface even when the scan exits
non-zero), see [references/trivy-config.md](references/trivy-config.md).

To scope the scan to a single IaC type, pass `--misconfig-scanners` per
[cli reference][cli]:

```bash
# Terraform only
trivy config \
  --misconfig-scanners terraform \
  ./terraform/

# Kubernetes manifests only
trivy config \
  --misconfig-scanners kubernetes \
  ./k8s/
```

Per [cli reference][cli], `--misconfig-scanners` accepts a
comma-separated list from: `azure-arm`, `cloudformation`, `dockerfile`,
`helm`, `kubernetes`, `terraform`, `terraformplan-json`,
`terraformplan-snapshot`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `--exit-code 0` in CI | Misconfigs are logged but never block | Use `--exit-code 1` with `--severity HIGH,CRITICAL` (Step 3) |
| `.trivyignore` entries without a `statement` | Invisible to reviewers; silent security debt | Use `.trivyignore.yaml` with `statement` + `expired_at` (Step 5) |
| Running `trivy config` and `tfsec` in parallel without a unifier | Duplicate findings flood CI output | Route both through a single unifying reporter |
| Custom policies missing METADATA block | No severity, no title in report output | Always include METADATA with `id`, `severity`, `schemas` (Step 6) |
| Skipping bundle updates (`--skip-check-update`) permanently | Stale checks miss new misconfig rules | Use for caching in CI; re-enable updates on a scheduled run |

## Limitations

- **Network required on first run.** Trivy downloads the checks bundle
  from `ghcr.io/aquasecurity/trivy-checks`. Air-gapped setups need the
  embedded binary fallback or a mirror.
- **Terraform variable resolution is partial.** Dynamic values computed
  at apply time may cause false positives; pass `--tf-vars` to reduce
  noise per [cli reference][cli].
- **Helm rendering requires chart values.** Pass `--helm-values` for
  accurate rendering of templated manifests per [cli reference][cli].
- **Custom policy schemas must match input type.** A policy with
  `schema["cloud"]` will not fire against Kubernetes manifests; use the
  correct selector type per [custom docs][custom].

## References

- [mc][mc] - Trivy misconfiguration scanner overview, supported IaC
  types, auto-detection behavior, air-gap fallback, network requirements.
- [inst][inst] - Official install methods: Homebrew, the apt repository,
  direct `.rpm` release package, container image.
- [cli][cli] - `trivy config` CLI reference: `--exit-code`,
  `--severity`, `--format`, `--output`, `--ignorefile`,
  `--config-check`, `--namespaces`, `--misconfig-scanners`,
  `--tf-vars`, `--helm-values`, `--cf-params`, `--include-non-failures`.
- [custom][custom] - Custom Rego policy authoring: METADATA fields
  (`title`, `description`, `schemas`, `custom.id`, `custom.severity`,
  `custom.input.selector.type`), `deny` rule pattern, `--namespaces`
  scoping.
- [filter][filter] - `.trivyignore` and `.trivyignore.yaml` suppression
  format (`id`, `paths`, `statement`, `expired_at`), `--ignore-policy`
  Rego-based filtering.
- [report][report] - Output formats: `table`, `json`, `sarif`,
  `template`; `--output` flag; SARIF 2.1.0 compliance.
- [checks][checks] - `aquasecurity/trivy-checks` - the upstream
  OPA bundle for all built-in checks.
- [tfsec legacy reference][tfsec] - Migration context: tfsec is
  transitioning to Trivy; this skill is the forward path. tfsec custom
  rules + CI live in
  [references/tfsec-custom-rules-and-ci.md](references/tfsec-custom-rules-and-ci.md).
- `checkov-policy` - Sister scanner;
  broader Python-check framework, different rule coverage.
