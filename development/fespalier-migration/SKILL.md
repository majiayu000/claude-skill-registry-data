---
name: fespalier-migration
description: "Moving to fespalier and between its versions — upgrading an app from 0.19 to 0.20 (nothing breaks: an app with a data.dart, an action.dart or a deferred page regenerates app.g.dart, whose private names and DevTools sites now follow the folders, so a hot reload swaps in a route inserted anywhere, and a deferred route added or removed beside another, its page imported under a prefix named after its folder), 0.18 to 0.19 (nothing breaks for an app whose telemetry sinks extend FespalierTelemetry; native crash records can name their screen with otel_zone v0.7.0 and onScreen, optional; FespalierTelemetry gains commit, told before the new page is built, so a sink that implements it instead of extending adds the method; fespalier_sentry names its scope at the commit, not after the page's first frame, which changes the names on a few events from that frame; `otel: true` writes the OpenTelemetry wiring into the generated main() instead of your startup.dart, optional; every app regenerates app.g.dart, and a hot reload swaps in a regenerated route table), 0.17 to 0.18 (nothing breaks; four new telemetry attributes need one restart of the local telemetry stack for their tiles, fespalier_launch is new and opt-in: nothing changes for an app that does not list it, and so is fespalier_frb's ChangeCodec), 0.16 to 0.17 (a freezed extra needs ExtraCodec.of, and fsp warns when build_runner would delete lib/app.g.dart: output: lib/routes.g.dart is the way out), 0.15 to 0.16 (Flutter 3.35 and Dart 3.9 are the floor: upgrade Flutter, go_router's lower bound is 17.2.3; FespalierAdapter.onEnter is a getter, FespalierEnter? get onEnter, so an adapter with an onEnter method no longer compiles and changes it to the getter; AppRoutes.router passes go_router an onEnter only when an adapter has one, so go() then push() keeps both for every other app; an app with a router of its own passes onEnter: AppAdapters.handlesEnter ? AppRoutes.onEnter : null; an upload ends Failed(other), an unknown outcome, after a 5xx, 408 or 499 and Failed(storage) when its registry entry cannot be saved; a CrateStack 5xx without an envelope keeps the intent's key and reads as offline; a request with a body is sent again after a 401 through DioHttpClient; a download that cannot reach its credentials offline is Failed(network), not Failed(unauthorized); a paused download resumes from the freshly granted URL and gets one renewal per resume; an app with a links: section regenerates app.g.dart with AppRoutes.urlOf; test: a11y and the DevTools Adapters tab are opt-in and add nothing to an app that ignores them, a plugin that throws is an AsyncError that nothing retries, a notification tap while the app starts is opened once instead of lost, and fsp check refuses a step folder that is no Dart enum constant), 0.14 to 0.15 (fespalier_dio/http.dart and problem.dart are removed: import package:fespalier_http and add it at the same url and ref), 0.13 to 0.14 (fespalier_push tokens are PushToken, a revocation its own event), 0.12 to 0.13 (nothing to change: app.g.dart is unchanged, and the new packages are opt-in), 0.11 to 0.12 (opt-in ready(container) and attach(router, container) in startup.dart: the gate makes the app's ProviderContainer, runs ready before the router and attach after the adapters'; no change for an app that exports neither), 0.10 to 0.11 (an app with an observe.dart regenerates: RouteHooks.onEnter takes a RouteScope, the generated main passes the container to AppRoutes.attach, and a replace of a tree page keeps its page instance; a third-party telemetry sink with an exhaustive switch on TelemetryOp needs a TelemetryOp.custom case; AppAdapters, main: manual with adapters, FespalierAdapter.attach, extends not implements; forms moved out of fespalier into the fespalier_forms package: an app with a form() adds the dependency at the same url and ref and regenerates, fsp errors until then, and code that names ActionForm, FieldCodec, ActionFormMessages and the rest imports package:fespalier_forms; FieldErrors, validate() and optimistic() stay; form drafts, opt-in, regenerate every app with a form and reserve the key name draft; multi-page forms, opt-in: a const steps map in a section's action.dart, and only a map literal called steps beside a form() is read as one), 0.9 to 0.10 (no generator or runtime change: app.g.dart is unchanged; the docs moved from the README to docs/ pages and some fsp messages now cite them; the opt-in fespalier_tolgee and fespalier_cratestack packages), 0.8 to 0.9 (a third-party telemetry sink needs a TelemetryOp.auth case; every app regenerates app.g.dart with page names, each pageBuilder wrapped in namedPage so a NavigatorObserver sees the route pattern; an app with telemetry: true also has data providers that call data() through traceDataCall, and the data span starts first and is current; the opt-in fespalier_auth and fespalier_dio packages and fespalier: adapters:), 0.7 to 0.8 (the generated main(): app.dart, startup.dart and splash.dart at the app root, main: manual; hooks_riverpod ^3.2.1, the reserved freshness and dataCache names), 0.6 to 0.7 (the unknown_path warnings), 0.5 to 0.6 (remount, replace in the address bar), 0.4 to 0.5 (pumpRouter disposes the router, new reserved names), 0.3 to 0.4 (publish_to none, currentLocation follows push) or 0.2 to 0.3 (regenerate app.g.dart with the matching fsp, PrefetchHandle replacing the timed prefetch, shell transitions, Riverpod retry now inherited, NotFoundScope, the hidden RouteMatch) and adopting fespalier in an existing go_router app by mounting its tree inside your GoRouter with AppRoutes.mount(at:), one folder at a time, siblings with a compound path (nest = false) included. Load before bumping the fespalier package or fsp, when an upgrade changes behaviour or fails to compile, or when planning a go_router-to-fespalier migration."
---

# fespalier-migration

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

## The one rule of upgrading

**The package and `fsp` move together, and `lib/app.g.dart` is regenerated every time.**
The generated code relies on runtime additions of its own release; the upgrade notes of
0.1.1, 0.2 and 0.3 each say "regenerate", and the rule stays even for a release that leaves the file unchanged
(0.10 and 0.13): regenerate and read the diff of `lib/app.g.dart`.

```sh
# 1. pubspec.yaml: bump `ref:` on the git dependency to the release tag, then
flutter pub get
# 2. regenerate with the fsp that matches the package your pubspec.lock resolved
dart run fespalier gen          # or: FSP_VERSION=<the same tag> install.sh, then `fsp gen`
# 3. commit lib/app.g.dart, then
flutter analyze && flutter test
```

`fsp --version` must print the package's version (`ref: vX.Y.Z` needs `fsp X.Y.Z`); an `fsp` of another
version on `PATH` is the usual source of an `app.g.dart` that does not compile.
`dart run fespalier` uses an `fsp` on `PATH` only when its version matches.

## 0.19 to 0.20: what to check

0.20.0 breaks nothing: an app with a `data.dart`, an `action.dart`, a deferred page or a type written with an import prefix in a route file regenerates `app.g.dart` (items 1 and 2), with no code change; any other app's is unchanged. Bump the `ref:` of `fespalier` and every companion to the 0.20.0 tag, regenerate, read the diff, then:

1. **The generated names follow the folders.** The providers, the deferred libraries, the optimistic layers and the actions are named after their folder, not after where the route sorts: `_dataProductsId`, `_libCheckout`, `_optimisticTeamsTeamId`, `_actionNotesId_edit`. So are the DevTools sites, `dProductsId` and `aNotesId_edit`; the guard and `redirect.dart` sites (`g5@6`, `r32`) do not change, and neither does a route's class. A prefixed type's import alias (`_e…_m`) is made from the library the prefix imports, not from the file that spells the type. The names are private and the DevTools extension reads any site, so no code changes; run `fsp gen` and commit the result. A hot reload now swaps a route added or removed anywhere, so `fsp dev` reloads it instead of restarting. Still refused: a changed `data()` or action, a moved folder that has one (and the second of two folders whose names share a stem, added or removed, when one has a `data.dart` or an `action.dart`; two deferred pages alone swap), an import prefix pointed at another library (it was accepted before 0.20.0), and a router setting. See [`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its dev diagnostics).
2. **A deferred route added or removed hot reloads too.** `AppRoutes.deferred` is a getter now, where it was a `static final` list, and a deferred page's import is named after its folder (`deferred as _pageCheckout`, where it was `_i7`). So an app with a deferred route regenerates `app.g.dart`, with no code change: code that reads `AppRoutes.deferred` or calls `loadDeferred()` works as before. Now a swap: a deferred route added, removed or moved beside another; a page added with `deferred: true`; `deferred` turned on or off. `fsp size` reads the new names, so run `flutter build web` again first; an older build is reported as built from another `lib/app.g.dart`. Before 0.20.0, adding a route before a deferred one was refused (it changed `AppRoutes.deferred`), but a file that is not a route (a `loading.dart`, an `error.dart` or a `guard.dart` in the root, or in a folder that sorts before a deferred route) renumbered the position-based import (`_i2` became `_i3`) while every hash the reload compares stayed the same. That swap went through, and the deferred page then threw "Deferred library ... was not loaded" until a restart: a bug of 0.19.0 that 0.20.0 fixes, since the import keeps its folder's name. See [`fespalier-routing`](../fespalier-routing/SKILL.md) (its route.dart reference, deferred routes).

Details: `docs/migration.md`, "0.20.0".

## 0.18 to 0.19: what to check

0.19.0 breaks nothing for an app whose telemetry sinks extend `FespalierTelemetry` (every sink fespalier ships does): every app regenerates `app.g.dart` (item 5), and an app that does not name its screen or set `otel: true` changes nothing else. A telemetry sink that implements `FespalierTelemetry` instead of extending it adds one method (below). With `fespalier_sentry`, the scope is named at the commit, which changes a few events from a page's first frame (below).
Native crash records can name their screen, which takes otel_zone v0.7.0 and one call (item 1). Bump the `ref:` of
`fespalier` and every companion to the 0.19.0 tag, regenerate, read the diff, then:

1. **Optional: native crash records can name the screen.** Bump `otel_zone` to v0.8.1 (the pin is the commit
   `64c4661ac6cd09718141864d528892916677cc38`; v0.7.0 was the first with `onScreen`, and `fespalier_otel` needs the rc.4 line
   from 0.19.0 anyway, which is `otel_zone` v0.8.0 or later), pass `onScreen: observability.setCrashScreen` to `FespalierOtel`, and
   run `fsp telemetry --stop`, then `fsp telemetry`, so the collector reads the attribute and the Errors table has its panel. `app.g.dart`
   is not changed by this item (item 5 regenerates it for every app), and an app that does none of this keeps its crash records as they are. See
   [`fespalier-observability`](../fespalier-observability/SKILL.md) (its telemetry section).
2. **A telemetry sink of your own.** `FespalierTelemetry` has a new member, `commit(navigation, commit)`, with an empty
   default: the router tells it what each navigation commits, before the page is built. A sink that extends
   `FespalierTelemetry` changes nothing; one that implements it stops compiling until it adds the method (or extends
   instead), and one with a member already named `commit` of another signature renames it. `RecordingTelemetry` writes
   commit lines only with `recordCommits: true`. See [`fespalier-observability`](../fespalier-observability/SKILL.md)
   (its telemetry reference, "Several sinks").
3. **Optional: OpenTelemetry without wiring.** Add `otel: true` under `fespalier:`, next to `telemetry: true`, and delete
   the hand wiring: in `lib/main.dart`, `Future<void> main() => AppMain.run();` (a root file makes `fsp` write the generated
   `main()`), and in `lib/app/startup.dart` the `OtelZone`, its `start()`, the `FespalierOtel` sink, the two observers and
   a `zone()` that runs `runGuarded`. `fsp gen` warns about the `OtelZone` and the `FespalierTelemetry.install` that are
   still there. A sink that `startup()` installs with `FespalierTelemetry.install` must use `FespalierTelemetry.add`, once
   (guarded by `FespalierTelemetry.contains`, because Retry runs `startup()` again), or it replaces the OpenTelemetry sink. `otel: true` needs `telemetry: true`, `fespalier_otel` and `otel_zone` (item 1's
   pin) under `dependencies:`, and not `main: manual`; `fsp` says which one is missing. `fespalier_otel` resolves with `otel_zone`
   v0.8.0 or later, but only v0.8.1 runs the generated zone on the web: on v0.8.0 the app works on mobile and its web build is blank,
   so use the pin. Only `lib/app.main.g.dart`
   changes for this item (`app.g.dart` changes for item 5). See [`fespalier-observability`](../fespalier-observability/SKILL.md) (its telemetry section).
4. **Sentry names a page at its commit.** The scope's transaction name, `fespalier.route` and, next to `fespalier_otel`, `otel.trace_id` and `otel.span_id` are set when a navigation commits, before the new page's `initState` and first `build`. Most events read the same: Sentry's own capture of an exception reads the scope after the frame, and a guard, `data()` or action error takes its `fespalier.route` from its call site. What changes is what reads the scope during that frame: an event captured on a copy of it (`captureException(..., withScope: ...)` in your code, and fespalier's own events, whose transaction name now is the page being opened), and code that reads `scope.transaction` or the tags, such as a page's `initState`. From the commit until the first frame, an event from the page being left names the destination too (`captureException` right after `router.go(...)` in the same handler). A search on the transaction name finds these events under the page being opened. Nothing to change in code; a test that read `sentry.tags` or `transactionName` before a pump now sees the new page. See [`fespalier-observability`](../fespalier-observability/SKILL.md) (its Sentry reference).

5. **Every app regenerates `lib/app.g.dart`.** Run `fsp gen` and commit the result (a committed file that is not regenerated is stale: the CI recipe in `docs/getting-started.md`, "Failing CI on a stale file", catches it). There is no code change. `AppRoutes.router()` builds a `GoRouter.routingConfig` over a routing config, the same router in release. The layouts' navigators and shells take their keys from `AppRoutes`, so a hot reload keeps the pages in them, and `AppManifest.byType` and `AppManifest.byPath` are getters over the same maps. A hot reload in a debug build now swaps in the regenerated route table, with limits: a route added, removed or moved swaps when no route after it in the order of `fsp routes` has a `data()` function, an action or a deferred page (the generated names of those are numbered by position, and a changed name is refused), and a provider, a deferred library or a router setting that changed is refused too. A refused swap prints one message and keeps the old routes until a hot restart; stable names made from the folders will lift the limit on position in a later release. `fsp dev` now hot reloads after a regeneration that swaps, and hot restarts after one that does not. See [`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its dev diagnostics).

Details: `docs/migration.md`, "0.19.0".

## 0.17 to 0.18: what to check

0.18.0 breaks nothing: the generated `app.g.dart` is unchanged unless an app lists the new `fespalier_launch` adapter.
It adds four attributes to the spans of a data load and an action (item 1), the telemetry stack needs one restart to
show them (item 2), `fespalier_launch` is new and opt-in (item 3), and so is `fespalier_frb`'s `ChangeCodec`
(item 4). Bump the `ref:` of `fespalier` and every companion to the 0.18.0 tag, regenerate, read the diff, then:

1. **Four attributes are new on the data and action spans**: `fespalier.data.attempt`, `fespalier.data.source`,
   `fespalier.action.rolled_back` and `fespalier.action.invalid`. They come with `telemetry: true`, like the others.
   A test that compares `RecordingTelemetry` lines whole gains the `attempt=`, `source=`, `rolled_back=` and
   `invalid` tokens. See [`fespalier-observability`](../fespalier-observability/SKILL.md) (its `conventions.md`).
2. **Restart the telemetry stack once for the new tiles.** Run `fsp telemetry --stop`, then `fsp telemetry`, which
   rewrites the files and updates the dashboards, so the collector reads its four new dimensions. An app before
   0.18.0 sends none of them, so those tiles read 0.
3. **`fespalier_launch` is new and opt-in: nothing changes for an app that does not list it.** It opens a typed route from a
   home-screen shortcut or a widget tap, cold or while the app runs (since 0.18.0). An app that lists it under
   `fespalier: adapters:` gets one more adapter in `AppAdapters`, calls `FespalierLaunch.configure(sources:, route:)` in
   `main()` before `AppMain.run()`, and configures it in every widget test that boots `AppMain.root()`
   (`FespalierLaunch.debugReset()` in `setUp` and `tearDown`, as for fespalier_push). The plugins (quick_actions and
   home_widget) stay the app's: their recipes are in [`fespalier-routing`](../fespalier-routing/SKILL.md) (its `launch-sources.md`).
4. **Optional (`fespalier_frb`): decode raw core messages with `ChangeCodec`.** Nothing changes for a feed over typed events.
   An `open` that decodes raw messages itself (`.map(decode)`) turns one bad message into an `AsyncError` in `latest`;
   `.transform(ChangeCodec(decode))` skips and counts it instead and keeps the feed going. Throw `UnknownChange` from the
   decoder for a variant a newer core added. See [`fespalier-data`](../fespalier-data/SKILL.md) (its `change-feeds.md`).

Details: `docs/migration.md`, "0.18.0".

## 0.16 to 0.17: what to check

0.17.0 breaks nothing, and changes nothing for an app that uses neither freezed nor `build_runner`: the generated
`app.g.dart` is unchanged. It handles two places where fespalier and a code generator trip over each other (items 1 and 2)
and drops a flag from the examples (item 3). Bump the `ref:` of `fespalier` and every companion to the 0.17.0 tag,
regenerate, read the diff, then:

1. **A freezed `extra` restores as `null` on a reload, though `extra_codec.dart` lists it.** freezed's
   `const factory Note(...) = _Note;` makes a private `_Note`, which `ExtraCodec({Note: ...})` (an exact runtime-type
   lookup) never matches. Replace the entry with `ExtraCodec.of([ExtraType<Note>(toJson: ..., fromJson: ...)])`, which
   matches with `is`; put the most specific type first. A debug build now prints one line, once per type, for an `extra` no
   entry takes. See [`fespalier-routing`](../fespalier-routing/SKILL.md) (its `typed-routes-and-extra.md`).
2. **`fsp gen`, `check`, `watch` and `dev` warn that `build_runner` can delete `lib/app.g.dart`** when the app lists
   `build_runner` and has a `lib/app.dart`: the builders that write `.g.dart` files claim `lib/app.g.dart` and delete it,
   with nothing logged. It is a warning (exit codes are unchanged). Set `output: lib/routes.g.dart` (and change the
   `app.g.dart` imports), rename `lib/app.dart`, or exclude `lib/app.dart` from `source_gen:combining_builder` in
   `build.yaml`. See [`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its `flutter-pitfalls.md`).
3. **Optional: drop `-d` from your `build_runner` commands in `tasks:`.** build_runner has ignored it since 2.7.0; the
   commented examples `fsp init` and `fsp create` write no longer have it.

Details: `docs/migration.md`, "0.17.0".

## 0.15 to 0.16: what to check

0.16.0 is a **breaking** release for an app on Flutter 3.32 to 3.34: the floor is now Flutter 3.35 and Dart 3.9. It
also changes one member of `FespalierAdapter`, fixes the places where a write could be sent twice, a provider started a
hidden timer, a notification tap was lost and a step name did not compile, and three outcomes of the network packages (one
port, `DownloadBackend.resume`, gains a named parameter: item 20), so some outcomes an app sees are different, and adds
opt-in tooling. The generated `app.g.dart` changes for an app with `adapters:` (an `AppAdapters.handlesEnter` getter, and
`onEnter: AppAdapters.handlesEnter ? onEnter : null` where it was `onEnter: onEnter`) and for an app with a `links:`
section (item 12); no file kind, key or command changed. Bump the `ref:` of `fespalier` and every companion to the 0.16.0
tag, regenerate, read the diff, then:

1. **Flutter 3.35 or newer (Dart 3.9 or newer) is needed** (since 0.16.0). `fespalier` and every companion that was in the
   3.32 floor job now say `sdk: ^3.9.0` and `flutter: ">=3.35.0"`; `fespalier_sign_keypair` (Flutter 3.44) and
   `fespalier_download_background` (Flutter 3.47) keep their own, higher ones. On an older Flutter `flutter pub get` fails
   with a version solving message that names the SDK, and `fsp create` says
   `Flutter {v} is too old: fespalier needs Flutter 3.35 or newer (https://docs.flutter.dev/release/upgrade)`.
   Upgrade Flutter (3.35.7 is the last 3.35 patch, with Dart 3.9.2), set the same `flutter-version` in CI, and raise
   your own `environment:` to `sdk: ^3.9.0` and `flutter: ">=3.35.0"` (what `fsp create` writes now). An app that has to
   stay on Flutter 3.32 to 3.34 stays on fespalier 0.15.x.
2. **go_router's lower bound is 17.2.3** (it was 17.0.0): `go_router: ">=17.2.3 <19.0.0"` in `fespalier`. An app that
   lets pub choose changes nothing, because 17.2.3 is the newest go_router that Flutter 3.35 to 3.37 resolve (3.38 and
   later take 17.5.0, and go_router 18 needs Flutter 3.44); an app whose `dependency_overrides:` or `pubspec.lock` holds
   go_router 17.0.0 to 17.2.2 runs `flutter pub upgrade go_router`.
3. **Why.** On Flutter 3.32 pub resolved go_router 17.0.0 and no newer one (17.0.1 asks for Flutter 3.35), and that release
   ran a `Block.then` of an `onEnter` inside the parse, before the commit, and asserted on a platform payload with no
   leading slash. On 17.2.3 neither needs a workaround, so the tests that tolerated them on the floor are strict now.
   What the floor still tolerates is go_router's and Flutter's own, and is true on every Flutter that has it: go_router 17
   builds the page a `go` lands on one frame after the location changes (go_router 18 builds it in the same frame), a
   `ShellRoute` pop skips the leaf's `onExit` before go_router 17.4, and Flutter before 3.38 drops a link's `linkUrl`.
4. **`fsp create`**: `--features all` now includes `otel` on every supported Flutter (it needed 3.35
   before), and an `fsp create` app declares `sdk: ^3.9.0` and `flutter: ">=3.35.0"`.
5. **An adapter's `onEnter` is a getter now.** `FespalierAdapter.onEnter` was a method (`FutureOr<OnEnterResult>? onEnter(InboundNavigation navigation)`)
   and is `FespalierEnter? get onEnter => null;`, where `FespalierEnter` is the function type of the old method. An
   adapter that overrides the method **no longer compiles**, on purpose: `Class 'MyAdapter' can't define method 'onEnter' and have field 'FespalierAdapter.onEnter' with the same name.`
   (`conflicting_method_and_field`), instead of its `onEnter` being skipped without a word. Return the same body as a
   function:

   ```dart
   // Before (0.15.0)
   @override
   FutureOr<OnEnterResult>? onEnter(InboundNavigation navigation) {
     if (navigation.next.uri.scheme != 'vaam') return null;
     return Block.then(() => navigation.router.go('/orders/42'));
   }

   // After (0.16.0)
   @override
   FespalierEnter? get onEnter => (navigation) {
     if (navigation.next.uri.scheme != 'vaam') return null;
     return Block.then(() => navigation.router.go('/orders/42'));
   };
   ```

   The getter is read once, when the router is built. No first-party adapter had an `onEnter`, so an app that lists only
   `fespalier_push`, `_analytics`, `_download`, `_sentry` or `_otel` changes nothing here.

6. **Every other app with `adapters:` navigates synchronously again.** `AppRoutes.router` now passes go_router an `onEnter`
   only when some adapter's getter is not null, and asks only those adapters. Before 0.16.0 any `adapters:` entry made
   go_router parse every navigation through an async `onEnter`, so `router.go('/a'); router.push('/b');` in one handler ended
   as `/home > /b` (the `go` lost) and `currentConfiguration` lagged a frame. Now it ends as `/a > /b`, committed in the
   call, as in an app without adapters. Code that worked around the lag (a `Future.delayed` or a frame between a `go` and
   a `push`) can go; an app with an adapter that has an `onEnter` keeps the async parse and its caveat.
7. **A router of your own** (`app.dart`'s `router()` building a `GoRouter` with `AppRoutes.mount`) that passed
   `onEnter: AppRoutes.onEnter` passes `onEnter: AppAdapters.handlesEnter ? AppRoutes.onEnter : null`. The old line still
   compiles and still calls the adapters that have one, but keeps go_router's async parse for an app whose adapters have
   nothing to say. Also new: with adapters and no `telemetry:`, `launchRouter` gets `links: AppAdapters.handlesEnter`, so
   no platform-link observer is added when no adapter has an `onEnter` (with `telemetry: true`, still `links: true`).
   Details: `docs/adapters.md` ("`onEnter` is a getter that answers a function") and `docs/migration.md`, "0.16.0".

8. **`fespalier_download_background`: a `5xx`, `408` or `499` on an upload is `Failed(other)`, not `Failed(rejected)`.**
   Only a client error that proves nothing was applied (`400`, `404`, `413`, `422`, ...) stays `rejected`. For an
   upload without an `Idempotency-Key` the new `other` is an unknown outcome: `outcomeUnknown(id)` is true, and `retry`
   and `start` refuse it (on 0.15.0 `retry` sent the write again after a `500` or `504`, which could run it twice).
   Search for `DownloadFailure.rejected` in the code that handles an upload and decide what an unknown outcome shows:
   ask your server, then `remove(id)` and `start` again, or give the upload an `Idempotency-Key`. Downloads are
   unchanged.
9. **`fespalier_download_background`: an upload whose registry entry cannot be saved ends `Failed(storage)` and is not
   sent.** `UploadStore.put` may now throw `UploadStoreException` (`FileUploadStore` does, on a failed write), and
   `FileUploadStore` no longer reads an unreadable file as an empty registry: `load` and `put` throw, the file is left
   alone, and until the next `open()` reads it (or `clearAccount()` deletes it) an upload **without** a key ends
   `Failed(storage)`. A custom `UploadStore` that swallows its failures keeps the old behaviour: let `put` throw.
   Handle `Failed(storage)` on an upload (`retry`); the two debug lines are in `fespalier-troubleshooting`.
10. **`fespalier_cratestack`: a `5xx` without a CrateStack envelope keeps the intent's key.** A bare `500`, a proxy's
    `520`, a panic handler's text is now `CrateStackOffline` (as `502`, `503`, `504` and `511` were), not
    `CrateStackUnavailable`: the write may have committed, and a new key would run it twice. Only a `5xx` in the
    envelope (`code` and `message`) is `CrateStackUnavailable` and moves to the next key. Visible effects: a read behind
    `serve` falls back to the saved copy on a bare `5xx` (it threw before), `DioFailures.read` and
    `CrateStackFailure.fromResponse` return `CrateStackOffline` for it, and `drain` stops at it as it stops at any
    `CrateStackOffline`. Search for `CrateStackUnavailable` in your own reader and tests; one that expected a bare `500`
    to be unavailable now sees offline.
11. **`fespalier_cratestack`: `drain` reads each intent again before it sends it.** An intent without a `subject` that a
    concurrent `submit` got accepted (or that was discarded, or wiped by a sign-out) while the drain was busy with an
    earlier one is no longer sent a second time. Nothing to change.
12. **An app with a `links:` section regenerates with `AppRoutes.urlOf`.** The diff is a doc comment and
    `static Uri urlOf(TypedLocation route, {String? locale})` after `matchUrl`:
    `Uri.parse('https://<first domain>${route.locationFor(locale)}')`, the mount prefix in it. Nothing has to change;
    use it for a share sheet, a notification payload or an `og:url`. An app without `links:` regenerates byte for
    byte. If the first domain of `links: domains` is not usable (none, not a host name, a wildcard first), `fsp gen`
    prints the warning ``! pubspec.yaml  `AppRoutes.urlOf` is not generated: ...`` and goes on, as before: only
    `fsp links` fails on it.
13. **`fespalier: test: a11y:` is opt-in.** Without it `fsp test` writes the file it always wrote. With `true` (or a list of
    `tap_targets`, `labels`, `contrast`) every smoke test also runs Flutter's accessibility guidelines on the whole screen,
    so the first run fails on whatever the app lacks, shared chrome first (an `IconButton` without a `tooltip`, an
    `InkWell` around a `Text`, pale text): fix the widget once and every route under it passes. An `fsp` older than
    0.16.0 rejects the key with the `unknown field` message that lists the `test:` keys.
14. **The DevTools extension has a seventh tab, _Adapters_**, and the protocol is still 1: the app lists `adapters` in
    `hello`'s features, sends `fespalier:adapter` events and a snapshot `adapters` list, and answers
    `ext.fespalier.adapterEdit`. A tool of your own that compares `features` exactly should ask `contains`. The tab
    is empty until a package calls `DevToolsAdapters.show`; on an app older than 0.16.0 it says so. Committed
    `devtools_options.yaml` files need no change.
15. **A plugin that throws is not asked again.** `biometricAvailable` (`fespalier_biometrics`), `pushPermission`
    (`fespalier_push`), `pendingIntents` (`fespalier_cratestack`) and `ChangeFeed.latest` (`fespalier_frb`) now pass
    `retry: (_, _) => null`. Before, Riverpod 3's default re-asked a plugin or store that threw an `Exception` up to ten
    times over about 50 seconds, with a `Timer` (a widget test whose fake threw ended with a pending timer; a `ChangeFeed`
    opened its single-subscription stream again). Now the provider is an `AsyncError`, read once. If you relied on the
    retries, call `ref.invalidate(provider)` where you want to ask again.
16. **A notification tap while the app starts is opened (`fespalier_push`).** It was lost: `launch()` runs before `runApp`,
    `attach` after `startup()` and the first frame, and nobody listened to `taps` in between. Now `launch()` keeps the
    latest tap (one, never a queue) and `attach` opens it once, as a warm tap, after the first frame. The cold-start
    notification seen again on `taps` is still opened once (by id; without an id, by an equal payload). Two things to
    check: a `PushSource.taps` built on a platform channel must return **one** stream every time (a `late final`
    field), because `taps` is now listened to twice while the app starts; and a test that taps between
    `AppAdapters.launch()` and `pumpWidget` now sees that tap open. See `docs/push.md`, "Cold start and taps".
17. **`fsp check` refuses a step folder that is no Dart enum constant.** A `steps` key written as `final`, `new`, `default`
    or `in`, a name every enum has (`values`, `index`, `hashCode`...), a name that starts with a digit (`2fa`), or two
    folders that become one constant (`contact_info`, `contact-info`) passed `fsp check` and then wrote a step enum that
    `flutter analyze` rejected, so no building app changes. Rename the folder and its key in `steps` (`final_step`,
    `step_2fa`); the messages are in [`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md).
18. **A request with a body is sent again after a 401 through `DioHttpClient`.** An `http.Request` (`get`, `post`, `put`,
    `patch`, `delete`) goes to Dio as bytes, so `SessionInterceptor` refreshes and sends it again whole (`WriteGuard` lets
    that one second send of a write through, as it always did after a 401). Before 0.16.0 it failed with
    `ClientException: fespalier_dio: unknown` and the refresh never helped: remove a retry you wrote around that. A streamed
    or multipart request (`StreamedRequest`, `MultipartRequest`) is not sent again: the caller gets the 401 as the response,
    after the refresh. A `ClientException` from `DioHttpClient` that has no Dio message now carries its cause
    (`fespalier_dio: unknown: <cause>`): code that compared the whole message changes.
19. **Offline while a token refreshes is `Failed(network)`, no longer `Failed(unauthorized)`.** A download whose credentials
    could not be reached ends `network` when its grantor, or the `HttpCredentials` of `HttpDownloadBackend`, throws an
    `http.ClientException` (`fespalier_auth`'s `AuthUnavailable` is one). `unauthorized` stays for a refusal and for any other
    throw. If your app treats `unauthorized` as "sign the person in again", it no longer does that for being offline: show
    "offline, try again" for `network` and call `Downloads.retry`. A `resume` whose grantor cannot be reached leaves the
    download `Paused` and returns false.
20. **A paused download resumes from its freshly granted address, and each resume gets its own renewal.** Before 0.16.0
    `resume` asked the grantor and threw the new `url` away, so an expired signed address earned a 403 first, and only one
    renewal existed for the whole life of the download: a second long pause ended `Failed(unauthorized)`. Now `resume` goes
    to the grant's `url` (the bytes kept stay), and a start, a retry and a resume each have one renewal. The grant a `resume`
    asks for is used now, not discarded. **A `DownloadBackend` of your own** (a
    fake in a test, a custom transfer) must accept the new `url:` named parameter of `resume(id, {authorization, url})`:
    `flutter analyze` names the override that is missing it. `FakeDownloadBackend.resumeUrls` records it.

Details: `docs/migration.md`, "0.16.0".

## 0.14 to 0.15: what to check

0.15.0 is a **breaking** release for an app that imports `package:fespalier_dio/http.dart` or
`package:fespalier_dio/problem.dart`: the `package:http` half of `fespalier_dio` is now the `fespalier_http` package,
and both libraries are **removed**, not deprecated (the 0.11.0 forms precedent). The generated `app.g.dart` is unchanged,
and a Dio-only app changes nothing (`package:fespalier_dio/fespalier_dio.dart` still exports `problem.dart`). Bump the
`ref:` of `fespalier` and every companion to the 0.15.0 tag, then:

- Add `fespalier_http` to `dependencies:` with the **same `url` and `ref`** as `fespalier`, and change the imports:
  `package:fespalier_dio/http.dart` becomes `package:fespalier_http/fespalier_http.dart` (which also exports
  `problem.dart`), and `package:fespalier_dio/problem.dart` becomes `package:fespalier_http/problem.dart`. No member was
  renamed. `flutter analyze` names every import left behind (`Target of URI doesn't exist`).
- `fespalier_auth` now depends on `fespalier_http` (its `Authorizer` implements `HttpCredentials`, `AuthAttempt`
  implements `HttpAuthorization`); an app that overrides dependencies by hand adds `fespalier_http` to the overrides.
- New and opt-in: `DioHttpClient` in `package:fespalier_dio/client.dart`, `HttpCredentials`, `HttpWrites.isWrite` (the one
  write rule both guards call; behaviour unchanged) and `FakeHttpClient` / `FakeHttpCredentials` in
  `package:fespalier_http/testing.dart`. [`fespalier-data`](../fespalier-data/SKILL.md) (its `http.md`) has the layer order.
  Details: `docs/migration.md`, "0.15.0".

## 0.13 to 0.14: what to check

0.14.0 is a **breaking** release for `fespalier_push`: every `PushSource` changes its `tokens` type, and an app with no token
callback changes nothing else. Bump the `ref:` of `fespalier` and every companion to the 0.14.0 tag, then:

- `PushSource.tokens` is a `Stream<PushToken>` (it was `Stream<String>`). Wrap the vendor's string:
  `PushToken(kind: PushTokenKind.fcm, value: token)`; `kind` is an open string (`PushTokenKind.fcm`, `apns`, `hms`,
  `unifiedpush`, `onesignal`, `mipush`, `oppo`, `vivo`, `honor`, `jpush`, or your own), `value` is never null, and `properties`
  (an unmodifiable `Map<String, String>`) carries what the backend needs besides the token, such as OneSignal's `subscription_id`.
- `onToken` in `FespalierPush.configure` takes a `PushToken`, and `pushToken` is a `StreamProvider<PushToken>`. Send `kind`,
  `value` and `properties` to the backend. `PushToken.toString` prints the kind only: do not print the value yourself.
- **A revocation is a separate event, never a null token**: `PushSource.revocations` (a `Stream<PushTokenRevoked>`, empty by
  default, so a source that never revokes needs nothing), the `pushTokenRevoked` provider, `onTokenRevoked` in `configure`.
- Tests: `FakePushSource(token: PushToken(...))`, `emitToken(PushToken(...))`, and `revokeToken(kind, properties:)`.
- No telemetry changed (no token event is reported). The vendor recipes (FCM, APNs, HMS, UnifiedPush, OneSignal, JPush,
  flutter_mix_push) are in the `fespalier-routing` skill's `push-sources.md`. Details: `docs/migration.md`, "0.14.0".

## 0.12 to 0.13: what to check

Bump the `ref:` of `fespalier` and every companion to the 0.13.0 tag and run the matching `fsp gen`; **`lib/app.g.dart` and
`lib/app.main.g.dart` come out unchanged** (no emitter or template changed since 0.12.0 but the version `fsp init` prints), and
`docs/migration.md` has no 0.13.0 entry because there is nothing to change. What is new is additive and opt-in: the companion
packages `fespalier_maps`, `fespalier_push`, `fespalier_biometrics`, `fespalier_analytics`, `fespalier_frb` and
`fespalier_riverpod` (each in the skill that owns its topic; they take the same `url` and `ref` as `fespalier`), and in
`package:fespalier`: `appShowSignal` (a `RefetchSignal` that fires when the app is shown again after it was hidden, not when
it only went inactive), `FespalierTelemetry.contains(sink)` (whether a sink is installed, alone or inside a `combine`), and
`package:fespalier/fespalier.dart` also exports Riverpod's `NotifierProviderFamily`, `ProviderFamily` and
`ProviderOrFamily`. No `TelemetryOp`, file kind, `fespalier:` key or command was added, so an exhaustive telemetry sink
still compiles.

## 0.11 to 0.12: what to check

0.12.0 changes nothing for an app that does not opt in: `app.g.dart` and `app.main.g.dart` regenerate to the same
bytes. New in `startup.dart` (since 0.12.0): `FutureOr<void> ready(ProviderContainer container)` and
`void attach(GoRouter router, ProviderContainer container)`, each optional. The gate makes the app's
`ProviderContainer` itself when `ready()` exists, runs it before the router is built, and calls `attach()` after the
first frame that shows the router, after the adapters' `attach`. The order is `zone()`, `startup()`, the container,
`ready()`, the router, `attach()`. `ready` and `attach` are reserved names in startup.dart: a helper of that name with another shape is now an `fsp` error (rename it or make it private). A `ready()` that throws goes to the splash's error and `retry`, which
disposes the container, makes a fresh one and runs `ready()` again (not `startup()`). To move a `main: manual` app's
`main()` over: its overrides to `startup()` (they are made before any container), the code between creating its
`ProviderContainer` and `runApp` (an `await container.read(x.future)`, an eager read, a `container.listen`) to
`ready()`, and the post-frame step that needs the router to `attach()`. Details: the `fespalier` skill's app-main reference; `docs/migration.md`, "0.12.0".

## 0.10 to 0.11: what to check

0.11.0 is a **breaking** release for apps with forms (`form()` in an `action.dart`); an app with none changes nothing. Bump the `ref:` of `fespalier` (and every companion) to the 0.11.0
tag, then:

1. **Add `fespalier_forms`** under `dependencies:`, at the **same git `url` and `ref` as `fespalier`** (the block is in
   `packages/fespalier_forms/README.md` and `docs/forms.md`), and run `fsp gen`. `app.g.dart` now imports
   `package:fespalier_forms/fespalier_forms.dart`, **only in an app with a `form()`**. Until the dependency is there `fsp`
   reports an error at each `form()`: `` `form()` is the form of `action()`, and since 0.11.0 forms are in the fespalier_forms
package: add `fespalier_forms` under `dependencies:` in pubspec.yaml, with the same git `url` and `ref` as fespalier ``.
2. **Imports of the form types.** Code that names `ActionForm`, `ActionField`, `ActionTextField`, `ActionFormFields`,
   `FieldCodec`, `ActionFormMessages`, `ActionFormValidation` or `useActionForm` imports
   `package:fespalier_forms/fespalier_forms.dart`: `package:fespalier/fespalier.dart` no longer exports them (no shim and no
   re-export). The names and the behaviour are the same, and a page that only calls the generated `useForm` needs no import.
3. **What stays in `fespalier`**: `FieldErrors`, `validate()` and `optimistic()`. A test of an action's `FieldErrors` or of
   `validate()` changes nothing; `fespalier_dio`, `fespalier_auth`, `fespalier_cratestack` and `fespalier_sentry` are
   unchanged. A test file that was `packages/fespalier/test/action_form_test.dart` in a fork is
   `packages/fespalier_forms/test/action_form_test.dart` now.
4. **Floor and CI**: `fespalier_forms` claims Flutter 3.32 like the packages it follows; a repository that copies this
   repository's `just floor` list adds it.
5. Where the form is documented now: the forms and optimistic pages of [`fespalier-data`](../fespalier-data/SKILL.md)
   (the one page it was part of is split in two).
6. **Drafts are new and opt-in, but every app with a `form()` regenerates.** `useForm` takes a `FormDraft? draft` and
   `useActionForm` gets the action's `id:`, `key:` and `shape:`; a `bool`, `DateTime` or enum field gets a `DraftCodec`.
   A key of an action with a form can no longer be called `draft` (`fsp` says `` `draft` can't be a key of an action with a
form: its hook, `useForm`, takes a parameter called `draft`; rename it ``). Drafts are kept in `formDraftStorage` (your
   `dataCacheStorage` by default): call `clearFormDrafts(ref)` at sign-out and give `formDraftScope` the account.
7. **Asking before unsaved changes go is new and changes no generated code.** A `leave.dart` that is
   `leaveIfClean(context, ref, page)` (from `fespalier_forms`) asks in a bottom sheet ("Keep editing", "Discard",
   "Keep as draft" for a form with a `draft:`); a `useForm` under a page with a `leave.dart` registers its form as the
   page's `LeaveSource` itself. The sheet is Flutter's (`showModalBottomSheet`), so an app on material_ui's
   `MaterialApp`, which has no `MaterialLocalizations`, overrides `leavePrompt` with its own sheet. See
   the forms reference of `fespalier-data`, "Leaving with unsaved changes".
8. **Multi-page forms are new and opt-in** (the flows reference of `fespalier-data`). A section's `action.dart` with a
   `const steps` map is a form over several pages that share one form and one draft; an app that adds none changes
   nothing. Only a map literal called `steps` (or `<action>Steps`) beside a `form()` is read as one from 0.11.0 (and
   reported when malformed); a `steps` of another shape is left alone. A flow section may have a page-less
   `leave.dart`. `LeaveScope.onBack` now blocks the pop on the first page of a navigator too.

### Route lifecycle

An app with an `observe.dart` regenerates `lib/app.g.dart`, and nothing else changes for a hook you wrote.

1. The generated closures read `onEnter: (ref, scope) => ...` now: `RouteHooks.onEnter` is
   `void Function(Ref ref, RouteScope scope)?`. A hand-built `RouteHooks` (a test, a fork) takes two parameters:
   `onEnter: (ref, _) => ...`. Run `fsp gen` with the 0.11.0 `fsp`.
2. `onEnter` may take `{required RouteScope scope}`: `scope.hold(provider)` keeps a provider (a route's `data`) loaded
   until the page is gone, a parked tab included, and `scope.onLeave(callback)` runs when it is gone. `onLeave` and
   `onFocus` cannot take it (an error). The page instance, the order at leave and the lifetimes are on
   [`fespalier-observability`](../fespalier-observability/SKILL.md)'s lifecycle page.
3. `AppRoutes.attach` takes the optional `ProviderContainer` in an app with an `observe.dart` too (it had it only with
   `adapters:`), and the generated `lib/app.main.g.dart` passes it (`attach: AppRoutes.attach`: regenerate both files).
   Hooks therefore run in the app's root container: a provider overridden only in a nested `ProviderScope` reads its
   default there. `AppRoutes.attach(router)` works as before.
4. A scope ends when its container is disposed too, so a `scope.onLeave` callback runs at the end of a `pumpRouter` test.
5. **Page ids changed for `replace`**: a page made by `replace` has the key of the page it replaced (go_router), and the
   lifecycle now uses it: `replace('/c/1?q=2')` on `/c/1` is no leave and enter, `replace('/c/2')` is. Telemetry page
   events and Sentry breadcrumbs follow. `push` and `pushReplacement` are unchanged. Test a hook with `TestRouteScope`
   (`package:fespalier/testing.dart`).

### Adapters

**An app without `fespalier: adapters:`
gets nothing from this part. An app with `adapters:` regenerates two files:**

1. `lib/app.g.dart` gains `AppAdapters` and the adapters' imports (`package:<name>/fespalier_adapter.dart as _a0`), and
   `AppRoutes.attach` takes an optional `ProviderContainer` and runs each adapter's `attach` with it.
2. `lib/app.main.g.dart` no longer imports the adapters: it calls `AppAdapters.zone`, `.beforeRun()`, `.wrap`,
   `.overrides()`, `.providerObservers()` and `.routerObservers()`, and gives the `StartupGate` `attach: AppRoutes.attach`.
3. `main: manual` with `adapters:` is accepted (0.10.0 refused it): call `AppAdapters` from your `main()` and
   `AppRoutes.attach(router, container)` once both exist (`fespalier`, app-main page).
4. `FespalierAdapter` has a new member, `attach(router, container)`, with an empty default. An adapter that
   **`implements`** `FespalierAdapter` (not `extends`) stops compiling: extend it.
5. `FespalierAdapter` also has `launch()` and `onEnter(InboundNavigation)` (empty defaults), and the runtime has `InboundLaunch`
   and `launchRouter`: a platform link is marked `NavigationSource.link` in telemetry when `launchRouter(links: true)` builds the
   router. The generated wiring is there too: `AppRoutes.router` takes `launch:` and passes `links: true` with telemetry or
   adapters, and with adapters there is an `AppRoutes.onEnter` (passed to `GoRouter(onEnter:)`, since 0.16.0 only when an adapter has an `onEnter`) and `AppAdapters.launch()`, which
   the generated main asks once and hands to the router as `AppMain.launch`. Every app's `app.g.dart` changes (the router is built
   inside `launchRouter`: run `fsp gen`). An app.dart `router()` passes `launch: AppMain.launch` on (`fsp` warns otherwise); a
   `main: manual` app calls `AppAdapters.launch()` itself. Any `onEnter` makes go_router parse every navigation asynchronously and
   apply its redirect limit, so it is generated only with adapters.
6. Moving from `main: auto` to `manual`: delete `lib/app.main.g.dart`. Each adapter's top-level `adapter` is read once, at the first `AppAdapters` call. `attach` runs after the first frame that shows the router.

### Guards above tabs (0.11.0)

A guard above a tab layout (the tabs folder's own, or a page-less folder over it) is now generated once, on the `StatefulShellRoute`'s `redirect:`, not copied into each tab's route (`fsp gen`). Behaviour is the same; its telemetry and DevTools site is one, with the tab folder's pattern as `fespalier.route` (`/` for a group), so dashboards grouping guard outcomes by route see the tabs merged. A tab's own `guard.dart` stays on its route.

### Telemetry (0.11.0)

`TelemetryOp` gains `custom`, for a package's own operation (`FespalierTelemetry.begin` and `finish`; `TelemetryStart` has
new `name` and `attributes` fields and `TelemetryEnd` a new `attributes` field). **A `FespalierTelemetry` sink of your own
with an exhaustive `switch` on `TelemetryOp` stops compiling**: add a `TelemetryOp.custom` case or end the switch with
`_ =>`. The error says the switch does not handle `TelemetryOp.custom`. An app that uses only `FespalierOtel`,
`FespalierSentry` or `RecordingTelemetry` changes nothing. `FespalierSentry` does not send a `custom` failure as an event
unless you pass a `capture:` that returns true for it (the exception text is the package's).

## 0.9 to 0.10: what to check

Bump the `ref:` to the 0.10.0 tag, run the matching `fsp gen` as always, and expect **`lib/app.g.dart` unchanged**. This was
checked as of `bfbbf87f` (after 0.9.1): nothing the emitter writes, no runtime file of `package:fespalier` and no template
that `fsp new` or `fsp init` writes into an app changed behaviour since 0.9.1, only comments and the documentation pointers
of a few messages. Re-run `fsp gen` and `git diff lib/app.g.dart` on the release itself to confirm; a diff there is a bug to
report, not something to accept.

1. **The documentation moved.** The long README is now a short one, and the reference is one-topic pages under `docs/`
   (`docs/routing.md`, `docs/data.md`, `docs/i18n-tolgee.md`, ...). The old README anchors still work (the README keeps one
   per old heading, and `docs/README.md` maps them). **Some `fsp` messages cite a page now**, where 0.9 cited the README:
   `fsp init`'s pointer (`see docs/app-startup.md`), the `fsp run` and `tasks:` messages (``docs/cli.md, "Tasks: commands
around `flutter run`"``) and the warning `⚠ this app sends no fespalier spans yet ... (docs/observability.md,
"Telemetry")`. A CI step or a script that greps for the old `(README, "...")` text must follow; the message's meaning is
   the same.
2. **Two new, opt-in companion packages** with **no generator change** (no file kind, `fespalier:` key or `fsp` command):
   `fespalier_tolgee` (translated texts, the language from the URL: [`fespalier-i18n`](../fespalier-i18n/SKILL.md)) and
   `fespalier_cratestack` (offline-first reads, queued writes and sync, with a CrateStack client:
   [`fespalier-offline`](../fespalier-offline/SKILL.md), [`fespalier-cratestack`](../fespalier-cratestack/SKILL.md)). Like
   every companion, they take **the same `url` and the same `ref` as `fespalier`** (and `fespalier_cratestack` needs
   `fespalier_dio` at the same tag too). An app that does not depend on them is byte for byte what it was. **Neither ships a
   `fespalier_adapter.dart`**, so they go in `startup()`, not in `adapters:`.
3. **Adopting translations from `gen-l10n` or from the `tolgee` SDK** is not a mechanical change (keys become strings, the
   locale comes from the route, apostrophes before a brace are doubled): the steps are in
   [`fespalier-i18n`](../fespalier-i18n/SKILL.md) (its `messages-and-catalogs.md` page).
4. **Nothing to do for telemetry sinks**: 0.10.0 adds no `TelemetryOp` and no convention (contract version 1), so an
   exhaustive sink still compiles. Reads through `serve` and `submit` run inside the existing data and action spans.

## 0.8 to 0.9: what to check

Bump to `v0.9.0`, regenerate (`lib/app.g.dart` changes in every app, by its page names: item 10), and look at these:

1. **A `FespalierTelemetry` sink that switches exhaustively over `TelemetryOp` stops compiling** (`The type 'TelemetryOp' isn't exhaustively matched by the switch cases since it doesn't match the pattern 'TelemetryOp.auth'`, and `'TelemetryOp.image'`). Add a `TelemetryOp.auth` case (it is what `package:fespalier_auth` reports, with
   `TelemetryStart.authStep`, `authBackend`, `authTrigger` and `authDpop`) and a `TelemetryOp.image` case (what `package:fespalier_image` reports, with
   `TelemetryStart.imageCdn`, `imageWidth` and `imagePreload`, and `TelemetryEnd.imageStatus`), or end the switch with `_ =>`.
   `fespalier_otel` and `RecordingTelemetry` have it. A sink with a `default`, or one that does not switch, is
   unaffected. `TelemetryOutcome` gains `none`, `expired`, `rejected` and `cancelled`, and
   `FespalierTelemetry.begin` and `finish` (for adapter packages).
2. **The telemetry conventions gain an `auth` and an `image` operation, with `fespalier.auth.*` and
   `fespalier.image.*` attributes**, within contract version 1 (new values of `fespalier.operation`, new keys): a
   dashboard that lists the operations shows two more. `fsp telemetry`'s dashboards label them "Session (sign-in,
   refresh, sign-out)" and "Image load".
3. **New, opt-in:** `package:fespalier_auth` ([`fespalier-guards`](../fespalier-guards/SKILL.md), its
   `auth-package.md`), with OpenID Connect and Keycloak (`package:fespalier_auth/oidc.dart`), a dio interceptor
   (`package:fespalier_auth/dio.dart`) and, as a separate package, device-bound tokens
   (`package:fespalier_sign_keypair`, DPoP; its `auth-dpop.md`). An app that adds `fespalier_sign_keypair` needs
   **Dart 3.12 and Flutter 3.44**, the same `url` and `ref` as `fespalier` and `fespalier_auth` for the three, and
   network access to `github.com/vaam-apps/flutter-sign-keypair` at `pub get` (it is a git dependency, not on
   pub.dev). Nothing else changes: no generated code, file kind, key or command.
4. **An app with `telemetry: true` regenerates a different `app.g.dart`.** Each data provider calls `data()`
   through `traceDataCall(ref, 'd4', id, () => _i5.data(ref, id: id), telemetry: ...)` instead of
   `traceData(ref, 'd4', id, _i5.data(ref, id: id), telemetry: ...)` (an app without `telemetry: true` keeps
   `traceData`). It costs one closure per provider build, with no `Future` and no microtask.
   What follows: a `data` span **starts before `data()` runs**, so its duration includes the synchronous part;
   a `data()` that throws before it returns now gets a `data` span (`fespalier.data.state = error`,
   `fespalier.async = false`; before 0.9.0 it got none); and `FespalierOtel` makes data and action spans
   current while they run, so the spans of `otel_http` and `otel_dio` made inside are their children.
5. **New, opt-in:** `package:fespalier_image` ([`fespalier-images`](../fespalier-images/SKILL.md)): a
   `ResponsiveImage` that fetches a network image at the width its box needs through an image CDN (imgproxy,
   EmgR, Cloudinary, imgix, Thumbor, a template or a signed srcset), and `RouteLink(onPreload:)` in fespalier
   itself, which runs a callback when a link starts a preload (a nullable parameter: nothing changes for a link
   that does not pass it). The same `url` and `ref` as `fespalier` for the two. No generated code, file kind,
   key or command changes.
6. **New, opt-in, in `fespalier-observability`:** `FespalierTelemetry.combine` and `add` (several sinks in
   the one slot, each with its own tokens and isolated), the `within` hook a sink may override (an instance
   member with a default, so a sink compiles unchanged unless it already had a member named `within` with
   another signature: rename it), `FespalierTelemetry.run` for adapter packages, and `navigateFrom` with
   `NavigationSource` and the attribute `fespalier.navigation.source` (contract version 1 gains a key; absent
   unless a bridge marks the navigation). `RecordingTelemetry` gains `recordWithin:` and `source=`.
7. **The package asks for `hooks_riverpod: ^3.3.2`** (it was `^3.2.1`): on riverpod 3.2.1, the lowest the old
   constraint admitted, a closed `PrefetchHandle` left its provider alive and `freshness` did not load again.
   An app already resolves 3.3.2 or newer; one pinned lower must raise its own constraint.
8. **New, opt-in:** `package:fespalier_dio` ([`fespalier-data`](../fespalier-data/SKILL.md), its `http.md`): `ref.cancelToken()` and
   `ref.abortable(client)`, `withFieldErrors()` and `WriteGuard` for Dio and `package:http`. A repository dependency
   with the same `url` and `ref` as `fespalier`; an app that does not add it is unchanged (no generated code, file kind,
   key or command).
9. **New, opt-in:** `package:fespalier_sentry` ([`fespalier-observability`](../fespalier-observability/SKILL.md)):
   Sentry, errors first (events tagged with the route pattern, the app file and the action, one breadcrumb per page
   change, the OpenTelemetry trace id on each event next to `fespalier_otel`; screen-load transactions only with
   `tracing: true`). The same `url` and `ref` as `fespalier`, and `sentry_flutter` 9.26.0 or newer. No generated code,
   file kind, key or command changes. `FespalierTelemetry` gains `traceOf` and `linkTrace` (instance members with
   defaults) and `TelemetryTrace`, which `combine` uses to tell a sink which trace an operation is in (`FespalierOtel`
   answers it): a sink that already had a member named `traceOf` or `linkTrace` with another signature must rename it.
10. **An app that opts in to nothing regenerates with page-name changes only (since 0.9.0).** Each `pageBuilder:`
    fespalier writes (a route with a `transition.dart` or `present.dart`, a `remount` route, a layout's
    shell) is wrapped in `namedPage('<pattern>', () => ...)`: two lines per page builder, the first
    gaining `namedPage('/products/:id', () =>` and the last a `)`. The pages `Transitions.*`,
    `layoutPage` and `remountPage` build are then named by their route pattern (`RouteSettings.name`),
    so a `NavigatorObserver` (Sentry's, Firebase Analytics', PostHog's) sees `/products/:id` where it
    saw `null` (a `remount` page saw `:id`). Keys, restoration ids, transitions and the release build
    are otherwise the same. A route with neither (a bare `builder:`) is go_router's own page and
    unchanged. With `telemetry: true` each `data.dart` provider also becomes
    `traceDataCall(..., () => data(...), telemetry: ...)` (item 4). A `transition.dart` that builds a
    `Page` of its own can pass `name: Transitions.pageName`.
11. **New, opt-in, in [`fespalier`](../fespalier/SKILL.md) (its app-main page):** the `fespalier: adapters:`
    key in `pubspec.yaml` (a list of package names), and `FespalierAdapter` in `package:fespalier/startup.dart`. Each listed
    package ships `lib/fespalier_adapter.dart` with a top-level `adapter`, and the generated `main()` calls its
    `zone`, `beforeRun`, `overrides`, `providerObservers`, `routerObservers` and `wrap`; the key makes `main: auto`
    write `lib/app.main.g.dart` on its own. An app without the key regenerates the same `lib/app.main.g.dart`
    as before. An `fsp` older than 0.9.0 rejects the key as an unknown field.

## 0.7 to 0.8: what to check

Bump to `v0.8.1`, regenerate, and look at these:

1. **`unknown_path` checks segment types.** The string-path lint (`lints: unknown_path`)
   now also reports a literal path that reaches a route whose segment cannot parse it:
   `` `/products/abc` reaches /products/:id, but `abc` is not an int, so it shows not-found
[unknown_path] `` (on one line). It is the same id and level, so an app with
   `unknown_path: error` that passed on 0.7.0 can fail on 0.8.1, for a path that always
   showed not-found. Fix the literal, use the typed route, or `// fsp:ignore unknown_path`.
   Messages and what is checked: `fespalier-troubleshooting`, "String paths"
   in its diagnostics reference.
2. **The package asks for `hooks_riverpod: ^3.2.1`** (it was `^3.0.0`): `Ref.mounted` is right for a stale ref and a
   paused provider resumes, which `freshness` relies on, and the experimental `persist()` that `dataCache` is built on
   is there. An app already resolves 3.4.x; one pinned lower must raise its own constraint.
3. **An app that opts in to nothing regenerates with DevTools-only changes.** A data route's view now watches through
   `watchData(ref, 'dN', provider)` and `lib/app.g.dart` gains a `_devToolsProviders()` map that `devToolsRegister`
   receives. `watchData` returns `ref.watch(provider)` unchanged (a pass-through: no `Future`, no microtask, and in a
   release build it is `ref.watch`) and the map is only read under `kFespalierDevTools`, so behaviour, timing and the
   release build are the same; only the diff of the generated file is new.
4. **`freshness` and `dataCache` are now names `fsp` reads in a `data.dart`.** A public top-level variable of that name and
   another type is an error (`` `freshness` must be a `Freshness(...)` ``); rename it. A private `_freshness` is never read.
   A `route.dart` may hold `const freshness = Freshness(...)` too (the "expected ..." error now names seven constants).
5. **New, opt in:** `Freshness` (`staleTime`, `refetchOnResume`, `refetchOnReconnect`), `DataCache` with
   `dataCacheStorage` and `MemoryDataStorage`, `package:fespalier/persist.dart`, and the `fresh` and `cached` tags of
   `fsp routes`. A route that opts in keeps its page when a reload fails (the freshness page of [`fespalier-data`](../fespalier-data/)).
6. **A `lib/app/app.dart`, `startup.dart` or `splash.dart` at the root that is something else** is the one thing that can
   break: `fsp` reads them now (`main: auto`) and errors with "the app's widget gets the router: ...". Move the file into
   `_components/`, or set `main: manual`. Moving a hand-written `main()` to the generated `AppMain` is optional; the
   table is in [`references/upgrading-0-7-to-0-8.md`](references/upgrading-0-7-to-0-8.md). An app with none of the
   three gets no new file (`lib/app.main.g.dart` is written only when one exists, or with `main: generated`).
7. **New, opt-in:** `observe.dart` (`onEnter`, `onFocus`, `onLeave` per page), the `telemetry` key,
   `package:fespalier_otel`, `RecordingTelemetry` and `fsp new --observe`. See
   [`fespalier-observability`](../fespalier-observability/SKILL.md).
8. **`fsp new` with nothing to create** now lists `--observe`: `nothing to create: ... also pass --action,
--layout, --loading, --error, --not-found, --guard, --observe or --transition`.
9. **A new tag on `fsp routes`**: a page with an `observe.dart` at or above it is tagged `observe` (and
   `--json` `tags` and the route tree's `markers` gain the value); consumers that match tags
   exactly should accept it.
10. **`otel_zone` and the dartastic rc.4 line** (since 0.19.0). `fespalier_otel` needs `dartastic_opentelemetry`
    ^1.1.0-beta.17 and API rc.4, which is `otel_zone` v0.8.1 (commit `64c4661ac6cd09718141864d528892916677cc38`):
    bump that `ref`. It accepts go_router 17 and 18, so the `go_router: ^18.0.0` override is
    gone; an `otel_zone` up to v0.7.0 pins go_router 17 (through `otel_go_router` ^0.2.0) and cannot resolve
    beside this package.
11. **`DeferredLibrary` has an optional `route`** (the generator sets it with `telemetry: true`), and
    `traceGuard` and `traceData` take an optional `telemetry:`; nothing to do unless you call them yourself.
    An app with no `observe.dart` and no `telemetry: true` gets none of items 7 to 11 in `app.g.dart`:
    no `TelemetrySite`, no `AppRoutes.attach`, no `observe:` (the generator's `no_companions` test pins it).

## 0.6 to 0.7: what to check

Bump to `v0.7.0` and regenerate. A route that is not deferred generates exactly what it did before. The one visible change is
new **warnings**: `fsp gen`, `check` and `watch` now read the string paths in `lib/` and warn about one that matches no route
(``no route matches `/nope`, so it shows not-found [unknown_path]``; the severity is the pubspec's `lints: unknown_path`, and
`error` makes the commands exit 1). Fix the path, use the typed route, `// fsp:ignore unknown_path`, or set `off`. New and
opt-in: `deferred` (a page's code loads on demand), `fsp maestro` with `semantics_ids`, the DevTools extension,
`TypedLocation.pushReplacement` and `RouteInfo.sibling`.

## 0.5 to 0.6: what to check

Bump to `v0.6.0`, regenerate, and look at these:

1. **`remount: never` is what fespalier generated before 0.6.0** (a page keeps its state when its URL changes), and the generated
   code keys a page by the URL where it used go_router's `state.pageKey`. A route that should start again when its URL changes
   opts in with `remount` (`fespalier-routing`).
2. **`replace` now shows its location in the address bar and replaces the history entry** on the web; on 0.5.0 it was go_router's
   in every case (the address bar followed it only when no page was below it), so use `go` for URL state there.
3. **`pumpRouter(disposeRouter: false)`** is the way to keep a test's own `addTearDown(router.dispose)` (item 1 of
   "0.4 to 0.5").

## 0.4 to 0.5: what to check

Bump to `v0.5.0`, regenerate, and look at these:

1. **`pumpRouter` disposes the router when the test ends.** A test that registered
   `addTearDown(router.dispose)` before calling it now fails with _A
   GoRouteInformationProvider was used after being disposed_, because that teardown runs
   after `pumpRouter`'s. Delete the line, or, since 0.6.0, keep it and pass
   `disposeRouter: false`.
2. **New reserved names.** Every typed route gains `preload`, `of`, `maybeOf` and
   `copyWith`, so a segment or query parameter with one of those names is refused by
   `fsp`; rename it. An `action.dart` function can't use them either.
3. **`AppRoutes.router()` without a `navigatorKey` makes a fresh one**, so tests no longer
   share a navigator through the generated class. A test that mounts under a prefix
   restores the defaults with `addTearDown(AppRoutes.mount)`.
4. **New, and nothing changes unless you use it:** `action.dart`, `RouteLink` with
   `preload` (it brings in `url_launcher`), `XRoute.of(context)` and `copyWith`, guards
   and redirects that take a `Ref`, and `fsp links` / `fsp routes --graph`.

## 0.3 to 0.4: what to check

Nothing in the generated code or the runtime API breaks; bump, regenerate, and look at
these:

1. **The package is `publish_to: 'none'`.** It was never on pub.dev; keep the git
   dependency and move its `ref:` to `v0.4.0`.
2. **`currentLocation(tester)` follows a `push`** (the top of the stack). A test that
   asserted the old location after a push, or read
   `currentConfiguration.last.matchedLocation` to work around it, can now use
   `currentLocation`; one that expected the old value fails.
3. **Three diagnostics read differently** (folder names accept `A-Z`, a hand-written
   family keyed by a query parameter, an optional parameter of a non-query type). Only a
   test that matches `fsp`'s text notices.
4. **New: `const nest = false;` in `route.dart`** makes a route a sibling of the page
   above it, with a compound path (`fespalier-routing`). Nothing uses it unless you write
   it.

## 0.2 to 0.3: what to check

Six things can change behaviour or break the build; the full table, with what to do for
each, is in [`references/upgrading-0-2-to-0-3.md`](references/upgrading-0-2-to-0-3.md).

1. **`prefetch` returns a `PrefetchHandle` and lives until you `close()` it** (it lapsed
   after 30 s before); **`prefetchKeepAlive` is gone**. Pass `keepFor:` for timed behaviour.
2. **A `transition.dart` at or above a layout now animates that layout's shell too**
   (`fsp init` writes a root one, so most apps see it). Look at every layout; take
   `bool shell` in `transition()` to treat the shell differently.
3. **Generated `data()` providers keep Riverpod's automatic retry** (no more
   `retry: null`). Give the app `ProviderScope(retry: ...)` a policy or set
   `data_retry: none`; tests that count calls or leave timers will notice.
   `DataView` also keeps the old state on screen during a reload (`keep_previous`).
4. **`NotFoundScope` takes a named `caseSensitive:`** (hand-written scopes only).
5. **`fespalier.dart` hides go_router's own `RouteMatch`** for fespalier's; import
   `package:go_router/go_router.dart` (prefixed, or with `hide`) if you used it.
6. **`router()` and `mount()` gained `navigatorKey`**, and layouts are built as
   `pageBuilder` pages. Regenerate; nothing to write.

Plus new reserved names (`extra` as a segment; later, `of`, `maybeOf` and `copyWith`, since 0.5.0) and `pumpRouter`'s default of **no
retries**. Everything else in 0.3.0 is additive.

## Adopting fespalier in a go_router app

Mount the tree **inside** your router under a prefix and move routes one folder at a
time:

```dart
GoRouter(
  navigatorKey: rootKey,
  routes: [
    ...legacyRoutes,
    ...AppRoutes.mount(at: '/shop', navigatorKey: rootKey),   // pass YOUR router's key
  ],
  errorBuilder: (context, state) => AppRoutes.notFound(state.uri),
)
```

- `at` is the URL prefix: typed routes, `uri` in guards, `dataAt` and `match` all know it
  (`ProductRoute(id: 2).location` is `/shop/products/2`; a location outside the prefix
  is `null` for `dataAt`). **Mount once**: `mount` stores `at` and the key in static
  fields.
- **Pass the host router's own `navigatorKey`**; routes using `navigator.dart` or
  `present.dart` need it as their `parentNavigatorKey`.
- `mount` passes **no** `extraCodec`, `restorationScopeId`, `observers` or
  `initialLocation`: they belong to your router. Forward unknown URLs to
  `AppRoutes.notFound(state.uri)`.
- Move a route = a folder with a `page.dart`; a `ShellRoute` = a `layout.dart`; a
  stateful shell = a tab layout; a route `redirect` = `guard.dart`/`redirect.dart`;
  `pageBuilder` transitions = `transition.dart`; string paths = typed routes.
- **Siblings with a compound path.** A folder below a page nests under it, so a deep link
  to `/orders/1/refund/confirm` builds `/orders/1/refund` too. If your tree had
  `GoRoute(path: 'refund')` and `GoRoute(path: 'refund/confirm')` side by side on purpose,
  keep that shape with `const nest = false;` in `refund/confirm/route.dart` (0.4.0).

The step-by-step guide, with a compiled, tested host router, the mapping table and the
things `mount` does not carry, is in
[`references/go-router-adoption.md`](references/go-router-adoption.md).

`examples/adopt` is that guide as a running app: the old routes beside `AppRoutes.mount(at: '/shop')`
in an `app.dart` `router()` under `main: auto`, the old URLs redirected to the typed routes,
`ready()` and `attach()` in `startup.dart`, the pre-adoption version kept compiled in `lib/before/`,
and `test/parity_test.dart`, which opens the same URLs in both. Read it next to the guide.

## Coming from RIBs

A team that knows Uber's RIBs maps each part onto a file kind or a provider, never onto classes of the same names:
a router's attach decision is a `guard.dart`, an interactor is `data.dart`, `action.dart` and `observe.dart`, the
builder and component are the generated `lib/app.g.dart` and Riverpod providers, a viewless RIB is a `(group)`
folder, and a workflow is a URL with guards in front. The difference that matters: the location, not business logic,
decides what is on screen. The table, the tutorial app as folders and the traps are in
[`references/from-ribs.md`](references/from-ribs.md); the user documentation is `docs/coming-from-ribs.md`.

## Also

- `fsp init` in an existing project **never overwrites** a file: it prints `skip  ... (exists)`.
- Keep `lib/app.g.dart` committed and add `dart run fespalier gen` plus
  `git diff --exit-code lib/app.g.dart` to CI: `fsp check` does not see a stale file.
- Releases are cut by release-please; each tag is a package and an `fsp` of the same
  version and takes the same steps (bump, matching `fsp`, regenerate). Read the root
  `CHANGELOG.md` entry of **that** release: its "BREAKING CHANGES" first (0.3.0 has an
  "Upgrading from 0.2" section instead).

If `fsp` or `flutter analyze` complains after an upgrade, see
[`fespalier-troubleshooting`](../fespalier-troubleshooting/).
