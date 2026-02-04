---
name: setup-github-app
description: Guide users through creating and configuring a GitHub App for workspace authentication. Use when setting up GitHub App authentication for happy-little-claude-coders, creating github-app-credentials secret, or configuring automatic token refresh.
allowed-tools: Read, Bash(gh:*), Bash(curl:*), Bash(cat:*), Bash(base64:*), Bash(kubectl get:*), Bash(kubectl describe:*), WebFetch
---

# GitHub App Setup for happy-little-claude-coders

This skill guides you through creating a GitHub App and configuring it for workspace authentication.

## Overview

The happy-little-claude-coders chart uses GitHub Apps for secure, scoped repository access. Each workspace gets automatically refreshed tokens via the sidecar container.

## Before You Start

**Ask the user:**
1. Which repositories should the GitHub App have access to?
2. Personal account or organization?
3. Do they want browser-assisted setup or manual setup?

## Setup Options

### Option 1: Browser-Assisted Setup (Recommended)

If the user has browser automation available, this provides a guided experience.

**Using Claude in Chrome:**
If Claude Code was started with `claude --chrome` or the user has the Claude in Chrome extension:
- Use the `mcp__claude-in-chrome__*` tools to navigate and assist with form filling
- Can help click through the GitHub App creation flow

**Using Playwright MCP:**
This repo includes a `.mcp.json` config for Playwright MCP with browser extension mode.

**Setup steps:**
1. Download the Playwright MCP Bridge extension from:
   https://github.com/microsoft/playwright-mcp/releases
2. Go to `chrome://extensions`, enable Developer mode
3. Click "Load unpacked" and select the extension folder
4. The `.mcp.json` in this repo auto-configures the MCP server

Claude Code will prompt to approve the MCP server on first use.

**Manual CLI setup (alternative):**
```bash
claude mcp add playwright -- pnpx @playwright/mcp@latest --extension
```

### Option 2: Manual Setup

Follow the step-by-step instructions below.

---

## Step 1: Create the GitHub App

### Navigate to GitHub App creation:
- **Personal account**: `https://github.com/settings/apps/new`
- **Organization**: `https://github.com/organizations/YOUR_ORG/settings/apps/new`

### Fill in the form:

| Field | Value |
|-------|-------|
| **GitHub App name** | `hlcc-workspace-auth` (must be unique on GitHub) |
| **Homepage URL** | `https://github.com/dbirks/happy-little-claude-coders` |
| **Webhook > Active** | Uncheck (not needed) |
| **Repository permissions > Contents** | Read-only |
| **Where can this app be installed?** | Only on this account |

Click **Create GitHub App**.

## Step 2: Generate Private Key

After creating the app:

1. You'll be redirected to the app's settings page
2. Scroll to **Private keys** section
3. Click **Generate a private key**
4. A `.pem` file will download automatically

**Save this file securely!** You cannot regenerate it.

## Step 3: Install the App on Repositories

1. From the app settings page, click **Install App** (left sidebar)
2. Select your account/organization
3. Choose **Only select repositories**
4. Select the repositories the user specified earlier
5. Click **Install**

## Step 4: Gather Required Information

You need three pieces of information:

### App ID
Found on the app settings page under "About" section:
```
https://github.com/settings/apps/YOUR_APP_NAME
```
Look for: `App ID: 123456`

### Installation ID
After installing, check the URL:
```
https://github.com/settings/installations/12345678
                                          ^^^^^^^^
                                          This is your Installation ID
```

Or use gh CLI:
```bash
gh api /user/installations --jq '.installations[] | select(.app_slug == "YOUR_APP_NAME") | .id'
```

### Private Key
The `.pem` file downloaded in Step 2.

## Step 5: Create Kubernetes Secret

### Preview the command (dry-run) - ALWAYS SHOW THIS FIRST

```bash
kubectl create secret generic github-app-credentials \
  --from-literal=app-id=YOUR_APP_ID \
  --from-literal=installation-id=YOUR_INSTALLATION_ID \
  --from-file=private-key=/path/to/your-app.private-key.pem \
  --namespace=default \
  --dry-run=client -o yaml
```

**Show the user the output and ask if it looks correct before proceeding.**

### Create the secret (only after user confirms)

```bash
kubectl create secret generic github-app-credentials \
  --from-literal=app-id=YOUR_APP_ID \
  --from-literal=installation-id=YOUR_INSTALLATION_ID \
  --from-file=private-key=/path/to/your-app.private-key.pem \
  --namespace=default
```

### Verify the secret

```bash
kubectl get secret github-app-credentials -n default
kubectl get secret github-app-credentials -n default -o jsonpath='{.data.app-id}' | base64 -d
```

## Step 6: Enable GitHub App in HelmRelease

Update the HelmRelease values:

```yaml
values:
  githubApp:
    enabled: true
    secretName: github-app-credentials
    refreshIntervalMinutes: 50  # Tokens expire after 1 hour
```

## Verification

After deployment, check the sidecar logs:

```bash
# Find workspace pods
kubectl get pods -l app.kubernetes.io/name=happy-little-claude-coders

# Check sidecar logs for token refresh
kubectl logs <pod-name> -c github-token-refresh
```

Expected output:
```
Token refreshed successfully for repositories: [your-org/repo1, your-org/repo2]
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| "Resource not accessible by integration" | App doesn't have repo access | Add repository to app installation |
| "Bad credentials" | Token expired | Check sidecar logs, should auto-refresh |
| "Not Found" for repository | App not installed on repo | Add repo in app installation settings |
| Secret not found | Secret doesn't exist | Create using Step 5 |

## Reference

For detailed information, see the comprehensive guide:
- [GITHUB_APP_SETUP_GUIDE.md](../../../history/GITHUB_APP_SETUP_GUIDE.md)

## Quick Reference

| Item | Where to Find |
|------|---------------|
| App ID | App settings page > About section |
| Installation ID | URL after installing the app |
| Private Key | Downloaded `.pem` file |
| Create App (Personal) | `https://github.com/settings/apps/new` |
| Create App (Org) | `https://github.com/organizations/ORG/settings/apps/new` |
