---
name: gcloud-secrets
description: Manage Google Cloud Secret Manager for storing and fetching environment secrets. Use when working with deployment, secrets, or gcloud commands.
---

# Google Cloud Secret Manager

## Safety Rules

1. **NEVER push local dev `.env.client` or `.env.api` files directly to prod secrets.** They contain test Stripe keys, empty secrets, and placeholder values. This WILL break production.
2. **Always keep at least 2 enabled versions** of each secret (one live, one backup). Before destroying an old version, verify there are 2+ enabled versions remaining.
3. **Always fetch the current prod secret first**, modify only what's needed, then push the modified copy — never push from local dev files.

## Project Configuration

- **Project ID**: `myimageupscaler-auth`
- **Account**: `jfurtado141@gmail.com`
- **Secrets**:
  - `myimageupscaler-api-prod` → `.env.api.prod`
  - `myimageupscaler-client-prod` → `.env.client.prod`

## Setup Commands

```bash
# Set correct account and project
gcloud config set account jfurtado141@gmail.com
gcloud config set project myimageupscaler-auth

# Verify access
gcloud secrets list
```

## Common Issues

### "Failed to fetch secret" Error

1. Check current project: `gcloud config get-value project`
2. Check current account: `gcloud config get-value account`
3. Switch to correct account/project (see above)

### Wrong Project

The CLI might default to `definya-447700`. Always ensure you're on `myimageupscaler-auth`.

### Service Account vs Personal Account

- Service account `cloudstartlabs-service-acc@coldstartlabs-auth.iam.gserviceaccount.com` does NOT have access to myimageupscaler-auth
- Use personal account `jfurtado141@gmail.com` for secret access
- **Or** use the service account key at `./cloud/keys/myimageupscaler-auth-6348371fe8c6.json`:
  ```bash
  gcloud auth activate-service-account --key-file=./cloud/keys/myimageupscaler-auth-6348371fe8c6.json
  ```

## Deploy Flow

The deploy script (`scripts/deploy/deploy.sh`) fetches secrets in step 0:

1. Fetches `myimageupscaler-api-prod` → `.env.api.prod`
2. Fetches `myimageupscaler-client-prod` → `.env.client.prod`
3. Cleans up these files after deploy (success or failure)

## Updating Secrets

### CRITICAL SAFETY RULE: Never push local dev files directly to prod secrets

Local `.env.client` and `.env.api` contain **test/placeholder values** (test Stripe keys, empty secrets, etc.). **NEVER** run `gcloud secrets versions add ... --data-file=.env.api` or `--data-file=.env.client` directly. This will overwrite production secrets with dev values and break the live app.

### Mandatory Safe Update Process

**Step 1**: Fetch the current prod secret to a temp file:

```bash
gcloud secrets versions access latest --secret=myimageupscaler-api-prod > /tmp/api-prod.env
gcloud secrets versions access latest --secret=myimageupscaler-client-prod > /tmp/client-prod.env
```

**Step 2**: Verify the fetched file looks like prod (has live keys, not test keys):

```bash
# Should show live Stripe keys (pk_live_, sk_live_), real API keys, NOT test/empty values
grep -E "STRIPE_SECRET_KEY|STRIPE_PUBLISHABLE" /tmp/api-prod.env
grep -E "STRIPE_PUBLISHABLE" /tmp/client-prod.env
```

**Step 3**: Edit ONLY the specific values you need to change in the temp file:

```bash
# Example: adding a new variable
echo "GA4_API_SECRET=new-secret-value" >> /tmp/api-prod.env
```

**Step 4**: Push the updated temp file:

```bash
gcloud secrets versions add myimageupscaler-api-prod --data-file=/tmp/api-prod.env
gcloud secrets versions add myimageupscaler-client-prod --data-file=/tmp/client-prod.env
```

**Step 5**: Verify the new version is correct:

```bash
gcloud secrets versions access latest --secret=myimageupscaler-api-prod | grep -E "STRIPE_SECRET_KEY|GA4_API_SECRET"
gcloud secrets versions access latest --secret=myimageupscaler-client-prod | grep -E "STRIPE_PUBLISHABLE|GA_MEASUREMENT"
```

**Step 6**: Clean up temp files and destroy old versions:

```bash
rm /tmp/api-prod.env /tmp/client-prod.env

# List and destroy previous version
gcloud secrets versions list myimageupscaler-api-prod
gcloud secrets versions destroy N --secret=myimageupscaler-api-prod --quiet
```

## Service Account Key Location

Local keys available at:

- `./cloud/keys/coldstart-labs-service-account-key.json` (Note: Does not have access to myimageupscaler-auth project)
- `./cloud/keys/myimageupscaler-auth-6348371fe8c6.json` (myimageupscaler-auth project)

**Important**: The `cloud/keys/` directory is gitignored. Never commit service account keys.
