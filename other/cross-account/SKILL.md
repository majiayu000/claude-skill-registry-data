---
name: cross-account
description: Multi-account credential switching and iteration for cross-account security audits. Enables the existing single-account pipeline to run sequentially across multiple AWS accounts defined in config/accounts.yaml.
---

# Cross-Account Auditing

Enables the existing single-account audit pipeline (Director → Expert → Critic) to run sequentially across multiple AWS accounts. Each account is audited independently using its own credentials, pre-flights, and findings. Results are consolidated into a single multi-account report.

**This skill does NOT add cross-account relationship modeling (Tier 2) or cross-account blast radius analysis (Tier 3).** It adds credential switching and iteration only — the pipeline runs identically per account.

---

## Table of Contents

- [When to Trigger](#when-to-trigger)
- [Configuration Reference](#configuration-reference)
- [Credential Strategies](#credential-strategies)
- [Iteration Model](#iteration-model)
- [Suppression Scoping](#suppression-scoping)
- [Data Storage](#data-storage)
- [Session Management](#session-management)
- [Limitations (Tier 1)](#limitations-tier-1)
- [Troubleshooting](#troubleshooting)

---

## When to Trigger

The Director triggers multi-account mode during the **Multi-Account Discovery** pre-flight (see `agents/roles.md`) when:

1. `config/accounts.yaml` exists AND
2. The `accounts` list contains at least one enabled entry

When the file is absent or the list is empty, `MULTI_ACCOUNT_STATUS = DISABLED` — all behavior is identical to single-account mode. No other skill or validation rule needs to change.

---

## Configuration Reference

Full schema for `config/accounts.yaml`:

### Top-Level Structure

```yaml
defaults:                    # Optional — fallback values
  credential_strategy: environment
  session_duration_seconds: 3600
  regions: []                # Empty = discover per account

iteration:                   # Optional — processing controls
  mode: sequential           # sequential | parallel (Tier 2)
  stop_on_error: false
  skip_disabled: true

accounts:                    # Required — the account list
  - account_id: "123456789012"
    name: production
    credential_strategy: profile
    aws_profile: prod-audit
    # ... strategy-specific and optional fields
```

### Account Entry Fields

| Field | Required | Type | Description |
|:------|:---------|:-----|:------------|
| `account_id` | Yes | String (12 digits) | AWS account ID |
| `name` | Yes | String | Human-readable label (used in reports) |
| `credential_strategy` | Yes* | Enum | `profile`, `assume_role`, or `environment` (* falls back to `defaults` if omitted) |
| `aws_profile` | If `profile` | String | Named profile from `~/.aws/config` |
| `role_arn` | If `assume_role` | String | Full ARN of the role to assume |
| `external_id` | No | String | ExternalId for the trust policy condition |
| `session_name` | No | String | Session name (default: `cloud-audit-{{account_id}}`) |
| `duration_seconds` | No | Integer | Session duration (default: from `defaults`) |
| `source_profile` | No | String | Profile to assume FROM (default: current credentials) |
| `regions` | No | List[String] | Override region discovery for this account |
| `enabled` | No | Boolean | Default `true` — set `false` to skip without removing |
| `tags` | No | Map | Freeform metadata (e.g., `environment: production`) |

### Validation Rules

The Director validates the config during the Multi-Account Discovery pre-flight:

1. `account_id` must be exactly 12 digits
2. `credential_strategy` must be one of: `profile`, `assume_role`, `environment`
3. `profile` strategy requires `aws_profile`
4. `assume_role` strategy requires `role_arn`
5. `role_arn` must match pattern `arn:aws:iam::\d{12}:role/.+`
6. No duplicate `account_id` entries

If validation fails, the Director sets `MULTI_ACCOUNT_STATUS = ERROR`, warns the user with the specific failure, and falls back to single-account mode.

---

## Credential Strategies

### Strategy: `profile`

Uses an AWS CLI named profile. All `aws` commands for this account get `--profile {{aws_profile}}` appended.

```bash
# Validation
aws sts get-caller-identity --profile {{aws_profile}} --output json

# Usage — every CLI call during this account's audit includes the flag
aws s3api list-buckets --profile {{aws_profile}} --output json
aws iam list-users --profile {{aws_profile}} --output json
```

**Setup:** The profile must exist in `~/.aws/config` or `~/.aws/credentials` before running the audit.

### Strategy: `assume_role`

Calls `sts:AssumeRole` to obtain temporary credentials, then sets environment variables for the duration of the account's audit.

```bash
# Step 1: Assume the role
aws sts assume-role \
  --role-arn {{role_arn}} \
  --role-session-name {{session_name | cloud-audit-{{account_id}}}} \
  --duration-seconds {{duration_seconds | 3600}} \
  --external-id {{external_id}}  # only if configured \
  --profile {{source_profile}}   # only if configured \
  --output json

# Step 2: Set environment variables from the response
export AWS_ACCESS_KEY_ID={{Credentials.AccessKeyId}}
export AWS_SECRET_ACCESS_KEY={{Credentials.SecretAccessKey}}
export AWS_SESSION_TOKEN={{Credentials.SessionToken}}

# Step 3: Validate the assumed identity
aws sts get-caller-identity --output json
# Verify Account matches the declared account_id

# Step 4: Run the full audit for this account
# ... all pre-flights and claims use these credentials ...

# Step 5: Clear credentials before next account
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
```

**Trust policy requirement:** The target role must trust the source credentials. Minimum required permissions on the target role: read-only access for the services being audited (see `CLAUDE.md` → Requirements).

### Strategy: `environment`

No credential changes — uses whatever is active in the shell. This is the implicit single-account mode and the default when no `accounts.yaml` exists.

```bash
# Validation only
aws sts get-caller-identity --output json
```

---

## Iteration Model

When `MULTI_ACCOUNT_STATUS = AVAILABLE`, the Director processes accounts sequentially in the order listed in `accounts.yaml`.

### Per-Account Lifecycle

```
For each enabled account in accounts.yaml:
  1. Set credential context (profile flag or assume-role env vars)
  2. Validate credentials (sts:get-caller-identity, verify account_id match)
  3. Run ALL pre-flights for this account:
     a. Suppression Expiry Audit
     b. SCP Visibility
     c. PMapper Graph (if IAM escalation is in scope)
  4. Run ALL claims for this account (same routing as single-account)
  5. Run Exploit Chain Analysis for this account
  6. Collect per-account results
  7. Clear credential context
  8. Move to next account
```

**Pre-flights run per account.** SCP status, PMapper graph, and suppression state are account-specific — they cannot be shared across accounts.

### Error Handling

| Scenario | `stop_on_error: false` (default) | `stop_on_error: true` |
|:---------|:---------------------------------|:----------------------|
| Credential validation fails | Log error, skip account, continue | Abort all remaining accounts |
| Pre-flight fails (e.g., PMapper) | Use fallback (same as single-account), continue | Use fallback, continue |
| CLI command fails mid-audit | Handle per existing Expert rules (ERROR status) | Handle per existing Expert rules |
| Account ID mismatch | Log error, skip account, continue | Abort all remaining accounts |

Skipped accounts are reported in the results: `"Account {{name}} ({{id}}): SKIPPED — {{reason}}"`.

---

## Suppression Scoping

The existing `account` field in `config/suppressions.yaml` user entries becomes meaningful in multi-account mode:

```yaml
user:
  - check: ec2_securitygroup_allow_ingress_from_internet_to_any_port
    resource: "sg-0abc123"
    account: "222222222222"    # Only matches in this account
    reason: "Staging load balancer — expected open port"
    approved_by: "Security Team"
    expires: "2026-12-31"
```

| Suppression has `account` field? | Behavior |
|:---------------------------------|:---------|
| No | Matches claims in ALL accounts (existing behavior, backward compatible) |
| Yes | Matches claims ONLY in the specified account |

Builtin suppressions never have an `account` field and always apply globally.

---

## Data Storage

Multi-account mode requires no changes to data storage. All output already uses `{account_id}-{date}` naming:

```
data/
├── pmapper/
│   ├── analysis/
│   │   ├── 111111111111-2026-03-30.json    # Account 1
│   │   └── 222222222222-2026-03-30.json    # Account 2
│   └── privesc/
│       ├── 111111111111-2026-03-30.json
│       └── 222222222222-2026-03-30.json
├── poc-generator/playbooks/
│   ├── 111111111111-2026-03-30-finding.md
│   └── 222222222222-2026-03-30-finding.md
└── identity-blast-radius/reports/
    ├── 111111111111-2026-03-30-role.md
    └── 222222222222-2026-03-30-role.md
```

Each account's data naturally partitions by the account ID prefix.

---

## Session Management

### Token Expiry

`assume_role` sessions default to 1 hour (3600 seconds). For large accounts with many resources, a full posture assessment (qa-01 through qa-10 + deep dives) can approach this limit.

**Proactive refresh:** If the Director estimates remaining checks will exceed the remaining session time, re-run `aws sts assume-role` to obtain fresh credentials before continuing. The refresh is transparent — no claims need to be re-run.

**Guidance:**
- Small accounts (<50 resources): 3600 seconds is sufficient
- Medium accounts (50-200 resources): 3600 seconds, monitor for expiry
- Large accounts (200+ resources): Set `duration_seconds: 7200` or higher (max 12 hours, depends on role's `MaxSessionDuration`)

### Credential Isolation

Credentials for one account MUST be fully cleared before setting credentials for the next account. The lifecycle is:

1. Set credentials (profile flag or env vars)
2. Run entire audit
3. Clear credentials (`unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN`)
4. Verify cleared: `aws sts get-caller-identity` should return the original/default identity

This prevents credential leakage between accounts.

---

## Limitations (Tier 1)

Tier 1 provides multi-account iteration only. The following are **not in scope** and are planned for future tiers:

| Limitation | Planned Tier |
|:-----------|:-------------|
| Cross-account trust policy analysis (who trusts whom) | Tier 2 |
| Cross-account resource sharing detection (S3, KMS, snapshots across accounts) | Tier 2 |
| Consolidated PMapper graph (stitched cross-account edges) | Tier 2 |
| Cross-account attack chain analysis (chains spanning accounts) | Tier 2 |
| Cross-account blast radius (compromise propagation across accounts) | Tier 3 |
| Parallel account processing | Tier 2 |
| Organization-wide SCP inheritance tree | Tier 2 |

Tier 1 findings are **per-account only** — the same quality as today's single-account audit, repeated across N accounts. The cross-account summary table provides visibility across accounts, but does not analyze relationships between them.

---

## Troubleshooting

| Issue | Cause | Fix |
|:------|:------|:----|
| `AssumeRole` returns AccessDenied | Trust policy doesn't allow source credentials | Verify the target role's trust policy includes the source principal |
| Account ID mismatch after assume | `role_arn` points to wrong account | Check the account ID in the `role_arn` matches `account_id` |
| Session expired mid-audit | Duration too short for large account | Increase `duration_seconds` in the account entry or role's `MaxSessionDuration` |
| Profile not found | `aws_profile` doesn't exist in `~/.aws/config` | Run `aws configure list-profiles` to check available profiles |
| `accounts.yaml` parse error | Invalid YAML syntax | Validate with `python3 -c "import yaml; yaml.safe_load(open('config/accounts.yaml'))"` |
| ExternalId mismatch | `external_id` doesn't match the role's trust policy condition | Verify the ExternalId in `accounts.yaml` matches the `sts:ExternalId` condition exactly |
| PMapper slow across many accounts | Graph creation is expensive per account | PMapper only runs when IAM escalation is in scope — limit escalation queries to targeted accounts |
| Output too long for many accounts | Complete enumeration across N accounts | Use the cross-account summary table for overview; per-account details use standard section activation rules |
