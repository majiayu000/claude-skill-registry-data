---
name: jc-mobile-develop
description: Use when building new pages, components, or feature modules for the JapaConnect Flutter mobile app (apps/mobile, Dart, v2.1 fast-follow). Covers the shared japaconnect_core package, device-scoped JWT auth, Riverpod state, the v2.1 screen contract, push notification wiring, offline/caching policy, and the API-Readiness Gate per §77, ADR-067, ADR-074, and ADR-113.
---

# JapaConnect Mobile App — Development Skill

You are building the native iOS + Android Flutter client for JapaConnect. One Dart codebase in `apps/mobile/`, one shared Dart package in `packages/japaconnect_core/`. The app is a **thin client over `/api/v1`**. All data comes from the Go backend. The web surfaces are the source of feature truth — the mobile app renders the same features with a touch-first shell.

## ⛔ API-READINESS GATE — RUN BEFORE ANY IMPLEMENTATION

Before writing a single line for any screen or feature module:

1. **List every API endpoint** the screen will consume (reads + mutations).
2. **Verify each exists** in `.jeos/conventions/api-routes-catalog.md` or probe the running backend (`curl -s http://localhost:8080/api/v1/...`).
3. **If ANY endpoint is missing or returns 404:** STOP. Do not implement. Do not mock. Do not hardcode placeholder data. Output the alert:

```
⚠️ MISSING BACKEND API ROUTES — mobile implementation paused
Feature: [feature name]
Missing routes:
  - GET  /api/v1/...
Action needed: implement these routes in the Go backend before mobile work continues.
```

Rule 16 (no hardcoded data) applies to Flutter exactly as to SvelteKit. No mock user objects, no static option lists, no hardcoded navigation. Every list, every option, every user-owned value must come from the API.

## Non-Negotiable Stack

- **Flutter** (stable channel), **Dart**, **Bun** is not used in Flutter — use `flutter` CLI and `dart` CLI directly.
- **State:** Riverpod (preferred) or equivalent; no `setState` soup in feature screens.
- **Auth:** `flutter_secure_storage` (refresh token + device ID), in-memory access token, `X-Device-Id` header on every request.
- **HTTP:** the typed `japaconnect_core` API client only — no raw `http` or `dio` in feature code.
- **Models:** typed Dart models in `japaconnect_core/lib/models/` generated from the OpenAPI spec (§47).
- **UI:** JapaConnect design tokens (colors, typography, spacing) in `japaconnect_core/lib/widgets/`. Shared components: `EntityCard`, `FeedCard`, `AvatarWidget`, `LoadingShimmer`.
- **Images:** `CachedNetworkImage` (or equivalent) for remote images; placeholder + error widget.
- **Push:** `firebase_messaging` (Android) / `flutter_apns` or `firebase_messaging` iOS with APNs. Device token registered via `POST /api/v1/me/devices`.
- **Charts:** `fl_chart` for mobile analytics (do not import web-only chart libraries).
- **Navigation:** `go_router` for deep links and shell routing.

Forbidden in production Flutter code:
- Raw `http` calls in `apps/mobile/lib/features/`
- Hardcoded data that should come from the API (Rule 16)
- Storing access tokens in `flutter_secure_storage` or `SharedPreferences`
- `localStorage` (no browser here)
- AI attribution in comments or commit messages (Rule 17)

## Repository Structure

```
apps/mobile/
  pubspec.yaml              # depends on japaconnect_core (path: ../../packages/japaconnect_core)
  lib/
    main.dart               # entry point, ProviderScope, GoRouter
    app/                    # shell, theme, router, global providers
      app_shell.dart
      theme.dart            # JapaConnect tokens
      router.dart           # go_router configuration
      auth_guard.dart
    features/               # each feature is self-contained
      auth/
      feed/
      forum/
      content/
      tools/
      spaces/
      social/
      learning/
      profile/
      gamification/
      jobs/
packages/japaconnect_core/
  lib/
    api/                    # generated typed client
    auth/                   # AuthService, token refresh, device ID
    models/                 # typed Dart models
    widgets/                # shared UI primitives + design tokens
```

Every feature module owns its routes, screens, providers, and service layer. It depends only on `japaconnect_core`. No imports from sibling `features/` modules.

## The Mobile App Shell

- **Bottom navigation** (iOS + Android): Home, Spaces, Tools, Notifications, Profile. Center tab is a Compose FAB.
- **Top app bar**: context-aware; search opens a search delegate; avatar opens account menu.
- **Home feed**: `FeedCard` list, pull-to-refresh, infinite scroll (`scrollController` + pagination from API).
- **Single-screen pattern**: blog/guides/comparisons open as single scrollable pages; forums use a list-detail pattern; DMs use chat bubbles; JapaBot is a chat thread.
- **Safe area + insets**: respect `MediaQuery` padding and `viewInsets` for keyboards.
- **Dark mode**: theme token toggled from `jc_theme` (synced via `PATCH /api/v1/me/settings`).

## `japaconnect_core` — The Contract

### API client (`lib/api/client.dart`)

Generated from the OpenAPI spec (§47). Every method maps to one `/api/v1` route. It handles:
- Base URL from `JC_API_BASE_URL` env / `system_settings`
- Bearer token injection from in-memory access token
- `X-Device-Id` header injection from `flutter_secure_storage`
- 401 → refresh token → retry with new access token (max 1 retry)
- Standard error format (`{ error: { code, message, status } }`) → typed exceptions

### Auth service (`lib/auth/service.dart`)

- `login(username, password)` → `POST /api/v1/auth/login`; stores refresh token + device ID; keeps access token in memory.
- `refresh()` → `POST /api/v1/auth/refresh` with refresh token; updates in-memory access token.
- `logout()` → `POST /api/v1/auth/logout`; deregisters push token (`DELETE /api/v1/me/devices/:device_id`); clears stored tokens.
- `deviceId` — generated UUID on first install, persisted in `flutter_secure_storage`, sent as `X-Device-Id`.
- `TOTPPrompt` widget — shown when login response requires TOTP; calls `POST /api/v1/auth/totp/verify`.

### Models (`lib/models/`)

Typed Dart classes for all API entities: `User`, `Content`, `Space`, `Guide`, `Assessment`, `Notification`, `Conversation`, etc. Use `freezed` or hand-written `fromJson`/`toJson`. Every model property is nullable where the API schema is nullable.

### Widgets (`lib/widgets/`)

- `EntityCard` — generic list item
- `FeedCard` — full feed card with avatar, name, space, content preview, engagement bar
- `AvatarWidget` — rounded avatar with placeholder and error
- `LoadingShimmer` — skeleton loading
- `JcErrorWidget` — standard error state with retry
- `EmptyState` — illustration + message + CTA
- `JcButton`, `JcIconButton`, `JcTextField`, `JcBadge`, `JcPill`
- Design tokens: `JcColors`, `JcTypography`, `JcSpacing` — used by all feature screens.

## Feature Module Pattern

To add a new mobile screen:

1. Verify API routes exist (API-Readiness Gate).
2. Create `lib/features/<name>/` with the scaffold:
   - `screens/` — one screen per route
   - `providers/` — Riverpod providers (notifiers / async notifiers)
   - `services/` — thin service calling `japaconnect_core` API client
   - `widgets/` — private widgets used only by this feature
3. Add routes in `app/router.dart`.
4. Wire providers to `app/` global providers only when truly global; prefer local scoping with `ProviderScope`.
5. Use the shared widgets; never define a second `FeedCard` inside a feature.
6. Add widget tests under `test/features/<name>/`.
7. Run `flutter analyze` and `flutter test` before finishing.

## Authentication & Onboarding

- Login, Register, Forgot, TOTP — use `auth/` feature.
- Onboarding wizard calls `GET /api/v1/onboarding/*` and posts selections to `PATCH /api/v1/me`.
- No browser cookies. CSRF exemption. All auth via Bearer token.

## Push Notifications

1. Request permission via `firebase_messaging`.
2. On token refresh, call `POST /api/v1/me/devices` with `{ device_id, platform, token }`.
3. Store the token locally only for re-registration; the backend owns the authoritative list (`GET /api/v1/me/devices`).
4. On logout, call `DELETE /api/v1/me/devices/:device_id`.
5. Foreground messages: show an in-app snackbar or update the notifications badge.
6. Background/terminated: route via deep link (`/notifications`, `/messages/:id`, `/spaces/:slug`, etc.).

## Offline / Caching Policy

- **Feed and content**: in-memory Riverpod cache (or `Riverpod` provider state); show last-loaded state while refresh runs.
- **No local SQLite / Hive database** (deferred to v3).
- **Optimistic UI**: reactions, follows, bookmarks update local state first and revert on API error with a snackbar.
- **Compose drafts**: small JSON blob in `flutter_secure_storage`, restored on reopen.
- **Image cache**: `CachedNetworkImage` disk cache.

## V2.1 Screen Contract

Build order follows backend completion. Every screen below must have verified endpoints before implementation.

**Launch screens (v1 endpoints — build first):**
Auth/onboarding, home feed, discover, blog, guides, comparisons, forum, JapaBot chat, spaces, follow/social, notifications, DMs, Japa Academy, profile, settings, wallet, bookmarks, badges/challenges/leaderboard, jobs finder.

**V2 tool screens (add as backend phases 43–44 complete):**
Visa Checklist, Readiness Assessment, Cost of Living, Scholarship Finder, Remittance Rate Tracker.

**Out of scope for mobile:** Admin Panel, Control Panel, AI Content Studio, Persona management, Creator/Instructor dashboard.

## Implementation Checklist

Before finishing any mobile feature, verify:
- [ ] All API routes exist and are called through `japaconnect_core`
- [ ] No hardcoded data that should come from the API
- [ ] Feature module is self-contained (no sibling imports)
- [ ] `X-Device-Id` header is sent on all authenticated requests
- [ ] Access token is in memory only; refresh token + device ID in `flutter_secure_storage`
- [ ] Push token registration/unregistration is wired (if the feature triggers notifications)
- [ ] Optimistic UI has rollback on error
- [ ] Widget tests pass
- [ ] `flutter analyze` passes with zero issues
- [ ] iOS Simulator and Android Emulator both render the screen without overflow
- [ ] Dark mode tokens are applied
