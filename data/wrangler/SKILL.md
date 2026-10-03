---
name: wrangler
description: "Use Cloudflare Wrangler CLI for Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and secrets."
---

# Wrangler CLI

Deploy, develop, and manage Cloudflare Workers and associated resources.

## FIRST: Verify Wrangler Installation

```bash
wrangler --version  # Requires v4.x+
```

If not installed:
```bash
npm install -D wrangler@latest
```

## Key Guidelines

- **Use `wrangler.jsonc`**: Prefer JSON config over TOML. Newer features are JSON-only.
- **Set `compatibility_date`**: Use a recent date (within 30 days).
- **Generate types after config changes**: Run `wrangler types` to update TypeScript bindings.
- **Local dev defaults to local storage**: Bindings use local simulation unless `remote: true`.
- **Validate config before deploy**: Run `wrangler deploy --dry-run` to catch errors early.
- **Use environments for staging/prod**: Define `env.staging` and `env.production` in config.

## Quick Start: New Worker

```bash
npx wrangler init my-worker
npx create-cloudflare@latest my-app  # With a framework
```

## Quick Reference: Core Commands

| Task | Command |
|------|---------|
| Start local dev server | `wrangler dev` |
| Deploy to Cloudflare | `wrangler deploy` |
| Deploy dry run | `wrangler deploy --dry-run` |
| Generate TypeScript types | `wrangler types` |
| Validate configuration | `wrangler deploy --dry-run` |
| View live logs | `wrangler tail` |
| Delete Worker | `wrangler delete` |
| Auth status | `wrangler whoami` |

---

## Configuration (wrangler.jsonc)

### Minimal Config

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01"
}
```

### Full Config with Bindings

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  "compatibility_flags": ["nodejs_compat_v2"],
  "vars": { "ENVIRONMENT": "production" },
  "kv_namespaces": [{ "binding": "KV", "id": "<KV_NAMESPACE_ID>" }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket" }],
  "d1_databases": [{ "binding": "DB", "database_name": "my-db", "database_id": "<DB_ID>" }],
  "ai": { "binding": "AI" },
  "vectorize": [{ "binding": "VECTOR_INDEX", "index_name": "my-index" }],
  "hyperdrive": [{ "binding": "HYPERDRIVE", "id": "<HYPERDRIVE_ID>" }],
  "durable_objects": { "bindings": [{ "name": "COUNTER", "class_name": "Counter" }] },
  "triggers": { "crons": ["0 * * * *"] },
  "env": {
    "staging": { "name": "my-worker-staging", "vars": { "ENVIRONMENT": "staging" } }
  }
}
```

### Generate Types from Config

```bash
wrangler types                      # Generate worker-configuration.d.ts
wrangler types ./src/env.d.ts       # Custom output path
wrangler types --check              # Check types are up to date (CI)
```

---

## Local Development

```bash
wrangler dev                        # Local mode (default)
wrangler dev --env staging          # With specific environment
wrangler dev --local                # Force local-only
wrangler dev --remote               # Remote mode (legacy)
wrangler dev --port 8787            # Custom port
wrangler dev --live-reload          # Live reload for HTML changes
wrangler dev --test-scheduled       # Test scheduled/cron handlers
# Then visit: http://localhost:8787/__scheduled
```

### Remote Bindings for Local Dev

Use `remote: true` in binding config for real resources while running locally:

```jsonc
{
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket", "remote": true }],
  "ai": { "binding": "AI", "remote": true },
  "vectorize": [{ "binding": "INDEX", "index_name": "my-index", "remote": true }]
}
```

**Recommended remote**: AI (required), Vectorize, Browser Rendering, mTLS, Images.

### Local Secrets

Create `.dev.vars`:
```
API_KEY=local-dev-key
DATABASE_URL=postgres://localhost:5432/dev
```

---

## Deployment

```bash
wrangler deploy                     # Deploy to production
wrangler deploy --env staging       # Deploy specific environment
wrangler deploy --dry-run           # Validate without deploying
wrangler deploy --keep-vars         # Keep dashboard-set variables
wrangler deploy --minify            # Minify code
```

### Manage Secrets

```bash
wrangler secret put API_KEY                  # Set interactively
echo "value" | wrangler secret put API_KEY   # Set from stdin
wrangler secret list                         # List secrets
wrangler secret delete API_KEY               # Delete
wrangler secret bulk secrets.json            # Bulk from JSON
```

### Versions and Rollback

```bash
wrangler versions list
wrangler versions view <VERSION_ID>
wrangler rollback
wrangler rollback <VERSION_ID>
```

---

## Storage & Compute Services

> 상세 CLI 레퍼런스: [references/storage-services.md](references/storage-services.md) (KV, R2, D1, Vectorize, Hyperdrive)

> 상세 CLI 레퍼런스: [references/compute-services.md](references/compute-services.md) (AI, Queues, Containers, Workflows, Pipelines, Secrets Store, Pages)

---

## Observability

```bash
wrangler tail                       # Stream live logs
wrangler tail my-worker             # Tail specific Worker
wrangler tail --status error        # Filter by status
wrangler tail --format json         # JSON output
```

Config: `"observability": { "enabled": true, "head_sampling_rate": 1 }`

---

## Performance

```bash
wrangler check startup                       # Worker 시작(startup) 단계 CPU 프로파일 생성
wrangler check startup --args="--no-bundle"  # deploy를 --no-bundle로 할 때
```

`wrangler check startup`은 Worker의 **시작 단계 CPU 프로파일**을 만들어, 시작 시간 한도를 초과하는 스크립트를 찾게 해줍니다. 생성된 프로파일을 Chrome DevTools로 import하거나 VSCode에서 열어 flamegraph로 분석합니다.

- 측정은 **로컬 머신 CPU** 기준이라 Cloudflare 실제 시작 시간과 절대값이 다릅니다 — "전체 시간"이 아니라 "어디에 시간이 쓰이는지"를 보는 용도.
- 시작 시간 한도 초과로 배포가 실패하면 Wrangler가 자동으로 CPU 프로파일을 생성합니다.
- 주의: `wrangler check`는 이 `startup` 서브커맨드뿐 — 설정 검증 명령이 아닙니다(설정/빌드 검증은 `wrangler deploy --dry-run`).

---

## Testing with Vitest

```bash
npm install -D @cloudflare/vitest-pool-workers vitest
```

```typescript
// vitest.config.ts
import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: { wrangler: { configPath: "./wrangler.jsonc" } },
    },
  },
});
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: wrangler` | `npm install -D wrangler` |
| Auth errors | `wrangler login` |
| Config validation errors | `wrangler deploy --dry-run` |
| Type errors after config change | `wrangler types` |
| Local storage not persisting | Check `.wrangler/state` directory |
| Binding undefined in Worker | Verify binding name matches config |

## Best Practices

1. **Version control `wrangler.jsonc`**: Source of truth for Worker config.
2. **Use automatic provisioning**: Omit resource IDs for auto-creation.
3. **Run `wrangler types` in CI**: Catch binding mismatches.
4. **Use environments**: Separate staging/production.
5. **Set `compatibility_date`**: Update quarterly.
6. **Use `.dev.vars` for local secrets**: Never commit secrets.
7. **Test locally first**: `wrangler dev` before deploying.
8. **Use `--dry-run` before major deploys**.
