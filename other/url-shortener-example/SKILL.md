---
name: url-shortener-example
description: Reference implementation of a URL shortener using injectable with Axum, SQLite, authentication, and a multi-level service dependency graph. Use when building a similar app or as a complete injectable reference.
---

# URL Shortener — Complete Example

A production-style URL shortener demonstrating injectable's full feature set.
Source: `examples/11_url_shortener.rs`.

Run:
```bash
cargo run --example 11_url_shortener --features axum
```

## Dependency graph (4 levels)

```
AppConfig            (level 0 — constructor injection, reads env)
    ↓ make_db_pool   (#[injectable(factory)] — called once per service type)
AuthService          (level 1 ← pool)
UrlService           (level 1 ← pool, Arc<AppConfig>)
AnalyticsService     (level 2 ← pool, Arc<UrlService>)
RedirectService      (level 3 ← Arc<UrlService>, Arc<AnalyticsService>)
LinkPreviewService   (level 2 ← Arc<UrlService>, Arc<AppConfig>)
```

## Key patterns demonstrated

| Feature | Where used |
|---|---|
| `#[injectable(factory)]` factory | `make_db_pool` reads `Inject<AppConfig>` |
| `use_factory_async` | pool field on AuthService, UrlService, AnalyticsService |
| `Arc<T>` service deps | AnalyticsService holds `Arc<UrlService>` |
| `#[injectable(post_construct)]` | DB migrations on each service |
| `#[injectable(pre_destruct)]` | Pool shutdown on AuthService |
| Custom Axum extractor | `AuthenticatedUser` calls `Inject::<AuthService>::extract` |
| Multiple `Inject<T>` in one handler | dashboard handler injects AnalyticsService |

## Quick start

```bash
# Register and get API key
KEY=$(curl -s -X POST http://localhost:3000/api/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"alice@example.com"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['api_key'])")

# Shorten a URL
CODE=$(curl -s -X POST http://localhost:3000/api/shorten \
  -H "x-api-key: $KEY" -H 'Content-Type: application/json' \
  -d '{"url":"https://www.rust-lang.org","title":"Rust"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['code'])")

# Follow redirect (records click)
curl -L http://localhost:3000/$CODE

# Dashboard
curl http://localhost:3000/api/dashboard -H "x-api-key: $KEY"
```

See the full source at `examples/11_url_shortener.rs`.
