---
name: aws-login
description: Authenticate to AWS using SSO. Use when user selects AWS from cloud provider selection, or says "login to AWS", "AWS SSO", "authenticate to AWS".
allowed-tools: Bash, Read, AskUserQuestion
---

# AWS Login Skill

Authenticate to AWS using SSO (Single Sign-On) with optional resource discovery.

## Version

**v1.1** - Auto-discovery of management account (no hardcoded env vars)

## Activation Triggers

- `/auth-aws` slash command
- User says: "login to AWS", "AWS SSO", "authenticate to AWS"

## Prerequisites

Environment variables in `.env`:

```bash
AWS_SSO_START_URL="https://your-org.awsapps.com/start"
AWS_DEFAULT_REGION="us-east-1"  # Optional, defaults to us-east-1
```

**Note:** `AWS_ROOT_ACCOUNT_ID` and `AWS_ROOT_ACCOUNT_NAME` are no longer required. The management account is auto-detected from the AWS Organizations API (`MasterAccountId`).

## Usage

### Human CLI

```powershell
# Interactive account selection
./scripts/aws-auth.ps1

# Login to specific account (by alias)
./scripts/aws-auth.ps1 sandbox
./scripts/aws-auth.ps1 provision-iam  # Management account uses its alias

# Force re-login
./scripts/aws-auth.ps1 sandbox -Force

# Force SSO device auth flow (full discovery)
./scripts/aws-auth.ps1 -Login

# Login with auth only (no resource discovery)
./scripts/aws-auth.ps1 -Login -SkipVpc

# Login with VPCs only (skip S3/SQS/SNS/SES)
./scripts/aws-auth.ps1 -Login -SkipResources

# Inspect: clear cache, re-auth, rebuild config
./scripts/aws-auth.ps1 -Inspect

# Inspect with auth only (no resource discovery)
./scripts/aws-auth.ps1 -Inspect -SkipVpc
```

### Claude Agent

```bash
# Via skill invocation
uv run --directory ${CLAUDE_SKILLS_PATH}/aws-login python -m lib [account] [--force]

# With flags
uv run --directory ${CLAUDE_SKILLS_PATH}/aws-login python -m lib --login --skip-resources
uv run --directory ${CLAUDE_SKILLS_PATH}/aws-login python -m lib --inspect
```

## First-Run Setup (v1.1 Auto-Discovery)

When no `accounts.yml` config exists:

1. **SSO Device Authorization**: Uses SSO OIDC to authenticate without pre-configured profiles
2. **Account Discovery**: Lists available accounts via `sso.list_accounts()`
3. **Organization Query**: Uses any available account to query AWS Organizations
4. **Management Account Detection**: Auto-detects from `MasterAccountId` in Organizations API
5. **Profile Creation**: Creates AWS CLI profiles for all accounts (using aliases, not "root")
6. **Resource Discovery**: Discovers resources for each account (parallel, 8 workers)
7. **Config Save**: Saves auth config with `is_manager: true` flag on management account

### Profile Naming

All accounts use their **alias** as the profile name - there is no special "root" profile:

| Account | Profile Name | accounts.yml Flag |
|---------|--------------|-------------------|
| Provision IAM Manager | `provision-iam` | `is_manager: true` |
| Sandbox | `sandbox` | |
| Operations | `operations` | |

## Discovery Flags

| Flag | Effect |
|------|--------|
| `--skip-vpc` | Skip ALL resource discovery (auth only) |
| `--skip-resources` | Skip S3/SQS/SNS/SES (VPCs still discovered) |
| (none) | Full discovery (VPCs + S3 + SQS + SNS + SES) |

## SSO URL Detection

The skill captures and displays the SSO URL and device code:

| Field | Value |
|-------|-------|
| URL | https://your-org.awsapps.com/start/#/device |
| Code | **XXXX-XXXX** |

## Data Architecture (v1.0)

### Directory Structure

```
.data/aws/
├── accounts.yml                    # Auth-only config
└── {org-id}/                       # Organization ID (o-xxx)
    ├── {ou-path}/                  # OU hierarchy path
    │   └── {alias}.yml             # Per-account inventory
    └── root/                       # Root-level accounts
        └── {alias}.yml
```

Example:
```
.data/aws/
├── accounts.yml
└── o-abc123xyz/
    ├── root/
    │   └── provision-iam.yml       # Management account
    ├── piam-dev-accounts/
    │   └── sandbox.yml
    └── piam-ops-accounts/
        └── operations.yml
```

### accounts.yml Schema (v1.1)

```yaml
schema_version: "1.0"
organization_id: "o-abc123xyz"
management_account_id: "883269661255"  # Auto-detected from MasterAccountId
default_region: us-east-1
sso_start_url: "https://your-org.awsapps.com/start"

accounts:
  provision-iam:                    # Management account uses its alias
    id: "883269661255"
    name: "Provision IAM Manager"
    ou_path: "root"
    sso_role: "AdministratorAccess"
    is_manager: true                # Flags this as the management account
    inventory_path: "root/provision-iam.yml"
  sandbox:
    id: "411713055198"
    name: "provision-iam-sandbox"
    ou_path: "piam-dev-accounts"
    sso_role: "AdministratorAccess"
    inventory_path: "piam-dev-accounts/sandbox.yml"
  operations:
    id: "123456789012"
    name: "provision-iam-operations"
    ou_path: "piam-ops-accounts"
    sso_role: "AdministratorAccess"
    inventory_path: "piam-ops-accounts/operations.yml"
```

### Inventory File Schema ({alias}.yml)

```yaml
schema_version: "1.0"
account_id: "411713055198"
account_alias: "sandbox"
discovered_at: "2025-12-16T15:56:49Z"
region: "us-east-1"

vpcs:
  - id: "vpc-xxx"
    cidr: "10.0.0.0/16"
    is_default: false
    internet_gateways:
      - id: "igw-xxx"
        state: "attached"
    subnets:
      - id: "subnet-xxx"
        cidr: "10.0.1.0/24"
        az: "us-east-1a"
        type: "public"
      - id: "subnet-yyy"
        cidr: "10.0.2.0/24"
        az: "us-east-1b"
        type: "private"
        nat_gateway:
          id: "nat-xxx"
          state: "available"
          elastic_ip: "eipalloc-xxx"

elastic_ips:
  - allocation_id: "eipalloc-xxx"
    public_ip: "54.123.45.67"
    region: "us-east-1"

s3_buckets:
  - name: "my-bucket"
    region: "us-east-1"
    arn: "arn:aws:s3:::my-bucket"

sqs_queues:
  - name: "my-queue"
    region: "us-east-1"
    arn: "arn:aws:sqs:us-east-1:411713055198:my-queue"

sns_topics:
  - name: "my-topic"
    region: "us-east-1"
    arn: "arn:aws:sns:us-east-1:411713055198:my-topic"

ses_identities:
  - identity: "example.com"
    type: "Domain"
    region: "us-east-1"
```

## Code Structure

```
apps/src/claude_apps/
├── skills/aws_login/
│   ├── __init__.py
│   ├── __main__.py       # Entry point with CLI
│   ├── config.py         # Auth config (accounts.yml)
│   ├── sso.py            # SSO login with URL detection
│   ├── discovery.py      # Resource discovery (uses aws_utils)
│   └── profiles.py       # AWS CLI profile management
└── shared/aws_utils/     # Shared library
    ├── core/
    │   ├── session.py    # Boto3 session factory
    │   └── schemas.py    # Pydantic models
    ├── services/
    │   ├── ec2.py, s3.py, sqs.py, sns.py, ses.py
    │   └── organizations.py  # Org/account discovery
    └── inventory/
        ├── reader.py     # Load inventory files
        └── writer.py     # Save inventory files
```

## Migration from v1.0

If you have existing configuration from v1.0:

1. Run `-Inspect` to clear cache and regenerate config with the new schema
2. The management account will be auto-detected and flagged with `is_manager: true`
3. The old "root" profile will be replaced with the account's alias

You can remove `AWS_ROOT_ACCOUNT_ID` and `AWS_ROOT_ACCOUNT_NAME` from your `.env` file.

## Parameter Reference

| Parameter | Python Flag | Description |
|-----------|-------------|-------------|
| `-Login` | `--login` | Force SSO device auth flow (full discovery) |
| `-Inspect` | `--inspect` | Clear cache, re-auth, rebuild config |
| `-Force` | `--force` | Force re-login even if credentials valid |
| `-SkipVpc` | `--skip-vpc` | Skip all resource discovery (auth only) |
| `-SkipResources` | `--skip-resources` | Skip S3/SQS/SNS/SES (VPCs still discovered) |
