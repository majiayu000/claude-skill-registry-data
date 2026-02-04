---
name: azure-setup-guide
description: Research and generate Azure deployment guide with EasyAuth (Google + Facebook) and CosmosDB. This skill searches for current documentation and screenshots to produce an up-to-date setup guide at .docs/azure-setup-guide.md.
---

# Azure Setup Guide Skill

This skill researches and generates a comprehensive Azure deployment guide for the finans application. It actively searches for the latest documentation to ensure instructions are current.

## Stack Components

- **Azure App Service** (Free F1 tier preferred)
- **EasyAuth** (Azure App Service Authentication)
- **Google OAuth** login
- **Facebook Login**
- **Azure CosmosDB** (NoSQL database)

## Credentials Location

OAuth credentials are stored in `backend/.env`:
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
- `FACEBOOK_APP_ID` / `FACEBOOK_APP_SECRET`
- `COSMOS_DB_ENDPOINT` / `COSMOS_DB_KEY`

Reference these when configuring EasyAuth instead of creating new credentials.

## When to Use

Use this skill when:
- Setting up a new Azure environment for finans
- Updating deployment documentation after Azure Portal changes
- Verifying current setup steps against latest Azure UI
- Onboarding new developers who need deployment guidance

## Workflow

### Phase 1: Research Current Documentation

Search for the latest setup procedures:

1. **Azure App Service Authentication (EasyAuth)**
   - Search: "Azure App Service authentication 2024 2025 configure Google Facebook"
   - Search: "Azure EasyAuth setup guide latest"
   - Look for Azure Portal UI screenshots and current menu paths

2. **Google OAuth Configuration**
   - Search: "Google Cloud Console OAuth setup 2024 2025"
   - Search: "Google OAuth web application redirect URI Azure"
   - Verify current Google Cloud Console menu structure

3. **Facebook Login Configuration**
   - Search: "Facebook Developer Portal app setup 2024 2025"
   - Search: "Facebook Login OAuth redirect URI configuration"
   - Verify current Facebook Developer Portal menu structure

4. **Azure CosmosDB Setup**
   - Search: "Azure CosmosDB create database container 2024 2025"
   - Search: "CosmosDB Node.js SDK connection setup"
   - Verify current Portal paths and CLI commands

5. **Azure CLI Commands**
   - Search: "az webapp auth update syntax 2024"
   - Search: "az cosmosdb create CLI 2024"
   - Verify command flags haven't changed

### Phase 2: Compile Guide

After research, write the guide to `.docs/azure-setup-guide.md` with:

1. **Prerequisites section** - Azure CLI, accounts needed
2. **Resource Group creation**
3. **App Service Plan** - Free F1 tier
4. **Web App creation**
5. **CosmosDB setup** - Account, database, containers (users, portfolios)
6. **Google OAuth setup** - Step-by-step with current menu paths
7. **Facebook Login setup** - Step-by-step with current menu paths
8. **EasyAuth configuration** - CLI and Portal methods
9. **Environment variables** - Connection strings, secrets
10. **Deployment steps** - Build, package, deploy
11. **Testing section** - Verify auth URLs work
12. **Troubleshooting** - Common issues and fixes
13. **Cleanup commands** - Delete resources when done

### Phase 3: Verification

After writing the guide:
- Confirm all CLI commands use current syntax
- Verify Portal menu paths match latest Azure UI
- Include both CLI and Portal alternatives where possible
- Note any recent changes from previous guide versions

## Base Template

Use this as the foundation, updating with researched information:

---

# Finans App - Azure Deployment Guide

**Stack**: App Service + EasyAuth + Google/Facebook Login + CosmosDB
**Tier**: Free (F1) - suitable for development and testing

## Prerequisites

- Azure CLI installed and logged in (`az login`)
- Azure subscription with Contributor access
- Google Cloud Console account
- Facebook Developer account
- Node.js 20.x LTS

Verify Azure login:
```bash
az account show --query "{Name:name, SubscriptionId:id}" -o table
```

---

## Step 1: Create Resource Group

```bash
az group create --name finans-rg --location norwayeast
```

---

## Step 2: Create App Service Plan (Free Tier)

```bash
az appservice plan create \
  --name finans-plan \
  --resource-group finans-rg \
  --location norwayeast \
  --sku F1 \
  --is-linux
```

**Free Tier Limits:**
- 1 GB storage
- Shared compute
- No custom domains or SSL
- Good for development/testing

---

## Step 3: Create Web App

```bash
az webapp create \
  --name finans \
  --resource-group finans-rg \
  --plan finans-plan \
  --runtime "NODE|20-lts"
```

Get app URL:
```bash
az webapp show --name finans --resource-group finans-rg --query defaultHostName -o tsv
```

---

## Step 4: Create CosmosDB Account

### 4.1 Create Account (Serverless - Cost Effective)

```bash
az cosmosdb create \
  --name finans-cosmos \
  --resource-group finans-rg \
  --locations regionName=norwayeast \
  --capabilities EnableServerless \
  --default-consistency-level Session
```

### 4.2 Create Database

```bash
az cosmosdb sql database create \
  --account-name finans-cosmos \
  --resource-group finans-rg \
  --name finans-db
```

### 4.3 Create Containers

**Users container** (partition key: /id):
```bash
az cosmosdb sql container create \
  --account-name finans-cosmos \
  --resource-group finans-rg \
  --database-name finans-db \
  --name users \
  --partition-key-path /id
```

**Portfolios container** (partition key: /userId):
```bash
az cosmosdb sql container create \
  --account-name finans-cosmos \
  --resource-group finans-rg \
  --database-name finans-db \
  --name portfolios \
  --partition-key-path /userId
```

### 4.4 Get Connection String

```bash
az cosmosdb keys list \
  --name finans-cosmos \
  --resource-group finans-rg \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" \
  -o tsv
```

---

## Step 5: Configure Google OAuth

[RESEARCH CURRENT STEPS - Google Cloud Console menu structure may have changed]

1. Navigate to **Google Cloud Console** → **APIs & Services** → **Credentials**
2. Create OAuth consent screen (External, app name: finans)
3. Create OAuth 2.0 Client ID:
   - Type: Web application
   - Redirect URI: `https://finans.azurewebsites.net/.auth/login/google/callback`
4. Save Client ID and Client Secret

---

## Step 6: Configure Facebook Login

[RESEARCH CURRENT STEPS - Facebook Developer Portal menu structure may have changed]

1. Navigate to **developers.facebook.com** → **My Apps** → **Create App**
2. Select app type: Consumer
3. Add Facebook Login product
4. Configure:
   - Site URL: `https://finans.azurewebsites.net`
   - Valid OAuth Redirect URI: `https://finans.azurewebsites.net/.auth/login/facebook/callback`
5. Set Privacy Policy URL
6. Switch app to Live mode
7. Save App ID and App Secret

---

## Step 7: Enable EasyAuth

### CLI Method

```bash
# Enable authentication
az webapp auth update \
  --name finans \
  --resource-group finans-rg \
  --enabled true \
  --unauthenticated-client-action RedirectToLoginPage \
  --token-store true

# Add Google provider
az webapp auth google update \
  --name finans \
  --resource-group finans-rg \
  --client-id {GOOGLE_CLIENT_ID} \
  --client-secret {GOOGLE_CLIENT_SECRET} \
  --yes

# Add Facebook provider
az webapp auth facebook update \
  --name finans \
  --resource-group finans-rg \
  --app-id {FACEBOOK_APP_ID} \
  --app-secret {FACEBOOK_APP_SECRET} \
  --yes
```

### Portal Method

[RESEARCH CURRENT PORTAL PATH - Azure Portal UI may have changed]

1. Azure Portal → App Services → finans → Authentication
2. Add identity provider → Google
3. Add identity provider → Facebook
4. Configure unauthenticated access

---

## Step 8: Configure App Settings

```bash
az webapp config appsettings set \
  --name finans \
  --resource-group finans-rg \
  --settings \
    COSMOS_DB_ENDPOINT="https://finans-cosmos.documents.azure.com:443/" \
    COSMOS_DB_KEY="{PRIMARY_KEY}" \
    COSMOS_DB_DATABASE="finans-db" \
    NODE_ENV="production"
```

---

## Step 9: Deploy Application

### Build & Package

```cmd
pnpm --filter frontend build
pnpm --filter backend build
```

### Deploy

```bash
az webapp deploy \
  --name finans \
  --resource-group finans-rg \
  --src-path deploy.zip \
  --type zip
```

---

## Step 10: Verify Deployment

Test URLs:
- App: `https://finans.azurewebsites.net`
- Google login: `https://finans.azurewebsites.net/.auth/login/google`
- Facebook login: `https://finans.azurewebsites.net/.auth/login/facebook`
- User info: `https://finans.azurewebsites.net/.auth/me`
- Logout: `https://finans.azurewebsites.net/.auth/logout`

---

## Troubleshooting

### Common Issues

**"Reply URL does not match"**
- Check redirect URI matches exactly including trailing slash

**"/.auth/me returns null"**
- User not logged in or session expired
- Check AppServiceAuthSession cookie

**Facebook app not working**
- Ensure app is in Live mode (not Development)
- Privacy Policy URL must be accessible

### View Logs

```bash
az webapp log tail --name finans --resource-group finans-rg
```

---

## Cleanup

Delete all resources:
```bash
az group delete --name finans-rg --yes --no-wait
```

---

## Output Requirements

After completing research and compilation:

1. Create `.docs/` directory if needed
2. Write complete guide to `.docs/azure-setup-guide.md`
3. Report any steps that couldn't be verified
4. Note any significant changes from previous documentation
5. Confirm file creation with path

## Notes

- Always prefer free tier options where available
- Include both CLI and Portal methods
- Use norwayeast region for GDPR compliance
- Serverless CosmosDB for cost efficiency
