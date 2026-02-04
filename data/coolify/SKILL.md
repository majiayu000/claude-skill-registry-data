---
name: coolify
description: Manage Coolify deployments - create applications, trigger deploys, manage servers and projects.
metadata: {"moltbot":{"emoji":"🚀","requires":{"env":["COOLIFY_TOKEN","COOLIFY_URL"]}}}
---

# Coolify Deployment Skill

This skill enables managing deployments via the Coolify API.

## Quick Reference

```bash
# List applications
curl -s "$COOLIFY_URL/api/v1/applications" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[] | {uuid, name, fqdn, status}'

# Trigger deployment
curl -X POST "$COOLIFY_URL/api/v1/applications/APP_UUID/restart" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Deploy from webhook
curl -X GET "$COOLIFY_URL/api/v1/deploy?uuid=APP_UUID&force=false" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

**Required env vars**: `COOLIFY_TOKEN`, `COOLIFY_URL`

## Server Operations

### List Servers

```bash
curl -s "$COOLIFY_URL/api/v1/servers" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[] | {uuid, name, ip, is_usable}'
```

### Get Server Details

```bash
curl -s "$COOLIFY_URL/api/v1/servers/SERVER_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq
```

### Get Server Resources

```bash
curl -s "$COOLIFY_URL/api/v1/servers/SERVER_UUID/resources" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq
```

## Project Operations

### List Projects

```bash
curl -s "$COOLIFY_URL/api/v1/projects" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[] | {uuid, name}'
```

### Create Project

```bash
curl -X POST "$COOLIFY_URL/api/v1/projects" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description"
  }'
```

### Get Project Details

```bash
curl -s "$COOLIFY_URL/api/v1/projects/PROJECT_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq
```

### Delete Project

```bash
curl -X DELETE "$COOLIFY_URL/api/v1/projects/PROJECT_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

## Application Operations

### List Applications

```bash
curl -s "$COOLIFY_URL/api/v1/applications" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[] | {uuid, name, fqdn, status}'
```

### Create Application (Public Git Repo)

```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/public" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_uuid": "PROJECT_UUID",
    "server_uuid": "SERVER_UUID",
    "environment_name": "production",
    "name": "my-app",
    "git_repository": "https://gitea.digpulsepi.com/user/repo.git",
    "git_branch": "main",
    "build_pack": "dockerfile",
    "domains": "http://myapp.digpulsepi.com",
    "ports_exposes": "80",
    "is_auto_deploy_enabled": true,
    "is_force_https_enabled": false
  }'
```

**Note:** Use `http://` for domains when behind Cloudflare Tunnel (Cloudflare handles HTTPS).

### Create Application (Private Repo with Deploy Key) - Recommended

```bash
# First add the private key to Coolify
PRIVATE_KEY=$(cat deploy-key | jq -Rs .)
KEY_RESP=$(curl -sf -X POST "$COOLIFY_URL/api/v1/security/keys" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"my-deploy-key\", \"private_key\": $PRIVATE_KEY}")
KEY_UUID=$(echo $KEY_RESP | jq -r '.uuid')

# Generate webhook secret
WEBHOOK_SECRET=$(openssl rand -hex 16)

# Create application with deploy key
curl -X POST "$COOLIFY_URL/api/v1/applications/private-deploy-key" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_uuid\": \"PROJECT_UUID\",
    \"server_uuid\": \"SERVER_UUID\",
    \"environment_name\": \"production\",
    \"private_key_uuid\": \"$KEY_UUID\",
    \"git_repository\": \"git@gitea:user/repo.git\",
    \"git_branch\": \"main\",
    \"name\": \"my-app\",
    \"domains\": \"http://myapp.digpulsepi.com\",
    \"ports_exposes\": \"80\",
    \"build_pack\": \"dockerfile\",
    \"is_auto_deploy_enabled\": true,
    \"is_force_https_enabled\": false,
    \"manual_webhook_secret_gitea\": \"$WEBHOOK_SECRET\"
  }"
```

**Important:** The `git_repository` uses internal hostname `git@gitea:user/repo.git` because Coolify's helper container needs to resolve it on the Docker network.

### Get Application Details

```bash
curl -s "$COOLIFY_URL/api/v1/applications/APP_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq
```

### Update Application

```bash
curl -X PATCH "$COOLIFY_URL/api/v1/applications/APP_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "domains": "https://newdomain.example.com"
  }'
```

### Delete Application

```bash
curl -X DELETE "$COOLIFY_URL/api/v1/applications/APP_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

## Deployment Operations

### Trigger Deploy (Restart)

```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/APP_UUID/restart" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

### Deploy via Webhook (Manual Gitea Webhook)

The correct webhook URL format for Gitea integration:

```bash
# Webhook URL (use this in Gitea webhook config)
WEBHOOK_URL="https://coolify.digpulsepi.com/webhooks/source/gitea/events/manual?app=APP_UUID"

# Create webhook in Gitea with matching secret
curl -X POST "http://127.0.0.1:3000/api/v1/repos/OWNER/REPO/hooks" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "active": true,
    "type": "gitea",
    "config": {
      "url": "'"$WEBHOOK_URL"'",
      "content_type": "json",
      "secret": "YOUR_WEBHOOK_SECRET"
    },
    "events": ["push"],
    "branch_filter": "*"
  }'
```

**Note:** The `secret` must match the `manual_webhook_secret_gitea` value in the Coolify application.

### Stop Application

```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/APP_UUID/stop" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

### Start Application

```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/APP_UUID/start" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

## Deployment History

### List Deployments

```bash
curl -s "$COOLIFY_URL/api/v1/deployments" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[0:5] | .[] | {uuid, status, created_at}'
```

### Get Deployment Details

```bash
curl -s "$COOLIFY_URL/api/v1/deployments/DEPLOYMENT_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq
```

## Environment Variables

### Get Application Env Vars

```bash
curl -s "$COOLIFY_URL/api/v1/applications/APP_UUID/envs" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq
```

### Create Env Var

```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/APP_UUID/envs" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "MY_VAR",
    "value": "my-value",
    "is_build_time": false
  }'
```

### Update Env Var

```bash
curl -X PATCH "$COOLIFY_URL/api/v1/applications/APP_UUID/envs" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "MY_VAR",
    "value": "new-value"
  }'
```

### Delete Env Var

```bash
curl -X DELETE "$COOLIFY_URL/api/v1/applications/APP_UUID/envs/ENV_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

## Build Packs

| Build Pack | Auto-detected For | Use Case |
|------------|-------------------|----------|
| `nixpacks` | Most languages | Default (recommended) |
| `dockerfile` | Has Dockerfile | Custom builds |
| `dockercompose` | Has docker-compose.yml | Multi-container apps |
| `static` | HTML/CSS/JS | Static sites |

## Common Patterns

### Get UUIDs for App Creation

```bash
# Get server UUID
SERVER_UUID=$(curl -s "$COOLIFY_URL/api/v1/servers" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq -r '.[0].uuid')

# Get project UUID
PROJECT_UUID=$(curl -s "$COOLIFY_URL/api/v1/projects" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq -r '.[0].uuid')

# Get destination UUID (requires querying database or using default)
echo "Server: $SERVER_UUID"
echo "Project: $PROJECT_UUID"
```

### Check Deployment Status After Trigger

```bash
# Trigger deploy
curl -X GET "$COOLIFY_URL/api/v1/deploy?uuid=APP_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Wait and check status
sleep 10
curl -s "$COOLIFY_URL/api/v1/deployments" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[0] | {status, created_at}'
```

### Full App Creation Flow

```bash
# Use the setup-ci-cd.sh script for automated setup
bash /srv/paas/scripts/setup-ci-cd.sh REPO_NAME SUBDOMAIN PORT

# Or manually:
# 1. Get server/project/destination UUIDs
# 2. Create application
# 3. Set up webhook in Gitea
```

## Troubleshooting

### Test API Connection

```bash
curl -s "$COOLIFY_URL/api/v1/servers" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" -w "\nHTTP: %{http_code}\n"
```

### Check Health

```bash
curl -s "$COOLIFY_URL/api/health"
```

### View Application Logs

```bash
# Via API (if supported)
curl -s "$COOLIFY_URL/api/v1/applications/APP_UUID/logs" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Via Docker (on server)
docker logs CONTAINER_NAME
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Unauthenticated` | Invalid/expired token | Regenerate token: `bash /srv/paas/scripts/refresh-tokens.sh --coolify` |
| `API is disabled` | API not enabled | Enable in Coolify Settings or bootstrap handles it |
| `Server not usable` | SSH/sudo not configured | Enable SSH, configure passwordless sudo |

## Scripts Available

```bash
# Connect repo to Coolify (creates app + webhook)
bash /srv/paas/scripts/setup-ci-cd.sh REPO_NAME SUBDOMAIN PORT

# Refresh tokens
bash /srv/paas/scripts/refresh-tokens.sh --coolify
```

## API Documentation

Full API docs: `$COOLIFY_URL/docs/api`
