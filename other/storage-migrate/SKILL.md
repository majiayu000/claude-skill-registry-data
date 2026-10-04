---
name: storage-migrate
description: Switch the Baan storage backend between local, GCS, S3, and R2, and migrate required files safely. Use when asked to "switch storage", "migrate from local to S3", "move content to GCS", "change storage provider", or to diagnose storage-migration failures.
---

# Storage Migration Workflow

Baan abstracts storage across four backends (Local, GCS, S3, R2). Switching providers involves config + credential setup plus a structured migration of files that are required for the system to run (auth, settings).

## Required Reference

**Always read `docs/spec/storage.md` first** — it is the authoritative reference. The layout, required-file lists, and endpoint details below are a summary.

Related references:
- `docs/spec/auth-serverless.md` — token storage specifics (`_auth/`)
- `docs/spec/settings-serverless.md` — settings obfuscation rules (`_settings/`)

## Step 1: Confirm the current state

Before touching anything:

1. Read `settings/site.json` → `system.storageProvider` to find the current backend
2. Confirm the DB file exists at the configured `DATABASE_URL` (default `data/app.db`)
3. Snapshot critical files: `.refresh-tokens.json`, `settings/*.json`
4. Run `npm run build` to confirm the current state is healthy before migrating

If build fails, fix that first. Migrating from a broken state compounds problems.

## Step 2: Set credentials for the target backend

| Target | Required env vars |
|--------|-------------------|
| GCS | `GOOGLE_CLOUD_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS_JSON`, `GCS_BUCKET_NAME` |
| S3 | `AWS_REGION`, `AWS_S3_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| R2 | `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME` |
| Local | (none — uses `content/` on disk) |

Credentials go in `.env`, never in `settings/site.json`. See `docs/env-variables.md` for the full list.

## Step 3: Run the migration

Two paths:

### Admin UI (preferred)

`/baan-admin/[secretPath]/settings/system/storage` → Migrate. The UI:

1. Validates the target-backend connection
2. Auto-migrates required files (`_auth/`, `_settings/`)
3. Asks the user whether to migrate content (`content/`, images, pages)
4. Updates `settings/site.json` on success

### Direct API

`POST /baan-admin/api/storage/migrate`

```json
{
  "from": "local",
  "to": "s3",
  "deleteOld": false
}
```

Use `deleteOld: false` on the first attempt — keep a rollback copy.

## Step 4: Verify

1. `npm run dev` (or restart production)
2. Log in — if the `_auth/` migration failed, login is broken (most common failure mode)
3. Open Admin → verify settings loaded correctly
4. Open a public post → verify images resolve

## Common failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cannot log in after switching | `_auth/refresh-tokens.json` not migrated, or session-secret DB rotated | Re-run migration targeting `_auth/`, confirm DB untouched |
| Settings return defaults | `_settings/*.json` not migrated, or obfuscation key mismatch | Confirm session-secret DB is the same as pre-migration, then re-migrate `_settings/` |
| Images 404 | Content migration was skipped | Re-run migration with content included, or manually copy `content/images/` → cloud `images/` |
| "Invalid storageProvider" on startup | `settings/site.json` edited but env vars for the target not set | Set the credentials, restart |

## Required-files checklist (auto-migrated — never skip)

These must exist at the target for the system to function:

- `_auth/refresh-tokens.json` (encrypted, AES-256-GCM)
- `_settings/site.json`, `header.json`, `pages.json`, `security.json`, `integrations.json`, `ai.json`, `ai-usage.json`, `bot.json`, `aeo.json` (obfuscated, Base64 + XOR)

If the migration UI / API skipped any of these, stop and investigate. Do not hand-migrate `_auth/` without understanding the encryption — use the endpoint.

## Do not

- Do not edit `settings/site.json` `storageProvider` manually before the migration — the system reads it during migration to know the source
- Do not delete `data/app.db` — the session secret lives there; losing it invalidates every token in `_auth/`
- Do not migrate with `deleteOld: true` until the target is verified working
