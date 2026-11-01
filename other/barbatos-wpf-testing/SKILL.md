---
name: barbatos-wpf-testing
description: "Writing and running the xUnit v3 suites under tests/ for Barbatos.Wpf - StaThread.Run vs TestApplication.Invoke, PumpDispatcher, GcProbe.AssertCollected/AssertAlive leak tests, ModuleInit warm-up, fake platforms, per-TFM dotnet test -f runs. Use before running or trusting a test result, when adding a test or test project, or when a test is flaky or passes alone but fails in a full run, the run aborts, a test hangs, 'The calling thread must be STA', 'The Application object is being shut down', NETSDK1005, an assertion misses a deferred update, or a memory leak (an object never garbage collected) needs a test. For changing library code use barbatos-package-authoring. Vietnamese prompts too - chạy test, viết unit test, test chạy riêng pass chạy chung fail, test bị treo, rò rỉ bộ nhớ, lỗi STA."
---

# Testing Barbatos.Wpf

Four xUnit.net v3 projects under `tests/`, one per package, on the VSTest runner
(`xunit.v3.mtp-off` + `xunit.runner.visualstudio` + `Microsoft.NET.Test.Sdk`). WPF objects need
an STA thread and some need a live `Application`, so each suite carries its own copies of a few
helpers - there is no shared test-support project. What a feature *should* do lives in its
feature skill; changing `src/` is `barbatos-package-authoring`.

## Sources of truth

- Helpers: [StaThread.cs](../../../tests/Barbatos.Wpf.AquariusValee.UnitTests/StaThread.cs),
  [TestApplication.cs](../../../tests/Barbatos.Wpf.AquariusRouter.UnitTests/TestApplication.cs),
  [GcProbe.cs](../../../tests/Barbatos.Wpf.Aquarius.UnitTests/GcProbe.cs),
  [AssemblyInfo.cs](../../../tests/Barbatos.Wpf.Aquarius.UnitTests/AssemblyInfo.cs) (why
  parallelism is off). The per-project copies differ - see [Adding a test project](#adding-a-test-project).
- Core: [ModuleInit.cs](../../../tests/Barbatos.Wpf.Core.UnitTests/ModuleInit.cs),
  [FeatureTestFakes.cs](../../../tests/Barbatos.Wpf.Core.UnitTests/FeatureTestFakes.cs) (the
  `Fake*` platform doubles), `TestServices.cs` (DI stubs), and the file-local `RunOnStaThread` in
  `DialogServiceTests.cs`, `InputSystemScopeTests.cs`, `SplashScreenTests.cs`.
- Tests that pin the patterns below: `LifecycleLeakTests.cs`, `RouterLeakTests.cs`,
  `RouterViewTests.cs` + `ValeeXamlTests.cs` (deferred failures), `RouterDialogWindowTests.cs`,
  `TransitionTests.cs`, `FormMetaStalenessTests.cs`, `AquariusDependencyInjectionTests.cs`,
  `RunOnStartupFeatureTests.cs`, `PreferencesTests.cs`, `VersionTrackingTests.cs`.
- Build: the four `tests/*/*.UnitTests.csproj`,
  [Directory.Build.props](../../../Directory.Build.props) (derives `IsTestProject` from the
  project name), [Directory.Packages.props](../../../Directory.Packages.props).
- [patterns.md](patterns.md) - read when writing a test: copy-ready code, trimmed from the suites,
  for every pattern named here (STA, pumping, timed pumps, Core's running dispatcher, deferred
  failures, modal windows, XAML strings, both leak-test shapes, fake platforms + configuration,
  restored statics, async gates, store keys, `Validate()`).

## Running tests - read this before believing any result

| Project | `-f` values |
| --- | --- |
| `tests/Barbatos.Wpf.Core.UnitTests` | `net8.0-windows10.0.17763.0`, `net10.0-windows10.0.17763.0` (a bare `net10.0-windows` fails with `NETSDK1005`) |
| `tests/Barbatos.Wpf.Aquarius.UnitTests`, `…AquariusRouter.UnitTests`, `…AquariusValee.UnitTests` | `net8.0-windows`, `net10.0-windows` |

```bash
dotnet test tests/Barbatos.Wpf.Core.UnitTests -f net10.0-windows10.0.17763.0
dotnet test tests/Barbatos.Wpf.Aquarius.UnitTests -f net8.0-windows --filter "FullyQualifiedName~KeepAliveTests"
```

- **A bare `dotnet test` lies** (solution, or a project without `-f`). Both TFMs run in parallel
  against one real per-user store (`Preferences`/`SecureStorage` under `%LocalAppData%`) and
  process-wide WPF state, so a combined run fails spuriously - and on some machines the full run
  aborts partway, which reads as a false green.
- **A failure is real only once it reproduces with that class alone, on that one TFM.** Known
  flaky in combination: `Barbatos.Wpf.Core.UnitTests` (the shared per-user store) and Valee's
  `ValeeXamlTests` (STA/`Application` interaction) - different causes, same remedy.
- Before calling a change done, run every affected project on **both** of its TFMs, one at a time.
- Run Debug (the default). `BuildConfigurationTests.ThisTestAssemblyBuiltDebugIsReportedAsDebug`
  correctly fails under `-c Release`.
- net9.0 is built by every library but tested by no project: a `#if NET9_0_OR_GREATER` branch is
  only exercised through the net10 run.
- `.github/workflows/barbatos-wpf-ci.yml` runs every project on both of its TFMs, one step each,
  on pull requests and pushes to `main`, with `--blame-crash` and an 8-minute hang collector. The
  release workflow strips `/tests/` and runs none, so a green release says nothing about tests:
  look at the CI run for that commit.
- When the test host dies mid-run, rerun that project and TFM with `--blame-crash` to name the
  test that was executing (how the crash behind `AssemblyInfo.cs` was confirmed).

## Pick the thread helper

| The test touches | Use |
| --- | --- |
| Pure logic: `Ref`/`Computed`, `Expr` parsing, path parser/tokenizer, `RouteMatcher`, `RouteSearchIndex`, `MemoryRouterHistory`, `Form`/`Field<T>` validation, `PeriodicSchedule`, input interactions | plain `[Fact]` or `async Task` |
| A `DependencyObject`, control, `Window`, deferred dispatcher work, or a `Router` navigation (it constructs the entering Views through `Setup.Resolve`) | `StaThread.Run(() => …)` |
| `Application.Current` (its `Windows`, `DispatcherUnhandledException`), or a failure the library defers with `BeginInvoke` to the application's dispatcher | `TestApplication.Invoke(() => …)` (Lifecycle error capture listens on the element's own dispatcher, so it also works under `StaThread.Run` when the test pumps that thread) |
| Core, a `Window` whose show/close/activation/focus must settle synchronously | a file-local `RunOnStaThread` that runs the body inside `Dispatcher.Run()` ([pattern](patterns.md#a-running-dispatcher-for-core-windows)) |

- **Why two helpers.** `Application.Current` is a process-wide singleton bound to the thread that
  constructed it. Created from a `StaThread.Run` thread, it works for the first test only; every
  later test finds it pointing at a dispatcher whose thread has exited, and anything posted to it
  never runs. `TestApplication` owns one background STA thread running `Dispatcher.Run()` for the
  whole process - which is also the only place a `BeginInvoke`'d exception ever executes, since a
  `StaThread.Run` body never pumps continuously.
- **`TestApplication` is shared by every test in the process.** Unsubscribe
  `DispatcherUnhandledException` handlers in `finally`, raise `Unloaded` on Lifecycle-enabled
  elements before returning (Lifecycle subscribes its element's own `Dispatcher.UnhandledException`
  while mounted - for a `TestApplication` element that is the shared dispatcher - and would
  intercept a later test's exception), and set `e.Handled = true` in an observer so the host
  survives. All three copies use `ShutdownMode.OnExplicitShutdown`; the Aquarius copy also fails
  the next `Invoke` fast, naming a stray exception an earlier test left queued, instead of letting
  it kill the pump thread.
- **A control left loaded outlives its test's thread.** Each `StaThread.Run` body gets a fresh
  thread, and a window it never closes keeps its controls' subscriptions to static events after
  that thread exits. A later test raising that event then runs the old control's handler on the
  new thread - `"The calling thread cannot access this object"` from inside a `Loaded` handler,
  which aborted the whole Aquarius run on CI (`Teleport` on `TeleportHost.HostRegistered`; fixed
  by ignoring events from another thread). A library handler on a static event checks
  `CheckAccess()` first; a test that leaves a control loaded on purpose (`AssertAlive` controls)
  is fine once it does. `StaThread.Run` fails a body that runs past two minutes rather than
  hanging the run.
- **Wait outside `TestApplication.Invoke`**, with a timeout (`signal.Wait(TimeSpan.FromSeconds(5))`).
  Waiting inside blocks the very dispatcher that has to deliver the signal - a deadlock.
- Core has no `StaThread`, `TestApplication` or `GcProbe`, and no Core test touches
  `Application.Current`. A WPF dispatcher itself does not need STA: `DispatchingTests` and
  `InputChordTests` pump `Barbatos.Wpf.Dispatching.Dispatcher.GetForCurrentThread()` on the xUnit
  thread.
- Never assert inside a bare `new Thread(...)`: an exception escaping that thread terminates the
  test host instead of failing the test. Capture and rethrow on the test thread, as
  `StaThread.Run` does.

## Pumping and waiting

- `StaThread.PumpDispatcher()` is `Dispatcher.CurrentDispatcher.Invoke(() => { }, DispatcherPriority.Background)`:
  it returns once everything queued at `Background` or higher has run, including WPF's own
  `Loaded`-priority tree-connection work. Every deferral in `src/` posts at `Background` or higher
  (`NextTick.Run`/`RunAsync`, `WatchFlush.Post`, Lifecycle's `IOnUpdated` batching, `FormMeta`
  change notifications, `Valee` mask at `Input`), so one pump flushes them. Work scheduled from
  a worker thread lands on the watcher's or element's UI thread, else `Application.Current`'s -
  so pump that thread, not the worker (`NextTickTests`). Pump after
  `window.Show()`, after anything deferred, after changing `Component.Is` or the route, and after
  `window.Close()`. Inside `TestApplication.Invoke` it pumps the shared dispatcher.
- **It does not let time pass.** Storyboards (`Transition`), dispatcher timers, chord
  `StepTimeout`, hold interactions and periodic services need a bounded timed pump
  ([pattern](patterns.md#time-based-behaviour)). A `Dispatcher.PushFrame` that only the code under
  test can end hangs the whole run when that code is broken; end it from a one-shot timer.
- **Values are not notifications.** `FormMeta` properties are computed on every read; only the
  `PropertyChanged` is batched through `NextTick`. `FormMetaStalenessTests` deliberately never
  pumps, proving there is no cache - do not add a pump there.
- **Synthetic vs real lifecycle.** `element.RaiseEvent(new RoutedEventArgs(FrameworkElement.LoadedEvent, element))`
  drives `Loaded`/`Unloaded` with no window and is the direct way to reproduce a double `Loaded`.
  Use a real `Window` + `Show()` + pump when layout, templates, bindings or the logical tree
  matter, and close it in `finally`, then pump.
- `Loaded` is broadcast root-first: at `Window.Loaded` an inner `RouterView` has not resolved
  anything yet - hook the inner element's `Loaded`. `ShowDialog()` blocks, so assert from that
  handler and `Close()` the dialog there ([pattern](patterns.md#modal-windows)). An `Owner` must
  already be shown.
- **Blocking on a task on the STA thread** (`router.Push("/x").GetAwaiter().GetResult()`,
  `form.HandleSubmit(...).ExecuteAsync(null).GetAwaiter().GetResult()`) is safe only when nothing
  in the chain awaits work that needs this thread - the suites do it with guards returning
  `Task.FromResult(...)` and synchronous validators. Real async belongs in an `async Task` test off
  the STA thread, driven by `TaskCompletionSource` gates (`AsyncValidationRaceTests`).
- XAML-loader behaviour (content properties, DataContext through the logical tree,
  `TemplatedParent` bindings in a `ControlTemplate`) needs `XamlReader.Parse` on a real string with
  the `aq` xmlns ([pattern](patterns.md#real-xaml-strings)); building the graph in C# does not
  reproduce it. `Setup` resolves at `Initialized`, so C#-built Views call
  `((ISupportInitialize)element).BeginInit()`/`EndInit()` (`SetupTests`).

## Process-wide state

- **Parallelism.** The three Aquarius-family assemblies set
  `[assembly: Parallelization(Mode = ParallelMode.None)]`: with many `StaThread.Run` windows
  alive at once, WPF's composition engine crashed the test host. Core does not, so Core test
  classes run concurrently.
- **Essentials facades** (`AppInfo.Current`, `Preferences.Default`, ...) use MAUI's lazy
  `static` getter (`currentImplementation ??= new XxxImplementation()`), which is not thread-safe
  on first access. `ModuleInit.WarmUpSingletons` touches each in a `[ModuleInitializer]` before
  any test runs. **Add every new Essentials facade there.**
- The facades' `SetCurrent`/`SetDefault` are internal, so a test cannot swap them: the
  `Preferences`/`SecureStorage`/`VersionTracking` tests hit the real per-user store. Use a unique
  key per test (`$"Test.{Guid.NewGuid():N}"`), `Remove` it at the end, call
  `Preferences.Clear(sharedName)` only on a `sharedName` that is itself unique, and assert
  `VersionTracking` invariants rather than first-launch booleans (its history persists across
  runs).
- To keep a service off the real store, register a fake for its interface instead -
  `FakeFileSystem(tempPath)`, `FakeSecureStorage`, `FakeAppInfo`, `FakeDeviceInfo` - and delete
  any temp directory in the test (`AgentFeatureTests.TempDirectory`).
- Never mutate process environment variables (`DOTNET_ENVIRONMENT`): parallel Core classes see
  the change. Feed configuration through `builder.Configuration.AddInMemoryCollection(...)`
  (`WpfHostEnvironmentTests`).
- **Statics written by `UseXxx` or by a test**: `Setup.ServiceProvider`, `Setup.Resolver`,
  `Setup.ThrowOnUnresolved`, `Expr.ThrowOnUnresolvedIdentifiers`, `Router.Current`. Save and
  restore them in `try/finally` ([pattern](patterns.md#aquarius-and-router-di-with-restored-statics)).
- To prove "called from another thread", start a dedicated `Thread`, not `Task.Run` - the pool can
  hand the work back to the calling thread (`DispatchingTests`).

## Leak tests with GcProbe

`GcProbe.AssertCollected(WeakReference reference, string what)` and
`GcProbe.AssertAlive(WeakReference reference, string what)` exist in the Aquarius, Router and
Valee suites. `AssertCollected` makes up to five attempts - full blocking compacting collection,
finalizer drain, second collection - with a `PumpDispatcher()` between, because WPF can still hold
the graph in queued work on the first pass; a real leak fails all five. Call both on the thread
that built the subject (inside `StaThread.Run`/`TestApplication.Invoke`), since the retry pumps
the current dispatcher. Use `GcProbe` only when the leak is "something still holds a strong
reference" and nothing in the type's own API shows it.

1. **The subject must never be reachable from the test's frame.** Build it and take the
   `WeakReference` in a separate `[MethodImpl(MethodImplOptions.NoInlining)]` helper; in Debug a
   local is rooted for the whole method body and every assertion fails for the wrong reason.
2. **Always pair `AssertCollected` with an `AssertAlive` control** (and a one-`Loaded` baseline
   for a double-`Loaded` regression). Without the control you have not shown the probe can fail.
3. **Root what is supposed to stay alive.** Return the still-open `Window` (or whatever owns the
   live tree) so the caller keeps it rooted across the assertion; an unrooted `KeepAlive` is
   collected with everything it caches and the two cases stop being comparable.
4. **Root the long-lived owner the leak would hang off** (an app-lifetime `Router`): keep it in
   the test's frame and `GC.KeepAlive(router)` after asserting. Unrooted, owner, orphaned
   subscription and subject form one unreachable island that is collected together, and the test
   passes with the leak present.
5. **Remove legitimate references first.** A `Router` holds the current route's View in
   `RouteRecord.Instances`, and that View's logical parent is the outlet - navigate away before
   asserting the outlet is collectable.

**The hazard these exist for:** WPF raises `Loaded` a second time with no `Unloaded` in between
(a `TabControl` realizes every tab up front, then raises `Loaded` again on the one that becomes
selected). A control that subscribes on `Loaded` and unsubscribes on `Unloaded` then leaves one
subscription behind - against a `static` event or an app-lifetime object that is a
process-lifetime root for the control, its subtree and, through `DataContext`, the ViewModel
graph. `Teleport`, `RouterView`, `Lifecycle`, `Directives.Use`, `Directives.Event` and
`RouterWindows` all guard it. When writing or reviewing lifecycle code: guard both edges, always
re-hook what you unhook, and reproduce with two synthetic `Loaded` events and one `Unloaded`.

## DI and feature tests

- **Core**: `WpfApp.CreateBuilder()` → `builder.Services.AddSingleton<IStartupRegistrar>(fake)`
  (or `ITrayIconPlatform`, `INotificationPlatform`, `IHotkeyPlatform`, `IPowerManager`,
  `IPushNotificationTransport`, ... with the matching `Fake*`) → `builder.ConfigureXxx(...)` →
  `Build()` → `wpfApp.Services.GetRequiredService<...>()`. `ConfigureXxx` registers the real
  OS-backed platform with `TryAddSingleton`, so registering the fake **first** is what keeps a test
  off the registry, the tray and the toast system.
- Per feature, pin: not registered without `ConfigureXxx` (`GetService` returns `null`); a
  `Barbatos:Xxx` value from `AddInMemoryCollection` is applied; configuration overrides code values
  ([pattern](patterns.md#core-feature-with-a-fake-platform-and-configuration)).
- Internal implementations are reached through their public interface with fakes underneath -
  `AgentFeatureTests` resolves the internal file-backed `IAiSessionStore` over `FakeFileSystem`.
  Per CLAUDE.md, never `InternalsVisibleTo`; if that is not enough, the behaviour becomes public
  API first (`barbatos-package-authoring`).
- **Aquarius/Router**: `new ServiceCollection()` → `AddAquarius(...)`/`AddAquariusRouter(...)` →
  `BuildServiceProvider()` → `UseAquarius()`/`UseAquariusRouter()`, inside the statics-restoring
  wrapper. Prove `TryAdd` precedence by registering the app's own service before the `Add` call
  (`AnAppsOwnHistoryRegistrationWins`).
- **Apsu**: stores that interceptors must proxy are `public`, non-`sealed`, with `virtual`
  `[Action]` methods (`StoreActionInterceptorTests`); a `sealed` store with interceptors registered
  throws `InvalidOperationException` on resolve.

## What to test, and how

| Surface | How |
| --- | --- |
| Reactivity (`Ref`, `Computed`, sync `Watch`) | plain objects, no STA |
| `WatchFlush.Post`, `NextTick`, `IOnUpdated` | `StaThread.Run`; assert the deferral, `PumpDispatcher()`, assert the effect |
| Attached properties, directives, controls | `StaThread.Run` + `SetXxx` + assert; real `Window` when layout or bindings matter |
| Anything reading `Application.Current`; deferred `BeginInvoke` failures | `TestApplication.Invoke` + wait outside |
| Navigation pipeline (guards, redirects, failures, history) | `StaThread.Run`, no window: `router.Start(...)`/`Push(...)` + `GetAwaiter().GetResult()`, assert the returned failure and `CurrentRoute.Value` |
| Path parsing, matching, search | plain objects, no STA |
| `Form`/`Field<T>` and rules | `async Task`, `TaskCompletionSource` gates for races; `aqv:` markup needs `StaThread.Run` + window |
| Input shortcuts | `IInputSystemService.ProcessKeyDown(key, modifiers)`/`ProcessKeyUp(...)` - no window, no keyboard; timed pump for chords/holds |
| Schedules | `PeriodicSchedule.GetNextOccurrence(now, lastRun)` is pure and never reads the clock - pass fixed instants |
| Descriptor/options `Validate()` | `Assert.Throws<InvalidOperationException>` + the offending property's `nameof` in the message; `Record.Exception` is `null` for valid input |
| DI entry points | descriptors/resolution, default-off, config-over-code, `TryAdd` precedence |
| Leak fixes | `GcProbe`, per the rules above |

Prefer the headless seam when one exists - `ProcessKeyDown`, `GetNextOccurrence`, `Validate()`,
the platform interfaces and `Router`'s window-free pipeline exist partly so tests need no UI.

## Conventions

- Plain xUnit assertions (`Assert.Equal`, `Assert.Same`, `Assert.Throws`, `Assert.Single`,
  `Record.Exception`); `[Theory]` + `[InlineData]` for tables. No assertion library is referenced -
  do not introduce `.Should()`.
- A class per type under test, `<Type>Tests`, or `<Type><Concern>Tests` for a focused concern
  (`LifecycleLeakTests`, `RouterNavigationGuardOrderTests`, `AsyncValidationRaceTests`). Method
  names are sentences describing the behaviour (`SettingTheSameValueDoesNotRaisePropertyChanged`);
  `PeriodicScheduleTests` uses `Frequency_Case_Result` for its matrix.
- Arrange/act/assert separated by blank lines, no `// Arrange` headers. A comment above a test says
  why the behaviour matters or which bug it pins - not what the code does.
- In the Aquarius-family projects the package's own namespaces come from `<Using Include="..."/>`
  in the test `.csproj`; add there rather than repeating `using` lines. Core's `.csproj` adds only
  `Xunit` and `Barbatos.Wpf.Hosting`, so Core test files carry per-file `using` lines
  (`Barbatos.Wpf.Storage`, `Microsoft.Extensions.DependencyInjection`, ...) - match the project.
- Shared doubles: `TestDoubles.cs` (`internal sealed`, Aquarius and Router) and
  `FeatureTestFakes.cs` (`public sealed`, Core). Reuse before adding.
- Start every new file with the MIT header from `.editorconfig` - copy it from any neighbouring
  test file; every file in `tests/` carries it.

## Symptom → cause → fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Passes alone, fails in a full or solution run | Both TFMs and many classes against one per-user store / process-wide state | Rerun that class alone on one TFM; only that result counts |
| Run stops partway, fewer tests reported, host crashed | Concurrent STA windows (parallelism), or a synchronous throw from `Loaded` inside WPF's render pipeline | Keep `ParallelMode.None` in WPF suites; `--blame-crash`; the library must defer that throw with `BeginInvoke` and a test must pin it ([pattern](patterns.md#a-deferred-failure-through-dispatcherunhandledexception)) |
| `InvalidOperationException`: "The calling thread must be STA" | WPF object built on the xUnit thread | `StaThread.Run` |
| Only the first `Application` test works; later ones never see posted work | `Application.Current` created on a short-lived `StaThread.Run` thread | `TestApplication.Invoke` for every `Application`-touching test |
| Later tests fail with "The Application object is being shut down" | A test closed the last window on the shared `Application` without `ShutdownMode.OnExplicitShutdown` | Every shipped `TestApplication` copy sets it; a new suite's copy must too |
| `[FATAL ERROR] System.InvalidOperationException: The calling thread cannot access this object`, then the run hangs | A handler on a static event, subscribed by a control an earlier test left loaded (its thread now gone), ran on the raising thread | The library handler checks `CheckAccess()`; see "A control left loaded outlives its test's thread" |
| Assertion sees the old value | Deferred work not flushed | `StaThread.PumpDispatcher()` before asserting |
| Animation/timer/chord assertion fails although the logic is right | `PumpDispatcher` does not advance time | Bounded `PumpFor`/`PumpUntil` |
| Test hangs | Waiting inside `TestApplication.Invoke`; `ShowDialog()` never closed; unbounded `PushFrame`; `GetResult()` on real async on the STA thread | Wait outside with a timeout; close from the inner `Loaded`; bound every wait; make it an `async Task` test |
| `AssertCollected` fails though the fix is right | Subject rooted by the test frame, or legitimately held (current route's View) | `NoInlining` helper; navigate away / close first |
| `AssertCollected` passes with the bug still present | Owner unrooted, so the whole island was collected | Root the owner and `GC.KeepAlive` it; add the `AssertAlive` control |
| A later test's dispatcher exception is swallowed or misattributed | A handler or mounted Lifecycle element left on the shared dispatcher | Unsubscribe in `finally`; raise `Unloaded` before returning |
| Sporadic Core failure around a facade's first access (two instances created by racing classes) | New Essentials facade not warmed | Add it to `ModuleInit.WarmUpSingletons` |
| `DataContext` or resolved View leaks into the next test | `Setup.ServiceProvider`/`Resolver`/`Router.Current` not restored | Save and restore in `try/finally` |
| `NETSDK1005` | Core run with `-f net10.0-windows` | Use `net10.0-windows10.0.17763.0` |
| `ThisTestAssemblyBuiltDebugIsReportedAsDebug` fails | Ran `-c Release` | Run Debug |

## Adding a test project

- Name it `Barbatos.Wpf.<Package>.UnitTests`. `Directory.Build.props` sets `IsTestProject` from
  the name containing `Test` and derives `IsCoreProject=False` from it, which turns off
  `IsPackable`, `GeneratePackageOnBuild`, `GenerateDocumentationFile` and publishing, adds
  `NoWarn` `CS8002;SA0001`, and keeps `Directory.Build.targets` from strong-name signing it in a
  SourceLink build. A project named otherwise is built as a library - setting `IsTestProject` in
  its own `.csproj` comes too late to change that.
- `.csproj`: `TargetFrameworks` `net8.0-windows;net10.0-windows` (SDK-suffixed
  `…windows10.0.17763.0` when it references Core), `UseWPF`, `IsPackable=false`,
  `IsTestProject=true`, `OutputType=Exe` with the existing comment (xUnit.net v3 test projects are
  self-hosting executables). `PackageReference`s without versions: `coverlet.collector`,
  `Microsoft.NET.Test.Sdk`, `xunit.v3.mtp-off`, `xunit.runner.visualstudio`, plus
  `CommunityToolkit.Mvvm` / `Microsoft.Extensions.DependencyInjection` when needed. One
  `ProjectReference` to the package; `<Using Include="Xunit" />` plus its namespaces. Do not set
  `Nullable`, `ImplicitUsings` or `LangVersion`.
- The trim/AOT analyzers from `Directory.Build.targets` apply to test projects too; a suppression
  carries a comment, as Valee's `IL2026` does.
- Copy the helpers and change the namespace: `StaThread.cs` (Valee's has `Run<T>`),
  `TestApplication.cs` (the Aquarius copy is the most defensive: it also fails fast on a stray
  exception),
  `GcProbe.cs` if it will have leak tests, and `AssemblyInfo.cs` whole (`ParallelMode.None` plus
  `ThemeInfo`) if it creates windows.
- Add it to `Barbatos.Wpf.slnx` inside the `/tests/` folder (which the release workflow strips),
  and give it one step per TFM in `.github/workflows/barbatos-wpf-ci.yml`, copied from a
  neighbouring step.
- Add its `-f` values to the table in `.claude/rules/tests.md` and the examples in `CLAUDE.md` §2.

## Checklist: adding or changing a test

- [ ] Helper chosen from [Pick the thread helper](#pick-the-thread-helper); pure logic stays off STA.
- [ ] Every deferred effect pumped; every timed effect pumped with a bound; every wait has a timeout.
- [ ] Windows closed in `finally` and pumped; handlers on the shared dispatcher removed.
- [ ] Statics restored; store keys unique and removed; no environment variables touched.
- [ ] Core feature: fake platform registered before `ConfigureXxx`; default-off and config-over-code pinned.
- [ ] Leak test: `NoInlining` helper, rooted owner, `AssertAlive` control.
- [ ] The class run alone on both TFMs of its project, then the whole project per TFM.

## Related skills

- `barbatos-package-authoring` - changing `src/`, csproj and TFMs, and turning internal behaviour
  into public API a test can reach.
- `barbatos-aquarius-view`, `barbatos-aquarius-router`, `barbatos-valee-form`,
  `barbatos-apsu-store`, `barbatos-wpf-host`, `barbatos-wpf-essentials`, `barbatos-mcp-ai` - what
  each feature is supposed to do.
- `barbatos-docs-sync` - the docs a behaviour change also touches.
