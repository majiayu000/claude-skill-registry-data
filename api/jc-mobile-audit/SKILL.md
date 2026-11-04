---
name: jc-mobile-audit
description: Use when performing a comprehensive quality audit of the JapaConnect Flutter mobile app (apps/mobile) before merge or release. Verifies the v2.1 screen contract, API-Readiness Gate, Rule 16, feature module isolation, auth model, push notification wiring, japaconnect_core contract, and build quality per §77, ADR-067, ADR-074, and ADR-113.
---

# JapaConnect Mobile App — Audit Skill

You are auditing the Flutter mobile client before merge or release. The audit cross-checks `apps/mobile/` and `packages/japaconnect_core/` against the JEOS specs: `sections/77-flutter-mobile-app.md`, `adr/ADR-067-flutter-mobile-app.md`, `adr/ADR-074-flutter-mobile-app-surface.md`, `adr/ADR-113-mobile-framework-agent-ease-tradeoff.md`, `AGENTS.md` Rule 16, and `conventions/api-routes-catalog.md`.

## Pre-requisites

1. `apps/mobile/` and `packages/japaconnect_core/` exist. If not, the audit stops: the mobile app is not implemented.
2. `flutter analyze` passes with zero errors (warnings are acceptable if documented).
3. `flutter test` passes.
4. The backend is running so live API routes can be probed.

## 1. API-Readiness Gate

For every screen in the v2.1 contract (ADR-074 §5), verify:

- [ ] The screen exists in `lib/features/<feature>/screens/`.
- [ ] The screen consumes API endpoints documented in `conventions/api-routes-catalog.md`.
- [ ] Every endpoint the screen calls returns a non-404 response under correct auth.
- [ ] If a required endpoint is missing, record it as a **backend gap**, not a frontend gap.

Launch-screen checklist:
- Auth/onboarding, home feed, discover, blog, guides, comparisons, forum, JapaBot, spaces, follow/social, notifications, DMs, Japa Academy, profile, settings, wallet, bookmarks, badges/challenges/leaderboard, jobs finder.

V2 tool-screen checklist (only required as their backend phases complete):
- Visa Checklist, Readiness Assessment, Cost of Living, Scholarship Finder, Remittance Rate Tracker.

Out-of-scope screens (must NOT exist in `apps/mobile/`):
- Admin Panel, Control Panel, AI Content Studio, Persona management, Creator/Instructor dashboard.

## 2. Rule 16 — No Hardcoded Data

Search `apps/mobile/lib/features/` for:

- [ ] No mock user objects (e.g., `const user = User(name: 'Test', ...)`).
- [ ] No static option lists that should come from API (countries, currencies, languages, categories, nav items).
- [ ] No hardcoded content or feed data.
- [ ] No static feature flags — must come from `GET /api/v1/feature-flags`.
- [ ] `pubspec.yaml` does not contain runtime API data.

Permitted hardcoded values:
- Pure client constants (animation durations, padding tokens, debounce delays).
- Asset paths and l10n keys.
- Environment/build-time constants (base URL, build flavor).

## 3. Feature Module Isolation

For each feature module in `lib/features/`:

- [ ] The feature has its own `screens/`, `providers/`, `services/`, and `widgets/`.
- [ ] The feature depends only on `japaconnect_core` and Flutter SDK packages.
- [ ] No imports from sibling `features/` modules.
- [ ] No service layer directly imports another feature's service.
- [ ] Route definitions live in `app/router.dart` or inside the feature's own `routes/` directory.

## 4. `japaconnect_core` Package Audit

### 4.1 API client

- [ ] Generated from the OpenAPI spec (§47) and the generation command is documented in `packages/japaconnect_core/README.md` or `Makefile`.
- [ ] No raw `http` or `dio` calls outside the generated client.
- [ ] Base URL is configurable (env or `system_settings`).
- [ ] `Authorization: Bearer <access_token>` sent on authenticated requests.
- [ ] `X-Device-Id` header sent on every request.
- [ ] 401 triggers one refresh-retry cycle.
- [ ] Standard error format is parsed into typed exceptions.

### 4.2 Auth service

- [ ] Access token is kept in memory only.
- [ ] Refresh token and device ID are stored in `flutter_secure_storage`.
- [ ] Device ID is a stable UUID generated on first install.
- [ ] TOTP prompt wires `POST /api/v1/auth/totp/verify`.
- [ ] Logout calls `POST /api/v1/auth/logout` and `DELETE /api/v1/me/devices/:device_id`.
- [ ] No secret values are logged or printed.

### 4.3 Models

- [ ] Every model has `fromJson` / `toJson`.
- [ ] Nullable fields match the API schema.
- [ ] No `dynamic` or `Map<String, dynamic>` leaking into feature code.
- [ ] Types are generated and checked against the OpenAPI spec.

### 4.4 Widgets

- [ ] Shared widgets exist: `EntityCard`, `FeedCard`, `AvatarWidget`, `LoadingShimmer`.
- [ ] Design tokens exist: `JcColors`, `JcTypography`, `JcSpacing`.
- [ ] Shared widgets are used in feature screens; no duplicate card implementations.

## 5. Authentication & Session Audit

- [ ] No SameSite cookie usage.
- [ ] CSRF-immune Bearer token only.
- [ ] Login/Register/Forgot/TOTP/Onboarding screens map to verified routes.
- [ ] Session scoping is per device (`jc:refresh:{user_id}:{device_id}` pattern, §02).
- [ ] Logout invalidates the current device only, not all sessions.

## 6. Push Notification Audit

- [ ] `firebase_messaging` (or APNs equivalent) is configured.
- [ ] `POST /api/v1/me/devices` is called on token registration.
- [ ] `DELETE /api/v1/me/devices/:device_id` is called on logout.
- [ ] Foreground, background, and terminated message handlers are wired.
- [ ] Deep links from push payloads route correctly (`go_router`).
- [ ] Backend `notification:send_push` Asynq task is wired and enqueued.
- [ ] `device_tokens.is_active` is set to `false` on invalid-token feedback (FCM/APNs).

## 7. Offline / Caching Policy

- [ ] Feed and content show last-loaded state while refresh runs.
- [ ] No SQLite / Hive dependency.
- [ ] Optimistic UI is implemented for reactions, follows, bookmarks and reverts on API error.
- [ ] Compose drafts are persisted in `flutter_secure_storage`.
- [ ] Images are cached via `CachedNetworkImage` or equivalent.

## 8. UI / UX Audit

- [ ] App shell follows the mobile design: bottom nav, context top app bar, search delegate.
- [ ] Feed uses `FeedCard` consistently across all content types.
- [ ] Screens adapt to 320dp–720dp widths.
- [ ] Dark mode tokens applied via theme data.
- [ ] Loading, empty, and error states are present on all data-driven screens.
- [ ] Pull-to-refresh and infinite scroll work on feed/list screens.
- [ ] Tap targets are at least 48×48dp.
- [ ] Screen readers / TalkBack labels are set for icon-only buttons.

## 9. Performance Audit

- [ ] No unbounded widget rebuilds.
- [ ] Images are constrained and cached.
- [ ] Lists are paginated from the API, not loaded all at once.
- [ ] No heavy computation inside `build` methods.
- [ ] `const` constructors are used for static subtrees.

## 10. Test & Build Audit

- [ ] `flutter analyze` returns zero errors (warnings documented).
- [ ] `flutter test` passes.
- [ ] Android build succeeds: `flutter build apk --flavor dev` or `flutter build appbundle`.
- [ ] iOS build succeeds on macOS: `flutter build ios --no-codesign` (simulator) or with provisioning (device).
- [ ] No debug code (print statements, fake data, commented-out routes) is committed.

## 11. Security Audit

- [ ] No secrets in `pubspec.yaml` or Dart code.
- [ ] Access token is not written to secure storage, logs, or crash reports.
- [ ] Refresh token is not logged.
- [ ] `flutter_secure_storage` is used for refresh token and device ID.
- [ ] Certificate pinning is not bypassed.
- [ ] No `allowClearTextTraffic` in release AndroidManifest (unless a dev flavor).

## Audit Output

Write findings to `.jeos/audit/mobile-audit.md` using the standard audit report format:

```
## 1. API-Readiness Gate
| Screen | Primary Endpoint | Status | Gap |
...

## 2. Rule 16 Findings
...

## 3. ...

## Summary
- Total bugs: <n>
- Conformance: <n> ✅ / <n> ⚠️ / <n> ❌
- Blockers: <list>
```
