---
name: barbatos-templates
description: "The Barbatos.Wpf dotnet new templates under templates/ - item templates aq-view and aqv-form, the barbatos-wpf-app starter project with its --Include* module flags and AquariusEffective, template.json symbols, sourceName, ide.host.json and the PackageVersion pin. Use when scaffolding a view, form or starter app, files land in ChangeMe.Namespace, installing or testing a template, adding a template or flag, a flag with no Visual Studio checkbox, a generated app that won't restore or build, or a template out of date after an API change or release. For code inside a view or form use barbatos-aquarius-view or barbatos-valee-form. Vietnamese prompts too - tạo view bằng template, tạo form bằng aqv-form, tạo dự án khởi đầu, cài template dotnet new, thêm tùy chọn template, template lỗi thời."
---

# Barbatos.Wpf `dotnet new` templates

Three templates scaffold consumer code: `aq-view` (View + ViewModel, the Vue single-file
component analogue), `aqv-form` (a validated form) and `barbatos-wpf-app` (a starter app, the
`npm create vue@latest` analogue). They are installed from their folders in this repo; nothing
packs them into a template NuGet package. The generated code is the user's code - the APIs it
calls belong to the feature skills, and the version bump itself to `barbatos-package-authoring`.

## Sources of truth

- [`templates/README.md`](../../../templates/README.md) - the user-facing description of every
  template - plus the two copies of its commands: the root
  [README Templates section](../../../README.md#templates) (install and IDE notes) and the
  scaffolding note in the Aquarius README Quick Start
  ([`src/Barbatos.Wpf.Aquarius/README.md`](../../../src/Barbatos.Wpf.Aquarius/README.md#quick-start)).
  All three must move with any template change.
- Each template's `.template.config/template.json` (and `ide.host.json` for the project
  template) plus the content files beside it. The files win over the READMEs.
- [barbatos-wpf-app.md](barbatos-wpf-app.md) - read when editing the project template or
  answering what one flag generates: every file, symbol, conditional seam and identity setting.
- APIs the templates mirror: `samples/Barbatos.Wpf.Core.Sample/WpfProgram.cs` (the
  `ConfigureXxx` calls), `samples/Barbatos.Wpf.AquariusRouter.Sample/WpfProgram.cs` (the
  `AddAquarius`/`UseAquarius` wiring), `samples/Barbatos.Wpf.AquariusValee.Sample/` (i18n).
- **No test and no CI step builds a template.** The template folders are not in
  `Barbatos.Wpf.slnx`, and `barbatos-wpf-app`'s `MainWindow.xaml` is not even well-formed XAML
  before the template engine runs. The only check is instantiating and building the output,
  which works on any OS with `-p:EnableWindowsTargeting=true` (see the loop below); running it
  needs Windows.

## The map

Layout is package, then kind, then template: `templates/<Package or Combined>/{item-templates,
project-templates}/<template>/.template.config/template.json`. An empty kind folder holds a
`.gitkeeper` so git keeps it (Core, AquariusRouter and Combined `item-templates`, and every
`project-templates` except Combined's, are placeholders).

| shortName | Folder | identity | sourceName | Symbols |
| --- | --- | --- | --- | --- |
| `aq-view` | `Barbatos.Wpf.Aquarius/item-templates/aquarius-view` | `Barbatos.Wpf.Aquarius.Templates.View` | `AquariusComponent` | `namespace` (replaces `AquariusTemplateNamespace`) |
| `aqv-form` | `Barbatos.Wpf.AquariusValee/item-templates/valee-form` | `Barbatos.Wpf.AquariusValee.Templates.Form` | `ValeeForm` | `namespace` (replaces `ValeeTemplateNamespace`) |
| `barbatos-wpf-app` | `Combined/project-templates/barbatos-wpf-app` | `Barbatos.Wpf.Templates.CombinedApp` | `BarbatosWpfApp` | `PackageVersion`, 15 `Include*` bools, computed `AquariusEffective` |

Item templates set `"preferNameDirectory": false` (files land in the current folder or `-o`);
the project template sets `true` (`-n MyApp` creates `MyApp/`).

## Using them

From the repo root, once per template:

```powershell
dotnet new install ./templates/Barbatos.Wpf.Aquarius/item-templates/aquarius-view
dotnet new install ./templates/Barbatos.Wpf.AquariusValee/item-templates/valee-form
dotnet new install ./templates/Combined/project-templates/barbatos-wpf-app
```

`dotnet new uninstall <same folder>` removes one; `dotnet new uninstall` with no argument lists
what is installed and from where.

### `aq-view` and `aqv-form`

```powershell
dotnet new aq-view -n Dashboard --namespace MyApp.Features.Dashboard
dotnet new aqv-form -n Checkout --namespace MyApp.Features.Checkout
```

- **Always pass `--namespace`.** The CLI cannot read the target project's `RootNamespace`: a
  `msbuild:`-bound symbol is silently skipped on the CLI path (confirmed by testing, per
  `templates/README.md`). The default `ChangeMe.Namespace` is deliberately fake so a forgotten
  flag is visible instead of landing in a plausible wrong namespace.
- **Pass the bare feature name to `-n`.** `sourceName` is replaced inside file and type names,
  so `-n Dashboard` yields `DashboardView` / `DashboardViewModel`; `-n DashboardView` yields
  `DashboardViewView`.
- **Keep View and ViewModel in one namespace.** Both rely on `aq:Setup.Enable="True"`, whose
  default `Setup.Resolver` maps the View's *full* name `X.YView` to `X.YViewModel` - moving the
  ViewModel to another namespace leaves `DataContext` null, silently unless
  `Setup.ThrowOnUnresolved` (or `AquariusOptions.ThrowOnUnresolvedViewModels`, applied only by
  `UseAquarius()`) is on.
- `aq-view` output: a `UserControl` with `aq:Setup.Enable` and `aq:Lifecycle.Enable` (so the
  ViewModel's lifecycle hooks fire), a code-behind with only `InitializeComponent()`, and a
  `sealed partial` `ObservableObject` with one `[ObservableProperty]`. The ViewModel is parameterless, so `Setup.Resolve`'s `Activator`
  fallback builds it; register it in DI only once it gains constructor dependencies.
- `aqv-form` output: **schema mode** (`Form.FromModel(new XModel())`) over a DataAnnotations
  model with `[Compare]` on `ConfirmPassword` - schema mode is the only mode where `[Compare]`
  can read its sibling - plus `ConfirmPassword.DependsOn(Password)`, because only
  `IDependsOnProperties` attributes get automatic re-validation and without it fixing the
  password leaves a stale "don't match" error. `HandleSubmit(onValid, onInvalid)` gates only on
  `IsSubmitting`, never validity, so an untouched submit surfaces every error.
- The consuming project needs only the package (`Barbatos.Wpf.Aquarius` /
  `Barbatos.Wpf.AquariusValee`). `CommunityToolkit.Mvvm` and its `[ObservableProperty]` /
  `[RelayCommand]` generators arrive transitively: `aq-view` and `aqv-form` output generated
  into a `barbatos-wpf-app` project (which has no direct `CommunityToolkit.Mvvm` reference)
  builds with 0 warnings, and the generated members are in the assembly.

### `barbatos-wpf-app`

```powershell
dotnet new barbatos-wpf-app -n MyApp
dotnet new barbatos-wpf-app -n MyApp --IncludeAquariusRouter true --IncludeValee true --IncludeMcp true
dotnet new barbatos-wpf-app -n MyApp --help        # every flag, description and default
dotnet new barbatos-wpf-app -n MyApp --dry-run     # the file list, nothing written
```

- Defaults: `IncludeAquarius` and `IncludeI18n` on, everything else off. Turn a default off with
  `--IncludeAquarius false`.
- Flags: Aquarius-family `IncludeAquarius`, `IncludeAquariusRouter`, `IncludeValee`; `IncludeI18n`;
  eleven Core features `IncludeSingleInstance`, `IncludeRunOnStartup`, `IncludeTrayIcon`,
  `IncludeKeepAwake`, `IncludeNotifications`, `IncludePushNotifications`,
  `IncludePeriodicServices`, `IncludeInputSystem`, `IncludeDialogs`, `IncludeMcp`,
  `IncludeSplashScreen`. What each one generates: [barbatos-wpf-app.md](barbatos-wpf-app.md).
- Router or Valee alone still references Aquarius, through `AquariusEffective` - the Aquarius
  checkbox can stay unticked while its content is included.
- `--PackageVersion` picks the `Barbatos.Wpf.*` version; it must be one that exists on the feed
  the generated project restores from.
- Visual Studio's new-project wizard renders each `Include*` symbol as a checkbox, driven by
  `ide.host.json` `symbolInfo[].isVisible` plus the symbol's `displayName` / `description`.
  Rider shows only a raw extra-parameters field, so pass the same flags there by hand.
- `IncludeTrayIcon` shows the icon from launch: `TrayIconOptions.Enabled` defaults to `false`,
  so the generated `ConfigureTrayIcon` sets `options.Enabled = true` (`Barbatos:TrayIcon:Enabled`
  in configuration still overrides it). `IncludeRunOnStartup` deliberately leaves
  `RunOnStartupOptions.Enabled` off - setting it would register the app with Windows startup on
  its first run, unasked - and adds a "Launch when Windows starts" `CheckBox` bound to
  `MainViewModel.RunOnStartupEnabled`, which calls `IRunOnStartupService.SetEnabled`.
  `IncludeKeepAwake` is registered but off, with no toggle.

## Editing a template

Template-engine syntax used here:

- C#: `#if (IncludeXxx)` / `#else` / `#endif`, expressions allowed (`#if (IncludeValee &&
  !IncludeAquariusRouter)`).
- XAML and `.csproj`: `<!--#if (IncludeXxx) -->` / `<!--#else -->` / `<!--#endif -->`, each on its
  own line like the existing ones.
- Whole files: `template.json` `sources[0].modifiers` entries of the form
  `{ "condition": "(!IncludeXxx)", "exclude": [ "File.cs", ... ] }`.

Rules that bite:

- **Replacement is plain text across every file.** `sourceName` (`BarbatosWpfApp`,
  `AquariusComponent`, `ValeeForm`) is replaced in file names and contents, so it also renames
  strings like `"BarbatosWpfAppAssistant"` - never write the token where you mean it literally.
  `PackageVersion` `replaces` the literal current version string: any other occurrence of that
  string in any template file (a comment, another package's version) is rewritten too.
- **The template engine owns every `#if` in a template `.cs` file.** A real compiler directive
  such as `#if DEBUG` is evaluated by the engine, not left for the compiler; none exist today,
  so look up the engine's `//-:cnd:noEmit` escape before adding one.
- **Gate `using` lines with the code that needs them**, and keep the MainViewModel constructor's
  comma ladder and MainWindow's split open/close layout consistent - see the seams section in
  [barbatos-wpf-app.md](barbatos-wpf-app.md#conditional-seams-that-break-when-edited).
- **Generated code is the user's code** (the `templates` and `csharp-style` rules): no MIT
  header, no repo-only conventions, comments that explain decisions to an app author. The project template
  sets `Nullable` / `ImplicitUsings` itself because it has no `Directory.Build.props`.
- **The project template references published packages** - `PackageReference` with an explicit
  `Version`, never a `ProjectReference` into `src/` - so a generated app restores anywhere. It
  is the one `.csproj` in the repo allowed to carry `Version=`.

## Testing a change (the loop)

A WPF app runs on Windows only, but it compiles anywhere the .NET SDK does: in a Linux session,
steps 1, 2 and 4 work as written with `dotnet build -p:EnableWindowsTargeting=true` (XAML
included). Only step 3's `dotnet run` and the click-through need Windows - say so when you
could not do them.

1. `dotnet new uninstall <folder>` then `dotnet new install <folder>` after every edit -
   `dotnet new` caches installed templates, so an edit is not reliably picked up otherwise.
   On a machine other sessions share, add `--debug:custom-hive <scratch folder>` to every
   `dotnet new` call (install and instantiate) so the install stays out of the user-wide cache.
2. Instantiate **outside the repo clone**. Inside it, MSBuild picks up the repo's
   `Directory.Build.props` and `Directory.Packages.props`: central package management rejects
   the template's `Version=` attributes (`NU1008`) and the app inherits the library's packaging
   settings.
3. `dotnet build`, then `dotnet run` and click through what the change touched.
4. For `barbatos-wpf-app`, cover the combinations the conditionals branch on, at least: the
   defaults; `--IncludeAquarius false --IncludeI18n false` (the no-`Setup` constructor path);
   `--IncludeAquarius false --IncludeAquariusRouter true` (`AquariusEffective` via Router);
   `--IncludeValee true` alone (inline `SignUpView`); Router + Valee + Dialogs with i18n on (the
   `/signup` route); `--IncludeRunOnStartup true` alone with `--IncludeAquarius false
   --IncludeI18n false` and again with Router or Dialogs (the last rung of `MainViewModel`'s
   constructor ladder); every flag on; `--dry-run` for file lists.
5. Against unreleased `src/` changes: pack each package to a local folder under a fresh
   prerelease version (`dotnet pack src/<Package> -c Release -o <feed> -p:Version=<next>-dev.<n>`),
   add a `nuget.config` beside the generated project listing that folder (and mapping
   `Barbatos.Wpf.*` to it if the config uses `packageSourceMapping`, as the repo's does), and
   instantiate with `--PackageVersion <next>-dev.<n>`. Do not pass `-p:SourceLinkEnabled=true`
   locally: it turns on strong-name signing with `src/barbatos.snk`, which only CI writes.
6. **Never re-pack the same version number.** NuGet resolves an already-extracted package from
   the global cache (`~/.nuget/packages`) by id + version and never re-checks the local feed.
   Bump `-dev.<n>`, or delete `~/.nuget/packages/barbatos.wpf.*/<version>/` before restoring.

## Keeping templates in step with the API and the release

Templates are documentation that compiles, so they rot silently - nothing builds them.

- **API changes:** before changing or obsoleting a public member, `grep -rn "<Member>" templates/`.
  Move the template to the replacement in the same change (a generated app must not start life
  with `[Obsolete]` warnings), and update `templates/README.md` if the scaffolded shape changed.
- **`WpfProgram.cs` wires Aquarius and the router through the library's two-call pattern**:
  `builder.Services.AddAquarius()` + `AddAquariusRouter(_ => AppRoutes.Build())` before
  `Build()`, `app.Services.UseAquarius()` + `UseAquariusRouter()` after, mirroring
  `samples/Barbatos.Wpf.AquariusRouter.Sample/WpfProgram.cs`. Keep it that way - never go back to
  assigning `Setup.ServiceProvider` or `Router.Current` by hand - and when that wiring changes,
  update the `templates/README.md` paragraph that describes the bridge.
- **Versions the project template pins** - `grep -rn "<old version>" templates/ README.md` before
  committing:
  - the four `Barbatos.Wpf.*` `Version="..."` attributes in `BarbatosWpfApp.csproj`, the
    `PackageVersion` symbol's `replaces` **and** `defaultValue`, and the default quoted in
    `templates/README.md` - all equal to `<Version>` in `Directory.Build.props`. They move in
    the release commit, which touches exactly these four files (`Directory.Build.props`,
    `template.json`, `BarbatosWpfApp.csproj`, `templates/README.md`); a generated app can
    restore that version only after the release workflow has pushed it to NuGet.org.
  - `Barbatos.i18n.Wpf` / `Barbatos.i18n.DependencyInjection`: a separate literal (not covered by
    `PackageVersion`) that should match the `Barbatos.i18n*` entries in `Directory.Packages.props`.
  - The `NuGet.Mcp.Server` version in `WpfProgram.cs`'s `IncludeMcp` block - an external tool
    run through `dotnet dnx`.
  - `TargetFramework` stays SDK-suffixed (`net10.0-windows10.0.17763.0`).

## Adding a module flag to `barbatos-wpf-app`

1. `template.json`: a `"type": "parameter"`, `"datatype": "bool"` symbol named `IncludeXxx` with
   `defaultValue` `"false"`, a `displayName` and a `description` saying what it adds.
2. `ide.host.json`: `{ "id": "IncludeXxx", "isVisible": true }` - without it Visual Studio shows
   no checkbox.
3. Gate every touch point: `#if (IncludeXxx)` in C# (code **and** its `using`),
   `<!--#if (IncludeXxx) -->` in XAML and the `.csproj` (a `PackageReference` if it needs a new
   package), and a `sources[0].modifiers` `exclude` entry for each file only it needs. If it
   depends on Aquarius, add it to the `AquariusEffective` expression.
4. `templates/README.md`: the module list, the flag example if useful, and the Core feature
   count ("11 independently-optional features") when it is a Core flag.
5. Test the flag on and off, alone and combined with the flags whose code it shares a file
   with.

## Adding a new template

1. Folder `templates/<Package>/<item-templates|project-templates>/<kebab-name>/`; delete that
   kind folder's `.gitkeeper` once it holds a real template.
2. `.template.config/template.json` modelled on the closest existing one: same `$schema` and
   `author`, `classifications`, `identity` `Barbatos.Wpf.<Package>.Templates.<Name>` (stable -
   changing it later installs as a different template), `shortName` prefixed like the XAML
   namespace (`aq-`, `aqv-`, and by that convention `aqr-` for the router), `tags` `language` /
   `type`, a distinctive `sourceName` used in the file names, and `preferNameDirectory`.
3. An item template copies the `namespace` symbol: a unique `replaces` token and
   `defaultValue` `ChangeMe.Namespace`.
4. Content follows the current API and the repo's own samples; comments explain decisions to
   the app author.
5. Docs in the same change: `templates/README.md` (layout tree, install and uninstall lists, a
   section for the template), the root `README.md` Templates section, the package README's
   scaffolding note if it has one (Aquarius's Getting Started does), and the template list in
   CLAUDE.md's repository map.
6. Run the test loop above.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| `dotnet new aq-view` reports no such template | Not installed (installs are per folder, per machine) | `dotnet new install <folder>` |
| Generated files are in `ChangeMe.Namespace` | `--namespace` omitted | Regenerate with `--namespace`, or fix both files by hand |
| Generated View shows nothing, `DataContext` is null | ViewModel moved to another namespace or renamed away from `XView` → `XViewModel` | Keep them paired, or use `aq:Setup.ViewModel="{x:Type ...}"` |
| Edited a template, output unchanged | Stale install | Uninstall, then install the folder again |
| A new flag has no checkbox in Visual Studio | Missing `ide.host.json` `symbolInfo` entry | Add `{ "id": ..., "isVisible": true }` |
| A flag is off but its file or code is still generated | Code not wrapped in `#if`, or the file has no `modifiers` `exclude` | Gate it; whole files need the `exclude` |
| `NU1008` when building a generated app | Instantiated inside the repo; central package management applies | Instantiate outside the clone |
| Restore fails to find `Barbatos.Wpf.*` | `--PackageVersion` (or the pinned default) not on any configured feed | Use a published version, or the local-feed loop |
| `The tag 'RouteTo' does not exist in XML namespace ...` against a local pack | Global packages cache still holds an older build of the same version | New `-dev.<n>` version, or delete the cached folder |
| `--IncludeTrayIcon true` but no tray icon | `Barbatos:TrayIcon:Enabled` is `false` in configuration (it overrides code), or `options.Enabled = true` was removed from `ConfigureTrayIcon` - the option defaults to `false` | Remove the configuration value or restore the line; `ITrayIconService.SetVisible(true)` shows it at runtime |
| "Launch when Windows starts" is ticked but the app does not start at sign-in | The user switched it off in Task Manager's (or Settings') Startup apps list: Windows records that apart from the `HKCU\...\Run` value, which `IRunOnStartupService.IsEnabled` reads, so the box still shows ticked | Switch it back on there; the box cannot see or change that switch |
| Clicking a search result throws `InvalidOperationException` ("is searchable but its RouteRecord has no Name") | A route added to `AppRoutes.cs` with `Search` entries but no `Name` | Give every searchable route a `Name` |

## Related skills

- `barbatos-aquarius-view` - what goes inside an `aq-view` output; `Setup` resolution.
- `barbatos-valee-form` - the `aqv-form` and SignUp forms.
- `barbatos-aquarius-router` - `AppRoutes.cs`, `RouterView`, search.
- `barbatos-wpf-host` - the `ConfigureXxx` features behind the Core flags and the splash screen.
- `barbatos-wpf-essentials` - the csproj identity block (`AppId`, `Company`, version properties).
- `barbatos-mcp-ai` - what `IncludeMcp` sets up.
- `barbatos-package-authoring` - the release and version bump the template follows.
- `barbatos-docs-sync` - the README updates a template change carries.
