---
name: jc-mobile-refactor
description: Use when refactoring or modernizing existing JapaConnect Flutter mobile app code (apps/mobile). Covers feature module extraction, japaconnect_core consolidation, migration to Riverpod, removal of hardcoded data per Rule 16, OpenAPI client regeneration, app-shell conformance, and the v2.1 screen contract per §77, ADR-067, ADR-074, and ADR-113.
---

# JapaConnect Mobile App — Refactor Skill

You are refactoring the Flutter mobile client without changing behavior. Goals: improve structure, remove duplication, align with JEOS, and make the codebase easier for agents to navigate and modify. All refactors must preserve the v2.1 screen contract, API-Readiness Gate, and Rule 16.

## When to Use This Skill

- Migrating from one state-management approach to Riverpod.
- Extracting a duplicated widget into `japaconnect_core`.
- Splitting a monolithic feature into a self-contained module.
- Regenerating the typed API client after OpenAPI spec changes.
- Converting hardcoded data to API-driven data (Rule 16).
- Aligning an older screen with the new app shell (ADR-058 mobile adaptation).
- Removing dead routes, screens, or dependencies.
- Preparing the app for a new backend phase (v2 tool screens).

## Step 0 — Verify Before Refactoring

1. Read the relevant spec: `sections/77-flutter-mobile-app.md`, `adr/ADR-067-flutter-mobile-app.md`, `adr/ADR-074-flutter-mobile-app-surface.md`, `adr/ADR-113-mobile-framework-agent-ease-tradeoff.md`.
2. Identify every endpoint the refactored feature consumes. Confirm they still exist in `conventions/api-routes-catalog.md`.
3. Run `flutter analyze` and `flutter test` before the refactor and capture the baseline.
4. Create a branch or checkpoint if you plan to make large changes. Do not force-push.

## 1. Refactor Patterns

### 1.1 Extract duplicated widget into `japaconnect_core`

When the same widget appears in two or more feature modules:

1. Move it to `packages/japaconnect_core/lib/widgets/<name>.dart`.
2. Use the shared design tokens (`JcColors`, `JcTypography`, `JcSpacing`).
3. Make it configurable via constructor parameters.
4. Replace all occurrences in `apps/mobile/lib/features/` with the shared import.
5. Add/update widget tests in `packages/japaconnect_core/test/`.

### 1.2 Migrate state to Riverpod

Replace `StatefulWidget` + `setState` chains with:

- `StateProvider` or `StateNotifier` for simple state.
- `AsyncNotifier` / `FutureProvider` for API-backed state.
- `StreamProvider` for WebSocket / real-time streams.

Rules:
- Keep providers as close to the consuming widgets as possible (feature-scoped when possible).
- Do not put business logic directly in UI; put it in the service layer.
- Do not access providers across feature-module boundaries.

### 1.3 Convert hardcoded data to API-driven

Find hardcoded data in `apps/mobile/lib/features/`:

```dart
// WRONG — Rule 16 violation
const countries = [Country(code: 'NG', name: 'Nigeria'), ...];

// CORRECT — from API
final countries = await ref.read(apiClientProvider).spaces.listCountries();
```

After converting, verify the API route exists and returns the expected shape. Update the typed `japaconnect_core` client if the route was added or changed.

### 1.4 Regenerate the typed API client

When the OpenAPI spec (§47) or backend route contract changes:

1. Run the documented generator in `packages/japaconnect_core/` (e.g., `dart run build_runner build --delete-conflicting-outputs` or the OpenAPI generator command).
2. Review the generated diff. Do not hand-edit generated files.
3. If a generated model field is missing, fix the spec or the backend, then regenerate.
4. Update feature code to use the new method names.

### 1.5 Extract a monolithic feature module

If a feature has grown into multiple concerns:

1. Create `lib/features/<new_feature>/`.
2. Move the relevant screens, providers, services, and widgets.
3. Update `lib/app/router.dart` to import the new routes.
4. Remove the moved files from the old feature.
5. Verify no cross-imports between old and new feature.

### 1.6 Update the app shell

If a screen predates the unified mobile shell:

1. Move the screen into the `AppShell` navigation structure.
2. Remove bespoke `AppBar`/`BottomNavigationBar` from the screen.
3. Use `go_router` for deep links and tab routing.
4. Ensure the bottom nav and top bar are defined once in `app/app_shell.dart`.

### 1.7 Remove dead code

- Delete routes with no screen.
- Delete providers that are never watched.
- Delete `print` statements, commented-out code, and unused imports.
- Run `flutter analyze` to catch unused symbols.
- Run `flutter test` to confirm nothing broke.

## 2. Refactor Checklist

- [ ] Feature modules remain self-contained (no sibling imports).
- [ ] `japaconnect_core` is the only package shared across features.
- [ ] All API calls go through the typed client (no raw HTTP in feature code).
- [ ] No hardcoded data remains after the refactor.
- [ ] OpenAPI client is regenerated if the contract changed.
- [ ] State management is migrated to Riverpod where applicable.
- [ ] Duplicate widgets are consolidated in `japaconnect_core`.
- [ ] App shell is used consistently; no per-screen bespoke nav.
- [ ] `flutter analyze` passes with zero errors.
- [ ] `flutter test` passes.
- [ ] iOS and Android builds still succeed on a baseline target.
- [ ] No AI attribution in comments or commit messages.

## 3. Common Refactor Dangers

- **Breaking feature-module isolation.** If a refactor causes one feature to import another, the standalone-app extraction promise (ADR-086 §7) is broken.
- **Drifting from the OpenAPI spec.** Always regenerate; never hand-edit generated models.
- **Losing the API-Readiness Gate.** A refactor that swaps one endpoint for another must verify the new endpoint exists and is live.
- **Token storage regression.** Refactors of auth code must keep access tokens in memory and refresh tokens in `flutter_secure_storage`.
- **State-management churn.** Do not partially migrate — a screen with both `setState` and Riverpod is worse than one or the other.

## 4. Verification

After every refactor:

1. `flutter pub get` in `apps/mobile/` and `packages/japaconnect_core/`.
2. `flutter analyze` — zero errors.
3. `flutter test` — all pass.
4. If UI changed, run on an Android emulator and an iOS simulator (iOS requires macOS).
5. Probe the affected API endpoints with `curl` to confirm the contract.
6. Run `gosec` and `go test ./...` if the refactor required backend changes.
