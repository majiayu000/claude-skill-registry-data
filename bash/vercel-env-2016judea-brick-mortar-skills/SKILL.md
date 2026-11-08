---
name: vercel-env
description: List, add or update Vercel project environment variables through the REST API with a personal token — no CLI, no dashboard clicking. Use whenever a task needs a new or changed Vercel env var (API keys, database ids, secrets), when a deploy fails because a var is missing, or when you would otherwise ask a human to paste a value into the Vercel dashboard.
compatibility: >-
  Python 3. Calls the Vercel REST API with the user's own VERCEL_TOKEN.
metadata:
  network-hosts: "api.vercel.com"
  network-purpose: "list and upsert project environment variables"
---

# Vercel env vars via the API

`scripts/vercel_env.py` talks to `api.vercel.com` directly. It is an upsert, so re-running is
safe, and `list` never prints values.

## Requires

`VERCEL_TOKEN` (Account Settings -> Tokens). For a project owned by a **team**, also
`VERCEL_TEAM_ID=team_...`: without it every call is scoped to your personal account and the
project "does not exist". If the token is missing, ask for one; do not try to obtain it any
other way.

## Commands

```bash
python3 scripts/vercel_env.py list --project my-site
python3 scripts/vercel_env.py set CRON_SECRET=$(python3 -c "import secrets;print(secrets.token_urlsafe(32))") --project my-site
python3 scripts/vercel_env.py set-from-env STRIPE_SECRET_KEY OPENAI_API_KEY --project my-site
```

- Default targets are `production,preview`. Add `--target production,preview,development` to
  cover local `vercel dev` too.
- `set-from-env` copies a value already exported in your shell, so a secret is never retyped
  into a command line or chat.

## After setting a var

**A new env var does not reach an existing deployment.** Redeploy (push a commit, or
`POST /v13/deployments` with the last deployment's `deploymentId` and `target: production`),
then check the function that reads it.

## Security

- `list` prints key names and targets only.
- Values are written `type: "encrypted"`; the script has no path to read a value back.
- Never put a token in a commit, a log line or a chat message.
