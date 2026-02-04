---
name: configuration-env
description: Configure mjr.wtf safely via environment variables and .env files.
license: MIT
compatibility: Requires bash, git, and Go tooling.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.1
allowed-tools: Bash(git:*) Bash(make:*) Bash(go:*) Read
---

## Primary references

- `.env.example` (template)
- README “Configuration” + “Authentication”

## Core variables

- `DATABASE_URL` (required): SQLite database file path (e.g. `./database.db`)
- `AUTH_TOKENS` (recommended): comma-separated bearer tokens
- `AUTH_TOKEN` (legacy): single bearer token
- `BASE_URL` (recommended): base URL used when constructing short links

## Security-sensitive settings

- `SECURE_COOKIES=true` in production behind HTTPS.
- `ALLOWED_ORIGINS`: set explicit origins in production.
- `METRICS_AUTH_ENABLED=true` if `/metrics` should not be public.
