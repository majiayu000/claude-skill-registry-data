---
name: gcp-login
description: Authenticate to Google Cloud Platform using Application Default Credentials. Use when user selects GCP from cloud provider selection, or says "login to GCP", "gcloud auth", "authenticate to Google Cloud".
allowed-tools: Bash, Read, AskUserQuestion
---

# GCP Login Skill

Authenticate to Google Cloud Platform using `gcloud auth login --update-adc`.

## Activation Triggers

- `/auth-gcp` slash command
- User says: "login to GCP", "gcloud auth", "authenticate to GCP"

## Prerequisites

- `gcloud` CLI installed and in PATH
- Environment variables in `.env` (optional):
  - `GOOGLE_CLOUD_PROJECT` - GCP project ID for quota project
  - `GCLOUD_EMAIL_ADDRESS` - Email for bucket policy bindings

## Usage

### Human CLI

```powershell
# Authenticate to GCP
./scripts/gcp-auth.ps1

# Force re-authentication
./scripts/gcp-auth.ps1 -Force
```

### Claude Agent

```bash
# Via skill invocation
uv run --directory ${CLAUDE_PATH} python -m claude_apps.skills.gcp_login [--force]
```

## Auth URL Detection

The skill captures and displays the authentication URL:

| Field | Value |
|-------|-------|
| URL | https://accounts.google.com/o/oauth2/auth?... |

## Workflow

1. Check if already authenticated (skip if valid, unless `--force`)
2. Set project from `GOOGLE_CLOUD_PROJECT` env var if available
3. Run `gcloud auth login --update-adc --no-launch-browser`
4. Display auth URL for user to open in browser
5. Verify authentication success

## Code Structure

```
apps/src/claude_apps/skills/gcp_login/
├── __init__.py
├── __main__.py    # Entry point
└── auth.py        # GCloud auth with URL detection
```
