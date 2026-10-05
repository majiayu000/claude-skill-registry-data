---
name: gmail
description: Fetch Gmail using existing Google Workspace credentials at ~/.google_workspace_mcp/credentials/greenteatree01@gmail.com.json
version: 1.0.0
---

# Gmail Skill

Fetches Gmail using existing Google Workspace OAuth credentials.

## Prerequisites

Credentials file exists at:
```
~/.google_workspace_mcp/credentials/greenteatree01@gmail.com.json
```

## Usage

Fetch most recent email:
```bash
uvx --from google-auth --with google-api-python-client --with google-auth-oauthlib python3 ~/.claude/skills/gmail/fetch.py
```

Fetch with options:
```bash
# Fetch N most recent emails
uvx --from google-auth --with google-api-python-client --with google-auth-oauthlib python3 ~/.claude/skills/gmail/fetch.py --count 5

# Search emails
uvx --from google-auth --with google-api-python-client --with google-auth-oauthlib python3 ~/.claude/skills/gmail/fetch.py --query "from:someone@example.com"
```

## Credential Location

The working credentials are at:
```
~/.google_workspace_mcp/credentials/greenteatree01@gmail.com.json
```

These contain a refresh token with full Gmail scopes (readonly, compose, send, modify).
