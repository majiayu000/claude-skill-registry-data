---
name: check-env
description: Use when validating environment variables exist before deploy, after fresh clone, or when debugging connection issues
disable-model-invocation: true
---

# Check Env — Validate Environment Variables

Checks that all required env vars from `.env.example` are set without exposing their values.

## What It Checks

Read `.env.example` and `.env.local` (or `.env`), then report:

| Variable | Status |
|----------|--------|
| `NEXT_PUBLIC_SUPABASE_URL` | Set / Missing / Empty |
| `SUPABASE_SERVICE_ROLE_KEY` | Set / Missing / Empty |
| ... | ... |

## Categories

**Required (app won't work without):**
- `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
- `NEYNAR_API_KEY`
- `SESSION_SECRET`
- `APP_FID`, `APP_SIGNER_PRIVATE_KEY`

**Optional (features degrade gracefully):**
- `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD` (Bluesky cross-posting)
- `PAPERCLIP_*` (AI agent company)
- `MINIMAX_*` (Minimax LLM)
- `X_*` (X/Twitter cross-posting)
- `ALCHEMY_*` (ENS resolution, webhook)
- `NEYNAR_WEBHOOK_SECRET` (webhook signature verification)

## Rules

- NEVER print or log actual values of env vars
- NEVER expose server-only vars (`SUPABASE_SERVICE_ROLE_KEY`, `NEYNAR_API_KEY`, `SESSION_SECRET`, `APP_SIGNER_PRIVATE_KEY`)
- Only report: Set / Missing / Empty
- Report a summary: "X/Y required vars set, Z optional vars configured"
- Flag any required var that is missing or still has placeholder value ("your_*")
