---
name: fespalier-data
description: "How fespalier routes load data — data.dart and its three forms (a function, a selector of a provider you already have, or a provider you write), how segments and query parameters key the provider, loading.dart and error.dart, keep_previous and data_retry, section data and the typed Section handle, prefetch handles and preload (the whole page's data behind one handle, as RouteLink uses it), the typed watch/read/refresh helpers, AppRoutes.dataAt and match, and how it all sits on Riverpod 3 — freshness and the data cache (since 0.8.1: staleTime, refetch on resume and reconnect, dataCache, DataCache, MemoryDataStorage, keepDataOnError; since 0.9.0 the fespalier_storage package: PrefsDataStorage and HiveDataStorage, a saved value on the first frame, size budgets and eviction, and the fespalier_connectivity package: reconnectSignal from connectivity_plus, hasNetwork for offline banners, connectivity versus reachability), and action.dart, the write side (typed submit and useAction, pending and error state, what a success invalidates, and since 0.8.1 validate() with FieldErrors and optimistic(), and its forms: form() and useForm, which are the fespalier_forms package since 0.11.0 and a breaking move out of fespalier, with opt-in drafts: FormDraft, formDraftStorage, formDraftScope, clearFormDrafts, DraftCodec), and since 0.9.0 fespalier_dio and fespalier_http (the package:http half since 0.15.0, on 0.14.0 and earlier fespalier_dio/http.dart), which tie Dio and package:http to the data and the write (a load cancelled with its page, a server's validation error as the form's FieldErrors, a write that a retry interceptor never sends twice), and since 0.13.0 fespalier_frb (a Rust core's change stream held in one subscription, a topic provider that a data.dart watches so a matching event rebuilds it, InvalidationTable, initRustCore for startup(), and since 0.18.0 ChangeCodec, which decodes a core's raw or batched messages and skips a bad or unknown one without ending the feed), and since 0.13.0 fespalier_riverpod (a provider per page instance: two pushes of one route are two states, a query change or a remount is one, holdForPage keeps state the page reads but does not watch, usePageInstance), and since 0.10.0 offline-first reads and queued writes (fespalier_cratestack: see fespalier-offline and fespalier-cratestack), and since 0.17.0 how models, immutable collections, validation libraries and results meet it (freezed, dart_mappable, fast_immutable_collections, acanthis, result_dart). Load before writing or changing a data.dart or an action.dart, a loading or error view, a retry policy, or an app-level prefetch queue, or when a page flashes loading.dart, shows a stale value or does not refresh after a write."
---

# fespalier-data

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

`data.dart` is what a route loads. Beside a `page.dart` it feeds that page: the
page is **only built once the data has arrived**, `loading.dart` shows meanwhile
and `error.dart` if it fails. Everything is Riverpod 3 underneath
(`package:fespalier/fespalier.dart` re-exports `hooks_riverpod`).

## Pick a form

| You have                                        | Write                                                                                                   |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Nothing yet; the fetch belongs to this route    | `Future<Product> data(Ref ref, {required int id}) => fetchProduct(id);`                                 |
| A provider already (often riverpod_generator's) | `ProviderListenable<AsyncValue<Product>> data({required int id}) => productProvider(id);`               |
| A notifier, `keepAlive` or `retry:` of your own | `final data = AsyncNotifierProvider<MyNotifier, Product>(MyNotifier.new);` (type arguments spelled out) |

**Do not** wrap a provider you have in `ref.watch(p(id).future)` inside a
function-form `data()`: a second provider in front of the real one drops the
error the real provider holds while it retries, so `error.dart` cannot show during
the retry window. Use the selector. Details, errors and samples that compile:
[`references/data-forms.md`](references/data-forms.md).

## Keys

The route exposes its data as `XRoute.data`, **keyed by the segments and query
parameters `data.dart` uses**: no keys gives a plain provider, one key a
`.family<T, int>` (`ProductRoute.data(42)`), several a record
(`ItemRoute.data((shop: 'a', id: 1))`). A `List` query parameter is keyed by a
`QueryList` (value equality); a catch-all by its encoded path; an enum by the
enum. A provider **you** write can be keyed by segments only.

A parameter of `data()` that is neither a segment nor an optional nullable query
parameter is an error naming it; the types must agree with every other file that
asks for the same segment.

## Loading, errors and reloads

- `loading.dart` and `error.dart` are **inherited** by every folder below, nearest
  wins, and can ask for the route's segments and query parameters (`error.dart`
  also for `error`, `stackTrace`, `retry`). Without any: `DefaultLoading` and
  `DefaultError`.
- **`keep_previous: true` (default):** `loading.dart` is only for the **first**
  load; a reload keeps rendering the old value or error. `false`: loading shows on
  every load.
- **`data_retry: inherit` (default):** generated providers set **no retry of their
  own**, so Riverpod 3's automatic retry (10 attempts with backoff) or your
  `ProviderScope(retry:)` applies; during the retry window `error.dart` stays up.
  `none`: a failure is final until `error.dart`'s `retry` runs it again. A selector
  or a provider you write ignores `data_retry`.

`references/loading-error-retry.md` has the mechanics and the test behaviour.

## Sections

A folder with a `layout.dart` and **no** `page.dart` can have a `data.dart`: the
data of the whole section. The layout waits for it (nearest `loading.dart`
replaces layout **and** pages meanwhile), and the layout and pages below take it
**by type** or as a parameter called `data`. `data()` runs **once** however many
take it. A typed handle (`TeamsTeamIdSection.watch/read/prefetch/refresh/data`)
is generated for it. Two `data.dart` files yielding the same type for one
parameter are an error: name the parameter `data` (the nearest) or change a type.
See [`references/sections.md`](references/sections.md).

## Freshness and the cache (since 0.8.1)

Opt in, per `data.dart` or per folder; an app that declares neither generates what 0.7.0 did.

```dart
const freshness = Freshness(staleTime: Duration(minutes: 1), refetchOnResume: true); // data.dart or route.dart
final dataCache = DataCache<Product>.json(toJson: (p) => p.toJson(), fromJson: (j) => Product.fromJson(j! as Map<String, Object?>)); // data.dart only
```

| Rule                                                                     | What it means                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Where                                                                    | `freshness` in a `data.dart` (that data) or a `route.dart` (every function-form `data()` at and below; the nearest wins, a `data.dart`'s own wins over all). `dataCache` in a `data.dart` only                                                                              |
| Which forms                                                              | The function form (`Future<T>`, `FutureOr<T>` or `T`). A `Stream`, a selector and a provider form are errors; a `route.dart` default skips them silently                                                                                                                    |
| Stale                                                                    | In memory for `staleTime` **since it arrived**. Loading and error values are never stale. Nothing polls                                                                                                                                                                     |
| What loads a stale value                                                 | A **read**: a new listener (a page opening, `SectionView`, `prefetch`/`preload`, `read`), a listener coming back (page uncovered, tab shown), or a resume/reconnect signal                                                                                                  |
| What it shows meanwhile                                                  | The stale value **at once**, then the new one (`keep_previous` decides if `loading.dart` shows)                                                                                                                                                                             |
| `refetchOnResume` / `refetchOnReconnect`                                 | Signals (`appResumeSignal`, `reconnectSignal`); threshold `staleTime ?? Duration.zero`. `reconnectSignal` **never fires by itself**: override it or call `fire()` `fespalier_connectivity` (0.9.0) is that signal: `reconnectSignal.overrideWith(ConnectivitySignal.new)`   |
| A failed reload                                                          | Keeps the page on its data (`keepDataOnError: true` on the `DataView`); `error.dart` only when there is nothing to show, or when the error is a `DataRefusal` (since 0.13.1)                                                                                                |
| An invalidation (`ref.invalidate`, `refresh`, an action's `invalidates`) | Loads **at once**, whatever the `staleTime`: it is not a read                                                                                                                                                                                                               |
| `dataCache`                                                              | Saved only if the app overrides `dataCacheStorage` (`null` by default). `MemoryDataStorage` for tests and the web; a `Storage<String, String>` on disk to survive a restart: `fespalier_storage` (0.9.0), `PrefsDataStorage` or `HiveDataStorage`, first frame, size budget |

Gotchas: every new reader counts (a small `staleTime` reloads a section each time a page below it opens);
`read` returns what is in memory even if stale (`refresh` waits for the network); `keepFor` is how long a
handle holds a value, not freshness; a failed user `refresh()` is hidden behind the old page; a cold start
always loads again; a failed load never deletes the saved value; `freshness` and `dataCache` are names `fsp`
now reads in a `data.dart` (a public variable of that name and another type is an error: rename it).
[`references/freshness-and-cache.md`](references/freshness-and-cache.md) has the samples that compile, the
reconnect signal, the storage, the key format and the tests. [`references/reconnect-and-network.md`](references/reconnect-and-network.md) (since 0.9.0) is `fespalier_connectivity`: the
reconnect signal, `hasNetwork` and an offline banner, connectivity versus reachability, a reachability recipe, and tests with
`FakeConnectivity`. [`references/storage-backends.md`](references/storage-backends.md)
(since 0.9.0) is `fespalier_storage`: choosing Prefs or Hive, the budget and eviction, versioning, corrupt entries, sign-out, the web's
quota, and a restart test that compiles.

**A Rust core that says what changed (since 0.13.0).** `fespalier_frb`: `ChangeFeed(open)` holds the core's change stream in
**one** keep-alive subscription, `feed.topic<K>(matches)(key)` is a provider whose value moves only on a matching event, and a
`data.dart` that does `ref.watch(orderChanged(id))` is rebuilt exactly then: no listener, no timer, no `invalidate` in the code
that holds the stream. `InvalidationTable` is the pure form for an app that owns its subscription
(`table.apply(event, container.invalidate)`). It has **no `flutter_rust_bridge` dependency** (the bindings pin their own runtime):
do not add one. Starting the core is the app's, not an adapter's: `Future<void> startup() => initRustCore(RustLib.init);`, and
`ready(container)` for what must run on the container after it. Equal events are two changes (`Change.seq`), events fed together
are one rebuild, a debounce would be a timer. [`references/change-feeds.md`](references/change-feeds.md) has the samples that compile,
`startup()` versus `ready()`, the tests with `FakeChangeSource`, and (since 0.18.0) `ChangeCodec`: a core that sends raw messages (JSON or bytes, one event or a batch each) is decoded in `open` with `raw.transform(codec)`, and a message or item that does not decode, or whose decoder throws `UnknownChange`, is skipped, counted and never numbered while the feed goes on.

**State that belongs to one page on a navigator (since 0.13.0).** A `data.dart` is keyed by the location, so `/c/1` is one
provider however often it is shown. `fespalier_riverpod` keys a provider by the **page instance** instead: `PageInstance<R>`
is core's `pageInstanceId` (the same string as `RouteScope.id`) plus the typed route, equal **by id only**, so `/c/1` pushed
twice is two states while `/c/1?q=2` and a `remount` are one. `pageProvider` / `pageNotifierProvider` are auto-dispose
families keyed by it, `PageInstance.of(context, ChatRoute.of)` (or `usePageInstance(ChatRoute.of)`) is the page's key,
`PageInstance.ofScope(scope, route)` the same key from an `observe.dart`, and `holdForPage(scope, provider)` (`scope.hold`
by another name) keeps state the page reads but does not watch, or that must outlive its widgets, until the page leaves (a
parked tab that watches keeps its state anyway; `onEnter` fires when the page first becomes top). The family keeps
the route it was first made with: what follows the query is `data.dart`'s. Nothing here survives a restart.
[`references/page-providers.md`](references/page-providers.md) has the samples that compile and the tests.

## Typed helpers, prefetch, lookup

```dart
ProductRoute.watch(ref, id: 42);             // static: AsyncValue<Product>, in build()
await ProductRoute.read(ref, id: 42);        // static: Future<Product>, in callbacks
final warm = ProductRoute(id: 42).prefetch(ref);   // PrefetchHandle: kept until close()
final all = ProductRoute(id: 42).preload(ref);     // 0.5.0: the page's whole data, sections included
final byUri = AppRoutes.preload(ref, Uri.parse('/products/42'));   // 0.5.0: the same from a location
await ProductRoute(id: 42).refresh(ref);
AppRoutes.dataAt(Uri.parse('/products/42')); // [ProductRoute.data(42)]; null if no route fits
AppRoutes.match(Uri.parse('/products/42'));  // RouteMatch: info, parsed params, typed route, data
```

- **`prefetch` holds until you `close()` the handle** (0.3.0 changed this from a
  30 s lapse; `prefetchKeepAlive` is gone). `keepFor:` auto-closes; `Duration.zero`
  keeps nothing; a failed load closes its own handle.
- **`preload` (0.5.0) is `prefetch` for everything the page reads**: the data of each
  section above it, then its own, behind one handle, never navigating and never
  running a guard. `RouteLink(preload: ...)` calls it for you
  ([`fespalier-routing`](../fespalier-routing/), its links page); a link whose
  page still shows `loading.dart` after a hover usually has `Preload.none` (the
  default) or a `uri:` without `RouteLinkScope(match: AppRoutes.matchUrl)`.
- **`dataAt` is outermost first** (sections, then the route) and is `null` for an
  unknown location **or an unparsable segment**; no guard runs and no widget is
  built.
- `watch`/`read` are static because an instance member would have to name your
  data type in the generated file. Do not call `read` from `build`.

[`references/prefetch-and-lookup.md`](references/prefetch-and-lookup.md) covers
these, `prefetchAll`, `RouteMatch` (fespalier hides go_router's own
`RouteMatch`) and Riverpod overrides.

## Writes: `action.dart` (since 0.5.0)

`action.dart` is the write side of a route: `Future<Refund> action(Ref ref, {required
int id, required RefundInput input})`, beside the `page.dart` (or, in a page-less
folder, beside the `layout.dart` of a section). Segments and query parameters bind as in
`data.dart`; the one other parameter is a **named, required `input`**, of any type.

```dart
final refund = RefundRoute.useAction(ref, id: id);   // build(): state, isPending, hasError, call(input)
await RefundRoute.submit(ref, id: 1, input: input);  // a callback or a test: the result, or it throws
```

- **State is a generated Notifier family** (`RefundRoute.action(1)`): `AsyncValue<T?>`,
  `AsyncData(null)` when idle. It works without a widget, in a `ProviderContainer`.
- **A failed write shows in `state`, not `error.dart`, and is never retried.** The handle's
  `call` never throws; `submit` does.
- **After a success** the route's own `data.dart` and the sections' above it are
  invalidated, or what `const invalidates = [OrderRoute, ...]` lists (typed route and
  section names, not providers; it replaces the default set; `<Object>[]` for none). The
  action has to take the keys of what it invalidates.
- **Any number of actions per file**, each a public function with a `Ref` first; a
  function not called `action` names its helpers after itself (`approve`,
  `useApprove`). A sync action stays sync.
- **Navigation after success is the caller's**; check `context.mounted` after the `await`.

[`references/actions.md`](references/actions.md) has the rules, the generated members,
what is invalidated and a test that compiles.

## Forms and optimistic updates (since 0.8.1; forms are `fespalier_forms` since 0.11.0)

Not a file kind: `form()`, `validate()` and `optimistic()` are _companion functions_ in the
`action.dart` of their action (`approveForm`, `approveValidate`, `approveOptimistic` beside
`approve`), and never actions themselves. **`form()` needs the `fespalier_forms` package** (since
0.11.0): list it under `dependencies:` at the same git `url` and `ref` as `fespalier`, or `fsp`
reports an error at the `form()`; the generated file imports it only in an app with a form.
`FieldErrors`, `validate()` and `optimistic()` stay in `fespalier`.

```dart
typedef NicknameFields = ({String nickname, bool newsletter});   // the input: a record, named fields
NicknameFields form(Profile profile) => (nickname: profile.nickname, newsletter: profile.newsletter);
FieldErrors? validate(NicknameFields input) => FieldErrors({if (input.nickname.isEmpty) 'nickname': 'Enter a nickname'});
Profile optimistic(Profile current, NicknameFields input) => Profile(input.nickname, input.newsletter);
// page (a HookConsumerWidget): final form = NicknameRoute.useForm(ref, data: profile);
```

- **The input is a record with named fields**, inline or a `typedef` in the **same** `action.dart`.
  `useForm` gives `form.fields.nickname.controller` / `.value` / `.error`, `onSubmit` (**null while
  the action runs**), `isPending`, `isDirty`, `error`, `reset()`. It is a **real hook**: only in a
  `HookConsumerWidget`. `data:` is the data the page got.
- **`validate()` runs in the form and in the action's provider**, before the action: a refused
  input never starts the write. The action throws `FieldErrors({'field': 'message'})` for what
  only the server knows; keys are the record's field names.
- **`optimistic()` patches the `data.dart` the action invalidates whose type is `T`**: shown from
  the start of the write, removed on failure, kept over the old value after a success until the
  data has loaded again (no frame of the old value, `keep_previous: false` too). `XRoute.data`,
  `read` and `refresh` stay the server's value.
- Fields the user has not changed follow new data; changed ones keep what was typed.
- **Drafts (since 0.11.0), opt-in**: `useForm(ref, data: p, draft: const FormDraft(exclude: {'password'}))`
  keeps what changed per route (written when the page is disposed and when the app goes to the
  background, restored when the form starts, deleted by a success or `reset()`) in
  `formDraftStorage` (your `dataCacheStorage` by default), scoped by `formDraftScope`; `clearFormDrafts`
  at sign-out.
- **Leaving with unsaved changes (since 0.11.0)**: a `leave.dart` that is `leaveIfClean(context, ref, page)`
  asks when a form has changed, in a bottom sheet: "Keep editing", "Discard" and, for a form with a
  `draft:`, "Keep as draft". The form registers itself as the page's `LeaveSource`; `leavePrompt` is the
  app's question (override it on material_ui); `LeavePrompts.answer(choice)` is the test's.

- **Multi-page forms (since 0.11.0)**: a section whose `action.dart` has `const steps` (step folder to the fields it
  asks for) is one form over several pages with one draft: `SignupSection.useFlow(ref)` in the layout (inside a
  `FormFlowScope`), `flowOf(context)` in a step, `flow.next(context)` checking that step's fields only, `back`, `goTo`,
  `progress`, server errors sent to the step that owns the field, a `guard.dart` calling `resume(ref, uri:)`, and one
  `leave.dart` beside the layout asked once when the flow is left.

[`references/forms.md`](references/forms.md) (the package, `form()` and `useForm`, fields, submit and
errors, drafts, a sample that compiles with its test),
[`references/flows.md`](references/flows.md) (multi-page forms) and
[`references/optimistic.md`](references/optimistic.md) (`validate()`, `FieldErrors` and `optimistic()`)
have every rule.

## HTTP clients: `fespalier_http` and `fespalier_dio` (since 0.9.0, split in 0.15.0)

The core has no HTTP client. `package:fespalier_dio` (Dio) and, **since 0.15.0**, `package:fespalier_http`
(`package:http`; on 0.14.0 and earlier it was `package:fespalier_dio/http.dart`, **removed in 0.15.0, not
deprecated**: change the import to `package:fespalier_http/fespalier_http.dart`), repository dependencies next to
fespalier with **the same `url` and `ref`**, make the two clients keep three promises. They change no generated code,
file kind, key or command, and start no timer.

```dart
final cancel = ref.cancelToken();                       // Dio, in a data.dart: before the first await
final client = ref.abortable(ref.watch(httpClient));    // package:http: every request of the build
await ref.read(dio).put<Object?>('/me', data: body).withFieldErrors();   // in an action.dart
WriteGuard.install(dio);                                // the last call on the Dio: it goes first
```

- **A load whose page is gone stops.** `ref.cancelToken()`, `ref.abortTrigger()` and `ref.abortable(client)` fire in
  `ref.onDispose`: on dispose **and** before a rebuild. **Ask before the first `await`**: on a stale `ref` the token
  comes back already cancelled. The request fails after its provider is gone (`DioException` of type `cancel`, whose
  `error` is `fespalier_dio: the provider that started this request was disposed`; `RequestAbortedException` for
  `package:http`), so telemetry shows `disposed`, never an error.
- **A server's validation error is the form's `FieldErrors`.** `.withFieldErrors()` is an extension on the action's
  `Future`, **not an interceptor** (an interceptor can only reject with a `DioException`, and a form reads a
  `FieldErrors`). For 400 and 422 it reads RFC 9457 and 7807, ASP.NET Core, Laravel and Rails, Spring, JSON:API,
  FastAPI and Django REST framework, with the **first** message per field. `fieldName:` maps the server's names to the
  record's (`FieldNames.camelCase` changes case only: `nick_name` is `nickName`, not `nickname`). A **422** with only a
  `detail` or `message` is `form.error`; a 400 like that is never converted (it is a bug, let it reach Sentry).
  Anything else rethrows the same error.
- **A write is never sent twice.** `dio_smart_retry` and `RetryClient` retry writes by default. `WriteGuard.install(dio)`
  puts a guard **first** that refuses a second send of a write (any method but `GET`, `HEAD`, `OPTIONS`, `TRACE`, unless
  it has an `Idempotency-Key` header or `extra[WriteGuard.idempotent]`) and returns the first error, except after a 401
  (an auth refresh); `HttpWrites.isWrite` is that one rule for both clients (since 0.15.0). `WriteGuard.readsOnly(evaluator)` keeps the retrier from trying. For `package:http`, put
  `WriteGuardClient(inner)` inside the `RetryClient` and pass it `when: WriteGuardClient.readsOnly()` and
  `whenError: WriteGuardClient.readErrorsOnly(rule)`. A retrier **before** the guard gives `WriteNotRetried`.
- **Keep one retry layer**: Riverpod's data retry and an HTTP retrier multiply each other's attempts.
- **The layers, outside in (since 0.15.0, proved by a test):** `ref.abortable(...)`, then
  `SessionClient(authorizer, inner: RetryClient(WriteGuardClient(client), ...))`. A retrier _outside_ the session
  sends the session a streamed copy that it will not send again after a 401, so use it only for DPoP. Any
  `http.Client` fits the seam, `DioHttpClient(dio)` (`package:fespalier_dio/client.dart`) included; `HttpCredentials`
  (`Authorizer` implements it) is the session for a transfer that is not an `http.Client`. Do not claim
  `cupertino_http` honours an abort: it is unchecked.
- **Not in it:** a retry policy of its own (a backoff needs a timer), logging, tracing (use `otel_dio` or `sentry_dio`).

[`references/http.md`](references/http.md) has the samples that compile and every rule; its tests are in
[`fespalier-testing`](../fespalier-testing/SKILL.md) (its `http.md`), its messages in
[`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its `diagnostics-errors-and-http.md`).

## Offline-first and CrateStack (since 0.10.0)

`package:fespalier_cratestack` (a repository dependency next to fespalier, **same `url` and `ref`**) adds a second way to
make a read survive without a network, and a queue for writes. It changes no generated code, file kind, key or
command. It is two skills of its own: [`fespalier-offline`](../fespalier-offline/SKILL.md) (the ideas and the API) and
[`fespalier-cratestack`](../fespalier-cratestack/SKILL.md) (wiring a CrateStack client).

- **`dataCache` or `ref.serve`, never both.** `dataCache` (since 0.8.1) saves **a route's value** under its key and shows
  it while the network is slow or away; `ref.serve(key:, codec:, fetch:)` saves **an account's answer** and returns a
  `Served<T>` that says where the value came from (`network` or `local`) and when (`fetchedAt`), so the page can write
  "offline copy, as of 10:42". `serve` keeps its own copy, per account, in a `LocalStore` or a `ReadCache`: do not put
  `dataCache` over it. `freshness` still decides **when** a read runs again; `serve` decides **where** the answer comes
  from.
- **The page type is `Served<T>`**, spelled exactly as `data()` returns it (`FutureOr<Served<List<Order>>>` is matched as
  `Served<List<Order>>`): `fsp` matches by type, syntactically.
- **Only a connection failure falls back to the device**; a refusal goes to `error.dart` like any error. A single row with
  nothing saved is `CrateStackNoLocalData`; a list says `neverFetched`.
- **A write that is the server's decision is an intent** (`ref.read(intentQueue).submit(...)` in an `action.dart`): it
  returns `Accepted` or `Queued`, never a success the server has not given.

## Models, collections, validation and results (since 0.17.0)

fespalier depends on **none** of freezed, dart_mappable, fast_immutable_collections, acanthis, luthor,
result_dart or fpdart, and `fsp` does not read them: they meet it in the value `data()` returns (Riverpod 3 filters
updates by `==`), an `extra` (freezed's factory syntax is a private `_Note`: `ExtraCodec.of`), `DataCache.json`
(dart_mappable's `toJson()` is a String: pass `toMap`), an action's record `input`, `validate()` and the failures
`data()` and `action()` throw.

- **Pick by Dart:** freezed 4.0.2 needs Dart 3.13 (Flutter 3.47), freezed 3.2.5 covers Dart 3.8 and up, dart_mappable
  4.10 needs 3.7; acanthis 2 needs Dart 3.13 (1.x, a different API, below it).
- **A selected `List` field notifies on every reload**, equal or not; an `IList` from fast_immutable_collections 12
  does not (measured, with a test that builds).
- **`validate()` stays a plain function**; a schema library is an adapter inside it. **Unwrap a result in `data()`**
  (`getOrThrow()`, or fpdart's `getOrElse((l) => throw l)`), so `error.dart` can switch on the sealed failure.
- A model class is not a form's `input` (a record is), and `build_runner` can delete `lib/app.g.dart`
  (`fespalier-troubleshooting`, its flutter-pitfalls page).

[`references/models-and-libraries.md`](references/models-and-libraries.md) has the samples that compile, the
primary-constructor note and what is not built.

## Seeing it in DevTools (since 0.7.0)

The `fespalier` tab's **Data** tab lists each provider fespalier makes from a `data.dart`: its state
(`loading`, `data`, `error`, `stream`, `disposed`), builds, listeners, key and value, with an **Invalidate**
button and, since 0.8.1, a **Holders** button that lists who keeps the provider (the page, a section, a
`prefetch` / `preload` handle, a `RouteLink` preload) and counts the other listeners. **Actions** lists the
runs of the `action.dart` functions. The generated provider body is wrapped in `traceData`, which returns the
function's own result (a value stays a value, a `Future` stays the `Future`), and every view watches with
`watchData(ref, 'dProductsId', provider)`, which is `ref.watch`. A `data.dart` that returns or selects a provider is
followed since 0.8.1 as an `app provider`, through the state the views got; its other listeners are not
visible (`fespalier-troubleshooting`, its DevTools page).

## Examples

Read these before inventing a pattern; each compiles and has widget tests
(the `fespalier` skill lists them all).

- `examples/features`: a `data.dart` keyed by a segment (`catalog/$productId`), a `teams/$teamId` section with its `data.dart`
  and `action.dart` (an optimistic `addMember`), forms on `action.dart`, a `Stream` in `ticks/data.dart`, and the cache and
  reconnect pair (`test/offline_test.dart`, `test/freshness_test.dart`).
- `examples/shop`: `products/$id/data.dart` with `error.dart` and Retry, and `test/refresh_test.dart`.
- `examples/auth`: two `data.dart` files (`orders/` and `orders/$id/`) that share one token refresh.

## Common symptoms

| Symptom                                                        | Look at                                                                                                                                                                         |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Page blinks to `loading.dart` on every reload                  | `keep_previous: false` in `pubspec.yaml` (the default is `true`)                                                                                                                |
| A failing `data.dart` runs several times in a test             | Default `data_retry: inherit`; `pumpRouter` already disables retries (`fespalier-testing`)                                                                                      |
| `error.dart` never shows during a retry                        | A function-form `data()` wrapping `.future` of your provider: use a selector                                                                                                    |
| `refresh`/`retry` throws a `StateError`                        | A selector that returns `.select(...)` of a provider: return the provider itself                                                                                                |
| A prefetched page still loads                                  | The handle was closed, or the id/query differs from the key the page uses                                                                                                       |
| `dataAt` is `null` for a URL that works in the app             | The segment fails to parse, or the URL is outside the mount prefix                                                                                                              |
| A page doesn't refresh after a write                           | The data is another route's: list it in `invalidates` (`references/actions.md`)                                                                                                 |
| A stale value stays on screen                                  | Nothing read it: `freshness` loads on a read, a resume or a reconnect, never by a timer (`references/freshness-and-cache.md`)                                                   |
| Offline start shows `error.dart`                               | No `dataCache`/`dataCacheStorage`, or nothing was saved yet or it passed `maxAge`                                                                                               |
| A saved value is not on the first frame (0.9.0)                | `open()` was not awaited in `startup()`, a `Future` was passed (one `loading.dart` frame), or in a test no `fakePrefsStore()`                                                   |
| `refetchOnReconnect` never reloads (0.9.0)                     | `startup()` does not override `reconnectSignal` (`ConnectivitySignal.new`), or the value is younger than its `staleTime`, or the network went Wi-Fi to mobile (not a reconnect) |
| An offline banner stays up after the network came back (0.9.0) | A hand-written signal that never asks again on a resume (iOS drops background events): use `fespalier_connectivity`                                                             |
| The form forgot what I typed (0.8.1)                           | The data loaded again while the fields were untouched: only fields the user changed are kept                                                                                    |
| The page flashes the old value after a save                    | `optimistic()` patches another type than the page shows, or the data is not in `invalidates`                                                                                    |
| A request outlives its page (0.9.0)                            | `fespalier_dio` or `fespalier_http`: the token was asked after an `await`, or not given to the request (`references/http.md`)                                                   |
| A 422 is not under its field (0.9.0)                           | `fespalier_dio` or `fespalier_http`: `withFieldErrors()` is missing or found no field: statuses, decoder, names (`references/http.md`)                                          |
| A write is retried, or `WriteNotRetried` (0.9.0)               | `WriteGuard` is not first (`WriteGuard.install(dio)` last), or the retrier has no `readsOnly` (`references/http.md`)                                                            |
| Another account's data shows offline (0.10.0)                  | Impossible by design: every `serve` answer, intent and row is keyed by `crateStackScope`. A copy that did show means the scope is not the signed-in user (`fespalier-offline`)  |
| A queued write never sends (0.10.0)                            | `fespalier_cratestack`: nothing watches `autoSync`, no trigger runs, or the intent is another account's (`fespalier-troubleshooting`, its `diagnostics-cratestack.md`)          |
| A CrateStack read is cancelled with another page (0.10.0)      | A provider is built inside `ref.cancellable(...)`: read and watch others before it, and keep the body to the client call (`fespalier-cratestack`)                               |
| An fsp error on `data.dart` or `action.dart`                   | `fespalier-troubleshooting`                                                                                                                                                     |
