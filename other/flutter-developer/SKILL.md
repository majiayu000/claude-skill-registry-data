---
name: flutter-developer
always: true
description: Master Flutter Engineer — Dart 3.13, architecture (clean/feature-first), state (Riverpod/BLoC), networking, persistence, testing, CI/CD, performance, security, offline sync, platform channels.
triggers:
  - flutter developer
  - flutter

---
[SKILL] flutter-developer
[OBJ] Engineer the non-visual layer of production Flutter apps — architecture, state management, networking, persistence, testing, CI/CD, performance profiling, security, and native platform integration.
[PERSONA] MOBILE (primary), DEV (secondary), ARCH (secondary), QA (secondary).
[PARENT] `flutter-architect` (visual layer -> `flutter-design`).

[RULES]
1. [CMD] Context7 IDs: Dart `/dart-lang/site-www`; Riverpod `/riverpod/riverpod`; BLoC `/felangel/bloc`; Freezed `/rrousselGit/freezed`; Drift `/simolus3/drift`; Dio `/cfug/dio`; go_router `/flutter/packages`; `flutter_dotenv` `/jonataslaw/dotenv`; `flutter_secure_storage` `/mogol/flutter_secure_storage`; `mocktail` `/mocktail/mocktail`; Fastlane `/fastlane/docs`.
2. [REQ] `[VER-01]` Pin to `pubspec.lock` exact versions. Reference baseline: Flutter 3.47 / Dart 3.13 (Aug 2026). Use Dart 3 features: records, patterns, sealed classes, exhaustive switch; Dart 3.13 primary constructors (lang version >= 3.1) for concise data classes. Enable `language: 3.13` in `pubspec.yaml` `environment: sdk:`.
3. [REQ] Architecture (feature-first + clean layers):
   - `lib/features/<feature>/{data,domain,presentation}/` + `lib/core/` (shared: error, network, theme, constants, utils) + `lib/config/` (env, router, di) + `lib/main.dart` (< 30 lines, entry only).
   - **Domain:** entities (freezed), repository interfaces (abstract), usecases (callable classes). No Flutter imports. No `BuildContext`.
   - **Data:** models (freezed + json_serializable), datasources (remote dio / local drift), repository impls. Maps DTO <-> entity.
   - **Presentation:** widgets/pages (dumb) + controllers/notifiers (smart, Riverpod `Notifier`/`AsyncNotifier` or BLoC). Controllers hold state + call usecases; widgets `ref.watch`/`BlocBuilder`.
   - Dependency rule: presentation -> domain <- data. Domain depends on nothing app-internal.
4. [REQ] Dependency injection: Riverpod providers (`@riverpod` code-gen via `riverpod_generator` preferred) OR `get_it` + `injectable` for non-Riverpod. Never `Provider.of` deep chains; never service-locator in widgets (inject via constructor / `ref`).
5. [REQ] State management (decision tree):
   - Widget-local ephemeral -> `setState` / `ValueNotifier`.
   - Scoped shared, reactive -> Riverpod: `Notifier`/`AsyncNotifier` + `ref.watch` (rebuild) / `ref.read` (one-shot) / `ref.listen` (side-effects). Use `AsyncValue` for async state (loading/data/error). Prefer code-gen `@riverpod` for type-safety + auto-dispose. Avoid `StateProvider`/`ChangeNotifierProvider` for complex state.
   - Event-driven, strict separation, large teams -> BLoC: `Bloc`/`Cubit` + events/states (freezed). Cubit for simple, Bloc for complex event-driven.
   - NEVER `setState` for app-wide state. NEVER InheritedWidget manual. NEVER mix stores. Keep state close to where it's used; hoist only when shared.
6. [REQ] Immutability & models: `freezed` for all domain/data models + union/sealed states; `@freezed` + `@JsonSerializable` + `fromJson`; `copyWith` for updates; `const` constructors; `@immutable`. Use Dart 3 `sealed` + pattern matching for exhaustive state handling (`switch (state) { case Loading(): ... case Data(:final data): ... }`).
7. [REQ] Networking:
   - `dio` for non-trivial (interceptors: auth-token attach, logging, retry, error-mapping); `http` for trivial only.
   - Deserialize via `freezed` + `json_serializable`; never hand-parse `Map<String,dynamic>` in widgets.
   - Repository pattern: `abstract class XRepo` (domain) + `XRepoImpl` (data) wrapping `XRemoteDatasource` + `XLocalDatasource`.
   - Error handling: typed `Result<T>` / `Either<Failure, T>` (fpdart or custom sealed) OR Riverpod `AsyncValue.guard`; never swallow exceptions; map HTTP errors to domain `Failure` enum/sealed.
   - Cancel in-flight on dispose (`CancelToken`); debounce search.
8. [REQ] Persistence:
   - Relational -> `drift` (typed SQLite, migrations, streaming queries via `Stream<List<T>>`).
   - KV / object -> `hive` (binary) or `isar` (query-able, fast).
   - Primitives -> `shared_preferences` ONLY.
   - Sensitive -> `flutter_secure_storage` (Keychain/Keystore).
   - Offline-first: local DB as source of truth; sync queue + conflict resolution (last-write-wins / server-wins / CRDT) on reconnect; `connectivity_plus` for network events; `workmanager` for background sync.
9. [REQ] Routing: `go_router` (declarative). `GoRoute` + `ShellRoute` (nested nav bars); typed `extra` args (define arg classes); `redirect` for auth/feature-flags; `StatefulShellRoute.indexedStack` for bottom-nav with state preservation; `PopScope` for predictive back (Android 14+). Never `Navigator.push` for complex apps; never raw `Map` route args.
10. [REQ] Error handling architecture: global `runZonedGuarded` + `FlutterError.onError` -> report to Sentry/Crashlytics; per-feature `Failure` sealed types; presentation maps `Failure` -> user message + retry CTA. Never expose stack traces / internal codes to users `[SEC-04]`.
11. [REQ] Testing two-tier `[TEST-07]`:
   - FAST: `flutter test test/path/touched_test.dart` (~5s). Mark slow (integration, golden, platform-channel) with `@Tags(['slow'])` + `--exclude-tags=slow`.
   - FULL (before done): `flutter test --coverage` (>= 80% logic, >= 70% total) + `flutter test integration_test/` on device/emulator.
   - Unit: `test()` for usecases/repos/services; mock deps with `mocktail` (no annotation boilerplate, Dart-friendly) — `when(() => mock.x()).thenReturn(...)`; `registerFallbackValue` for non-nullable args.
   - Widget: `testWidgets()` + `WidgetTester`; `pumpWidget` + `pump` + `pumpAndSettle`; assert with `find.byType`/`find.text`/`find.byKey`; wrap in `MaterialApp` + `ProviderScope`/`BlocProvider`. Test behavior, not implementation.
   - Integration: `integration_test/` package on real device/emulator; `IntegrationTestWidgetsFlutterBinding`.
   - Golden tests: `matchesGoldenFile` for pixel-regression (regenerate with `--update-goldens`).
   - AAA pattern; one behavior per test; factories not hardcoded IDs/dates `[TEST-03]`.
12. [REQ] CI/CD:
   - GitHub Actions / Codemagic / Fastlane. Pin action SHAs `[GIT-05]`.
   - Pipeline: `dart format --set-exit-if-changed lib/ test/` -> `flutter analyze --fatal-infos` -> `flutter test` -> `flutter build` (per platform) -> sign -> deploy.
   - Android: AAB (`flutter build appbundle`), Play App Signing, `fastlane supply` for upload; target latest Play API level.
   - iOS: `flutter build ipa` / `xcarchive`, App Store Connect API key, `fastlane pilot` for TestFlight, `deliver` for App Store.
   - Obfuscate release: `flutter build appbundle --obfuscate --split-debug-info=build/symbols` (keep symbols for symbolication; upload to Sentry/Crashlytics).
   - OIDC keyless auth where supported; SBOM + Cosign `[GIT-05]`.
13. [REQ] Performance engineering:
   - Budget: 60 FPS / 16.6 ms frame. Profile with Flutter DevTools (Performance tab: timeline, jank, shader compile jank; CPU profiler; Memory tab).
   - Reduce rebuilds: `const` widgets; scope `Consumer`/`BlocBuilder` to smallest subtree; `Selector`/`ref.watch` of granular providers; `ProviderScope`/`BlocSelector`.
   - Lists: `ListView.builder`/`SliverList.builder` + `itemExtent`/`prototypeItem`; `AutomaticKeepAliveClientMixin` only when needed.
   - Repaint: `RepaintBoundary` around animations / heavy static subtrees.
   - Shaders: pre-warm shader compile jank with `SkSL warmup` (legacy) or rely on Impeller (default on iOS since 3.10, Android since 3.16 — verify in `pubspec`/platform).
   - Images: `cached_network_image` + `cacheWidth`/`cacheHeight` to downscale decode; `precacheImage` for critical.
   - Avoid `Opacity` widget (use `FadeTransition`/`AnimatedOpacity`); avoid heavy work in `build()`.
14. [REQ] Platform channels & native:
   - Method channels for sync native calls; Event channels for streams; FFI (`dart:ffi`) for perf-critical; Pigeon for type-safe channel codegen (preferred over hand-written).
   - Plugins: prefer first-party (`flutter/packages`) + federated platform implementations; check pub points >= 80 + popularity + last-updated before adding `[VER-01]`.
   - Permissions: `permission_handler` + declare in `Info.plist` / `AndroidManifest.xml` with usage strings (App Store / Play review requirements).
15. [REQ] Security `[SEC-01..10]`:
   - Input validation: `Form` + validators; DTOs for API payloads; never trust client.
   - Secrets: `.env` + `flutter_dotenv` / `--dart-define-from-file`; NEVER commit secrets `[SEC-04]`.
   - Transport: HTTPS only; certificate pinning (`dio_certificate_pinning`) for sensitive.
   - Storage: `flutter_secure_storage` for tokens; encrypt local DB (`drift` with SQLCipher / `isar` encryption).
   - Release: `--obfuscate --split-debug-info`; root/jailbreak detection (`flutter_jailbreak_detection`); Play Integrity (Android) / DeviceCheck (iOS) for anti-tamper.
   - No PII in logs/analytics `[SEC-04]`.
16. [REQ] Observability: `package:sentry_flutter` or `firebase_crashlytics` for crashes; `package:analytics` / Firebase Analytics for product events; OpenTelemetry (`opentelemetry` pub) for distributed tracing; structured logs (never `print()` in release — use `logging` package with levels).
17. [REQ] Background work: `workmanager` (Android WorkManager / iOS BGTaskScheduler) for periodic sync; `flutter_background_service` for long-running; declare background modes in manifests; request battery-optimization exemptions only when justified.
18. [REQ] Code quality `[CODE-01..05]`: files < 300 lines, methods < 30; strict typing (no `dynamic` in public APIs — use `Object?` + pattern match or sealed); enums/constants over magic strings; SOLID + DRY; no inline `await import()` (not applicable in Dart but no dynamic imports); no `TODO`/`FIXME` without ticket tag.
19. [REQ] Concurrency: `Future`/`async`-`await` for IO; `Isolate.run` / `compute()` for CPU-heavy (parse, crypto, image) to avoid jank; `Stream` for reactive sequences; never block the UI isolate with heavy sync work.
20. [REQ] Query Context7 for ANY Dart/Flutter/package API before implementation. Run `flutter analyze` + `dart format` + targeted tests during iteration; FULL suite + coverage before done. Test on physical devices (iOS + Android) before release.

[PROHIBIT]
- `setState` for app-wide/shared state.
- `InheritedWidget` manual for app state.
- `dynamic` in public APIs.
- Business logic / HTTP / DB calls inside `build()`.
- Hand-written platform channels when Pigeon is viable.
- `print()` in release code.
- Secrets in code / committed.
- Swallowing exceptions silently.
- `Navigator.push` for complex apps (use `go_router`).
- Raw `Map` route args (use typed classes).
- `git add .` / `git add -A` `[GIT-06]`.
- Skipping FULL test suite + coverage before done `[TEST-07]`.
