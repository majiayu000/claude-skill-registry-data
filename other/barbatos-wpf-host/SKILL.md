---
name: barbatos-wpf-host
description: "Compose a Barbatos.Wpf.Core app and its opt-in desktop features - WpfProgram/WpfApp.CreateBuilder, IWpfInitializeService, lifecycle events, ConfigureSingleInstance, ConfigureTrayIcon, ConfigureInputSystem, ConfigureNotifications, ConfigurePushNotifications, ConfigureKeepAwake, ConfigureRunOnStartup, IWpfPeriodicService jobs, dialogs, splash screen. Use when wiring startup or WpfProgram.cs, registering a service or Barbatos:Xxx options, or symptoms like \"the app opens twice\", \"a second launch shows another window\", \"my Ctrl+K shortcut does nothing\", \"the toast never appears\", \"keep it running in the tray\". For AppInfo, Preferences and other Essentials, barbatos-wpf-essentials. Vietnamese prompts too - khởi động ứng dụng, đăng ký service, khay hệ thống, thu nhỏ xuống khay, thông báo toast, phím tắt toàn cục, chạy cùng Windows, màn hình chờ, tác vụ định kỳ."
---

# Barbatos.Wpf.Core hosting and desktop features

`Barbatos.Wpf.Core` gives unpackaged WPF a MAUI-shaped host: `WpfApp`/`WpfAppBuilder` (a real
`IHostApplicationBuilder`) mirror `MauiApp`/`MauiAppBuilder`, `WpfApplication` mirrors
`MauiWinUIApplication`, `IWpfInitializeService` mirrors `IMauiInitializeService`. Desktop
features (tray, single instance, shortcuts, toasts, ...) are opt-in `ConfigureXxx` calls on the
builder. Not here: the Essentials facades (`barbatos-wpf-essentials`), Apsu stores
(`barbatos-apsu-store`), `ConfigureMcp` (`barbatos-mcp-ai`), Aquarius/Router wiring after
`Build()` (`barbatos-aquarius-view`, `barbatos-aquarius-router`).

## Sources of truth

- Docs: [Hosting](../../../src/Barbatos.Wpf.Core/README.md#hosting),
  [Optional desktop features](../../../src/Barbatos.Wpf.Core/README.md#optional-desktop-features),
  [Dialogs](../../../src/Barbatos.Wpf.Core/README.md#dialogs), [SplashScreen](../../../src/Barbatos.Wpf.Core/README.md#splashscreen),
  [Periodic services](../../../src/Barbatos.Wpf.Core/README.md#periodic-services); members in
  [API-REFERENCE.md](../../../src/Barbatos.Wpf.Core/API-REFERENCE.md#barbatoswpfhosting-namespace) (where a document and `src/` disagree, trust `src/`).
- Startup/exit ordering is decided in
  [`Platform/WpfApplication.cs`](../../../src/Barbatos.Wpf.Core/Platform/WpfApplication.cs);
  the builder in [`Hosting/WpfAppBuilder.cs`](../../../src/Barbatos.Wpf.Core/Hosting/WpfAppBuilder.cs).
  Each feature's `ConfigureXxx` lives in `src/Barbatos.Wpf.Core/Essentials/<Feature>/AppHostBuilderExtensions.cs`.
- Reference app: [`samples/Barbatos.Wpf.Core.Sample`](../../../samples/Barbatos.Wpf.Core.Sample)
  (`WpfProgram.cs`, `App.xaml.cs`, `SettingsStore.cs`, `HeartbeatService.cs`). Minimal shape:
  [template `WpfProgram.cs`](../../../templates/Combined/project-templates/barbatos-wpf-app/WpfProgram.cs).
  An `IWpfInitializeService` done right:
  [`ShortcutRoutingInitializer.cs`](../../../samples/Barbatos.Wpf.AquariusRouter.Sample/Routing/ShortcutRoutingInitializer.cs).
- Behaviour pins in `tests/Barbatos.Wpf.Core.UnitTests/`: `WpfInitializeServiceTests.cs`,
  `HostBuilderLifecycleTests.cs`, `DispatchingTests.cs`, `WpfAppTests.cs`, `<Feature>FeatureTests.cs`, fakes in `FeatureTestFakes.cs`.

Per-feature behaviour (single instance, tray, toasts, push, periodic, input, dialogs, keep awake,
run on startup): [features.md](features.md). Read it before using or debugging any one feature.

## The shape every app takes

Three files. Do not invent another arrangement.

```xml
<!-- App.xaml: the root is WpfApplication, and there is no StartupUri - the container builds MainWindow -->
<hosting:WpfApplication x:Class="MyApp.App"
                        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                        xmlns:hosting="clr-namespace:Barbatos.Wpf.Hosting;assembly=Barbatos.Wpf.Core" />
```

```csharp
// App.xaml.cs
public partial class App : WpfApplication
{
    protected override WpfApp CreateWpfApp() => WpfProgram.CreateWpfApp();

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);   // builds the host - Services is usable only after this line

        MainWindow = Services.GetRequiredService<MainWindow>();
        MainWindow.Show();
    }
}

// WpfProgram.cs - the composition root, MAUI's MauiProgram
public static class WpfProgram
{
    public static WpfApp CreateWpfApp()
    {
        var builder = WpfApp.CreateBuilder();
        // configuration -> lifecycle events -> ConfigureSingleInstance -> other features -> services
        return builder.Build();
    }
}
```

Project file: SDK-suffixed TFM per CLAUDE.md (`net10.0-windows10.0.17763.0`); reference
`Microsoft.Extensions.Configuration.Json` yourself (Core does not bring `AddJsonFile`); mark
`appsettings.json` `CopyToOutputDirectory` - relative JSON paths resolve against the output folder.

## What runs when

`WpfApplication.OnStartup`, in order:

1. `CreateSplashScreen()` (default: a `SplashWindow` from `GetSplashScreenOptions()`). If non-null,
   `ShutdownMode` is forced to `OnExplicitShutdown` and the splash is shown. No container exists.
2. `CreateWpfApp()` -> `builder.Build()`: the provider is built, `builder.Services` turns
   read-only, and every `IWpfInitializeService` runs **in registration order** on the UI thread.
   Feature side effects happen here: the single-instance check, tray icon shown, hotkeys
   registered, schedules armed, push transport started.
3. `IWpfPlatformApplication.Current` is set; window class handlers and
   `DispatcherUnhandledException` are hooked.
4. Lifecycle `OnStartup` delegates run, then `base.OnStartup(e)`, then the rest of your override.

Consequences that bite:

- During `Build()` (initializers, factory lambdas resolved then) `IWpfPlatformApplication.Current`
  is `null` and `WpfApplication.Services` throws `InvalidOperationException` ("The application
  host has not been created yet"). Use the `IServiceProvider` passed to `Initialize`. After
  startup, static code (tray menu actions, lifecycle delegates) reaches the container through
  `IWpfPlatformApplication.Current?.Services`.
- `GetSplashScreenOptions()`/`CreateSplashScreen()` run before the container: only static
  facades (`AppInfo`, `VersionTracking`, `Preferences`) work there.
- A duplicate launch exits in step 2, after its splash window was already shown - a brief flash
  on a blocked second launch is expected.

`OnExit`: leftover splash closed -> lifecycle `OnExit` -> `base.OnExit` -> window scopes disposed
-> `Current` cleared -> host disposed (every singleton's `Dispose`; reentrant `Application` events
during that cascade are no-ops because the host field is cleared first).

## Composing the builder

- `WpfApp.CreateBuilder()` (`useDefaults: true`) already calls `ConfigureLifecycleEvents(null)`,
  `ConfigureDispatching()` and `UseEssentials()`. Do not repeat the last two; call
  `ConfigureLifecycleEvents(events => ...)` only to add handlers. `useDefaults: false` is for tests.
- Call `ConfigureSingleInstance()` before the other features. Its initializer exits a duplicate
  process with `Environment.Exit(0)`, which never disposes the host - whatever an earlier
  initializer did (adding a tray icon, starting a push connection) is never cleaned up.
- An initializer that calls `IInputSystemService.FindAction` must be registered after
  `ConfigureInputSystem`; the maps are only applied when that feature's own initializer runs.
- `ConfigureLifecycleEvents` delegates from every call accumulate, in call order.
- Configuration sources may be added before or after a `ConfigureXxx` call (binding reads the live
  `ConfigurationManager` when the options are first resolved), but before `Build()`.
- Environment: `DOTNET_ENVIRONMENT` arrives through a `DOTNET_` environment-variable source added
  first (lowest priority). `builder.Environment` reads `HostDefaults.EnvironmentKey` once, on first
  access - override before that, or set `builder.Environment.EnvironmentName` directly.
- Until a logging provider is added through `builder.Logging`, every `ILogger<T>` is a no-op - and
  features report failures only as log entries (refused hotkey, failed periodic run, push connect
  error), so those failures are invisible. Core ships no provider: add one, e.g.
  `builder.Logging.AddDebug()` from `Microsoft.Extensions.Logging.Debug` (the debugger's Output
  window; the app's `.csproj` needs that `PackageReference` - inside this repo it is versionless,
  since `Directory.Packages.props` already pins the version), plus a persisting provider in a
  shipped app.
- Swap the container with `ConfigureContainer(factory, configure)`; the last call wins.

## Configuration layering and settings that survive a restart

Copy the sample's order - last source wins:

```csharp
// adapted from samples/Barbatos.Wpf.Core.Sample/WpfProgram.cs
builder.Configuration.AddInMemoryCollection(new Dictionary<string, string?> { ["Sample:Greeting"] = "code default" });
builder.Configuration.AddJsonFile("appsettings.json", optional: true);       // shipped defaults
builder.Configuration.AddJsonFile(SettingsStore.FilePath, optional: true);   // what the user saved
```

- Every `ConfigureXxx(o => ...)` runs your delegate, then binds `Barbatos:Xxx` - **file values beat
  code values**, and the user file beats both.
- Feature services read `IOptions<T>.Value` once, at construction. Editing a JSON file (even with
  `reloadOnChange: true`) never changes a running feature; toggle it through its runtime service
  (`SetEnabled`/`SetVisible`/`UpdateSchedule`). For your own live settings use
  `IOptionsMonitor<T>` + `reloadOnChange: true` - its `OnChange` fires on a thread-pool thread
  (see `ShortcutRoutingInitializer.cs`).
- **Runtime toggles do not persist themselves.** Only run-on-startup is stored by the OS (the
  registry). To survive a restart, write the same `Barbatos:<Feature>` keys to the user JSON that
  is loaded last - `SettingsStore.Save` in the sample does exactly this.

## DI lifetimes

| Registration | Lifetime | Why |
| --- | --- | --- |
| `MainWindow` | singleton | Resolved once in `OnStartup`; tray/app actions re-show the same instance, so minimize-to-tray hides it rather than closing it |
| A ViewModel preloaded behind the splash | singleton | `MainWindow`'s constructor must receive the instance you already awaited |
| Dialog windows (`IDialogService.Show<T>`) | transient | A closed `Window` cannot be shown again - a singleton dialog throws on its second opening |
| Anything "per window" | not `AddScoped` | See below |

Each window gets a DI scope on its first `Loaded`, but no public API resolves from it - only
`IWpfInitializeScopedService` and the scoped `IDispatcher` use it. Windows and their ViewModels
are resolved from the root, and `Build()` uses `BuildServiceProvider()` with default options (no
scope validation), so a scoped service resolved there silently behaves as a singleton.

Replace any feature seam by registering it **before** the `ConfigureXxx` call (they use
`TryAdd*`): `ITrayIconPlatform`, `INotificationPlatform`, `IHotkeyPlatform`, `IStartupRegistrar`,
`IPowerManager`, `IPushNotificationTransport`, `IPushNotificationFallbackPresenter`.

Host disposal is synchronous (from `OnExit`): a singleton that implements only `IAsyncDisposable`
makes the container throw at shutdown - implement `IDisposable` too, as
`SignalRPushNotificationTransport` does. Never resolve from the provider inside a `Dispose()`
(`ObjectDisposedException`, pinned in `WpfAppTests.cs`).

## Initialize services

`IWpfInitializeService.Initialize(IServiceProvider services)` runs once inside `Build()` on the
UI thread. It is the place for "wire this up once the container exists" - attaching `Performed`
handlers, subscribing to feature events - instead of `GetRequiredService` calls in
`CreateWpfApp`. Ship it with a builder extension, as the router sample does:

```csharp
// samples/Barbatos.Wpf.AquariusRouter.Sample/Routing/ShortcutRoutingInitializer.cs, trimmed
public static WpfAppBuilder ConfigureShortcutRouting(this WpfAppBuilder builder)
{
    builder.Services.TryAddEnumerable(ServiceDescriptor.Singleton<IWpfInitializeService, ShortcutRoutingInitializer>());
    return builder;
}
```

- **Synchronous.** An exception escapes `Build()` and kills startup. Async work goes in `OnStartup`
  behind the splash, or starts fire-and-forget inside a logging `try/catch` (as the push initializer does).
- Capture the UI dispatcher here (`dispatcherProvider.GetForCurrentThread()`), never later from a
  background callback. `IWpfInitializeScopedService` runs once per window, on its first `Loaded`.

## Lifecycle events

```csharp
builder.ConfigureLifecycleEvents(events => events.AddWpf(wpf => wpf
    .OnStartup((app, args) => { })
    .OnDispatcherUnhandledException((app, args) => { /* args.Handled = true keeps the app alive */ })
    .OnWindowCreated(window => { })
    .OnWindowClosing((window, args) => { /* args.Cancel = true keeps it open */ })
    .OnWindowClosed((window, args) => { })));
```

`ConfigureLifecycleEvents`, `AddWpf` and the `On...` methods live in
`Barbatos.Wpf.LifecycleEvents`, not `Barbatos.Wpf.Hosting` - import both in `WpfProgram.cs`.

Application: `OnStartup`, `OnActivated`, `OnDeactivated`, `OnSessionEnding`,
`OnDispatcherUnhandledException`, `OnExit`. Window: `OnWindowCreated`, `OnWindowLoaded`,
`OnWindowActivated`, `OnWindowDeactivated`, `OnWindowStateChanged`, `OnWindowClosing`,
`OnWindowClosed`.

- Window events fire for **every** `Window` - the splash screen, dialogs and push fallback
  popups included. Filter before acting. `OnWindowCreated` fires on the first `Loaded`, not in
  the constructor.
- `WpfApplication` already subscribes to `Application.DispatcherUnhandledException`; observe it
  here, never with a second subscription in `App.xaml.cs`. It only sees UI-thread exceptions.
- App-defined events: `events.AddEvent("MyEvent", new Action(() => ...))`, raised with
  `ILifecycleEventService.InvokeEvents("MyEvent")` (`HostBuilderLifecycleTests.CanRegisterCustomEvents`).

Minimize-to-tray (adapted from `samples/Barbatos.Wpf.Core.Sample/WpfProgram.cs`):

```csharp
.OnWindowClosing((window, args) =>
{
    // Match your main window's type, not Application.MainWindow: WPF makes the first window
    // created - the splash screen - Application.MainWindow until it closes, so a reference
    // check would cancel the splash's close and hide it instead.
    if (window is not MainWindow || App.IsExiting)
        return;   // App.IsExiting: the sample's own flag, set by the tray "Exit" item before Shutdown()

    var tray = IWpfPlatformApplication.Current?.Services.GetService<ITrayIconService>();
    if (tray?.IsVisible != true)
        return;

    args.Cancel = true;
    window.Hide();
    tray.ShowBalloonTip("My app", "Still running in the system tray.");   // a hidden window looks closed otherwise
})
```

## Threading and dispatching

`IDispatcher` (`Dispatch`, `DispatchDelayed`, `CreateTimer`, `IsDispatchRequired`) plus
`DispatchAsync`/`DispatchIfRequiredAsync`; `DispatchAsync` faults with `InvalidOperationException`
once the dispatcher is shutting down.

- **Resolve `IDispatcher` on the UI thread.** It binds to whichever thread resolves it first, and
  `IDispatcherProvider.GetForCurrentThread()` on a worker thread creates a dispatcher nobody pumps:
  every later `Dispatch` returns `true` and never runs.
- Arrive on the UI thread: lifecycle events, `SecondInstanceLaunched`, tray clicks and menu
  actions, `InputAction` events (global hotkeys too), periodic `ExecuteAsync` and
  `ServiceExecuted`, push `NotificationReceived`, and `INotificationService.Activated` / push
  `RouteRequested` after a toast click - Windows reports the click on a background thread, and
  `INotificationService` marshals it to the application dispatcher before raising anything
  (an activation arriving after that dispatcher shut down is dropped).
- Do **not** assume the UI thread: `IOptionsMonitor.OnChange` and
  `IPushNotificationService.ConnectionStateChanged` (raised by the transport). Marshal before
  touching UI.

## Splash screen and slow startup

Override `GetSplashScreenOptions()` on `App` (non-null turns it on), or `CreateSplashScreen()` for
your own `Window` (implement `ISplashScreen` for `MinimumDisplayDuration`, else it is zero).
`SplashScreenOptions` is code only (it is built before the container, so there is no
`Barbatos:SplashScreen` section): `AppName`, `Tagline`, `LogoSource`, `Background`,
`ShowProgressIndicator` (default `true`), `MinimumDisplayDuration` (default 1.5 s),
`SponsorLogos` (`SplashScreenLogo`) and `RelatedLinks` (`SplashScreenLink`). `LogoSource` is a
`BitmapImage` URI — a pack URI to a `Resource` item or an absolute path, unlike the toast and tray
paths below — and an image that fails to load is simply hidden, with no error or log.

```csharp
// samples/Barbatos.Wpf.Core.Sample/App.xaml.cs, trimmed
protected override async void OnStartup(StartupEventArgs e)
{
    base.OnStartup(e);

    var mainViewModel = Services.GetRequiredService<MainViewModel>();   // singleton
    await mainViewModel.LoadWorkspaceSummaryAsync();

    await CloseSplashScreenAsync();   // waits out MinimumDisplayDuration (default 1.5s), restores ShutdownMode

    MainWindow = Services.GetRequiredService<MainWindow>();
    MainWindow.Show();
}
```

- Reach `CloseSplashScreenAsync()` on every path (`try/finally`). `ShutdownMode` stays
  `OnExplicitShutdown` until it runs, so an `OnStartup` that throws after an `await` (and is
  marked handled) or returns early leaves a stuck splash. A path that closes the splash but never
  shows a window leaves a windowless process: restoring `ShutdownMode` does not shut down an app
  that has no window left to close, so call `Shutdown()` on that path.
- Synchronous work blocks the splash's animation; only awaited work keeps it responsive.
- Show it conditionally by returning `null`; use `Environment.GetCommandLineArgs()` there (the
  method has no `StartupEventArgs`).

## Opt-in desktop features

Every `ConfigureXxx` is in `Barbatos.Wpf.Hosting`; options and services live in the feature's
namespace. "On" means what happens the moment the method is called with no further setup.

| Feature | Builder call | Namespace | Section | Runtime service | On |
| --- | --- | --- | --- | --- | --- |
| Single instance | `ConfigureSingleInstance()` | `Barbatos.Wpf.SingleInstance` | `Barbatos:SingleInstance` | `ISingleInstanceService` | **yes** |
| Run on startup | `ConfigureRunOnStartup()` | `Barbatos.Wpf.Startup` | `Barbatos:RunOnStartup` | `IRunOnStartupService` | no |
| Tray icon | `ConfigureTrayIcon(...)` | `Barbatos.Wpf.Tray` | `Barbatos:TrayIcon` | `ITrayIconService` | no |
| Keep awake | `ConfigureKeepAwake()` | `Barbatos.Wpf.Power` | `Barbatos:KeepAwake` | `IKeepAwakeService` | no |
| Toast notifications | `ConfigureNotifications()` | `Barbatos.Wpf.Notifications` | `Barbatos:Notifications` | `INotificationService` | yes |
| Push client | `ConfigurePushNotifications(...)` | `Barbatos.Wpf.PushNotifications` | `Barbatos:PushNotifications` (+ `:SignalR`) | `IPushNotificationService` | yes - connects at startup |
| Periodic services | `ConfigurePeriodicServices<T>()` | `Barbatos.Wpf.Hosting` | `Barbatos:PeriodicServices` | `IPeriodicServiceScheduler` | yes |
| Shortcuts / hotkeys | `ConfigureInputSystem(...)` | `Barbatos.Wpf.Input` | `Barbatos:InputSystem` | `IInputSystemService` | yes |
| Dialogs | `ConfigureDialogs()` | `Barbatos.Wpf.Dialogs` | `Barbatos:Dialogs` | `IDialogService` | - |
| Splash screen | override on `App` | `Barbatos.Wpf.Hosting` | - | - | - |

Without the call the service is not registered (`GetService` returns `null`, injection throws).
`TrayIconOptions.MenuItems` and `InputSystemOptions.ActionMaps` carry delegates: code only.

## Hard rules

- Never add `UseWindowsForms` or `NotifyIcon` for a tray icon; the built-in one is `Shell_NotifyIcon`.
- Do not branch on `ISingleInstanceService.IsPrimaryInstance` in app code: a duplicate never
  gets past `Build()`, so it is always `true` by the time your code runs.
- Toast `ImagePath`/`IconPath` and tray `IconPath` are local files; build them from
  `AppContext.BaseDirectory` (a relative path follows the current directory; a URL throws from
  a toast and silently falls back to the executable's icon in the tray).
- In a source file that imports both `System.Windows.Input` and `Barbatos.Wpf.Input`, alias
  `using KeyBinding = Barbatos.Wpf.Input.KeyBinding;` (WPF has its own `KeyBinding`).

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| App opens twice | `ConfigureSingleInstance()` missing, `Barbatos:SingleInstance:Enabled` false, or the two builds have different `AppInfo.AppId` (the mutex key) | Call it; keep `AppId` stable (`barbatos-wpf-essentials`) |
| Second launch's arguments (a file to open) are lost | `SecondInstanceLaunched` carries no data - only a wake signal | Own IPC; not built in |
| `InvalidOperationException` "host has not been created yet" | `WpfApplication.Services`/`Current` used during `Build()` or in splash overrides | Use `Initialize`'s `services` argument |
| Shortcut does nothing | Feature not configured; map `Scope` lacks keyboard focus; map or service disabled; `FindAction` name differs (exact match) | See [features.md](features.md#input-system) |
| Global hotkey never fires | Another app owns the combination (warning logged to a no-op logger), or a `GlobalKeyBinding` changed without `RefreshBindings()` | Add a logging provider; call `RefreshBindings()` |
| Toast never appears | `IsEnabled` false (setting or config), or `Availability != Enabled` | Check `Availability`, offer `OpenSystemSettings()` |
| Closing a dialog hides it and shows the tray balloon | Minimize-to-tray handler not filtered to the main window | Filter by the main window's type, as above |
| Tray balloon at startup, splash window lingers hidden | Minimize-to-tray filtered with `ReferenceEquals(window, Application.MainWindow)`; the splash is `MainWindow` until it closes | Filter by type (`window is not MainWindow`) |
| Stuck splash | `CloseSplashScreenAsync()` not reached | `try/finally` around the preload |
| Process alive with no window | Splash closed, then an early return or failure before any window was shown | Show a window or call `Shutdown()` on that path |
| Main window flashes empty, or preloaded data missing | Preloaded ViewModel not a singleton, or loaded in `Loaded` | Singleton + await before `CloseSplashScreenAsync()` |
| Second opening of a dialog throws | Dialog window registered as singleton | `AddTransient<TWindow>()` |
| Settings toggle lost after restart | Runtime services never persist | Write `Barbatos:<Feature>` to the user JSON loaded last |
| JSON edited, running feature unchanged | Features read `IOptions<T>` once | Call the runtime service |
| Exception at shutdown from the container | An `IAsyncDisposable`-only singleton, or a `Dispose()` that resolves services | Add `IDisposable`; resolve in the constructor |
| `DispatchAsync` never completes | `IDispatcher` first resolved on a worker thread | Resolve/capture on the UI thread |
| Warnings mentioned in docs never show | `builder.Logging` never given a provider | `builder.Logging.AddDebug()` (package `Microsoft.Extensions.Logging.Debug`) or another provider |
| `AddJsonFile` does not exist | Core does not reference the JSON provider | Add `Microsoft.Extensions.Configuration.Json` |

Feature-specific rows (tray menu not updating, periodic job runs at startup, stale run-on-startup
path, duplicate push) are in [features.md](features.md#feature-symptoms).

## Checklist: adding a feature to an app

1. `ConfigureXxx` in `WpfProgram` - single instance first, input system before any `FindAction` user.
2. File-configurable defaults under `Barbatos:Xxx` in `appsettings.json`.
3. Handlers in an `IWpfInitializeService` or after `base.OnStartup(e)`; marshal off-UI callbacks.
4. Settings screen: toggle the runtime service, persist the same keys to the user JSON (sample
   `MainViewModel` + `SettingsStore`).
5. Unit-test through the public platform seams with fakes (`FeatureTestFakes.cs`, `barbatos-wpf-testing`).

Changing a feature inside `src/` instead: the `ConfigureXxx` anatomy checklist is at the end of
[features.md](features.md#adding-or-changing-a-core-configurexxx-feature).

## Related skills

`barbatos-wpf-essentials` (AppInfo/AppId, Preferences, SecureStorage, VersionTracking, app
actions), `barbatos-aquarius-view` and `barbatos-aquarius-router` (wiring their ambient provider
after `Build()`), `barbatos-mcp-ai` (`ConfigureMcp`), `barbatos-apsu-store`,
`barbatos-wpf-testing`, `barbatos-package-authoring`, `barbatos-templates`, `barbatos-docs-sync`.
