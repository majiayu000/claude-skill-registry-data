---
name: env-management
description: Manage environment variables with split .env.client and .env.api structure. Use when adding new env vars, debugging config issues, or setting up environments.
---

# Environment Variables

## Split Structure

This project uses split env files (see `docs/PRDs/env-system-refactor.md`):

| File          | Purpose             | Prefix          |
| ------------- | ------------------- | --------------- |
| `.env.client` | Public browser vars | `NEXT_PUBLIC_*` |
| `.env.api`    | Server secrets      | No prefix       |

## Adding New Variables

### Client-side (Public)

1. Add to `.env.client`:
   ```
   NEXT_PUBLIC_API_URL=https://api.example.com
   ```
2. Access in code:
   ```typescript
   const url = process.env.NEXT_PUBLIC_API_URL;
   ```

### Server-side (Secret)

1. Add to `.env.api`:
   ```
   STRIPE_SECRET_KEY=sk_live_xxx
   ```
2. Access only in server code:
   ```typescript
   // Only in app/api/*, server/*, or Server Components
   const key = process.env.STRIPE_SECRET_KEY;
   ```

## Security Rules

- Never put secrets in `.env.client`
- Never prefix secrets with `NEXT_PUBLIC_`
- Supabase anon key is public (safe for client)
- Supabase service role key is secret (API only)

## Local Development

Copy example files:

```bash
cp .env.client.example .env.client
cp .env.api.example .env.api
```

## Cloudflare Deployment

Set vars in Cloudflare Pages dashboard under Settings > Environment Variables.
