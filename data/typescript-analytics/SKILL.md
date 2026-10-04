---
name: typescript-analytics
description: Use when implementing analytics with PostHog in a TypeScript app — capturing events, identifying users, adding feature flags, tracking errors, or wiring API lifecycle telemetry. Triggers on edits to analytics integration files, or mentions of "PostHog", "analytics", "feature flag", "event tracking", "capture", "identify", "A/B test", or "experiment".
when_to_use: |
  Use when instrumenting event tracking, adding analytics calls, or working with PostHog integration in a TypeScript/Next.js app: adding or modifying event capture, user identification, feature flags, A/B test experiments, error tracking, or API lifecycle telemetry. Triggers on edits to PostHog or analytics modules, or any work that involves event enums, analytics wrapper functions, or PostHog client/server initialization.

  Not when: the task is building data pipelines, ETL jobs, or BigQuery integrations — use typescript-data-engineering. Not when the task is writing tests for analytics code — use typescript-testing-backend or typescript-testing-frontend. Not when the need is the skills library's own opt-in usage telemetry — use telemetry.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Analytics Engineering (PostHog + TypeScript)

You are operating as an analytics engineer. Your job is to ship telemetry that product can actually trust — explicit events, consistent naming, and full lifecycle coverage — never autocapture noise.

PostHog client/server SDKs integrated into a Next.js app via a unified `getPostHog()` getter, with proxied ingest to bypass ad blockers, typed event enums, and serverless-safe flush semantics. Covers explicit event capture, feature flags, error tracking, user identification, and source-map uploads.

## Universal Rules

1. **Never use autocapture** — all events must be explicit and registered in the project's event enum.
2. **Track the full lifecycle** — `cta_clicked` → `in_progress` → `success` / `error`.
3. **Use the unified pattern** — use the project's analytics wrapper functions for both client and server, not raw SDK imports.
4. **Flush immediately on server** — `flushAt: 1`, `flushInterval: 0`, always `shutdown()` in `finally`.
5. **Default flags to disabled** — `false` on error or when flags haven't loaded (fail-closed).
6. **Identify by user ID** — never by email; set email as a person property.
7. **Proxy through `/ph`** — never call PostHog directly from the client.
8. **Add new events to the project's event enum** — never use raw strings for event names.
9. **Include domain context** — slug, name, status, and relevant IDs in every event.
10. **Mask sensitive data** — wallet addresses should be masked in properties.

## References

- [references/setup-and-architecture.md](references/setup-and-architecture.md) — dependencies, proxy, init, env vars, file layout, unified client/server pattern, automatic metadata injection
- [references/event-tracking.md](references/event-tracking.md) — `EVENTS` enum, naming convention, `capturePostHogEvent`, `captureApiEvent`, manual capture example
- [references/typed-analytics.md](references/typed-analytics.md) — `ANALYTICS_EVENTS`, typed property maps, `Analytics` class, `useAnalytics` hook, pageview tracking
- [references/user-identification.md](references/user-identification.md) — `PosthogTrackIdentity`, identify by user ID, group membership
- [references/feature-flags.md](references/feature-flags.md) — `FEATURE_FLAGS` enum, client-side `useFeatureFlag`, server-side `checkFeatureFlag`/`getFeatureFlag`
- [references/error-tracking.md](references/error-tracking.md) — `capturePosthogError`, `useComponentError`, `ERROR_TYPES`, automatic API error tracking
- [references/properties-and-source-maps.md](references/properties-and-source-maps.md) — auto-injected metadata, commonly tracked properties, PostHog source map upload workflow
