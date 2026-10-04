---
name: prowler
type: skill
description: AWS security posture assessment using Prowler. Runs compliance and security scans, filters findings through the Director-Expert-Critic pipeline, and produces human-readable reports from validated results.
---

# Prowler

Prowler is an open-source AWS security assessment tool that runs hundreds of checks across services and compliance frameworks. This skill integrates Prowler scans into the plugin's validation pipeline so that raw findings are confirmed with CLI evidence before being presented.

---

## Table of Contents

- [Installation](#installation)
- [When to Trigger](#when-to-trigger)
- [Scan Execution](#scan-execution)
- [Output Storage](#output-storage)
- [Pipeline Integration](#pipeline-integration)
- [Findings Report Format](#findings-report-format)
- [Compliance Frameworks](#compliance-frameworks)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## Installation

```bash
pip install prowler
```

Requires AWS credentials with read-only access. Prowler's [permissions documentation](https://docs.prowler.com/projects/prowler-open-source/en/latest/getting-started/requirements/) lists the exact IAM policies needed — the AWS-managed `SecurityAudit` policy covers most checks.

Verify installation:

```bash
prowler -v
```

---

## When to Trigger

The Director triggers this skill when the user asks for:
- "run a prowler scan", "prowler", "security posture scan"
- "compliance scan", "CIS benchmark", "run a baseline check"
- "full security assessment", "scan everything"
- "what's failing in this account?"

This skill can also be triggered after an Inventory query when the user wants a broader automated sweep beyond the plugin's targeted checks.

---

## Scan Execution

### Full account scan (default)

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TODAY=$(date +%Y-%m-%d)

prowler aws \
  -M json-ocsf csv \
  -o data/prowler/scans/${ACCOUNT_ID}-${TODAY} \
  -z
```

| Flag | Purpose |
|:-----|:--------|
| `-M json-ocsf csv` | Output in OCSF JSON (for pipeline processing) and CSV (for human review) |
| `-o` | Output directory |
| `-z` | Skip banner for cleaner output |

### Targeted scans

Prowler supports filtering by service, check, severity, or compliance framework.

**By service:**

```bash
prowler aws --services iam s3 ec2 lambda \
  -M json-ocsf csv \
  -o data/prowler/scans/${ACCOUNT_ID}-${TODAY} \
  -z
```

**By severity:**

```bash
prowler aws --severity critical high \
  -M json-ocsf csv \
  -o data/prowler/scans/${ACCOUNT_ID}-${TODAY} \
  -z
```

**By compliance framework:**

```bash
prowler aws --compliance cis_2.0_aws \
  -M json-ocsf csv \
  -o data/prowler/scans/${ACCOUNT_ID}-${TODAY} \
  -z
```

**By specific checks:**

```bash
prowler aws -c iam_root_mfa_enabled s3_bucket_public_access \
  -M json-ocsf csv \
  -o data/prowler/scans/${ACCOUNT_ID}-${TODAY} \
  -z
```

**By region:**

```bash
prowler aws -f ap-southeast-2 us-east-1 \
  -M json-ocsf csv \
  -o data/prowler/scans/${ACCOUNT_ID}-${TODAY} \
  -z
```

### List available checks

```bash
prowler aws --list-checks
prowler aws --list-services
prowler aws --list-compliance
```

---

## Output Storage

Raw scan output and processed findings are stored in `data/prowler/` following the project naming convention:

```
data/prowler/
├── scans/                                  # Raw Prowler output per scan
│   └── {account_id}-{date}/
│       ├── output.ocsf.json                # OCSF JSON (pipeline input)
│       ├── output.csv                      # CSV (human review)
│       └── compliance/                     # Compliance-specific reports
└── findings/                               # Pipeline-validated findings
    └── {account_id}-{date}-findings.md     # Human-readable report
```

### Extracting failures from raw output

After a scan completes, extract only the failed checks for pipeline processing:

```bash
# Extract FAIL findings from OCSF JSON
cat data/prowler/scans/${ACCOUNT_ID}-${TODAY}/*.ocsf.json \
  | jq '[.[] | select(.status_code == "FAIL")]' \
  > data/prowler/findings/${ACCOUNT_ID}-${TODAY}-fails.json
```

---

## Pipeline Integration

Prowler findings are NOT presented directly to the user. They are treated as unvalidated claims that must pass through the Director-Expert-Critic loop before being reported.

### Processing flow

```
Prowler scan
    │
    ▼
Extract FAIL findings (jq filter)
    │
    ▼
Director: Group by service, create Claim Envelopes
    │
    ▼
Expert: Cross-validate each claim with AWS CLI
    │
    ▼
Critic: Score evidence (1-5)
    │
    ▼
Report: Only Score 4-5 findings presented
```

### Step 1: Run the scan

Run the appropriate Prowler command (full or targeted) and save output to `data/prowler/scans/`.

### Step 2: Extract failures

```bash
cat data/prowler/scans/${ACCOUNT_ID}-${TODAY}/*.ocsf.json \
  | jq '[.[] | select(.status_code == "FAIL")]' \
  > data/prowler/findings/${ACCOUNT_ID}-${TODAY}-fails.json
```

### Step 3: Check suppressions

Before creating Claim Envelopes, cross-reference each failure against `config/suppressions.yaml`. Any matching suppression is logged in the Scope section and skipped.

### Step 4: Group and validate

The Director groups failures by service and creates Claim Envelopes. The Expert validates each claim using the matching CLI command from `skills/validation-rules/`:

| Prowler check prefix | Validation rules file |
|:---------------------|:---------------------|
| `iam_*` | `validation-rules/iam.md` |
| `ec2_*`, `vpc_*` | `validation-rules/compute.md` |
| `s3_*`, `rds_*`, `kms_*` | `validation-rules/storage.md` |
| `cloudtrail_*`, `guardduty_*`, `securityhub_*` | `validation-rules/detection.md` |
| External accessibility | `validation-rules/probes.md` |

For Prowler checks that don't map to an existing validation rule, the Expert constructs the appropriate `aws` CLI command based on the check description and the relevant service skill.

### Step 5: Score and filter

The Critic scores each validated finding. Only Score 4-5 findings appear in the final report. FALSE_POSITIVE findings (where CLI evidence contradicts Prowler) are discarded.

### Scoring guidance for Prowler findings

| Scenario | Score |
|:---------|:------|
| Prowler FAIL + CLI confirms the misconfiguration | 5 (Verified) |
| Prowler FAIL + CLI shows partial issue (e.g., compensating control exists) | 4 (Strong) |
| Prowler FAIL + CLI shows the finding is mitigated by other controls | 2-3 (Downgrade) |
| Prowler FAIL + CLI contradicts the finding | FALSE_POSITIVE (Discard) |
| Prowler PASS + user asked to verify | No claim needed — note as passing in Scope |

---

## Findings Report Format

After pipeline validation, the confirmed findings are written to a human-readable Markdown report at `data/prowler/findings/{account_id}-{date}-findings.md`.

The report uses the standard `skills/output/SKILL.md` format with the following additions:

```markdown
---
## Results

### Prowler Security Assessment
Policy & Config | {{YYYY-MM-DD}} | {{account_id}} | SCP: {{status}}

**Scope:** {{N}} Prowler checks executed | {{N}} FAIL | {{N}} confirmed after pipeline | **Regions:** {{regions}}
**Suppressions:** {{None | list with action taken}}
**Scan type:** {{Full | Service: X,Y | Compliance: framework}}

#### F1: {{short title}} · `{{SEVERITY}}` · `CONFIRMED {{N}}/5`
**Resource:** `{{ARN}}` | **Prowler check:** `{{check_id}}`

{{One paragraph — what is misconfigured, what it enables, what guardrail is missing.}}

#### F2: ...

### Impact
...

### Recommendations
| Priority | Action | Effort | Risk Reduction |
|:---------|:-------|:-------|:---------------|
| P0 | {{immediate action}} | Low/Med/High | {{what it eliminates}} |

### Confidence: {{N}}/5
{{What couldn't be verified}} | **Verdict:** {{verdict}}
```

Key differences from standard output:
- **Scope** includes Prowler-specific stats (total checks, fail count, confirmed count)
- **Scan type** records what kind of scan was run
- Each finding includes the **Prowler check ID** for traceability back to the raw scan
- Complete enumeration rule applies — all confirmed findings are listed, never truncated

### Saving the report

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TODAY=$(date +%Y-%m-%d)
# Save the validated findings report
# data/prowler/findings/${ACCOUNT_ID}-${TODAY}-findings.md
```

---

## Compliance Frameworks

Prowler supports multiple compliance frameworks. Common ones:

| Framework | Flag | Use case |
|:----------|:-----|:---------|
| CIS AWS Foundations 2.0 | `--compliance cis_2.0_aws` | Industry baseline |
| CIS AWS Foundations 3.0 | `--compliance cis_3.0_aws` | Latest CIS benchmark |
| AWS Well-Architected Security | `--compliance aws_well_architected_framework_security_pillar_aws` | AWS best practices |
| PCI-DSS 3.2.1 | `--compliance pci_3.2.1_aws` | Payment card compliance |
| SOC2 | `--compliance soc2_aws` | Service org controls |
| GDPR | `--compliance gdpr_aws` | Data protection |
| HIPAA | `--compliance hipaa_aws` | Healthcare compliance |

When the user asks for a compliance scan, include the framework name in the report header and scope.

---

## Troubleshooting

| Issue | Fix |
|:------|:----|
| `ModuleNotFoundError: prowler` | Install: `pip install prowler` |
| `AccessDenied` on scan | Credentials need `SecurityAudit` managed policy or equivalent read-only permissions |
| Scan takes too long | Use `--services` to target specific services, or `--severity critical high` to reduce scope |
| Too many findings to validate | Filter by severity first (`--severity critical high`), validate those, then expand if needed |
| Prowler version mismatch | Check `prowler -v` — this skill targets Prowler v4+. Earlier versions use different CLI flags |
| Output directory not created | Prowler creates the output dir automatically. Ensure the parent `data/prowler/scans/` exists |

---

## References

- [Prowler Documentation](https://docs.prowler.com)
- [Prowler GitHub](https://github.com/prowler-cloud/prowler)
- [Prowler CLI Reference](https://docs.prowler.com/projects/prowler-open-source/en/latest/tutorials/misc/)
- [Supported Compliance Frameworks](https://docs.prowler.com/projects/prowler-open-source/en/latest/tutorials/compliance/)
- [Check Registry](https://docs.prowler.com/projects/prowler-open-source/en/latest/checks/aws/)
