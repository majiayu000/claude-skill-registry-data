---
name: barbatos-package-authoring
description: "Change the Barbatos.Wpf libraries in src/ and their build - public API design (ConfigureXxx on WpfAppBuilder, AddXxx/UseXxx, TryAdd*, Setup.Resolve, Validate(), [Obsolete] renames), csproj/TFMs, Directory.Packages.props, C# 14 on net8/9/10, XmlnsDefinition, strong naming and the NuGet release workflow. Use when adding or reviewing public API, deprecating a member, adding a dependency to a library or a new package, preparing a release or version bump (every file that pins it), or when restore fails with NU1605/NU1008, nuget.org still shows the old version, or a new aq: control is not found in XAML. For app-side use, load the feature skill. Vietnamese prompts too - thêm API công khai, sửa thư viện trong src, đánh dấu lỗi thời, thêm gói NuGet, phát hành phiên bản mới, tăng version, ký strong name."
---

# Changing the Barbatos.Wpf libraries

You are changing four published NuGet packages, not an app: public API is the product, and a
careless signature is a breaking change in someone else's code. This skill covers API design,
project files, packaging and release. It is not about consuming a feature (load the feature
skill), writing tests (`barbatos-wpf-testing`), wording the docs (`barbatos-docs-sync`) or the
`dotnet new` templates (`barbatos-templates`). CLAUDE.md's non-negotiables apply throughout;
this skill gives the detail behind them.

## Sources of truth

- Build: [`Directory.Build.props`](../../../Directory.Build.props),
  [`Directory.Build.targets`](../../../Directory.Build.targets),
  [`Directory.Packages.props`](../../../Directory.Packages.props),
  [`nuget.config`](../../../nuget.config), [`Barbatos.Wpf.slnx`](../../../Barbatos.Wpf.slnx),
  [`.editorconfig`](../../../.editorconfig), the four `src/*/*.csproj`.
- Release: [`.github/workflows/barbatos-wpf-cd-nuget.yml`](../../../.github/workflows/barbatos-wpf-cd-nuget.yml).
- Precedent code to copy: a Core feature entry point,
  [`Essentials/KeepAwake/AppHostBuilderExtensions.cs`](../../../src/Barbatos.Wpf.Core/Essentials/KeepAwake/AppHostBuilderExtensions.cs);
  the two-call split,
  [`AquariusServiceCollectionExtensions.cs`](../../../src/Barbatos.Wpf.Aquarius/Composition/AquariusServiceCollectionExtensions.cs)
  and [`AquariusRouterServiceCollectionExtensions.cs`](../../../src/Barbatos.Wpf.AquariusRouter/Routing/AquariusRouterServiceCollectionExtensions.cs);
  the construction rule, `Setup.Resolve` in
  [`Setup.cs`](../../../src/Barbatos.Wpf.Aquarius/Composition/Setup.cs); a rename,
  `IAppInfo.AppGuid` in [`AppInfo.cs`](../../../src/Barbatos.Wpf.Core/Essentials/AppInfo/AppInfo.cs);
  XAML namespaces, [`AssemblyInfo.cs`](../../../src/Barbatos.Wpf.Aquarius/AssemblyInfo.cs).
- Tests that pin the conventions: `RunOnStartupFeatureTests.ConfigurationOverridesCodeValues`,
  `TrayIconFeatureTests` (fake platform registered before `ConfigureTrayIcon`),
  `McpOAuthTests.OAuthServicesAreRegisteredByConfigureMcpAndAreReplaceable`, fakes in
  `FeatureTestFakes.cs` (all in `tests/Barbatos.Wpf.Core.UnitTests/`);
  `AquariusDependencyInjectionTests.cs` and `AquariusRouterDependencyInjectionTests.cs`.
- "Already native" precedent: Aquarius [Patterns that are already native](../../../src/Barbatos.Wpf.Aquarius/README.md#patterns-that-are-already-native),
  the run-it-yourself table under [KeepAlive](../../../src/Barbatos.Wpf.Aquarius/README.md#keepalive),
  Valee [Already native: error display](../../../src/Barbatos.Wpf.AquariusValee/README.md#already-native-error-display).

MSBuild mechanics, the release workflow step by step, the `NoWarn` precedents and the
new-package checklist: [build-and-release.md](build-and-release.md). Read it before touching
any `Directory.*` file, a `.csproj`, the workflow, or before releasing.

## Before writing anything

Answer these three, in order:

1. **Does WPF already do this?** `{Binding}`, `ItemsControl` + `DataTemplate`,
   `ContentControl.Content`, the `INotifyDataErrorInfo` adorner, `Preview*` tunneling events and
   `new LengthAttribute(n, n)` were all recognized as native and got a README note, not new API.
   Verify claims about WPF's native behaviour **by running it**: the `TabControl`/`Frame`
   keep-alive table exists because the assumption was wrong.
2. **Which package owns it?** Aquarius stays Core-free and container-free. Router and Valee may
   use Aquarius. A third `src/` → `src/` reference, or a new package, needs the maintainer's yes.
3. **Is it reachable through DI?** If not, redesign it until it is.

When porting a Vue / Vue Router / vee-validate / Pinia concept, read that project's own docs and
copy its usage shape; an invented "better" design gets rejected. Say in `<remarks>` where the
port differs and why (`RouteRecord`, `RouteMatcher` are the model).

## Where the code goes

- **Core** folders do not match namespaces (`IDE0130` is off on purpose): the tray lives in
  `Essentials/TrayIcon/` but in `namespace Barbatos.Wpf.Tray`; power in `Barbatos.Wpf.Power`,
  hotkeys in `Barbatos.Wpf.Input`. Copy the neighbouring files' namespace, never derive it from
  the path. Core's `RootNamespace` is `Barbatos.Wpf`.
- Each opt-in Core feature's `ConfigureXxx` lives in a `public static partial class
  AppHostBuilderExtensions` in `namespace Barbatos.Wpf.Hosting`, in a file named
  `AppHostBuilderExtensions.cs` inside the feature folder. `ConfigureLifecycleEvents`
  (`WpfAppHostBuilderExtensions`, `Barbatos.Wpf.LifecycleEvents`) and `ConfigureEssentials`
  (`EssentialsExtensions`) are the exceptions; do not copy their shape.
- **Aquarius / Router / Valee** namespaces match folders (`Barbatos.Wpf.AquariusRouter.Matching`).
  A new namespace that holds XAML-usable types needs an `XmlnsDefinition` line (below).
- Public interface, `internal sealed` implementation, reached through DI:
  `ITrayIconService`/`TrayIconService`, `ITrayIconPlatform`/`Win32TrayIconPlatform`. Tests resolve
  the interface from the container, so the implementation never has to be public.

## DI entry points

### Core: `ConfigureXxx(this WpfAppBuilder)`

Adapted from `Essentials/KeepAwake/AppHostBuilderExtensions.cs`:

```csharp
namespace Barbatos.Wpf.Hosting;

public static partial class AppHostBuilderExtensions
{
    /// <summary>... configured from code via <paramref name="configure"/> and/or from the
    /// <c>Barbatos:Xxx</c> configuration section (configuration values override code values) ...</summary>
    public static WpfAppBuilder ConfigureXxx(this WpfAppBuilder builder, Action<XxxOptions>? configure = null)
    {
        var options = builder.Services.AddOptions<XxxOptions>();
        if (configure != null)
            options.Configure(configure);
        options.Bind(builder.Configuration.GetSection(XxxOptions.SectionName));

        builder.Services.TryAddSingleton<IXxxPlatform, Win32XxxPlatform>();
        builder.Services.TryAddSingleton<IXxxService, XxxService>();
        builder.Services.TryAddEnumerable(ServiceDescriptor.Singleton<IWpfInitializeService, XxxInitializer>());

        return builder;
    }

    class XxxInitializer : IWpfInitializeService
    {
        public void Initialize(IServiceProvider services)
        {
            if (services.GetRequiredService<IXxxService>() is XxxService service)
                service.ApplyOptions();
        }
    }
}
```

- `XxxOptions` carries `public const string SectionName = "Barbatos:Xxx";`.
- **`Configure` before `Bind`.** Options run in registration order, so binding last is what makes
  file values beat code values. `RunOnStartupFeatureTests.ConfigurationOverridesCodeValues` pins it.
- **Everything `TryAdd*`**, so an app (or a test) that registers its own platform or service
  *before* calling `ConfigureXxx` keeps it, and a second `ConfigureXxx` call registers no service
  twice. `TryAddEnumerable` dedupes the initializer by implementation type.
- **OS interop goes behind a public `IXxxPlatform`** so the service runs headless in tests
  (`ITrayIconPlatform`, `INotificationPlatform`, `IHotkeyPlatform`, `IStartupRegistrar`,
  `IPowerManager`; fakes in `FeatureTestFakes.cs`).
- **OS side effects start in the initializer's `internal ApplyOptions()`, not in a constructor.**
  The `is XxxService` check means an app's replacement service is left alone.
- **An initializer must not throw for a recoverable failure.** `IWpfInitializeService.Initialize`
  runs synchronously inside `Build()` with no surrounding try/catch, so an exception crashes app
  startup. `McpInitializer` (in `Essentials/Mcp/AppHostBuilderExtensions.cs`) fires each server
  connection and logs failures instead.

A new Essentials service follows a different shape (interface + static facade with a lazy
`Current`/`Default` + a `TryAddSingleton<IXxx>(sp => Xxx.Default)` line in `UseEssentials`, and a
warm-up line in the Core tests' `ModuleInit.cs`); load `barbatos-wpf-essentials` for it.

### Aquarius / Router / Valee: `AddXxx` declares, `UseXxx` wires

```csharp
builder.Services.AddAquariusRouter(sp => AppRoutes.Build(sp.GetRequiredService<AuthState>()));
var app = builder.Build();
app.Services.UseAquarius();
app.Services.UseAquariusRouter();
```

(from `samples/Barbatos.Wpf.AquariusRouter.Sample/WpfProgram.cs`)

- XAML-driven resolution (`aq:Setup.Enable`, `Component.Is`, `RouterView`) has no constructor to
  inject into, so it reads an ambient static (`Setup.ServiceProvider`, `Router.Current`).
  `UseXxx` is the one place that assigns it, once, after `Build()`.
- `AddXxx` only declares: no resolving, no statics. It must be safe to omit, and `UseXxx` must
  work without it (`UseAquariusStillWiresTheProviderWhenAddAquariusWasNeverCalled`).
- `UseXxx` returns the provider when the next call chains (`UseAquarius`) or the object the next
  line needs (`UseAquariusRouter` returns the `Router` for `Start`).
- Take a factory (`Func<IServiceProvider, ...>`) whenever the registration needs DI-resolved
  input, as `AddAquariusRouter`'s `routes` parameter does.
- Two static classes per package, `XxxServiceCollectionExtensions` and
  `XxxServiceProviderExtensions`, in one file; `ArgumentNullException.ThrowIfNull` on entry.
  Aquarius and Router have them; Valee has no DI entry point yet.
- Their only `Microsoft.Extensions` references are `DependencyInjection.Abstractions` and
  `Options` (Valee gets both through Aquarius), beside `CommunityToolkit.Mvvm`. Never build or
  own a container; adding any package (a configuration binder included) needs the maintainer's
  yes. Nothing in them binds `AquariusOptions.SectionName` or `RouterOptions.SectionName`: the
  `AddAquarius`/`AddAquariusRouter` docs say options come from code, and show the one-line
  `AddOptions<…>().Bind(…)` an app adds itself. A new `AddXxx` documents the same way.
- Tests that call `UseXxx` must save and restore the statics it writes (`WithRestoredStatics`,
  `WithRestoredCurrent` in the two DI test files).

### One construction path: `Setup.Resolve`

Anything the Aquarius family builds on the app's behalf (a View, a ViewModel, a routed window)
goes through `Setup.Resolve(Type)`: `Setup.ServiceProvider?.GetService(type)`, else
`Activator.CreateInstance(type)`. `Component`, `Router` and `RouterWindows` all call it. Do not
add a second path. An unregistered type therefore needs a public parameterless constructor.

## Type design

| Convention | Precedent in `src/` |
| --- | --- |
| `sealed` for a new type | `AquariusOptions`, `RouterOptions`, `RouteRecord`, `PeriodicSchedule`, `InterceptorHandle` |
| Never seal a shipped unsealed type - that is breaking | Core's `*Options`, the MCP descriptors, controls such as `SlotHost` (subclassed for its `protected` members) |
| Apsu stores non-`sealed` with `virtual` `[Action]` methods | `StoreBase` - Castle DynamicProxy subclasses them |
| Reference type when identity is the meaning | `RouteRecord` ("A deliberate reference type (not a record)") |
| `sealed record` for resolved, compared-by-value data | `RouteLocation`, `PathToken`, `NavigationFailure`, `RouteSearchResult` |
| `required` init members for shapes built in code | `RouteRecord.Path`, `RouteLocation.Path`, `PushNotification.Title` |
| Settable, nullable members + `Validate()` for shapes bound from configuration | `McpServerDescriptor.Name` is `string?`, enforced by `Validate()` |
| Pure `Validate()`, throws `InvalidOperationException`, no I/O - a settings UI's pre-flight | `PeriodicSchedule`, `McpServerDescriptor`, `McpOAuthOptions`, `AiProviderDescriptor`, `AiAgentDescriptor` |
| `ArgumentException` for a duplicate name, `InvalidOperationException` for an invalid one | `IPeriodicServiceScheduler.Register`, `IMcpServerRegistry.AddServerAsync` |
| A registration returns its undo | `Router.BeforeEach` and `Watch.On` return `IDisposable`; `AddStoreInterceptor(..., out InterceptorHandle)` |
| Strictness is opt-in, default `false` | `Setup.ThrowOnUnresolved`, `Expr.ThrowOnUnresolvedIdentifiers` |
| An attached property throws on the wrong element type | `Directives.Model`, `Valee.Numeric`, `TeleportHost.RegisterHost`, `RouterLink.To` |
| Generic type parameters that get constructed are annotated, not suppressed | `[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)]` on `ConfigurePeriodicServices<TService>`, `AddStore<TStore>`, `AddStoreInterceptor<TStore, TInterceptor>` |

XML docs on every public type and member (`CS1591` is a warning for `src/**.cs`). `<remarks>`
records the decision, what it was chosen over, and what was verified by running it.

## XAML namespaces

Each Aquarius-family package maps every CLR namespace onto one URI in its `AssemblyInfo.cs`:

```csharp
[assembly: XmlnsDefinition("http://schemas.barbatos.co/aquariusvalee/2026/xaml", "Barbatos.Wpf.AquariusValee.Xaml")]
[assembly: XmlnsPrefix("http://schemas.barbatos.co/aquariusvalee/2026/xaml", "aqv")]
```

- A new CLR namespace gets its own `XmlnsDefinition` line; `XmlnsPrefix` stays one per URI.
  Without it XAML reports the tag as missing from the `aq:`/`aqr:`/`aqv:` namespace.
- The URIs (including `2026`) are public API baked into every consumer's XAML. Never change one.
- Core has no URI mapping: XAML reaches it with `clr-namespace:`, as the template's and samples'
  `App.xaml` do with `xmlns:hosting="clr-namespace:Barbatos.Wpf.Hosting;assembly=Barbatos.Wpf.Core"`.

## C# 14 on three runtimes

`LangVersion` is `14.0` (from `Directory.Build.props`) but every library compiles for net8,
net9 and net10. Compiler-only features (`field`, `extension(...)` blocks, collection
expressions, primary constructors, `required`, list patterns, `obj?.Prop = value`) work on all
three. Anything whose *type* ships in the runtime needs `#if NET9_0_OR_GREATER` /
`#if NET10_0_OR_GREATER` or is not used. `src/` currently has no such guard: locking uses
`readonly object _fileLock = new();` + `lock (_fileLock)` (`PreferencesImplementation.cs`), not
`System.Threading.Lock`. A build only proves this if all three TFMs compiled.

## Removing, renaming and other breaks

- **Rename = keep the old member, `[Obsolete]`, returning the identical value.** `IAppInfo.AppGuid`
  is a default interface member (`string AppGuid => AppId;`) so existing implementers keep
  compiling; the static facade's `AppInfo.AppGuid` is obsoleted too; the old
  `Barbatos.Wpf.ApplicationModel.AppInfo.AppGuid` metadata key is still read as a fallback; the
  message names the replacement and the reason. Docs keep the old member, marked deprecated.
- Deleting public API happens only in a deliberate major release.
- **Adding a member to a public interface an app may implement** (`IRouterHistory`,
  `IAiApiKeyProvider`, `IMcpTokenStore`, the platform interfaces) breaks every implementer. Give
  it a default implementation, as `AppGuid` does, or add a new interface.
- Changing a default value, an exception type, or when a callback fires is a behaviour break:
  say so in the docs (`barbatos-docs-sync`).

## No `InternalsVisibleTo`

Per CLAUDE.md, never. When a test needs internal behaviour, that behaviour becomes real public
API with its own use case (`RouteMatcher` is public as "a real, independently useful, directly
unit-testable" type; `Expr.Evaluate` is the C#-callable counterpart of `{aq:Expr}`), or the test
goes through the public surface: DI-resolved interfaces, or a test subclass that exposes
`protected` members (`TestSlotHost` in `SlotHostTests.cs`). Weigh that before making something
`internal` in the first place.

## Project files, dependencies, packing

Detail and the reasons: [build-and-release.md](build-and-release.md). The rules that bite:

- A `src/` project file carries only its identity: `PackageId`, `TargetFrameworks`,
  `GeneratePackageOnBuild`, `UseWPF`, `CommonTags`, `Description`, `RootNamespace`,
  `PackageIconSourceFile`, a commented `NoWarn`, and its references. Never set `LangVersion`,
  `Nullable`, `ImplicitUsings` or a version there.
- Core uses `net10.0-windows10.0.17763.0;net9.0-windows10.0.17763.0;net8.0-windows10.0.17763.0`
  (WinRT projections for toasts); the other three use bare `netX.0-windows`. Per CLAUDE.md, never
  add a `netstandard`/`net6`/`net7` target or a shim for one.
- A non-Core package overrides `CommonTags` wholesale; the shared value is Core's tag list, whose
  words would mislead NuGet search for any other package.
- Versions only in `Directory.Packages.props`. `Microsoft.Extensions.AI*` moves with the floor
  `ModelContextProtocol.Core` depends on (the comment above them names it).
- Every new `NoWarn` code gets a comment naming the exact reflection call and why it is
  inherently dynamic. WPF is never trimmed, but the analyzers run on every project.
- **A project whose name contains `Test` is a test project** (`Directory.Build.props` decides
  from `MSBuildProjectName`): not packable, not packed, not signed. Never name a package so.

## Versioning and release

- One `<Version>` (and a matching numeric `<AssemblyVersion>`) in `Directory.Build.props` versions
  all four packages together. The `barbatos-wpf-app` template repeats it: `template.json`
  (`replaces` and `defaultValue`), the four `Version="..."` attributes in `BarbatosWpfApp.csproj`,
  and the default quoted in `templates/README.md`. Move them in the same commit
  (`barbatos-templates`).
- Publishing a GitHub Release (or running the workflow by hand) builds `Release` with
  `-p:SourceLinkEnabled=true`, which also strong-names the libraries with `src/barbatos.snk`
  written from the `STRONG_NAME_KEY` secret, then pushes `.nupkg` + `.snupkg` with
  `--skip-duplicate`. The release tag is never read: the version is whatever
  `Directory.Build.props` says on that commit, and an unchanged version publishes nothing while
  the run still goes green.
- The release workflow runs no tests. `barbatos-wpf-ci.yml` runs every project per TFM on pull
  requests and `main`; release only from a commit whose CI run is green (`barbatos-wpf-testing`).
- `*.snk` is git-ignored; never force-add a key or weaken that entry.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Release workflow green, nuget.org still on the old version | `--skip-duplicate` skipped a version that already exists | Bump `<Version>`/`<AssemblyVersion>` and the template copies, release again |
| Workflow fails in "Fetch the certificate" | `STRONG_NAME_KEY` secret missing, empty or not base64 | Set it (base64 of the `.snk`) where the `production` job can read it |
| `NuGet/login` step fails after a workflow edit | Trusted publishing on nuget.org is bound to this workflow file (and its environment) | Keep the file name and `environment: production`, or update the nuget.org policy |
| Local `dotnet build -c Release -p:SourceLinkEnabled=true` fails on the key file | That flag turns on signing, and `src/barbatos.snk` exists only in CI | Build without the flag locally; signing is CI's job |
| Signed CI build warns `CS8002`, local builds never do | A dependency is not strong-named; only test projects suppress `CS8002`, and only CI signs | Check a new package is strong-named before adding it |
| Restore `NU1605` after bumping `Microsoft.Extensions.AI*` | Out of step with `ModelContextProtocol.Core`'s floor | Bump both together |
| `NU1008` | `Version=` on a `PackageReference` | Move the version to `Directory.Packages.props` |
| `NU1010` | `PackageReference` with no `PackageVersion` entry | Add the `PackageVersion` line |
| Restore cannot find a package from another feed | `nuget.config` maps every pattern to nuget.org | Add the source **and** a `packageSourceMapping` entry |
| An app on bare `net10.0-windows` cannot restore Core (`NU1201`) | Core targets the SDK-suffixed TFM | Consumers use `net10.0-windows10.0.17763.0`; do not add a bare TFM to Core |
| A new control is "not found" in the `aq:` namespace | Its CLR namespace has no `XmlnsDefinition` | Add the line in that package's `AssemblyInfo.cs` |
| An app's replacement service is ignored, or both implementations end up registered | `Add*` instead of `TryAdd*`, or the app registered after `ConfigureXxx` | `TryAdd*`; document "register yours first" |
| Code values beat `appsettings.json` | `Bind` ran before `Configure` | `Configure`, then `Bind` |
| The app crashes inside `Build()` | An `IWpfInitializeService` threw | Catch and log recoverable failures in the initializer |
| A `Barbatos:Aquarius` / `Barbatos:AquariusRouter` value has no effect | Nothing in the package binds those sections | The app binds them itself after `AddAquarius`/`AddAquariusRouter` (`services.AddOptions<AquariusOptions>().Bind(configuration.GetSection(AquariusOptions.SectionName))`); adding binding to the package is a dependency change - ask |
| New package never reaches nuget.org | Not under the `/src/` folder of `Barbatos.Wpf.slnx`, or its name contains `Test` | Add it to the solution's `/src/` folder; rename |
| `IDE0073` error in the IDE (the build does not enforce code style, so CI never catches it) | Missing or altered MIT header | Copy the header from a neighbouring file |

## Checklist: a public API change

1. Three questions answered; the owning package and namespace chosen as above.
2. Reachable through DI (`ConfigureXxx`, or `AddXxx`/`UseXxx`); replaceable pieces `TryAdd*`.
3. Type design follows the table; no `InternalsVisibleTo`; renames keep an `[Obsolete]` twin.
4. XML docs with `<remarks>`; `XmlnsDefinition` for any new XAML namespace.
5. Builds for all three TFMs with no new warnings; any new `NoWarn` commented.
6. Tests added and run per TFM (`barbatos-wpf-testing`).
7. `src/<Package>/README.md` **and** `API-REFERENCE.md` updated; root `README.md` if a summary,
   the package list or the templates changed; root `API-REFERENCE.md` if a namespace was added or
   removed (`barbatos-docs-sync`).
8. The package's sample demonstrates it; a template updated if the scaffolded shape changed
   (`barbatos-templates`).
9. `grep -rn "<member or option name>" .claude/` and correct every skill claim (signature,
   default, thrown exception, ordering) the change made false; then `node .claude/evals/lint.mjs`.
   A new control, attached property or directive also follows the `Loaded`-guard and leak/XAML
   test rules in `.claude/rules/library-code.md`.

New package or release: the checklists in [build-and-release.md](build-and-release.md).

## Related skills

- `barbatos-wpf-testing` - STA helpers, leak probes, per-TFM runs.
- `barbatos-docs-sync` - README / API-REFERENCE after the change.
- `barbatos-templates` - the version copies and template symbols.
- Domain knowledge for the code you are changing: `barbatos-wpf-host`, `barbatos-wpf-essentials`,
  `barbatos-aquarius-view`, `barbatos-aquarius-router`, `barbatos-valee-form`,
  `barbatos-apsu-store`, `barbatos-mcp-ai`.
