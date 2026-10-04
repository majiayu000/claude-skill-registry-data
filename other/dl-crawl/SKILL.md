---
name: dl-crawl
description: 20 crawlers avec TokenBucket, CircuitBreaker, cursor persistence
paths:
  - "src/adapters/crawlers/**"
  - "src/core/use-cases/crawl*"
  - "src/config/sources.ts"
---

# Crawlers — Datalake Souverain

20 crawlers with shared patterns:
- **AsyncGenerator** for memory-efficient streaming
- **TokenBucket** rate limiting per source
- **withRetry** exponential backoff
- **CircuitBreaker** prevents cascading failures
- **Cursor persistence** resume on interrupt (dl_crawl_cursors)

## Commands
```bash
pnpm crawl -- --source sirene --department 31 --max 5 --dry-run
pnpm crawl -- --source all --persist
pnpm enrich -- --siren 123456789
pnpm enrich -- --batch --limit 10 --type association
pnpm process -- --cross-ref --score --limit 1000
```

## Key patterns
- SIREN = universal key across all sources
- Dry run: `--dry-run` flag on all CLIs
- Audit trail: dl_crawl_runs + dl_crawl_cursors
- Source config: src/config/sources.ts (20 sources + CircuitBreaker config)
- OSINT tools: src/config/tools.ts (12 tools)
