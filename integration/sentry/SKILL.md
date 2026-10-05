---
name: sentry
description: Error tracking setup, source maps, performance tracing, Releases, breadcrumbs, filtering, alerts, SDK config (JS/Python).
---

## sentry

Error monitoring and performance tracking with Sentry.

### SDK setup
- Sentry.init with DSN and environment
- JavaScript: @sentry/react, @sentry/node
- Python: sentry-sdk with integrations
- Release and environment tagging

### Error tracking
- Automatic error capture
- Manual capture with Sentry.captureException
- Breadcrumbs for user actions
- beforeSend for filtering and enrichment

### Source maps
- Upload source maps to Sentry
- sentry-cli releases files
- Webpack/Vite plugin for auto-upload
- Error grouping with fingerprint

### Performance
- Tracing: transactions and spans
- Automatic browser/DB instrumentation
- Custom spans for critical paths
- Performance thresholds and alerts

### Alerts and workflows
- Issue alert rules and conditions
- Webhook and Slack/email notifications
- Metric alerts for regression detection
- Dashboard for team visibility
