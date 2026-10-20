---
name: fespalier-testing
description: "Testing an app built with fespalier — package:fespalier/testing.dart (pumpRouter and currentLocation), booting the generated router at any location, deep links, typed navigation, not-found views and unparsable segments, loading and error states, faking a backend with provider overrides, guards and sign-in (fakeAuth from fespalier_auth, since 0.9.0), flagged routes (FakeFlags from fespalier_flags, since 0.9.0), a restart over a disk cache (fakePrefsStore and memoryBox from fespalier_storage, since 0.9.0), reconnects and offline banners (FakeConnectivity from fespalier_connectivity, since 0.9.0), translated routes (fakeTranslations, FakeTranslations.strict, RecordingEditor from fespalier_tolgee, since 0.10.0), offline and queued writes (FakeCrateStackTransport, FakeRowServer, ManualSyncTicker, crateStackTestOverrides from fespalier_cratestack, since 0.10.0), the window size of an adaptive layout (fespalier_adaptive, since 0.9.0), Dio and package:http without a network (a fake HttpClientAdapter, a MockClient that races the abort trigger, retriers with zero delays; fespalier_dio, since 0.9.0), pure tests of locations, dataAt and match, a generated smoke test per route (fsp test, setup.dart, smokeTestRoute), accessibility guidelines in it (test: a11y, tap targets, labels, contrast, routeA11yGuidelines; since 0.16.0), Maestro on a device or the web (semantics_ids, fsp maestro), local telemetry dashboards (fsp telemetry, OpenObserve, Grafana), and the traps that hang or fail a test (pending timers, retries, stale app.g.dart). Load before writing or changing a widget test that touches the router, or when a routing test hangs, leaves a timer pending, or reports the wrong location."
---

# fespalier-testing

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

`package:fespalier/testing.dart` has `pumpRouter` and `currentLocation`, `motionOf` and `pumpTransition` (since 0.19.0), and, around them, `sendPlatformLink(tester, Uri)` (since 0.12.0: a warm platform link, as the engine sends it, pumped until idle; see the platform links section of the `fespalier-routing` skill), `RecordingTelemetry`, `TestRouteScope` (since 0.11.0, for an `observe.dart` hook that takes a `RouteScope`) and the `fsp test` pieces `smokeTestRoute` and `findRoutePage`. It is a **separate library**, so
`package:fespalier/fespalier.dart` never imports `flutter_test`; the package lists
`flutter_test` (an SDK package) as a dependency, which your app already has as a dev
dependency.

```dart
import 'package:fespalier/testing.dart';

testWidgets('shows a product', (tester) async {
  final container = await pumpRouter(
    tester,
    AppRoutes.router(initialLocation: '/products/2'),
    overrides: [apiProvider.overrideWithValue(FakeApi())],
  );
  expect(find.byType(ProductPage), findsOneWidget);
  expect(currentLocation(tester), '/products/2');

  // navigate with typed routes from any widget under the router
  ProductsRoute().go(tester.element(find.byType(ProductPage)));
  await tester.pumpAndSettle();
  expect(currentLocation(tester), '/products');
});
```

- **Signed-in routes (since 0.9.0).** With `package:fespalier_auth`, `overrides: fakeAuth(signedInAs: ...)`
  (from `package:fespalier_auth/testing.dart`) signs a test in, or out with no argument, on a
  `FakeAuthBackend` and a `MemoryTokenStore`: no `startup()`, no network, no timer. Call it **inside the test
  body**, where the fake clock starts; `tokenLifetime:` plus `tester.pump(const Duration(minutes: 6))` ages the
  session. See "Signed-in routes" in [`references/recipes.md`](references/recipes.md).
- **Flagged routes (since 0.9.0).** With `package:fespalier_flags`, `overrides: [flagSource.overrideWithValue(FakeFlags({'labs': true}))]`
  (from `package:fespalier_flags/testing.dart`) turns a flag on for a `pumpRouter` test; `flags.set('labs', false)` then
  `await tester.pump()` takes the app off the flagged route. `FakeFlags.strict` fails a test on a key typo. See
  `references/recipes.md` and [`fespalier-guards`](../fespalier-guards/SKILL.md) (its feature-flags page).
- **A cache on disk (since 0.9.0).** With `package:fespalier_storage`, `setUp(fakePrefsStore)` (from
  `package:fespalier_storage/testing.dart`) makes shared_preferences an in-memory store, two `PrefsDataStorage.open()`s in one
  test are a restart, and `memoryBox()` is a Hive box in memory. Without `fakePrefsStore()`, `open()` is `null` and nothing is
  saved. See `references/recipes.md` and [`fespalier-data`](../fespalier-data/SKILL.md) (its storage page).
- **Reconnects and offline banners (since 0.9.0).** With `package:fespalier_connectivity`, `connectivitySource.overrideWithValue(FakeConnectivity())`
  (from `package:fespalier_connectivity/testing.dart`) in `pumpRouter`'s overrides; `fake.offline()` then `fake.online()`
  is a reconnect. **A widget test that reaches the plugin fails** (`while activating platform stream on channel
dev.fluttercommunity.plus/connectivity_status`). See `references/recipes.md` and [`fespalier-data`](../fespalier-data/SKILL.md).
- **Translated routes (since 0.10.0).** With `package:fespalier_tolgee`, `overrides: fakeTranslations(bundled: {...}, remote:
FakeTranslations.strict())` (from `package:fespalier_tolgee/testing.dart`) **and `app: (router) => App(router: router)`**:
  `pumpRouter`'s default app has no `TranslationScope`, so `context.tr` throws there. `FakeTranslations.strict()` fails the
  test on a key nobody has; a fetch lands on the next `pump`. See
  [`fespalier-i18n`](../fespalier-i18n/SKILL.md) (its `testing.md` page).
- **Offline and queued writes (since 0.10.0).** With `package:fespalier_cratestack`,
  `crateStackTestOverrides(transport: FakeCrateStackTransport()..on('op', ...))` (from
  `package:fespalier_cratestack/testing.dart`): `transport.offline = true` queues an intent, then `drain()` sends it once;
  `loseAnswer('op')` replays under the same key without running twice; `ManualSyncTicker.tick()` is the app's tick and
  `FakeRowServer` is the row server. The fakes are all `Future.value`s: a pending timer is **your own ticker**. See
  [`fespalier-offline`](../fespalier-offline/SKILL.md) (its `testing.md` page).
- **DPoP proofs (since 0.9.0).** With `package:fespalier_sign_keypair`, `FakeDpopSigner` (from
  `package:fespalier_sign_keypair/testing.dart`) is a software key from a fixed scalar (the same on every run, no
  platform), and `verifyDpopProof` is what a fake server checks every proof with. See "DPoP proofs" in
  [`references/recipes.md`](references/recipes.md).
- **Window size (since 0.9.0).** With `package:fespalier_adaptive`, Flutter's default 800 x 600 test window is a
  **rail**; set `tester.view.physicalSize` (and `devicePixelRatio = 1`, and `addTearDown(tester.view.reset)`) for a
  bar (under 600) or a drawer (1200 and up). See "An adaptive layout" in
  [`references/recipes.md`](references/recipes.md).
- **HTTP without a network (since 0.9.0).** With `package:fespalier_dio` or `package:fespalier_http` (the `package:http`
  half, since 0.15.0; `FakeHttpClient` and `FakeHttpCredentials` are in `package:fespalier_http/testing.dart`), a fake `HttpClientAdapter` under Dio and a
  `MockClient` under `package:http` answer with no network. Dio's chain starts with `Timer.run`: use a plain `test()`,
  `pumpAndSettle()`, or `pump(Duration.zero)` (a bare `pump()` does not run it). A `MockClient` does not abort by itself:
  its handler races `abortTrigger`. Give the retriers zero delays, and count what the adapter saw: a write must be sent
  **once**. See [`references/http.md`](references/http.md).
- **Hooks and telemetry (since 0.8.1).** An `observe.dart` hook fires at the end of the first frame that
  shows a change, so `await tester.pump()` before asserting what it did; `RecordingTelemetry` is a
  `FespalierTelemetry` that keeps lines for a test (`FespalierTelemetry.install` in `setUp`, `install(null)`
  in `tearDown`). Both are in [`fespalier-observability`](../fespalier-observability/SKILL.md).
- **`pumpRouter(tester, router, {overrides, container, settle, retry, disposeRouter, app})`** wraps the router
  in a `ProviderScope` and Flutter's `MaterialApp.router`, pumps, and returns the
  `ProviderContainer` (for `container.read(...)`).
  - `settle` (default **on**) pumps until nothing is scheduled; turn it off to look at a
    loading view, then `pump` the time you want.
  - Pass your own `container` **instead of** `overrides` to share one with code outside the
    tree (it is yours to dispose); passing both is an assertion.
  - **`retry` defaults to no retries**: a failing `data.dart` shows `error.dart` at once and
    leaves no timer. Pass `ProviderContainer.defaultRetry` (or your function) to test the
    app's policy.
  - **It disposes the router when the test ends** (since 0.5.0; on 0.4.x and earlier
    `LeakTesting` reported the `GoRouterDelegate` as not disposed). A test that keeps its own
    `addTearDown(router.dispose)` before the call passes `disposeRouter: false` (since 0.6.0):
    those teardowns run after `pumpRouter`'s, and a second `dispose` throws.
    Build one router per test.
  - **`app:` (since 0.8.1)** is a `Widget Function(GoRouter router)` that builds what goes around the router
    in place of the plain `MaterialApp.router`. With the generated `main()`
    (the `fespalier` skill's `app-main` page) pass `app: AppMain.app`: a page is then tested in
    `lib/app/app.dart`'s theme, localizations and `builder:`. **`startup()` does not run** in `pumpRouter`:
    pass what it would override as `overrides`. To boot all of it, pump `AppMain.root()` yourself
    (`await tester.pumpWidget(AppMain.root(router: () => AppRoutes.router(initialLocation: '/x')))`, then
    `pumpAndSettle`; a `startup()` that awaits real I/O needs `tester.runAsync`). The router is disposed
    with the tree. **A `startup()` that throws is reported to `FlutterError.onError`, which fails the test
    until `tester.takeException()` takes it**; then the splash with `error` and `retry` is on screen.
    `AppMain.run()` can be awaited in a test to check a `zone()`; pump afterwards.
  - **Deferred routes (since 0.7.0).** A route with `const deferred = true;` has its `page.dart`
    imported `deferred as`, whose `loadLibrary()` completes only on the real event loop, which a
    widget test's `pump` never runs. `pumpRouter` therefore loads every deferred route's code first,
    in `runAsync`, and the page is in the first settled frame like an eager one's. **A test that
    pumps a router of its own** (`MaterialApp.router` in `pumpWidget`) must do it itself, before:
    `await tester.runAsync(AppRoutes.loadDeferred);`. Forget it, and a debug build throws a
    `FlutterError` that says so (`pitfalls.md`) instead of hanging. The loading view of a _real_
    deferred page can't be seen in a widget test: use
    `DeferredLibrary(() => completer.future, 'x/page.dart', loadsInFakeAsync: true)` in a
    `DeferredView`.
  - **Guards: return synchronously when you can.** Any `Future`, even `Future.value(...)`,
    costs a frame, so a cold deep link shows a blank first frame before the page.
- **`motionOf(tester, {of})` (since 0.19.0)** is the `PageMotion` (`fade`, `slide`, `none`, `material`, `cupertino`,
  `dialog`, `sheet`, `fullscreenDialog`, `custom`, `sharedAxis`, `fadeThrough`) the root navigator's top page was tagged with by `Transitions.*`,
  or null for a page of the app's own. `of:` is a finder for a widget on the page you mean (a page inside a tab).
- **`pumpTransition(tester, {at = 1, of})` (since 0.19.0)** runs the transition a navigation just started: one pump, then
  `at` times the route's duration (its reverse duration while popping, and a popping route is no longer the top, so pass
  `of:` for the leaving page). `at: 1` ends it (one millisecond past, where the controller says `completed`), `at: 0.5`
  leaves it animating for a mid-flight assertion. Call it right after `router.go(...)`, once per transition; no `pumpAndSettle`. A page inside a layout or a tab needs `of:` (the root navigator's top route is the layout's, already complete: a debug assertion says so); an `of:` that finds no widget, or several, is a `StateError`.
- **`currentLocation(tester)`** is where the router is, as a string
  (`/products/2?tab=info`). It follows `go`, `pop` and, since 0.4.0, **`push`** (the
  pushed location, the top of the stack). On 0.3.0 and earlier it did not follow a
  `push`: there, read `router.routerDelegate.currentConfiguration.last.matchedLocation`.
- **The DevTools hooks run in widget tests** (a test is a debug build; since 0.7.0): `AppRoutes.router()` attaches
  its router to the extension's support, which adds one listener and a short history, and the generated guards,
  `data.dart` providers and actions report to it (`traceGuard`, `traceData`, an action's `site`). They return
  what they are given, so a sync guard stays sync and a `Future` is the same `Future`; the only additions are an
  `onDispose` callback per provider build and a side `then` that records how a `Future` ended. It starts no
  timer, schedules no frame, reads no provider and listens to no stream, so it cannot leave a timer pending or
  change a `pumpAndSettle`; run the tests with `--dart-define=fespalier.devtools=false` to compile it out.
- **One router per test**: a router remembers where it went. Build it in the test
  (`AppRoutes.router(initialLocation: ...)`), not in a shared `final`.
- **Boot once per test** when fakes use `Future.delayed`: a second boot leaves the first
  tree's timers behind (`A Timer is still pending even after the widget tree was
disposed`). A `for` loop that declares one `testWidgets` per location is the easy way.
- Import files from `$` folders with the dollar escaped:
  `import 'package:my_app/app/products/\$id/page.dart';`.

## What to test, and how

| You want to check                                          | Do                                                                                                                                                                                            |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A URL opens its page                                       | `pumpRouter(..., AppRoutes.router(initialLocation: '/products/2'))`, `find.byType(ProductPage)`                                                                                               |
| Not found                                                  | `/nope` or an unparsable segment (`/products/abc`): the page is never built, guards that read segments are skipped                                                                            |
| Loading, then data                                         | `settle: false`, `await tester.pump()`, `find.byType(ProductLoading)`, then `pump(delay)`                                                                                                     |
| An error view                                              | a fake that throws: `error.dart` shows at once (no retries in `pumpRouter`)                                                                                                                   |
| A backend fake                                             | override the provider your `data()` reads: `overrides: [apiProvider.overrideWithValue(FakeApi())]`                                                                                            |
| Typed navigation                                           | `ProductRoute(id: 1).go(tester.element(find.byType(ProductsPage)))`, then `pumpAndSettle`                                                                                                     |
| A guard                                                    | `c.read(session.notifier).signIn()` through the returned container, then navigate (or `pumpAndSettle`: a `Ref` guard that watches moves by itself)                                            |
| A signed-in route (0.9.0, `fespalier_auth`)                | `overrides: fakeAuth(signedInAs: const AuthUser(id: 'ada'))`; signed out: `fakeAuth()`, and the route lands on `/sign-in?from=...`                                                            |
| HTTP or a retry (0.9.0, `fespalier_dio`, `fespalier_http`) | a fake `HttpClientAdapter` or `MockClient`, no network; count what it saw, zero delays for retriers (`references/http.md`)                                                                    |
| A flagged route (0.9.0, `fespalier_flags`)                 | `overrides: [flagSource.overrideWithValue(FakeFlags({'labs': true}))]`; `flags.set('labs', false)`, then `pump()`: the app leaves it                                                          |
| A restart over a disk cache (0.9.0)                        | `setUp(fakePrefsStore)`, then two `PrefsDataStorage.open()`s; the 2nd `pumpRouter(settle: false)` shows the saved value                                                                       |
| A reconnect or an offline banner (0.9.0)                   | `connectivitySource.overrideWithValue(FakeConnectivity())`; `fake.offline()` then `fake.online()`, then `pump()`                                                                              |
| A translated route (0.10.0, `fespalier_tolgee`)            | `overrides: fakeTranslations(bundled: ..., remote: FakeTranslations.strict())` and `app: (router) => App(router: router)`; see `fespalier-i18n`                                               |
| A queued write or a sync (0.10.0, `fespalier_cratestack`)  | `crateStackTestOverrides(transport: fake)`; `fake.offline = true`, then `drain()`; `ManualSyncTicker.tick()`; see `fespalier-offline`                                                         |
| A network image (0.9.0, `fespalier_image`)                 | `overrides: [imageCdnProvider.overrideWithValue(fakes.cdn(yourCdn))]` with `FakeImages(image: image)`; `fakes.requested` is every URL asked for; see `recipes.md`                             |
| Sentry events and breadcrumbs (0.9.0, `fespalier_sentry`)  | `RecordingSentry()` and `FespalierTelemetry.install(FespalierSentry(hub: sentry.hub))`; `await tester.pump()`, then `sentry.lines()`, `sentry.sent()`, `sentry.breadcrumbs`; see `recipes.md` |
| Locations, matches, data providers                         | plain `test()`: `.location`, `locationFor`, `AppRoutes.dataAt(uri)`, `AppRoutes.match(uri)`                                                                                                   |
| A `WidgetRef` (prefetch, refresh)                          | `tester.element(find.byType(SomeConsumerWidget)) as WidgetRef`                                                                                                                                |
| An action (a write, since 0.5.0)                           | `container.read(XRoute.action(1).notifier).call(input)`; see `fespalier-data`                                                                                                                 |
| Restoration                                                | your own app widget building the router in `State`, `restartAndRestore()`                                                                                                                     |
| Scroll restoration (0.8.1)                                 | play the browser with `pushRouteInformation` **and the state the app reported**; a location alone starts at the top (`pitfalls.md`)                                                           |
| A deferred route (0.7.0)                                   | `pumpRouter` loads it; with your own router, `await tester.runAsync(AppRoutes.loadDeferred)` before `pumpWidget` (`pitfalls.md`)                                                              |
| Aging data, a resume, a reconnect, a cache (0.8.1)         | `pump(Duration)` ages by the fake clock; `handleAppLifecycleStateChanged`; `reconnectSignal.notifier.fire()`; a shared `MemoryDataStorage` (`pitfalls.md`)                                    |
| A `RouteLink` hover (0.5.0)                                | a mouse `createGesture`, `moveTo`, `pump`; `container.exists(XRoute.data(...))` (`pitfalls.md`)                                                                                               |

Full compiled tests for all of these are in
[`references/recipes.md`](references/recipes.md); the traps, each of which cost a test
run while these skills were written, are in
[`references/pitfalls.md`](references/pitfalls.md).

**Widget tests for logic and states; Maestro for real devices, the web and journeys across
routes.** Maestro reads the accessibility tree and cannot see a `Key`, so (since 0.7.0)
`semantics_ids: true` gives every page a `Semantics(identifier: 'route:<pattern>')` that is in the
tree only when the route's own page is built, and `fsp maestro` writes a smoke flow per route that
waits for it. The identifier contract, the test that proves it
(`find.bySemanticsIdentifier`, with the handle disposed in the test body) and the traps (hash URLs,
`maestro test .maestro` skipping `routes/`, the web reload under a guard flow, the semantics tree
staying on in a web build) are in [`references/maestro.md`](references/maestro.md).

**A smoke test per route, for free (since 0.8.1).** `fsp test` writes
`test/routes/routes_test.dart`: one `testWidgets` per route that opens it at a sample URL with
`pumpRouter` and waits, on the **fake** clock, until its page is on screen. Provider overrides and the app
around the router come from a `setup.dart` you own. `package:fespalier/testing.dart` has the pieces:
`smokeTestRoute`, `findRoutePage(pattern)`, `pumpRouter(app:)` and an `Override` export. The setup file, the
skips, the failure message and the traps are in
[`references/route-smoke-tests.md`](references/route-smoke-tests.md).
**`test: a11y: true`** (since 0.16.0) also has each of those tests check Flutter's accessibility guidelines (tap
targets, semantic labels, text contrast) once the page is on screen: `smokeTestRoute(guidelines:
routeA11yGuidelines)`. It checks the whole screen, so an unlabeled `IconButton` in the shared app bar fails every
route; the same page has the list form and the failures.

**To watch a running app rather than assert on it** (since 0.8.1), `fsp telemetry` starts OpenObserve (and
Grafana with `--grafana`) in Docker with four dashboards over fespalier's spans, written as questions (App
health, Screens, Actions, Errors; green, amber or red), and `fsp telemetry --report` prints the same answers in
the terminal. The command, the
endpoint an app on an emulator, a simulator, a phone or the web uses, which dashboard answers which
question, and the traps (empty dashboards, `otel_zone`'s `runGuarded` blanking a web app before v0.8.1) are in
[`references/observability.md`](references/observability.md).

## Examples

`examples/minimal`, `examples/shop`, `examples/features`, `examples/auth`, `examples/telemetry`, `examples/adopt`, `examples/cose`, `examples/i18n`,
`examples/maps` and `examples/offline` test their routes with `pumpRouter` from `package:fespalier/testing.dart`; `examples/plugins` pumps
`AppMain.root()` (and uses `pumpRouter` in its push test), and `examples/tabs` builds its own `MaterialApp.router`. `examples/shop` also carries what `fsp test` and
`fsp maestro` write (`test/routes/`, `.maestro/routes/`);
the `fespalier` skill lists every example.

## Three facts to keep in mind

1. go_router **builds the whole matched stack**: a deep link to `/products/2` also runs
   `/products`' `data.dart` underneath; pump long enough for both or `pumpAndSettle`.
2. **`fsp check` does not catch a stale `lib/app.g.dart`**: it writes and compares
   nothing. Regenerate and diff in CI (`dart run fespalier gen`, then
   `git diff --exit-code lib/app.g.dart`).
3. `await ProductRoute.read(ref, id: 1)` under a fake clock **hangs** until you `pump`
   the delay: start it, pump, then await.

Other skills: [`fespalier-data`](../fespalier-data/) for what the data providers do,
[`fespalier-guards`](../fespalier-guards/) for the guard behaviours you will be testing.
