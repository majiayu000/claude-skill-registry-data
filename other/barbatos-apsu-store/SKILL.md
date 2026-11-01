---
name: barbatos-apsu-store
description: "Shared state with Barbatos.Wpf.Apsu (in Barbatos.Wpf.Core), Pinia-style stores - StoreBase, StateChanged/Patch/Reset, Getter<T>, [Action] methods wrapped by IStoreActionInterceptor, AddStore, InterceptorHandle.Eject, IStorePlugin, IStoreRegistry. Use when state is shared by several ViewModels or windows, deriving a value from stores, logging, auditing or blocking an action without editing it, persisting a store, or when an [Action] is never intercepted, an action hangs forever, a sealed store throws on resolve, or a getter shows a stale value. For view-local state and Provide/Inject use barbatos-aquarius-view. Vietnamese prompts too - trạng thái dùng chung, chia sẻ state giữa màn hình, store kiểu Pinia, giá trị tính từ store, ghi log hành động, hành động bị treo, lưu trạng thái store."
---

# Barbatos.Wpf.Apsu - stores

Pinia's `defineStore`/getters/actions/plugins, ported to WPF and shipped inside
`Barbatos.Wpf.Core` (namespace `Barbatos.Wpf.Apsu`). A store is an app-lifetime DI singleton
deriving from `StoreBase` (a CommunityToolkit `ObservableObject`). Action interception is
ASP.NET Core-style middleware over a Castle DynamicProxy class proxy. Not here: view-local state,
`Ref`/`Computed`, Provide/Inject (`barbatos-aquarius-view`); persistence primitives such as
`IPreferences` (`barbatos-wpf-essentials`). Nothing in Apsu persists itself.

## Sources of truth

- Docs: README [State management](../../../src/Barbatos.Wpf.Core/README.md#state-management-barbatoswpfapsu)
  ([Stores](../../../src/Barbatos.Wpf.Core/README.md#stores),
  [Getters](../../../src/Barbatos.Wpf.Core/README.md#getters),
  [Actions and action interceptors](../../../src/Barbatos.Wpf.Core/README.md#actions-and-action-interceptors),
  [Removing an interceptor](../../../src/Barbatos.Wpf.Core/README.md#removing-an-interceptor-at-runtime),
  [Plugins](../../../src/Barbatos.Wpf.Core/README.md#plugins),
  [Registry](../../../src/Barbatos.Wpf.Core/README.md#registry)) and
  [API-REFERENCE `Barbatos.Wpf.Apsu`](../../../src/Barbatos.Wpf.Core/API-REFERENCE.md#barbatoswpfapsu-namespace).
- Code wins over docs: `src/Barbatos.Wpf.Core/Essentials/Apsu/` - `StoreServiceCollectionExtensions.cs`
  (registration, proxy vs plain path, plugin/registry order), `ActionInterceptor.cs` (pipeline,
  return-type handling), `StoreBase.cs`, `Getter.cs`, `IStoreActionInterceptor.cs` (awaiting,
  retrying, the sync-action deadlock).
- Samples: `samples/Barbatos.Wpf.Core.Sample/` - `CounterStore.cs`,
  `SampleActionLoggingInterceptor.cs`, `WpfProgram.cs`, `MainViewModel.cs` (forwarding a getter).
  `samples/Barbatos.Wpf.Aquarius.Sample/` - `UserStore.cs`/`OrderStore.cs` (cross-store),
  `WpfProgram.cs` (3 global + 3 local chain), the six `*Interceptor.cs`,
  `UserSessionPersistencePlugin.cs`, `ApsuActivityLog.cs`, `ApsuInteropDemoViewModel.cs`.
- Tests that pin behaviour: `tests/Barbatos.Wpf.Core.UnitTests/StoreBaseTests.cs` (StateChanged,
  Patch, Reset, Getter), `StoreFeatureTests.cs` (singleton, laziness, registry, plugins),
  `StoreActionInterceptorTests.cs` (chain order, short-circuit, errors, async, awaiting before
  `next`, retry, `next` on another thread, eject, sealed).
- [patterns.md](patterns.md) - read when you need a complete worked example: cross-store store,
  argument/state/cooldown guards, error reporting, persistence plugin, exposing a getter to XAML,
  an ejectable toggle, or a test harness for an interceptor.

## A store

Adapted from `samples/Barbatos.Wpf.Core.Sample/CounterStore.cs`:

```csharp
public class CounterStore : StoreBase
{
    int _count;
    readonly Getter<string> _doubleCountLabel;

    public CounterStore()
    {
        _doubleCountLabel = new Getter<string>(() => $"Double: {Count * 2}", this);
    }

    public int Count
    {
        get => _count;
        private set => SetProperty(ref _count, value);
    }

    public string DoubleCountLabel => _doubleCountLabel.Value;

    [Action]
    public virtual void Increment() => Count++;

    public override void Reset() => Count = 0;
}
```

```csharp
builder.Services.AddStore<CounterStore>();
```

Shape rules - each one fails differently, some only after the first interceptor is registered:

| Rule | What breaks otherwise |
| --- | --- |
| Not `sealed` | `InvalidOperationException` ("must not be sealed ...") at first resolution once any interceptor applies. A **global** interceptor applies to every store, so adding one can break a store that worked before. |
| Exactly one public constructor, every parameter a registered service | The proxy path resolves each parameter with `GetRequiredService`, so >1 public constructor throws `InvalidOperationException` ("must have exactly one public constructor ... (found N)") and optional/default parameters are not honoured. The plain path uses `ActivatorUtilities.CreateInstance`, which is more lenient - again, the break appears with the first interceptor. |
| `public` type (and any enclosing type) | Castle cannot subclass a type its generated assembly cannot see. Every intercepted store in the tests and samples is `public`. |
| Actions are `public virtual` and `[Action]`-marked | Non-virtual or unmarked methods silently pass through (`NonAttributedVirtualMethodIsNotIntercepted`). |
| Actions return `void`, a value, `Task` or `Task<T>` | See [Return types](#return-types-and-blocking). |
| `Reset()` overridden | The default throws `NotSupportedException` "... does not support Reset()". Deliberate: a forgotten override fails loudly. |
| State set via `SetProperty`, setters `private` | Public setters and `Patch` bypass interceptors; mutate through actions when audits/guards must see every change (`UserStore`/`OrderStore` use `private set`). |

## Registering

- `AddStore<TStore>(Action<StoreInterceptorBuilder<TStore>>? configureInterceptors = null)`
  registers a **singleton factory**, run lazily on first resolution
  (`StoreIsNotConstructedUntilFirstResolved`). The store is resolvable as `TStore` only.
- Always register with `AddStore`. `AddSingleton<TStore>()` or `new TStore()` in app code
  skips the proxy, the plugins and the registry.
- Call `AddStore<TStore>` once per type. It uses `AddSingleton`, not `TryAdd`: a second call adds
  a second descriptor, and a repeated callback registers its local interceptors again (they then
  run twice).
- A store's constructor may take services and other stores (`OrderStore(HttpClient, UserStore)`).
  It lives for the app's lifetime, so depend on singletons only.
- Interceptors and plugins are read when the store is **first resolved**, not when `AddStore`
  runs, so registering them before or after `AddStore` makes no difference; only their order
  among themselves matters. After that the chain is frozen - `Eject` is the only runtime change.
- No interceptor applies -> plain instance, `GetType() == typeof(TStore)`
  (`StoreWithoutInterceptorsRegisteredUsesThePlainNonProxiedPath`). Otherwise the instance is a
  generated subclass: test with `is OrderStore`, never `GetType() ==`.

## State, StateChanged, Patch, Reset

- `StateChanged` (the `$subscribe` counterpart) fires on **every** `PropertyChanged` the store
  raises - `StoreBase` subscribes to its own `PropertyChanged` in its constructor. That includes a
  manual `OnPropertyChanged(nameof(Derived))`. Setting an equal value raises nothing.
- Never raise the store's own `PropertyChanged` from its own `StateChanged` handler: each raise
  fires `StateChanged` again, recursing until the stack overflows.
- `Patch(Action<StoreBase> mutate)` batches: `PropertyChanged` still fires per property, but
  `StateChanged` fires once when the outermost `Patch` returns, and only if something changed.
  The callback parameter is typed `StoreBase` - ignore it and close over the typed store:
  `store.Patch(_ => { store.Count = 1; store.Name = "a"; })` (`StoreBaseTests`), or inside the
  store `Patch(_ => { A = 1; B = 2; })`.
- `Patch` is not a transaction: if `mutate` throws, changes already made stay, `StateChanged`
  still fires (from `finally`), then the exception propagates. Batching is per store - another
  store mutated inside the callback notifies on its own.
- `Patch` and `Reset` are not actions, so interceptors never see them. Call them from an
  `[Action]` when they must be audited or guarded.
- Wrap a multi-property `Reset` in `Patch`, as `UserStore.Reset` does: without it
  `StateChanged` fires once per property, and a plugin that persists on `StateChanged`
  (`UserSessionPersistencePlugin`) writes once per property too.

## Getters

- `new Getter<T>(Func<T> compute, params StoreBase[] dependencies)`. List **every** store
  `compute` reads, `this` included - there is no auto-tracking. Invalidation is deliberately
  coarse (a simplification, not a gap to close): any `StateChanged` on any dependency invalidates
  (`GetterInvalidatesEvenWhenAnUnrelatedPropertyChanges`); `Value` recomputes on the next read only.
- **A getter raises no change notification.** `{Binding OrderStore.Summary}` reads once and never
  updates. Expose the value through a ViewModel that re-raises it on `StateChanged` of every
  dependency store, as `ApsuInteropDemoViewModel.OrderSummary` does - see
  [patterns.md](patterns.md#exposing-a-getter-to-xaml).
- Forward on `StateChanged`, not `PropertyChanged`. Outside a `Patch`, `StoreBase`'s own handler
  runs first, so the getter is already invalidated when other `PropertyChanged` subscribers run.
  Inside a `Patch`, `PropertyChanged`
  arrives **before** the getter is invalidated, so a forwarded read returns the stale value and
  nothing re-notifies afterwards. The same applies to reading a getter inside the `Patch` callback.
- Create `Getter<T>` only inside stores. It subscribes to each dependency's `StateChanged` and has
  no `Dispose`, so a getter built in a short-lived ViewModel over a singleton store is kept alive
  by that store forever, with everything its closure captures. In ViewModels use Aquarius
  `Computed<T>.From(getter, params INotifyPropertyChanged[] dependencies)` (stores are
  `INotifyPropertyChanged`; `Computed<T>` is `IDisposable`) and read raw store state in it, not a
  store getter (same `Patch` staleness).

## Actions and interceptors

`IStoreActionInterceptor.InterceptAsync(StoreActionContext context, StoreActionDelegate next)`
returns `Task<object?>`. `context` carries `Store`, `ActionName` and `Arguments` (declaration
order). From `samples/Barbatos.Wpf.Aquarius.Sample/ApsuActionLoggingInterceptor.cs` (log prefix
shortened):

```csharp
public async Task<object?> InterceptAsync(StoreActionContext context, StoreActionDelegate next)
{
    // context.Store is the generated proxy subclass; BaseType is the store's own type.
    var label = $"{context.Store.GetType().BaseType!.Name}.{context.ActionName}()";
    _activityLog.Log($"[Interceptor] {label} starting");
    var stopwatch = Stopwatch.StartNew();
    try
    {
        var result = await next();
        _activityLog.Log($"[Interceptor] {label} finished in {stopwatch.Elapsed.TotalMilliseconds:0}ms");
        return result;
    }
    catch (Exception ex)
    {
        _activityLog.Log($"[Interceptor] {label} failed: {ex.Message}");
        throw;
    }
}
```

An interceptor only runs on a proxied store, so `context.Store.GetType().Name` is always the
generated type's name (`OrderStoreProxy`-style); `GetType().BaseType!.Name` is the store's own.

- **Short-circuit** by returning without calling `next` - the action body never runs. Return
  `Task.FromResult<object?>(null)` for `void`/`Task` actions; for value-returning actions return
  a boxed value of the declared type (`ShortCircuitMiddleware` returns `-1` for `int GetDoubled()`).
  The chain's result is cast back to the declared type, so `null` for a `Task<int>` action throws.
- Outer interceptors still run their after-code when an inner one short-circuits - from their
  side `next()` just returned (`AnyInterceptorBlockingInASixDeepChainPreventsTheActionAndEverythingAfterIt`).
- A local interceptor wraps **every** action of its store. Filter with
  `context.ActionName == nameof(OrderStore.CheckoutAsync)` and `return next();` for the rest.
- Read state from `context.Store` (`context.Store is OrderStore { OrderCount: 0 }`) instead of
  injecting the store the interceptor wraps.
- Errors: a synchronous action throws out of `next()` synchronously; an async one faults its
  task. An `async` interceptor with `await next()` inside `try`/`catch` sees both. `throw;`
  propagates the original exception type (not `AggregateException`); returning a value from the
  `catch` substitutes a fallback (`MiddlewareCanCatchAnErrorAndReturnAFallbackInstead`).
- The store instance is the proxy, so an action calling another action on `this`, a cross-store
  call (`OrderStore.CheckoutAsync` -> `UserStore.RefreshProfileAsync`) and a plugin calling an
  action each run the full chain again. Expect nested log lines; guards see inner calls too.

### Awaiting before `next`, and retrying

`ActionInterceptor` proceeds Castle's `IInvocation` only while the intercepted call is still
running on its own thread. Any later `next` - after an `await`, a retry, a call from another
thread - calls the action through the proxy again, flagged so that second pass skips the chain;
it never touches the original invocation, which Castle may still be unwinding. So `next` reaches
the action from any continuation and any thread
(`NextCalledFromAContinuationAfterTheInterceptedCallReturnedReachesTheAction`,
`NextCalledFromAThreadPoolContinuationWhileTheCallIsStillReturningRunsTheActionOnce`,
`SynchronousActionGetsItsArgumentsAndOutParameterWhenNextRunsOnAnotherThread`).

- An async precondition (a server check) may be awaited **before** `next` for a `Task` action
  (`MiddlewareCanGenuinelyAwaitAsynchronousWorkBeforeCallingNext`); real work after `next` works
  too (`MiddlewareCanGenuinelyAwaitAsynchronousWorkAfterCallingNext`). Wrapping a sync action
  called on the UI thread, either one deadlocks it - see [Return types](#return-types-and-blocking).
- Retry by calling `next` again after a failed attempt, also when the async action failed after
  its own first real `await` (`MiddlewareCanRetryAnAsyncActionThatFailedAfterItsFirstAwait`,
  `RetryGivesUpAndPropagatesTheErrorOnceItsAttemptsAreSpent`,
  `MiddlewareCanRetryASynchronousActionByCallingNextAgain`). Each call re-runs the interceptors
  **after** this one in the chain (see [Registration and order](#registration-and-order)) and then
  the action body; interceptors outside it see one call.
  Await one attempt before starting the next - never call `next` concurrently.
- No `ConfigureAwait(false)` before `next`: the action body runs on whichever thread calls
  `next`, and would then mutate UI-bound store state from the thread pool.
- Packages built before this fix called `IInvocation.Proceed()` from the innermost `next`
  wherever it ran, which re-entered the whole chain from a continuation: an `await` before
  `next` hung forever with no exception (the test host had to be killed) and a retry re-ran the
  outer interceptors, nested. A hang there on an old package version is that bug.
  (`IInvocation.CaptureProceedInfo()` alone is not the fix: a thread-pool continuation can run
  while the call is still returning, and then calls run the chain twice or never complete.)

### Return types and blocking

| Action returns | Chain behaviour |
| --- | --- |
| `Task` / `Task<T>` | Awaited properly; the caller gets a task that completes after every interceptor finished (`AwaitingTheReturnedTaskGuaranteesTheMiddlewareAlreadyRanToCompletion`). |
| `void` / a value | The proxy blocks: `pipeline().GetAwaiter().GetResult()`. |
| `ValueTask`, `ValueTask<T>`, `async void` | Treated as synchronous (`next()` returns the unfinished `ValueTask` itself, boxed): after-code runs before the work finishes and misses exceptions from its async part. Use `Task`. |

- Because sync actions block, an interceptor that genuinely suspends **anywhere** in a sync
  action's chain - even after `next` - waits for a UI-thread continuation while the UI thread is
  blocked: the classic WPF sync-over-async deadlock. Global interceptors wrap sync actions too,
  so a global interceptor must await nothing but `next()` itself (which a sync action completes
  synchronously); hand async I/O (a remote log flush) off to something that runs on its own.
- After `await next()` the interceptor resumes on the caller's context (the pipeline deliberately
  omits `ConfigureAwait(false)`), so after-code may touch UI-bound state. Keep it that way in
  your interceptors.

### Registration and order

| Registration | Scope | Built |
| --- | --- | --- |
| `services.AddSingleton<IStoreActionInterceptor, T>()` | global | by DI |
| `services.AddSingleton<IStoreActionInterceptor>(sp => new T(...))` | global | factory |
| `services.AddStoreInterceptor(interceptor, out InterceptorHandle handle)` | global, ejectable | instance |
| `AddStore<TStore>(i => i.Add<T>().Add(instance).Add(sp => new T(...)))` | local | DI / instance / factory |
| `AddStoreInterceptor<TStore, TInterceptor>()`, `AddStoreInterceptor<TStore>(instance)`, `AddStoreInterceptor<TStore>(factory)` | local | standalone equivalents of the builder |
| `AddStoreInterceptor<TStore>(interceptor, out InterceptorHandle handle)` | local, ejectable | instance - the builder has no ejectable `Add` |

- Every global runs outside every local; each group runs in registration (`Add`) order,
  outermost first. Globals A, B, C plus locals D, E, F give `A B C D E F ... F E D C B A`
  (`SixChainedInterceptorsAllRunInOrderWhenEveryOneCallsNext`).
- Order locals by cost: a guard that rejects goes before an interceptor that spends a token on
  the call (`NonEmptyCartGuardInterceptor` before `CheckoutCooldownInterceptor` in the Aquarius
  `WpfProgram.cs`).
- Use a factory when the constructor needs a value the container cannot invent (a `TimeSpan`)
  next to services it can. Type and factory registrations are built once, at the store's first
  resolution (`AddStoreInterceptorFactoryIsInvokedLazilyOnlyOnceOnFirstStoreResolution`).
- Locals are keyed by exactly `typeof(TStore)`: one registered for a base store type does not
  apply to a derived store registered as itself.
- One global instance serves every store's chain, so its fields are shared state.
- Interceptors are registered only as `IStoreActionInterceptor` (keyed for locals); the concrete
  type is not resolvable. Surface their output through a shared injectable sink, as
  `ApsuActivityLog` does, rather than injecting interceptors into ViewModels.

### Ejecting

`handle.Eject()` (idempotent; `handle.IsEjected` reports it) turns that slot into a pass-through
for every call that reaches it from then on; the chain is not rebuilt. A call already inside the
interceptor finishes with it; one still in an outer interceptor skips it when it gets there.
Ejecting before the first call works; ejecting a short-circuiting interceptor lets later calls
reach the action. There is no re-attach, and a store's chain is fixed once the store exists, so
getting the behaviour back means a new container. For an on/off setting, give the interceptor
its own enabled flag instead; use `Eject` for a one-way removal. Keep the handle where the code
that ejects can reach it.

## Plugins and registry

- `IStorePlugin.Apply(StoreBase store)`, registered with `services.AddSingleton<IStorePlugin, T>()`,
  runs once per `AddStore` store, in registration order, after the constructor and after the
  proxy is built, inside that store's DI resolution. It runs for every store - start with
  `if (store is not UserStore userStore) return;`.
- A plugin can read/write state, subscribe to `StateChanged`, and call actions (through the
  chain). It cannot wrap actions - that is an interceptor's job.
- State a plugin restores is set while the store is still being resolved, before anything else
  can subscribe, so its change notifications reach nobody. Whatever reacts to restored state must
  read the current value when it subscribes (an "immediate" watch): in the Aquarius sample,
  `UserSessionPersistencePlugin` restores `SelectedUserId` before `OrderStore` exists, so
  `OrderStore`'s constructor checks `_userStore.SelectedUserId` right after wiring its watch and
  loads that user's orders (`LoadOrdersForRestoredUser`).
- `IStoreRegistry.Stores` is a snapshot of the stores resolved so far, in the order each finished
  resolving (after its plugins; a store's dependency stores come first); a registered but
  never-resolved store is absent. It is registered by the first `AddStore` call
  and exists for introspection only - the container is the cache.

## Store, ViewModel or Provide/Inject

| Need | Use |
| --- | --- |
| State shared by unrelated ViewModels/windows for the app's lifetime | an Apsu store |
| State owned by one screen | the ViewModel (`[ObservableProperty]`, Aquarius `Ref<T>`) |
| A value scoped to one visual subtree | Aquarius `Provide`/`Inject` (`barbatos-aquarius-view`) |
| Derivation across stores | `Getter<T>` in a store |
| View-shaped derivation of store state | `Computed<T>` in the ViewModel, disposed with it |

Cross-store wiring (`OrderStore.cs`): inject the other store; "watch" it with an ordinary
`PropertyChanged` subscription (store-to-store subscriptions are fine - both are singletons); or
call its action directly. An `async` lambda handler is `async void`: when the change is raised on
the UI thread its exceptions reach `OnDispatcherUnhandledException` (`barbatos-wpf-host`), never a
caller. A ViewModel that is not a
singleton must unsubscribe from store events when it goes away - the store outlives it.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Interceptor never runs for an action | Method not `virtual`, missing `[Action]`, store not registered via `AddStore`, local registered for another `TStore`, or handle ejected | Fix the shape/registration; check `IsEjected` |
| Intercepted action never completes, no exception | An interceptor returned a task that never completes (it awaits something that never finishes); on a package built before `next` could run after an `await`, an `await` before `next` | Find the interceptor's unfinished await; update the package |
| UI freezes when a sync action runs | An interceptor genuinely suspends inside a sync action's chain | Make the action return `Task`, or keep interceptors synchronous |
| `InvalidOperationException` "must not be sealed" right after adding a global interceptor | A `sealed` store now needs a proxy | Remove `sealed` |
| `InvalidOperationException` "must have exactly one public constructor ... (found N)" | Proxy path needs one constructor | Collapse to one |
| "No service for type ..." resolving a store that worked before interceptors | Proxy path ignores optional/default constructor parameters | Register the dependency or drop the parameter |
| Castle error that the store type is not accessible | Store or an enclosing type is not `public` | Make it `public` |
| `NotSupportedException` "... does not support Reset()" | `Reset()` not overridden (when proxied, the message names the generated type) | Override `Reset()` |
| Getter-backed property never updates in the UI | `Getter<T>` raises no `PropertyChanged` | Re-raise from a ViewModel on `StateChanged` |
| Getter shows the old value after a `Patch` | Forwarded on `PropertyChanged`, which precedes invalidation inside `Patch` | Forward on `StateChanged` |
| Getter stale after another store changed | That store is not in `dependencies` | List every store `compute` reads |
| `StackOverflowException` in a store | Store raises its own `PropertyChanged` from its `StateChanged` handler | Raise on the ViewModel instead |
| ViewModel never garbage-collected | `Getter<T>` built in it over a singleton store, or store events never unsubscribed | `Computed<T>` + `Dispose`; unsubscribe |
| Interceptor logs a call twice | Action called from another action / store / plugin (nested chain), or `AddStore` called twice | Expected for nesting; register once |
| Logging/timing ends before an async action finishes; interceptors never see its error | Action returns `ValueTask` or is `async void` | Return `Task` |
| Exception (e.g. `NullReferenceException`, `InvalidCastException`) after a short-circuit | Returned `null` or the wrong boxed type for a value-returning action | Return a boxed value of the declared type |
| Log shows a generated type name instead of the store's | `context.Store` is the proxy subclass | `GetType().BaseType!.Name` |
| `IStoreRegistry` cannot be resolved | No `AddStore` call registered it | Register at least one store |
| Restored state did not trigger another store's watch | Plugin ran during resolution, before the watcher subscribed | Read current state at subscribe time |

## Checklist

Adding a store: `public`, non-`sealed`, one public constructor over singletons; state via
`SetProperty` with `private set`; actions `public virtual`, `[Action]`, returning `Task` when async;
`Reset()` overridden (multi-property in `Patch`); getters list every store they read; one
`AddStore<TStore>` call with its local interceptors in the callback; getter-backed values reach
XAML through a ViewModel forwarding `StateChanged`.

Adding an interceptor: await nothing but `next()` if it may wrap a sync action (every global
does); no `ConfigureAwait(false)` before `next`; retries call `next` one attempt at a time;
filter by `nameof` action; short-circuit with a correctly typed value; `throw;` after observing;
guards before token-spending interceptors; a test in the style of
`StoreActionInterceptorTests.BuildStore`, with async steps gated by a `TaskCompletionSource`
the test completes rather than by delays.

Changing `src/Barbatos.Wpf.Core/Essentials/Apsu/` itself: follow `barbatos-package-authoring`
(stores stay the documented `sealed` exception; the pipeline's reflection is why the Core
`.csproj` suppresses IL2075/IL2060); extend the three test files; update README "State management" and the
API-REFERENCE namespace (`barbatos-docs-sync`); keep both samples demonstrating it. Run tests per
TFM: `dotnet test tests/Barbatos.Wpf.Core.UnitTests -f net10.0-windows10.0.17763.0 --filter "FullyQualifiedName~UnitTests.Store"`.

## Related skills

`barbatos-wpf-host` (builder, lifecycle hooks such as `OnDispatcherUnhandledException`),
`barbatos-wpf-essentials` (`IPreferences` for persistence plugins), `barbatos-aquarius-view`
(`Ref`/`Computed`/`Watch`, Provide/Inject), `barbatos-wpf-testing` (running and writing tests),
`barbatos-package-authoring` (changing the library), `barbatos-docs-sync` (README/API-REFERENCE).
