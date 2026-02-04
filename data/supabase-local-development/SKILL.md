---
name: Supabase Local Development
description: This skill should be used when the user asks to "start supabase locally", "set up local supabase", "run supabase dev", "initialize supabase project", "configure local database", "start local postgres", "use supabase CLI", "generate database types", or needs guidance on local Supabase development, Docker setup, environment configuration, or database migrations.
version: 0.1.0
---

# Supabase Local Development

## Overview

Supabase Local Development provides a complete local Postgres database with all Supabase services (Auth, Storage, Edge Functions, Realtime) running in Docker containers. This enables offline development, faster iteration, and safe database migrations before deploying to production.

**Key benefits:**
- Full Supabase stack running locally
- Faster development without network latency
- Safe migration testing before production
- Automatic TypeScript type generation
- Environment variable management

## Skill-scoped Context

**Official Documentation:**
- Local Development Guide: https://supabase.com/docs/guides/local-development
- CLI Getting Started: https://supabase.com/docs/guides/local-development/cli/getting-started
- supabase init: https://supabase.com/docs/reference/cli/supabase-init
- supabase start: https://supabase.com/docs/reference/cli/supabase-start
- supabase status: https://supabase.com/docs/reference/cli/supabase-status
- supabase db: https://supabase.com/docs/reference/cli/supabase-db
- Managing Environments: https://supabase.com/docs/guides/deployment/managing-environments

## Prerequisites

### Docker Runtime

Supabase local development requires a Docker-compatible container runtime:

- **Docker Desktop** (macOS, Windows, Linux)
- **Rancher Desktop** (macOS, Windows, Linux)
- **OrbStack** (macOS) - Recommended for Apple Silicon
- **Podman** (macOS, Windows, Linux)

Verify Docker is running:
```bash
docker info
```

### Supabase CLI

Install via npm (recommended for Next.js projects):
```bash
npm install -g supabase
```

Or via Homebrew (macOS):
```bash
brew install supabase/tap/supabase
```

Verify installation:
```bash
supabase --version
```

## Workflow

### Step 1: Initialize Supabase Project

```bash
supabase init
```

This creates a `supabase/` directory with:
- `config.toml` - Local configuration
- `seed.sql` - Optional seed data
- `migrations/` - Database migrations

### Step 2: Start Local Services

```bash
supabase start
```

First run downloads Docker images (~2GB). Subsequent starts are faster.

Services started:
| Service | Local URL | Purpose |
|---------|-----------|---------|
| API | http://127.0.0.1:54321 | REST/GraphQL API |
| Studio | http://127.0.0.1:54323 | Database UI |
| Inbucket | http://127.0.0.1:54324 | Email testing |
| Database | postgresql://127.0.0.1:54322 | Direct Postgres |

### Step 3: Get Environment Variables

```bash
supabase status -o env
```

Output:
```
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_DB_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres
```

### Step 4: Configure Next.js Environment

Add to `.env.local`:
```bash
# Supabase Local Development
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

**Note:** `NEXT_PUBLIC_` prefix exposes variables to the browser.

### Step 5: Generate TypeScript Types

```bash
supabase gen types typescript --local > lib/supabase/database.types.ts
```

Regenerate after schema changes.

## Environment Variables

### Client-Side (Browser)

Prefix with `NEXT_PUBLIC_`:
```
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

### Server-Side Only

No prefix required:
```
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_DB_URL=postgresql://...
```

### Environment File Detection

| Framework | File | Priority |
|-----------|------|----------|
| Next.js | `.env.local` | 1st |
| Next.js | `.env.development.local` | 2nd |
| Generic | `.env` | 3rd |
| Cloudflare Workers | `dev.vars` | Special |

## Database Migrations

### Create Migration from Local Changes

```bash
supabase db diff -f migration_name
```

### Apply Migrations Locally

```bash
supabase db reset
```

### Push to Remote Database

```bash
supabase db push
```

### Link to Remote Project

```bash
supabase link --project-ref YOUR_PROJECT_REF
```

## Type Generation

### From Local Database

```bash
supabase gen types typescript --local > lib/supabase/database.types.ts
```

### From Remote Database

```bash
supabase gen types typescript --project-id YOUR_PROJECT_ID > lib/supabase/database.types.ts
```

### Usage in Code

```typescript
import { createClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `supabase init` | Initialize new project |
| `supabase start` | Start local services |
| `supabase stop` | Stop local services |
| `supabase status` | Show service status |
| `supabase status -o env` | Output as environment variables |
| `supabase db reset` | Reset database and apply migrations |
| `supabase db diff -f name` | Create migration from changes |
| `supabase db push` | Push migrations to remote |
| `supabase gen types typescript --local` | Generate types from local |
| `supabase link --project-ref REF` | Link to remote project |

## Troubleshooting

### Docker Not Running

```bash
# macOS - Start Docker Desktop
open -a Docker

# Linux - Start Docker daemon
sudo systemctl start docker
```

### Port Conflicts

If ports are in use:
```bash
supabase stop --no-backup
supabase start
```

Or configure different ports in `supabase/config.toml`.

### Reset Everything

```bash
supabase stop --no-backup
supabase start
supabase db reset
```

## Best Practices

**DO:**
- Always use `supabase db diff` for migrations
- Regenerate types after schema changes
- Use `.env.local` for local credentials (gitignored)
- Test migrations locally before pushing to production

**DON'T:**
- Commit local Supabase credentials
- Modify production database directly
- Skip local testing for migrations
- Use service role key in client-side code
