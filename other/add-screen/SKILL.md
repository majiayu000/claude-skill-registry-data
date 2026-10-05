---
name: add-screen
description: Add a Compose Multiplatform feature screen with its route, encoded arguments, NavGraph entry, ViewModel, Koin registration, shared UI conventions, and validation. Use when adding a screen or changing navigation and screen-level dependency wiring.
---

# Add a screen

## Route and navigation

Add the route to `ui/navigation/Screen.kt`. Encode every dynamic path segment with `encodeRouteSegment` when navigating and decode it through the navigation argument APIs at the destination.

Register the destination in `ui/navigation/NavGraph.kt`. Follow nearby destinations for transitions, argument declarations, back navigation, deep links, and scanner integration. Do not pass resource snapshots through routes; pass stable identifiers and load through the repository.

## ViewModel and dependency injection

Create a ViewModel for any screen that loads or mutates data. Start work in `viewModelScope`, cancel or supersede stale loads where the existing feature pattern does so, and represent loading through `LoadState<T>`.

Register the ViewModel with `viewModelOf(::X)` in `di/AppModule.kt`. Register new dependencies in the same module. Missing Koin registrations compile and fail at runtime, so verify the complete constructor graph.

Resolve screen-scoped dependencies with `koinViewModel()` or `koinInject()`. Obtain `AppPreferences` through Koin instead of threading it through `NavGraph`.

## Compose structure

- Use `AppTopBar` for a static title and `CollapsingAppTopBar` for an entity-name detail title.
- Use `PullToRefreshBox` with `loadState.isRefreshingNow`; do not translate content with `distanceFraction`.
- Render initial loading, error, loaded, empty, and refresh states consistently with neighboring screens.
- Use `AppIcon(AppIcons.X)`, `MaterialTheme.shapes`, `AppElevation`, the stock typography ramp, and motion specs from `AppAnimations.kt`.
- Reuse shared components in `ui/common` before adding a local variant.
- Use `collectAsStateWithLifecycle` for lifecycle-bound state.

## Documentation and tests

- Update `dev/architecture.md` for new routes, ViewModels, packages, or dependency injection wiring.
- Update `dev/style.md` only when introducing or changing a UI convention.
- Update `dev/platform-parity.md` if either platform behaves differently.
- Add an `Unreleased` changelog entry because a new user-facing screen is visible behavior.
- Test extracted deterministic logic in `commonTest`; do not invent a screen test harness for a single change.

## Verify

```bash
./scripts/verify-change.sh
./gradlew :composeApp:compileKotlinIosSimulatorArm64
```
