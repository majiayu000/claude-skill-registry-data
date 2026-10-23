---
name: checkov-policy
description: "Configures Checkov for IaC security scanning across Terraform, CloudFormation, Kubernetes, Helm, ARM, Serverless, AWS CDK - `pip install checkov`, custom Python checks, SARIF / JUnit output, and `--baseline` gating so CI fails only on new findings in legacy code. Use for the broadest built-in rule set with Python custom checks; for a consolidated new-project scanner (and the tfsec successor) use trivy-config."
---

# checkov-policy

## Overview

[ch]: https://www.checkov.io/

Per [checkov-home][ch], supported frameworks: Terraform and
Terraform plan, CloudFormation, Kubernetes, Helm, ARM Templates,
Serverless framework, AWS CDK. Checkov is the broadest IaC
security scanner - covers more frameworks than tfsec
(Terraform-only) or KICS (similar coverage but Checkov has more
built-in checks per release).

## When to use

- Team uses any of the supported IaC frameworks.
- Need security scanning for misconfigurations (open ports,
  unencrypted storage, overly broad IAM, etc.).
- Want one tool covering Terraform + Kubernetes + Dockerfile + CI
  pipelines.

## How to use

1. Install Checkov and pin the version in `requirements-dev.txt`
   for CI determinism (Step 1).
2. Run `checkov -d .` locally, narrowing frameworks with
   `--framework` when the repo mixes IaC types (Step 2).
3. Emit SARIF for GitHub Code Scanning and JUnit for CI test
   reporting (Step 3).
4. Triage findings - fix real issues, annotate intentional
   exceptions with justified `checkov:skip=` comments (Step 4).
5. Add custom Python or YAML checks for team-specific policy the
   built-in rules miss (Step 5).
6. Create a `.checkov.baseline` so CI fails only on new findings,
   then wire the scan into CI with SARIF upload (Steps 7-8).
7. Pair with tfsec / KICS and unify the reports for
   overlapping-but-non-identical coverage (Step 9).

## Step 1 - Install

```bash
pip install checkov
checkov --version
```

Per project (recommended for CI determinism):

```bash
echo 'checkov==3.2.500' >> requirements-dev.txt
pip install -r requirements-dev.txt
```

## Step 2 - Run

```bash
# Scan a directory
checkov -d .

# Scan a specific Terraform file
checkov -f main.tf

# Scan multiple frameworks
checkov -d . --framework terraform,kubernetes,dockerfile

# Scan a Terraform plan (deeper analysis)
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
checkov -f plan.json
```

## Step 3 - Output formats

```bash
# Default (CLI)
checkov -d .

# JSON for parsing
checkov -d . -o json

# SARIF for code-scanning dashboards (GitHub Code Scanning)
checkov -d . -o sarif --output-file-path checkov.sarif

# JUnit XML for CI test reporting
checkov -d . -o junitxml > checkov.xml

# Multiple
checkov -d . -o cli -o sarif
```

## Step 4 - Skip checks

```bash
# Skip specific checks
checkov -d . --skip-check CKV_AWS_18,CKV_AWS_20

# Skip a check class
checkov -d . --skip-check CKV_AWS_*
```

In code:

```hcl
# main.tf
resource "aws_s3_bucket" "logs" {
  bucket = "my-logs"

  # checkov:skip=CKV_AWS_20:Public read access intentional for log distribution
}
```

The `:skip=` annotation requires a justification - reviewable in
PRs.

## Step 5 - Custom Python checks

Author custom Python checks (and the no-code YAML-policy
alternative) for team-specific rules the built-in set misses:
[references/custom-checks-and-ci.md](references/custom-checks-and-ci.md).

## Step 6 - Soft fail / hard fail

```bash
# Default: any failed check exits non-zero (CI fails)
checkov -d .

# Soft fail: log issues but exit 0 (informational)
checkov -d . --soft-fail

# Soft fail only on specific checks
checkov -d . --soft-fail-on CKV_AWS_*
```

Pattern: hard fail on critical / new findings; soft fail on legacy
issues being ratcheted down.

## Step 7 - Baseline comparison

```bash
# Generate baseline (current state of findings)
checkov -d . --create-baseline

# Use baseline (fail only on NEW findings vs baseline)
checkov -d . --baseline .checkov.baseline
```

Baselines let teams adopt Checkov against legacy code without
fixing all existing issues at once - only new findings break the
build.

## Step 8 - CI integration

Wire the scan into CI with a baseline plus SARIF upload to GitHub
Code Scanning (findings surface as PR comments + the Security tab):
[references/custom-checks-and-ci.md](references/custom-checks-and-ci.md).

## Step 9 - Combine with other scanners

Checkov + tfsec + KICS catch overlapping but non-identical issues.
Combine results to a unified verdict.

```bash
checkov -d . -o json > checkov.json
tfsec . -f json > tfsec.json
kics scan -p . --report-formats json -o ./kics-results
# Combine the three reports into a unified verdict
```

## Worked example

A team adopts Checkov on a legacy Terraform + Kubernetes monorepo.

1. `pip install checkov==3.2.500`, pinned in `requirements-dev.txt`.
2. First run `checkov -d . --framework terraform,kubernetes`
   reports a large backlog of existing failures - too many to fix
   at once.
3. They capture the current state: `checkov -d . --create-baseline`
   writes `.checkov.baseline`.
4. CI runs `checkov -d . --baseline .checkov.baseline -o sarif
   --output-file-path checkov.sarif`; the build passes because no
   findings are new versus the baseline.
5. A PR adds an `aws_s3_bucket` with `acl = "public-read"`. Checkov
   flags `CKV_AWS_20` as a NEW finding and fails the build.
6. The author drops public-read (or adds a justified
   `checkov:skip=CKV_AWS_20` comment); the SARIF upload clears the
   Security-tab entry and the build goes green.

Result: legacy debt is ratcheted down, not ignored, and each PR is
gated only on net-new misconfigurations.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Skipping all failed checks via `--skip-check`                          | Defeats security scanning.                                                | Per-check `checkov:skip=` with justification (Step 4). |
| Baseline never updated                                                  | Legacy issues never fixed; only-new gating becomes meaningless.          | Periodic baseline review + ratchet down. |
| Checkov as the only IaC scanner                                        | Tool-specific gaps; some issues missed.                                  | Pair with tfsec / KICS (Step 9). |
| Ignoring SARIF / GitHub Security tab                                    | Findings invisible until someone runs the CLI.                          | SARIF upload (Step 8). |
| Custom checks without tests                                             | Custom logic bugs let bad config through.                                | Test custom checks (per OPA's `opa test` pattern). |

## Limitations

- **Per-framework rule depth varies.** Terraform / Kubernetes have
  hundreds of rules; ARM / Serverless have fewer.
- **False positives common in early adoption.** Use baseline to
  manage.
- **Performance on large repos.** Checkov scans whole-tree; can take
  minutes.
- **Built-in rules may not match team policy.** Custom checks for
  team-specific rules (Step 5).

## References

- [ch][ch] - Checkov overview, supported IaC frameworks, common
  CLI usage, Palo Alto Networks maintainer.
- `trivy-config` - sister scanner (tfsec legacy in its
  references/tfsec-legacy.md).
- `policy-as-code-runner` - 
  custom policies via OPA / Conftest (Checkov for built-in; OPA
  for custom).
