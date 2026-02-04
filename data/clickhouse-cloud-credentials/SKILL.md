---
name: clickhouse-cloud-credentials
description: Store ClickHouse Cloud credentials in Doppler + 1Password for gapless-crypto-clickhouse. Use when setting up new services, rotating credentials, or backing up authentication material. Covers API keys, connection details, and database password storage.
---

# ClickHouse Cloud Credentials

Establish dual credential storage pattern (Doppler + 1Password) for ClickHouse Cloud authentication.

## Purpose

Store and backup ClickHouse Cloud credentials in two secure locations:
1. **Doppler** (`aws-credentials/prd` project) - Runtime environment variables
2. **1Password** (Engineering vault) - Secure backup and team access

This skill guides the workflow of storing 8 required credentials for gapless-crypto-clickhouse service.

## When to Use

Use this skill when:
- **New service setup**: Initial credential storage for new ClickHouse Cloud service
- **Credential rotation**: Updating API keys or database passwords
- **Backup verification**: Ensuring credentials exist in both storage locations
- **Team onboarding**: Documenting required credentials for new team members

Triggers: User mentions "store credentials", "Doppler", "1Password", "ClickHouse API keys", "credential rotation"

## Prerequisites

**Credentials to Store**:
- API Key ID and Secret (from ClickHouse Cloud console)
- Organization ID (from ClickHouse Cloud API)
- Service ID (gapless-crypto-clickhouse service)
- Connection parameters (host, port, user, password)

**Required Access**:
- Doppler CLI access to `aws-credentials/prd` project
- 1Password CLI (`op`) access to Engineering vault

## Credential Schema

### Doppler Secrets (`aws-credentials/prd`)

8 required secrets:

| Secret Name | Description | Example Format |
|-------------|-------------|----------------|
| `CLICKHOUSE_CLOUD_KEY_ID` | API Key ID | `xnIdJM3n42LDImsZ9zzg` |
| `CLICKHOUSE_CLOUD_KEY_SECRET` | API Key Secret | (secured, ~40 chars) |
| `CLICKHOUSE_CLOUD_ORG_ID` | Organization UUID | `2404d339-6921-4f1c-bf80-b07d5e23b91a` |
| `CLICKHOUSE_CLOUD_SERVICE_ID` | Service UUID | `a3163f31-21f4-4e22-844e-ef3fbc26ace2` |
| `CLICKHOUSE_HOST` | Service hostname | `ebmf8f35lu.us-west-2.aws.clickhouse.cloud` |
| `CLICKHOUSE_PORT` | HTTPS port | `8443` |
| `CLICKHOUSE_USER` | Database user | `default` |
| `CLICKHOUSE_PASSWORD` | Database password | (secured, from console) |

**See**: [`references/doppler-schema.md`](./references/doppler-schema.md) for detailed descriptions

### 1Password Item (Engineering Vault)

**Vault**: Engineering (`fnzrqcsl3pl3bcdojrxf46whnu`)
**Item Title**: "ClickHouse Cloud - gapless-crypto-cli"

8 required fields:

| Field Name | Type | Description |
|------------|------|-------------|
| `username` | text | API Key ID |
| `credential` | concealed | API Key Secret |
| `organization_id` | text | Organization UUID |
| `organization_name` | text | "TE's Organization" |
| `service_id` | text | Service UUID |
| `service_name` | text | "gapless-crypto-cli" |
| `database_password` | password | Database password |
| `console_url` | url | https://clickhouse.cloud/ |

**See**: [`references/onepassword-schema.md`](./references/onepassword-schema.md) for detailed specifications

## Workflow

### Step 1: Store API Credentials in Doppler

```bash
# Store API Key ID and Secret
doppler secrets set CLICKHOUSE_CLOUD_KEY_ID "<key_id>" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_CLOUD_KEY_SECRET "<key_secret>" --project aws-credentials --config prd
```

### Step 2: Store Organization and Service Metadata in Doppler

```bash
# Store IDs
doppler secrets set CLICKHOUSE_CLOUD_ORG_ID "<org_id>" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_CLOUD_SERVICE_ID "a3163f31-21f4-4e22-844e-ef3fbc26ace2" --project aws-credentials --config prd
```

### Step 3: Store Connection Details in Doppler

```bash
# Store connection parameters
doppler secrets set CLICKHOUSE_HOST "ebmf8f35lu.us-west-2.aws.clickhouse.cloud" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_PORT "8443" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_USER "default" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_PASSWORD "<db_password>" --project aws-credentials --config prd
```

### Step 4: Backup Credentials in 1Password

```bash
# Create 1Password item with all fields
op item create --vault Engineering \
  --category "API Credential" \
  --title "ClickHouse Cloud - gapless-crypto-cli" \
  username="<key_id>" \
  credential="<key_secret>" \
  "organization_id[text]=<org_id>" \
  "organization_name[text]=TE's Organization" \
  "service_id[text]=a3163f31-21f4-4e22-844e-ef3fbc26ace2" \
  "service_name[text]=gapless-crypto-cli" \
  "database_password[password]=<db_password>" \
  "console_url[url]=https://clickhouse.cloud/"
```

### Step 5: Verify Storage

```bash
# Verify Doppler secrets (names only)
doppler secrets --project aws-credentials --config prd --only-names | grep CLICKHOUSE

# Verify 1Password item
op item get "ClickHouse Cloud - gapless-crypto-cli" --vault Engineering
```

## Success Criteria

- ✅ All 8 secrets stored in Doppler (`aws-credentials/prd`)
- ✅ All 8 fields stored in 1Password (Engineering vault)
- ✅ No plaintext credentials in version control
- ✅ Credentials accessible via Doppler CLI
- ✅ Backup accessible via 1Password CLI

## Security Notes

1. **No secrets in code**: Reference Doppler key names, never hardcode values
2. **Dual storage**: Doppler for runtime, 1Password for backup and team access
3. **Credential rotation**: Update both Doppler and 1Password when rotating
4. **Access control**: Doppler and 1Password enforce team-based access controls
5. **Audit trail**: Both systems log credential access for security monitoring

## Troubleshooting

**Issue**: "Doppler secrets not found"
- **Check**: Verify project name `aws-credentials` and config `prd`
- **Verify**: `doppler projects list` shows project exists

**Issue**: "1Password vault not accessible"
- **Check**: Engineering vault ID: `fnzrqcsl3pl3bcdojrxf46whnu`
- **Verify**: `op vault list` shows Engineering vault

**Issue**: "Credential format incorrect"
- **Check**: API Key ID format (example: `xnIdJM3n42LDImsZ9zzg`)
- **Verify**: UUIDs are valid format (8-4-4-4-12 hex digits)

## References

- **Doppler Schema**: [`references/doppler-schema.md`](./references/doppler-schema.md)
- **1Password Schema**: [`references/onepassword-schema.md`](./references/onepassword-schema.md)
- **Doppler Dashboard**: https://dashboard.doppler.com/workplace/13e9e4203ede563b1d37/projects/aws-credentials
- **ClickHouse Console**: https://clickhouse.cloud/ (API Keys → Settings)

## Next Steps

After credential storage, proceed to:
1. [`clickhouse-cloud-connection`](../clickhouse-cloud-connection/SKILL.md) - Test connection using stored credentials
