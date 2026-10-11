---
name: sentry
description: Sentry — error tracking, APM, SDK setup, source maps.
---

# Sentry — Error Tracking & Performance Monitoring

## Detection Signals

| Signal | Location |
|--------|----------|
| `SENTRY_DSN` env var | `.env`, `.env.example`, CI secrets |
| `@sentry/` prefix | `package.json` dependencies |
| `sentry-sdk` | `requirements.txt`, `pyproject.toml` |
| `sentry/sentry-laravel` or `sentry/sentry-php` | `composer.json` |
| `sentry` service | `docker-compose.yml` |
| `.sentryclirc` or `sentry.properties` | repo root |

---

## Core Concepts

| Term | Meaning |
|------|---------|
| **DSN** | Data Source Name — the endpoint URL that SDKs send events to |
| **Environment** | `production`, `staging`, `development` — segments events |
| **Release** | Tagged version (`v1.2.3` or git SHA) — ties issues to deploys |
| **Issue** | Grouped set of similar events (same error + stacktrace fingerprint) |
| **Transaction** | A performance trace for one request or operation |
| **Span** | A timed segment inside a transaction (DB query, HTTP call) |

---

## SDK Initialization (key rules)

- Initialize Sentry **before** any other imports/modules that could throw
- Set `sendDefaultPii: false` — the safe GDPR default
- Set `environment` from an env var per deployment target
- Set `release` from git SHA or semver tag via CI
- Never hardcode `SENTRY_DSN` in source — treat it as a credential

Load `references/sdk-setup.md` for: full initialization code for Node.js, Browser, Python, Go, PHP/Laravel; custom context (`setUser`, `setTag`, `setExtra`); custom span examples.

---

## Sampling

| Traffic volume | `tracesSampleRate` |
|---------------|-------------------|
| < 1k req/day | `1.0` |
| 1k – 50k req/day | `0.2` |
| > 50k req/day | `0.05` + dynamic sampler |

Error capture always uses `sampleRate: 1.0` — never drop errors. Exclude `/health`, `/ping`, `/metrics` from performance traces.

Load `references/configuration.md` for: dynamic sampler example, release tracking CLI commands, GitHub Actions deploy integration, source maps upload, alerts setup, self-hosted Docker setup.

---

## Before Declaring Done

- [ ] `SENTRY_DSN` injected via env var — not hardcoded anywhere in source
- [ ] `environment` set correctly per deployment target
- [ ] `release` tied to git SHA or semver and created via `sentry-cli` in CI
- [ ] Sampling rate appropriate for traffic volume (not blindly `1.0` in prod)
- [ ] Source maps uploaded in CI; `.map` files not publicly accessible
- [ ] At minimum: new-issue alert + error-rate > 5% alert wired to a channel
- [ ] Health/ping/metrics routes excluded from error and performance capture
- [ ] `send_default_pii: false` unless GDPR exemption is documented
- [ ] Alert ownership assigned — no unowned alert rules
- [ ] **If self-hosted**: backup procedure tested; cleanup cron configured
