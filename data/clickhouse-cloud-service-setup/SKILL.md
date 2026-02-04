---
name: clickhouse-cloud-service-setup
description: Fetch ClickHouse Cloud service details from API (organization ID, service endpoints, configuration). Use when setting up new ClickHouse Cloud services, discovering endpoints, or validating service metadata for gapless-crypto-clickhouse project.
---

# ClickHouse Cloud Service Setup

Automate service metadata discovery via ClickHouse Cloud API for gapless-crypto-clickhouse project.

## Purpose

Fetch and store ClickHouse Cloud service details using the ClickHouse Cloud REST API. This skill guides the workflow of:
1. Authenticating with ClickHouse Cloud API
2. Resolving Organization ID
3. Fetching service metadata
4. Extracting connection endpoints
5. Storing configuration in Doppler

## When to Use

Use this skill when:
- **Initial service provisioning**: Setting up a new ClickHouse Cloud service
- **Service discovery**: Finding endpoints and configuration for existing service
- **Endpoint resolution**: Determining HTTPS (port 8443) or Native (port 9440) endpoints
- **Configuration validation**: Verifying idle scaling, memory tier, IP access settings

Triggers: User mentions "ClickHouse Cloud service", "fetch service details", "organization ID", "service endpoints"

## Prerequisites

**Required Credentials** (stored in Doppler `aws-credentials/prd` project):
- `CLICKHOUSE_CLOUD_KEY_ID`: API Key ID (format: `xnIdJM3n42LDImsZ9zzg`)
- `CLICKHOUSE_CLOUD_KEY_SECRET`: API Key Secret (secured in Doppler)

**Service Context**:
- Service ID: `a3163f31-21f4-4e22-844e-ef3fbc26ace2` (gapless-crypto-clickhouse service)
- Organization: "TE's Organization"

## Workflow

### Step 1: Authenticate with ClickHouse Cloud API

```bash
# Retrieve API credentials from Doppler
KEY_ID=$(doppler secrets get CLICKHOUSE_CLOUD_KEY_ID --project aws-credentials --config prd --plain)
KEY_SECRET=$(doppler secrets get CLICKHOUSE_CLOUD_KEY_SECRET --project aws-credentials --config prd --plain)
```

**API Authentication**: HTTP Basic Auth with `KEY_ID:KEY_SECRET`

### Step 2: Resolve Organization ID

```bash
# Fetch organizations
curl -s -u "$KEY_ID:$KEY_SECRET" https://api.clickhouse.cloud/v1/organizations | jq -r '.[0].id'
```

**Expected Output**: UUID format (e.g., `2404d339-6921-4f1c-bf80-b07d5e23b91a`)

**Store in Doppler**:
```bash
doppler secrets set CLICKHOUSE_CLOUD_ORG_ID "<org_id>" --project aws-credentials --config prd
```

### Step 3: Fetch Service Details

```bash
# Get service metadata
SERVICE_ID="a3163f31-21f4-4e22-844e-ef3fbc26ace2"  # gapless-crypto-clickhouse service
ORG_ID=$(doppler secrets get CLICKHOUSE_CLOUD_ORG_ID --project aws-credentials --config prd --plain)

curl -s -u "$KEY_ID:$KEY_SECRET" \
  "https://api.clickhouse.cloud/v1/organizations/$ORG_ID/services/$SERVICE_ID" | jq '.'
```

**Response Schema**: See [`references/api-endpoints.md`](./references/api-endpoints.md)

### Step 4: Extract Connection Endpoints

From API response, extract:

**HTTPS Endpoint** (recommended for clickhouse-connect):
- Host: `ebmf8f35lu.us-west-2.aws.clickhouse.cloud`
- Port: `8443`

**Native Protocol Endpoint** (for clickhouse-client):
- Host: `ebmf8f35lu.us-west-2.aws.clickhouse.cloud`
- Port: `9440`

**Store in Doppler**:
```bash
doppler secrets set CLICKHOUSE_HOST "ebmf8f35lu.us-west-2.aws.clickhouse.cloud" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_PORT "8443" --project aws-credentials --config prd
doppler secrets set CLICKHOUSE_USER "default" --project aws-credentials --config prd
```

### Step 5: Extract Service Configuration

**Configuration Details**:
- **Idle Scaling**: Enabled (15 minutes timeout)
- **Memory Tier**: 8-24 GB (development tier)
- **Region**: us-west-2 (AWS)
- **ClickHouse Version**: 25.8.1.8702
- **IP Access**: `0.0.0.0/0` (open to world, consider restricting for production)

**State Validation**: Ensure service state is `running`

## Success Criteria

- ✅ Organization ID retrieved and stored in Doppler
- ✅ Service details fetched successfully
- ✅ Connection endpoints extracted (HTTPS 8443 confirmed)
- ✅ Configuration parameters validated (idle scaling enabled, region us-west-2)
- ✅ Service state confirmed as `running`

## Troubleshooting

**Issue**: "Could not authenticate with ClickHouse Cloud API"
- **Check**: Verify `CLICKHOUSE_CLOUD_KEY_ID` and `CLICKHOUSE_CLOUD_KEY_SECRET` in Doppler
- **Verify**: API keys not expired (check https://clickhouse.cloud/ → Settings → API Keys)

**Issue**: "Service not found"
- **Check**: Verify service ID matches gapless-crypto-clickhouse service
- **Expected**: `a3163f31-21f4-4e22-844e-ef3fbc26ace2`

**Issue**: "Service state is not running"
- **Action**: Check ClickHouse Cloud console (https://clickhouse.cloud/services/a3163f31-21f4-4e22-844e-ef3fbc26ace2)
- **Possible causes**: Service paused (idle scaling), payment issue, manual stop

## References

- **API Documentation**: [`references/api-endpoints.md`](./references/api-endpoints.md)
- **ClickHouse Cloud Console**: https://clickhouse.cloud/
- **Organization Settings**: https://clickhouse.cloud/organizations/2404d339-6921-4f1c-bf80-b07d5e23b91a
- **Service Dashboard**: https://clickhouse.cloud/services/a3163f31-21f4-4e22-844e-ef3fbc26ace2

## Next Steps

After service setup, proceed to:
1. [`clickhouse-cloud-credentials`](../clickhouse-cloud-credentials/SKILL.md) - Store all credentials in Doppler + 1Password
2. [`clickhouse-cloud-connection`](../clickhouse-cloud-connection/SKILL.md) - Test connection to ClickHouse Cloud
