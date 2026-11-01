---
name: barbatos-wpf-essentials
description: "Barbatos.Wpf.Core Essentials (UseEssentials facades) - AppInfo/PublisherInfo/AppId metadata, Preferences, SecureStorage (DPAPI), VersionTracking, Connectivity, DeviceDisplay, DeviceIdentity, Launcher, Email, AppActions. Use when saving a setting, storing a token securely, app version or what's-new after an update, checking offline, opening a URL, sending email, the app data folder, a Jump List, per-machine licensing, screen DPI, keeping the screen on while presenting, settings that vanish after a rename, or a null InstallDate. For startup, DI, ConfigureXxx features and keep-awake toggles use barbatos-wpf-host; for AI keys, barbatos-mcp-ai. Vietnamese prompts too - lưu cài đặt, lưu token bảo mật, phiên bản ứng dụng, chạy lần đầu sau cập nhật, kiểm tra mạng, mở trình duyệt, gửi email, bản quyền theo máy."
---

# Barbatos.Wpf.Core Essentials

The .NET MAUI Essentials surface ported to unpackaged WPF, shipped inside `Barbatos.Wpf.Core`.
Every module is a public interface plus a static facade over one shared instance, implemented
with Win32/.NET APIs because WinRT contracts are unavailable to a plain unpackaged app. Not
covered here: composing the host and the `ConfigureXxx` desktop features (`barbatos-wpf-host`),
and the AI key / MCP token stores that sit on `SecureStorage` (`barbatos-mcp-ai`).

## Sources of truth

- Docs: [README Essentials](../../../src/Barbatos.Wpf.Core/README.md#essentials) (with
  [AppInfo/PublisherInfo](../../../src/Barbatos.Wpf.Core/README.md#configuring-appinfo-and-publisherinfo),
  [installer](../../../src/Barbatos.Wpf.Core/README.md#publishing-with-an-installer),
  [DeviceIdentity](../../../src/Barbatos.Wpf.Core/README.md#license-enforcement-deviceidentity)) and
  [API-REFERENCE](../../../src/Barbatos.Wpf.Core/API-REFERENCE.md#barbatoswpfapplicationmodel-namespace)
  (the `ApplicationModel` through `Storage` namespaces). The code wins when they disagree:
  `src/Barbatos.Wpf.Core/Essentials/<Module>/` and `src/Barbatos.Wpf.Core/Hosting/EssentialsExtensions.cs`.
- Sample `samples/Barbatos.Wpf.Core.Sample/`: the `.csproj` (identity metadata),
  `GreetingService.cs` (injecting every info service), `MainViewModel.cs` (Preferences,
  SecureStorage, `ConnectivityChanged`, Email), `WpfProgram.cs` (`ConfigureEssentials`); template
  `templates/Combined/project-templates/barbatos-wpf-app/BarbatosWpfApp.csproj`.
- Tests `tests/Barbatos.Wpf.Core.UnitTests/`: `<Module>Tests.cs`, `EssentialsExtensionsTests.cs`
  (registration), `ModuleInit.cs` (facade warm-up).
- [reference.md](reference.md) - read when you need what each module's Windows code really
  does, every metadata key and fallback, the on-disk paths, the installer mapping, the full
  Permissions list with a custom-permission example, or which exceptions escape.

## How the modules are wired

- **Inject the interface** (`IAppInfo`, `IPreferences`, `ISecureStorage`, `IVersionTracking`,
  `IConnectivity`, `ILauncher`, ...) in services and ViewModels, as `GreetingService.cs` does;
  call the facade (`AppInfo.Name`, `Preferences.Get(...)`) only where there is no container.
- `UseEssentials()` registers each interface as `TryAddSingleton<IXxx>(sp => Xxx.Current)` (or
  `.Default`), so the injected object **is** the facade's instance (pinned by
  `EssentialsExtensionsTests.RegisteredServicesMatchTheStaticFacades`). It runs inside
  `WpfApp.CreateBuilder()`; with `CreateBuilder(useDefaults: false)` nothing is registered and Jump
  List activation is not detected until you call `builder.UseEssentials()`.
- **Replacing an implementation:** `UseEssentials()` has already run when `WpfProgram` gets the
  builder, so an app-side `TryAdd*` is a no-op. Register with `builder.Services.AddSingleton<...>()`
  (last registration wins). Only injected consumers see the replacement: facades cannot be
  swapped (`SetCurrent`/`SetDefault` are internal), and library code built on facades keeps the
  built-in - storage paths, `VersionTracking`, `DeviceIdentity`.
- Namespaces: `Barbatos.Wpf.ApplicationModel` (+ `.Communication` for Email, Contacts),
  `Barbatos.Wpf.Devices` (+ `.Sensors` for Geolocation), `Barbatos.Wpf.Networking`,
  `Barbatos.Wpf.Storage` - per module in [reference.md](reference.md#module-map).
- Facades use MAUI's unlocked lazy singleton
  (`currentImplementation ??= new AppInfoImplementation()`), which is **not thread-safe on
  first access**. Two first touches racing (UI thread plus a background job) can build two
  `PreferencesImplementation`s that overwrite each other's file. Touch a facade first on the UI
  thread during startup.

## App identity: AppInfo and PublisherInfo

Configure from the **exe** project's csproj (values are read from `Assembly.GetEntryAssembly()`).
For a standalone app:

```xml
<PropertyGroup>
  <Product>My App</Product>                      <!-- AppInfo.Name -->
  <Company>Contoso</Company>                     <!-- PublisherInfo.Name, part of the data path -->
  <Copyright>Copyright (c) Contoso</Copyright>   <!-- PublisherInfo.Copyright -->
  <Version>1.2.0</Version>                       <!-- AssemblyVersion and FileVersion derive from it -->
</PropertyGroup>
<ItemGroup>
  <AssemblyMetadata Include="Barbatos.Wpf.ApplicationModel.AppInfo.AppId" Value="Contoso.MyApp" />
  <AssemblyMetadata Include="Barbatos.Wpf.ApplicationModel.PublisherInfo.Website" Value="https://contoso.example" />
  <AssemblyMetadata Include="Barbatos.Wpf.ApplicationModel.PublisherInfo.SupportEmail" Value="support@contoso.example" />
</ItemGroup>
```

- **Set `AppId` explicitly from the first release and never change it.** Without metadata it
  falls back to the assembly title, then the assembly name, so renaming the project silently
  moves the data folder. `PublisherInfo.Name` + `AppId` decide
  `%LocalAppData%\{Publisher}\{AppId}\`, which holds Preferences, SecureStorage, `AppDataDirectory`,
  version history and the DeviceIdentity install id; `AppId` also salts the hardware fingerprint
  and names the single-instance mutex. Changing either one (a rebrand of `<Company>` included)
  strands every existing user's data.
- `AppId` need not be a GUID. Use a GUID when it doubles as an MSI product code; otherwise a
  readable `Contoso.MyApp`, since it becomes a folder name.
- `AppInfo.AppGuid` is an `[Obsolete]` alias of `AppId`, and the `...AppInfo.AppGuid` metadata
  key a deprecated fallback read when the `AppId` key is absent
  (`AppInfoTests.ObsoleteAppGuidStillForwardsToAppId`). Rename call
  sites to `AppId`; do not delete the alias (CLAUDE.md obsoletion rule).
- `Website`/`SupportUrl`/`SupportEmail` have no MSBuild property: metadata only, else `null`.
- `AppInfo.Version` reads the entry assembly's `AssemblyName.Version`, which always has four
  parts: `VersionString` reads `"1.2.0.0"`. Show `AppInfo.Version.ToString(3)`. `BuildString`
  is `Version.Revision`, normally `"0"`.
- The SDK derives `AssemblyVersion` from `<Version>` with any prerelease suffix stripped
  (`<Version>1.3.0-beta.1</Version>` gives `1.3.0.0`, verified with a probe project), and
  `FileVersion` defaults to it, so `<Version>` alone is right even for a prerelease. Writing
  `<AssemblyVersion>$(Version)</AssemblyVersion>` with a prerelease `<Version>` fails the build
  with `CS7034`: set `<AssemblyVersion>`/`<FileVersion>` only to a numeric value, and only when
  something else already set them.
- The `...AppInfo.Version` metadata override goes through `Version.Parse`: a prerelease value
  such as `1.2.0-beta` throws `FormatException` on every read.
- **Inside this repo** `Directory.Build.props` sets `<Product>`, `<Copyright>`, `<Version>` and
  `<AssemblyVersion>` for every project: a new sample overrides all four, `<AssemblyVersion>`
  with a numeric value (`FileVersion` follows it unless set), as the Core sample does, or
  Explorer and `AppInfo.Version` report the library's version.

## Choosing where to persist

| Need | Use |
| --- | --- |
| Small app-owned values: launch count, last tab, window size, "don't show again" | `IPreferences` |
| Tokens, passwords, refresh tokens, licence keys | `ISecureStorage` |
| A value a `ConfigureXxx` feature reads from `Barbatos:<Feature>` (tray on/off, keep awake) | A JSON file added to `builder.Configuration` - Preferences is not a configuration source (`barbatos-wpf-host`, sample `SettingsStore.cs`) |
| Files, databases, logs, caches | `FileSystem.AppDataDirectory` / `FileSystem.CacheDirectory` |
| State shared between open windows while running | An Apsu store (`barbatos-apsu-store`) |

### Preferences

```csharp
// samples/Barbatos.Wpf.Core.Sample/MainViewModel.cs
LaunchCount = _preferences.Get("Sample.LaunchCount", 0) + 1;
_preferences.Set("Sample.LaunchCount", LaunchCount);
```

- Types: `string`, `int`, `bool`, `long`, `double`, `float`, `DateTime`, `DateTimeOffset`.
  `IPreferences.Set<T>` with anything else throws `NotSupportedException`; store enums as
  `int`/`string`, objects as JSON strings. Setting a `null` string removes the key.
- `sharedName` gives a separate container in the same file. `Clear()` without one clears only
  the default container (version-tracking history survives).
- Loaded once per process; **every `Set`/`Remove`/`Clear` rewrites the whole file**. Do not
  write on every slider tick - save on commit.
- Two running processes each keep their own copy and the last writer wins, silently dropping
  the other's changes. An app that can be launched twice uses `ConfigureSingleInstance()`.
- A corrupt file is read as empty without an error, and the next write replaces it.
- Plain-text JSON on disk: nothing secret goes here.

### SecureStorage

```csharp
string? token;
try
{
    token = await _secureStorage.GetAsync("Auth.RefreshToken");
}
catch (CryptographicException)
{
    // DPAPI cannot decrypt a blob written under another Windows user or machine profile.
    _secureStorage.Remove("Auth.RefreshToken");
    token = null;
}
```

- Strings only. A null/whitespace key or a `null` value throws `ArgumentNullException` at the
  call (delete with `Remove`). The `Async` methods complete synchronously.
- DPAPI current-user scope with a fixed, public entropy: it protects against other Windows
  accounts and a copied file, **not** against other code running as the same user.
- `RemoveAll()` clears the whole file, including the DeviceIdentity install id and the default
  AI key / MCP token stores. A "sign out" button removes its own keys by name.

### FileSystem

- `AppDataDirectory`/`CacheDirectory` are `...\{AppId}\Data` and `...\Cache`, created on first
  access; nothing cleans the cache, the app owns its size. `OpenAppPackageFileAsync(name)` opens
  a file next to the exe (`AppContext.BaseDirectory`), so it needs `CopyToOutputDirectory` (the
  sample's `appsettings.json` item) and throws `FileNotFoundException` when missing
  (`DirectoryNotFoundException` for a missing subfolder) - probe with
  `AppPackageFileExistsAsync`. WPF `Resource` items are not reachable this way.

## VersionTracking: first run and upgrades

```csharp
builder.ConfigureEssentials(essentials => essentials.UseVersionTracking());

// later, after the main window is shown (ShowWelcome/ShowWhatsNew are the app's own)
if (_versionTracking.IsFirstLaunchEver)
    ShowWelcome();
else if (_versionTracking.IsFirstLaunchForCurrentVersion)
    ShowWhatsNew(_versionTracking.PreviousVersion, _versionTracking.CurrentVersion);
```

- The launch is recorded when the instance is constructed (first access, or resolving
  `IVersionTracking`). `UseVersionTracking()` forces that during `Build()`, so a run that never
  reads version tracking is still recorded. `Track()` is idempotent.
- The flags are computed once and stay `true` for the whole process. The version is recorded
  before you show anything; if "shown" must survive a crash, keep your own Preferences flag.
- `CurrentVersion`/`PreviousVersion` are four-part `AppInfo.VersionString` values; compare them
  as `Version`, not as strings. A downgrade also sets `IsFirstLaunchForCurrentVersion`.
- `IsFirstLaunchForCurrentBuild` follows `BuildString` (the revision, usually `"0"`), so it does
  not fire on ordinary upgrades. Use the version flags unless you stamp the fourth part.

## Connectivity

- `NetworkAccess.Internet` means an up, non-loopback, non-tunnel adapter has a default gateway.
  Nothing is probed (a captive portal still reads `Internet`; `ConstrainedInternet` is never
  reported): use it for UI hints and treat the real request's failure as the truth.
- `ConnectivityChanged` runs OS listeners only while subscribed and is raised on the UI thread,
  only on a real change. The facade lives for the process, so a handler on a short-lived
  ViewModel keeps it alive - unsubscribe when its window closes (the sample's is a singleton).
- The facade's `Connectivity.ConnectionProfiles` is de-duplicated; the injected
  `IConnectivity.ConnectionProfiles` is not (two Ethernet adapters yield two entries).

## DeviceDisplay and DeviceInfo

- `MainDisplayInfo` describes the monitor of the **active window** (else `MainWindow`), and is
  `default(DisplayInfo)` (all zeros) until a window has a handle. Read it from `Loaded`, as the
  sample's `MainWindow` does via `MainViewModel.RefreshDisplayInfo()`.
- `Width`/`Height` are physical pixels; `Density` is window DPI / 96 (1.5 at 150 %), so WPF
  units are `Width / Density`. `MainDisplayInfoChanged` fires on
  `SystemEvents.DisplaySettingsChanged` (a display-settings change such as resolution), not when
  a window moves to another monitor.
- `KeepScreenOn` holds `SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)` on a
  background thread of its own while `true`, never on the caller's thread. Execution state is
  per thread and Windows combines all threads, so it stacks with `IKeepAwakeService` (which
  holds `ES_SYSTEM_REQUIRED` on the UI thread) and with the app's own calls; turning either off
  leaves the other in force, and it may be set and cleared from any thread. For a persisted
  toggle prefer `ConfigureKeepAwake` with `KeepAwakeOptions.KeepDisplayOn` (`barbatos-wpf-host`);
  for a temporary "while presenting", `DeviceDisplay.KeepScreenOn`.
- `DeviceInfo.Version` is the OS version: Windows 11 still reports major version 10 (build
  22000+). `Platform` is always `DevicePlatform.WPF`; `Idiom` and `DeviceType` are heuristics.

## DeviceIdentity: per-machine licensing

```csharp
var instanceId = await _deviceIdentity.GetInstanceIdAsync();
var fingerprint = await _deviceIdentity.GetHardwareFingerprintAsync();
```

| Member | What it is | Changes when |
| --- | --- | --- |
| `GetInstanceIdAsync()` | Random GUID created on first use, kept in `SecureStorage` | `securestorage.dat` is lost (data cleared, new Windows user or machine), `SecureStorage.RemoveAll()`, `AppId`/`<Company>` change |
| `GetHardwareFingerprintAsync()` | 64-char uppercase hex SHA-256 of `AppId` + board/BIOS serials + CPU id via WMI | Hardware swap, `AppId` change; falls back to `Environment.MachineName` when WMI is locked down |

- An ordinary uninstall/reinstall leaves `%LocalAppData%` - and the instance id - in place; do
  not describe it as "resets on reinstall". Use it alone when an activation may reset with the
  app's data; add the fingerprint when deleting that data or switching Windows user must not
  reset a per-machine activation count. To reset it deliberately, remove the
  `Barbatos.Wpf.DeviceIdentity.InstanceId` key from `ISecureStorage`.
- Raw serials are never stored or returned and the `AppId` salt makes fingerprints incomparable
  across apps - keep both properties. Both values are still personal data once a server links
  them to a customer (README privacy note). No client-side IP lookup: the licence server already
  sees the caller's address, and IP is a soft signal (NAT, VPN).
- The fingerprint does WMI work once per process on the thread pool: load it on demand, as
  `GreetingService.GetDeviceIdentityDescriptionAsync` does. `GetInstanceIdAsync` serializes its
  read-or-create, so concurrent first calls in one process get the same id; two processes
  starting at once can still each create one (last write wins on disk).

## Launcher and Email

```csharp
await _launcher.OpenAsync("https://example.com");
await _launcher.OpenAsync(new OpenFileRequest("Logs", FileSystem.AppDataDirectory));
await Email.ComposeAsync("Bug report", body, PublisherInfo.SupportEmail!);
```

- `Launcher` is `Process.Start` with `UseShellExecute = true`. The `string` overloads build a
  `Uri`, so a relative path throws `UriFormatException` - open files and folders with
  `OpenFileRequest`. The result is `true` whenever `Process.Start` did not throw - including a
  hand-off to an already-running or COM-activated app, where no `Process` comes back - and
  `false` when the shell refused the target (no handler, a missing file). `false` is a real
  failure worth reporting.
- `CanOpenAsync` checks `HKEY_CLASSES_ROOT\<scheme>` for a handler; `TryOpenAsync` is
  `CanOpenAsync` then open.
- `Email` is Simple MAPI through its Unicode entry point `MAPISendMailW`: it opens the default
  desktop mail client's compose window, and Vietnamese or other non-code-page text survives
  (a client implementing only the ANSI call gets the stub's conversion, the one case where
  `?` can still appear). `IsComposeSupported` is always `true`; whether a client answers is
  only known by calling. With no usable client `ComposeAsync` throws
  `FeatureNotSupportedException` - catch it and offer a `mailto:` link through `Launcher`. A
  user cancelling the compose window is a normal completion.
- `EmailBodyFormat.Html` throws `FeatureNotSupportedException`. Attachments are
  `EmailAttachment(fullPath)`; one that does not exist throws `FileNotFoundException` before any
  client starts. Any other MAPI error is an `InvalidOperationException` naming the code.

```csharp
try
{
    await _email.ComposeAsync("Bug report", body, supportAddress);
}
catch (FeatureNotSupportedException)
{
    await _launcher.OpenAsync($"mailto:{supportAddress}?subject={Uri.EscapeDataString("Bug report")}");
}
```

## AppActions: the taskbar Jump List

```csharp
// samples/Barbatos.Wpf.Core.Sample/WpfProgram.cs
builder.ConfigureEssentials(essentials => essentials
    .AddAppAction("open", "Open", "Show the main window")
    .OnAppAction(action => LogLifecycleEvent($"App action activated ({action.Id})"))
    .UseVersionTracking());
```

- A click launches a **new process** with `BARBATOS_APP_ACTIONS-<base64 id>` on its command line.
  `UseEssentials()` matches it in the `WpfLifecycle.OnStartup` event against the actions set in
  *that* process, which `ConfigureEssentials` applies during `Build()`. Actions added later with
  `AppActions.SetAsync` are not recognised on relaunch unless they are declared again at startup.
- Handle activations with `.OnAppAction(...)` in `ConfigureEssentials`, or with
  `AppActions.OnAppAction +=` placed **before** `base.OnStartup(e)` (the sample's `App.xaml.cs`
  does). The lifecycle event fires inside `base.OnStartup(e)`, so a subscription after it never
  sees the activation. The handler runs before the main window exists - showing or activating
  `Application.Current.MainWindow` from it finds no window on a cold start: record the action id
  and act on it after `MainWindow.Show()`, as `App.OnStartup` in the sample does.
- With `ConfigureSingleInstance()` and the app already running, the new process exits inside
  `Build()` before `OnStartup`: the action is lost and the running instance only receives
  `SecondInstanceLaunched` (no arguments). Only cold-start activations work in that combination.
- `SetAsync` replaces any Jump List declared in `App.xaml`, hides the Recent/Frequent categories
  and needs a running `Application`; failures inside `ConfigureEssentials` are logged as
  "App Actions could not be applied." and never stop startup. `GetAsync` returns the last set
  list from this process - WPF's `JumpList` cannot be read back.

## Installer publishing, InstallDate and InstallLocation

`AppInfo.InstallDate`/`InstallLocation` read `...\Uninstall\{name}`, the name being the
`Barbatos.Wpf.ApplicationModel.AppInfo.UninstallRegistryKey` metadata or, by default, `AppId`
verbatim; both are `null` (never an exception) when not installed - normal under the IDE.
**Inno Setup** always names its key `{AppId}_is1`: put that in `UninstallRegistryKey` and keep
`AppId` clean, since it is also the data-folder name. **MSI/WiX** keys by product code: make
`AppId` that GUID. Lookup order, date format and the `[Setup]` mapping:
[reference.md](reference.md#installer-field-mapping).

## Not available on Windows: Contacts, Geolocation, some Permissions

- `Contacts` and `Geolocation` queries throw `FeatureNotSupportedException` by design (they need
  WinRT contracts and packaging); do not "fix" them with stubs returning fake data. The type
  surface exists so MAUI-shared code compiles; `Geolocation.IsEnabled` is `false` and
  `Location.CalculateDistance(...)` works.
- A real implementation is app code, `builder.Services.AddSingleton<IContacts, MyGraphContacts>();`,
  seen only by injected `IContacts`/`IGeolocation` consumers; the facades keep throwing.
- `Permissions` is static and generic, with no DI interface. `ContactsRead`, `ContactsWrite`,
  `LocationWhenInUse`, `LocationAlways`, `Microphone` and `Sensors` throw; every other type
  returns `Granted` **without checking anything** - `PostNotifications` says nothing about
  toasts (read `INotificationService.Availability`, `barbatos-wpf-host`). For a real check,
  subclass `Permissions.BasePlatformPermission` ([reference.md](reference.md#permissions-on-windows)).

## Hard rules

- Identity lives in the exe's csproj, never in DI: replacing `IAppInfo` renames the
  single-instance mutex but not the data folder. `AppId` and `<Company>` freeze at first release.
- Secrets go to `SecureStorage`, never `Preferences`; `SecureStorage.RemoveAll()` is not a sign-out.
- Replace an Essentials service with `AddSingleton`, not `TryAdd*`; `FeatureNotSupportedException`
  modules stay honest, and a real implementation is an app-side registration.
- Per CLAUDE.md, no `InternalsVisibleTo` to reach `SetCurrent`/`SetDefault`: tests hit the real
  per-user store with unique keys (`$"Test.{Guid.NewGuid():N}"`, as in `PreferencesTests`).

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Settings, secrets or what's-new history gone after a rename or rebrand | Data path is `{Company}\{AppId}`; `AppId` fell back to the assembly name, or `<Company>` changed | Set `AppId` metadata; restore the old values or copy the old folder once |
| Two apps in one solution report the same name/publisher | `<Product>`/`<Company>` set in a shared `Directory.Build.props` | Set them per project, or use the `...AppInfo.Name` / `...PublisherInfo.Name` metadata |
| About box shows `1.2.0.0`; or `AppInfo.Version` throws `FormatException` | Four-part assembly version; non-numeric `...AppInfo.Version` metadata | `AppInfo.Version.ToString(3)`; numeric metadata or none |
| `IsFirstLaunchForCurrentBuild` never true after an update | `BuildString` is the revision, usually `0` | Use `IsFirstLaunchForCurrentVersion` |
| `InstallDate` null after an Inno Setup install | Key is `{AppId}_is1` | `UninstallRegistryKey` metadata |
| A preference "saved" earlier is gone | Second process rewrote the file, or a corrupt file was read as empty | `ConfigureSingleInstance()`; never hand-edit `preferences.dat` |
| `SecureStorage.GetAsync` throws `CryptographicException` | Blob from another user/machine profile | Catch, `Remove` the key, ask again |
| Licence server sees a new install after "sign out" | `SecureStorage.RemoveAll()` deleted the instance id | Remove only your own keys |
| Online indicator says Internet but requests fail | Gateway heuristic, no probe | Trust the request result |
| ViewModel never collected after its window closes | Handler left on a facade event (`ConnectivityChanged`, `MainDisplayInfoChanged`, `OnAppAction`) | Unsubscribe on close |
| `MainDisplayInfo` is all zeros | No window handle yet | Read it in `Loaded` |
| Jump List click does nothing | Handler subscribed after `base.OnStartup`; action not declared in `ConfigureEssentials`; or app already running under single instance | `OnAppAction` in `ConfigureEssentials` (or subscribe before `base.OnStartup`); declare at startup; accept the single-instance limit |
| Jump List handler runs but the window does not come forward | Handler acted on `MainWindow` during startup, before it exists | Record the id; act after `MainWindow.Show()` |
| `Email.ComposeAsync` throws `FeatureNotSupportedException` | No Simple MAPI client answered (none installed or default), or an HTML body | Catch it and offer a `mailto:` link via `Launcher` |
| `Launcher.OpenAsync` returns `false` | The shell refused the target: no handler, missing file | Report it - a hand-off to a running app already returns `true` |
| Replacement service ignored (`Contacts.PickContactAsync()` still throws, own `IPreferences` unused) | Facades ignore DI; an app-side `TryAdd*` loses to `UseEssentials()` in `CreateBuilder()` | Inject the interface; register with `AddSingleton` |

## Adding or changing an Essentials module (library work)

Load `barbatos-package-authoring` as well. Then:

1. `src/Barbatos.Wpf.Core/Essentials/<Module>/`: public `IXxx`, a public static `Xxx` facade
   (`Current`/`Default` via `??=`, an `internal static` `SetCurrent`/`SetDefault`), an
   internal `XxxImplementation` on Win32/.NET - not WinRT - whose `<remarks>` name the MAUI counterpart.
2. Register it in `UseEssentials()` as `TryAddSingleton<IXxx>(sp => Xxx.Current)`. Unsupported
   on Windows: keep the type surface, throw `FeatureNotSupportedException` naming the WinRT API.
3. Tests: warm the facade in `tests/Barbatos.Wpf.Core.UnitTests/ModuleInit.cs` (the `??=` race
   under parallel xUnit), add an `Assert.Same(Xxx.Current, wpfApp.Services.GetService<IXxx>())`
   line to `EssentialsExtensionsTests`, then the three `AppInfoTests.cs` shapes - cached,
   registered and `Assert.Same` as the facade, absent without defaults. Run per TFM
   (`barbatos-wpf-testing`).
4. Docs: the README Essentials table and section, the API-REFERENCE namespace section
   (`barbatos-docs-sync`), a line in the sample's `GreetingService.cs`/`MainViewModel.cs`, and a
   row in this skill's [reference.md](reference.md#module-map).
5. A new metadata key or a changed fallback chain is a behaviour change for shipped apps: update
   the template csproj comments too (`barbatos-templates`).

## Related skills

- `barbatos-wpf-host` - `WpfProgram`, DI, lifecycle events, single instance, keep awake,
  notifications, settings files for `Barbatos:<Feature>` sections.
- `barbatos-mcp-ai` (keys and tokens on `ISecureStorage`), `barbatos-apsu-store` (in-memory
  shared state), `barbatos-package-authoring`, `barbatos-wpf-testing`, `barbatos-docs-sync`,
  `barbatos-templates`.
