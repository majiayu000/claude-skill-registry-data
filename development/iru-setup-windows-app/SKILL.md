---
name: iru-setup-windows-app
description: >-
  Scaffold a new Windows desktop app on .NET 10 / C# 14 at the repository root — `global.json` (SDK pinned,
  `rollForward: latestFeature`), `Directory.Build.props` (the app `<Version>` `x.y.z[-dev]`, nullable, implicit usings,
  warnings as errors, `AnalysisLevel latest-recommended`, code style enforced in the build, XML docs,
  `EnableWindowsTargeting` so WPF/WinForms build on Linux/macOS, one SARIF analyzer log per project), central package
  management in `Directory.Packages.props` (StyleCop.Analyzers as a `GlobalPackageReference`), `.editorconfig`,
  `stylecop.json`, an `<AppName>.slnx` solution, a UI-framework-free `src/<AppName>.Core` (`net10.0`: `Services/`,
  plus `ViewModels/` with CommunityToolkit.Mvvm 8.4 partial-property `[ObservableProperty]`/`[RelayCommand]` for
  `architecture: mvvm`, or `Models/` + `Controllers/` + a passive-view `Views/IMainView.cs` for `architecture: mvc`),
  the `src/<AppName>` UI project per `ui` — `wpf` (`{Binding}` + `DataContext`, Fluent `ThemeMode`), `winui` (WinUI 3 /
  Windows App SDK 2.x, `x:Bind`, Mica, single-project MSIX `Package.appxmanifest`, publish profiles) or `winforms`
  (designer-compatible `MainForm.Designer.cs`, PerMonitorV2, system color mode; `mvc` passive view or `mvvm`
  `BindingSource` + `Button.Command`) — all composed with the Generic Host, an `app.manifest` (`asInvoker`, Windows
  10/11, PerMonitorV2 for WPF/WinUI), an MSTest 4 + coverlet `tests/<AppName>.Core.Tests` project at 100% Core line
  coverage, `tests/coverlet.runsettings` (cobertura + opencover, UI assembly excluded = "not measured"), an optional
  FlaUI `tests/<AppName>.UITests` project (`[TestCategory("UI")]`, Windows only) that — per the catalog's UI
  contract — renders the main screen in every left-to-right/right-to-left × light/dark combination (launch arguments
  `--ui-direction`/`--ui-theme` applied by the app's `UiTestOptions`), captures it into `.ui-screenshots/` through the
  shared `UiScreenshots` helper and runs an Axe.Windows accessibility scan at the level of a root `.ui-quality.yml`
  (written for every `ui`), a DocFX `docfx.json` for the Core
  API, generated placeholder icon/tile PNGs, and for WPF/WinForms with `msix: yes` a `packaging/` folder
  (`AppxManifest.xml` with an `x.y.z.0` identity version + `build-msix.ps1`: publish per RID → makeappx → signtool).
  Invoke as `/iru-setup-windows-app`. Accepts pre-resolved inputs via `args` (`key: value` lines) — `ui`
  (`wpf`/`winui`/`winforms`), `architecture` (`mvvm`/`mvc`; WPF and WinUI are `mvvm` only), `app-name` (PascalCase,
  also solution/project/assembly name), `display-name`, `root-namespace`, `publisher` (`CN=…`), `publisher-display-name`,
  `package-name`, `version`, `rids` (default `win-x64;win-arm64`), `msix` (`yes`/`no`), `ui-tests` (`flaui`/`none`),
  `branching` (`gitflow`/`main-only`), `accessibility` (`enforce`/`report`/`off`/`none`, default `enforce`), `license`,
  `developer-name`, `developer-email`, `organization-url`, `open-source`, `visibility`, `ci`, `sonar` (+
  `sonar-organization`/`sonar-project-key`/`sonar-host-url`),
  `distribution` (`none`/`internal`/`store`), `mode` (`new`/`existing`) and `on-existing` (`ask`/`keep`/`update`/
  `replace`) — so `iru-setup-windows-repository` can supply them without re-prompting. Announces whether it is
  scaffolding from scratch or updating; for every file group it owns that already exists it warns and asks Update /
  Keep as is / Replace / Stop (unless `on-existing` decides), never overwrites hand-written source, and treats a
  foreign layout (a single-project `dotnet new wpf` app, a `.sln` with other projects, a `.wapproj` packaging
  project) as foreign — add alongside or stop, never convert. Every version is looked up at run time (NuGet
  flat-container API, .NET release metadata) with a verified 2026-10-16 fallback table. Use whenever a new WPF, WinUI 3
  or Windows Forms app repository needs its solution, quality tooling, tests, docs and packaging bootstrapped from this
  house template.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(dotnet *) Bash(pwsh *) Bash(docfx *) Bash(curl *) Bash(git *) Bash(gh *) Bash(python3 *) Bash(mkdir *) Bash(find *) Agent
---

# Setup Windows App

Generate a complete, buildable Windows desktop app on .NET 10 — a solution with a UI-free `Core` library holding all
testable logic, a WPF, WinUI 3 or Windows Forms app project composed with the Generic Host, an MSTest 4 Core test
project at 100% line coverage, optional FlaUI UI tests, DocFX API docs and MSIX packaging — from the templates in this
skill's `reference/` files. Every template was rendered into throwaway projects and proven against the real toolchain
on 2026-10-16 (.NET SDK 10.0.402 on macOS arm64, DocFX 2.81.0, PowerShell 7.6.7) for `ui: wpf` (mvvm), `ui: winforms`
(mvc and mvvm) and `ui: winui` (mvvm); everything that needs Windows is listed as unverified in **Known quirks /
verification notes**.

The layout is the **scaffold contract** the Windows coding and gate skills (`iru-windows-code-one-task(-group)`,
`iru-dotnet-test`, `iru-dotnet-coverage`, `iru-dotnet-code-quality`, `iru-dotnet-docfx`, `iru-dotnet-bump-version`)
and `iru-setup-windows-github-workflows` detect and call — Step 8's contract table lists the confirmed commands and
report paths. This skill writes no CI workflow, `.gitignore`, README or changelog (`iru-setup-windows-repository`
chains the skills that do) and no Sonar file: SonarScanner for .NET takes the project key and organization on its
command line, so `iru-setup-windows-github-workflows` owns them.

Sources: the facts behind every template are the official Microsoft Learn pages — WPF
(`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/`, incl. `app-development/how-to-use-host-builder`), Windows
Forms (`https://learn.microsoft.com/en-us/dotnet/desktop/winforms/`, incl. `high-dpi-support-in-windows-forms` and
`whats-new/net100`), WinUI / Windows App SDK (`https://learn.microsoft.com/en-us/windows/apps/winui/winui3/`,
`…/windows-app-sdk/single-project-msix`, `…/develop/platform/xaml/x-bind-markup-extension`,
`…/package-and-deploy/ci-for-winui3`), the MVVM Toolkit
(`https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/`, `generators/observableproperty`,
`generators/relaycommand`, `generators/errors/mvvmtk0042`), the Generic Host
(`https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host`), .NET publishing
(`https://learn.microsoft.com/en-us/dotnet/core/deploying/`, `…/trimming/incompatibilities`), MSIX
(`https://learn.microsoft.com/en-us/windows/msix/overview`, `…/package/sign-app-package-using-signtool`) and MSTest
(`https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-mstest-intro`) — plus irurueta docs:
programming-languages/csharp/build-and-tooling.adoc, coding-conventions-and-documentation.adoc and testing.adoc
(https://github.com/albertoirurueta/docs; its planned Windows Apps section is issue #191). Gaps stated honestly: there
is no Microsoft Learn MVVM article specific to WPF, no official dialog/navigation service, no official desktop UI-test
recommendation (FlaUI is third-party; WinAppDriver has had no release since 2020), and trimming/Native AOT are
unsupported for WPF/WinForms.

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/common-templates.md` | **Always.** `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `.editorconfig`, `stylecop.json`, `<AppName>.slnx`, the Core project and sample code (per `architecture`), `app.manifest`, the Core test project, `tests/coverlet.runsettings`, `docfx.json` + `docfx/`. |
| `reference/wpf-templates.md` | `ui: wpf` only. |
| `reference/winui-templates.md` | `ui: winui` only. |
| `reference/winforms-templates.md` | `ui: winforms` only (both architectures). |
| `reference/packaging-templates.md` | **Always** — the `generate-assets.py` helper (app icon for every `ui`, WinUI tiles), plus `packaging/` for `ui: wpf\|winforms` with `msix: yes`. |
| `reference/uitest-templates.md` | `ui-tests: flaui` only — the FlaUI project plus the UI-contract helpers (`UiQuality`, `UiScreenshots`, `AccessibilityCheck`) and the matrix capture test. |

**Conditional-marker convention used in every reference file**: a line `// >>> <condition>` (or `# >>> <condition>`,
or `<!-- >>> <condition> -->` in XML/XAML) opens a block that is written only when the condition holds, and the
matching `<<<` line closes it; the marker lines themselves are never written. Conditions: `ui: <v>` and
`architecture: <v>` (`|` separates alternatives, e.g. `ui: wpf|winforms`), `msix` (= `msix: yes`) and `flaui`
(= `ui-tests: flaui`); comma-separated conditions must all hold. A file heading suffixed `(condition)` exists only
when it holds. **Placeholders** are written `__Token__` (not `<token>`, which collides with C# generics and XML) and
come from Step 5's table; a heading's path uses them too (`src/__AppName__.Core/…`).

## Architecture matrix — which `ui` × `architecture` combinations are valid

| `ui` | `architecture` | Why |
|---|---|---|
| `wpf` | `mvvm` only | XAML's data binding + `ICommand` is the pattern WPF is designed around; MVC has no XAML idiom (no controller concept, the view *is* bound declaratively). Microsoft's guidance for XAML apps is MVVM. |
| `winui` | `mvvm` only | Same reason; WinUI's own "Data binding and MVVM" guidance and tutorial use the MVVM Toolkit, and `x:Bind` binds to a view-model property on the window/page. |
| `winforms` | `mvc` **(Recommended)** or `mvvm` | The designer produces event-driven forms that map naturally onto a controller handling view events through a passive-view interface (`IMainView` in Core, so the controller is unit-tested with a fake view). `mvvm` is viable since .NET 8 (`BindingSource` + `Button.Command` binding to MVVM Toolkit view models). |

The architecture is recorded by the **directory layout** the coding skills detect: `src/<AppName>.Core/ViewModels/`
→ MVVM; `src/<AppName>.Core/Controllers/` + `src/<AppName>.Core/Views/I<X>View.cs` (+ `Models/`) → MVC.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-windows-app`) or by `iru-setup-windows-repository` / the `iru-setup-repository`
front door, which pass resolved answers as `key: value` lines, e.g.:

```
ui: wpf
architecture: mvvm
app-name: Bookshelf
display-name: Bookshelf Desktop
publisher: CN=Jane Doe
publisher-display-name: Jane Doe
package-name: JaneDoe.Bookshelf
branching: gitflow
license: MIT License
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
visibility: public
ci: yes
sonar: cloud
distribution: store
mode: new
on-existing: ask
```

Recognized keys: `ui` (`wpf`/`winui`/`winforms`), `architecture` (`mvvm`/`mvc` — validated against the matrix; an
invalid combination from `args` is reported and re-asked, never silently changed), `app-name` (PascalCase C#
identifier `^[A-Z][A-Za-z0-9]*$` — the solution, project, assembly and exe name), `display-name` (window title, MSIX
`DisplayName`; default `app-name`), `root-namespace` (default `app-name`; Core uses `<root-namespace>.Core`),
`publisher` (MSIX `Identity/@Publisher`, an X.500 subject `CN=…` that must equal the signing certificate's subject, or
the Partner Center value for the Store; default `CN=<developer-name>`), `publisher-display-name` (default
`developer-name`), `package-name` (MSIX `Identity/@Name`, 3–50 chars of `[A-Za-z0-9.-]`; default
`<Owner>.<app-name>` from Step 3, non-identifier characters dropped), `version` (default `1.0.0-dev` for `branching:
gitflow`, `1.0.0` for `main-only`), `rids` (default `win-x64;win-arm64` — WinUI `RuntimeIdentifiers`/`Platforms` and
the packaging script's default), `msix` (`yes`/`no`; `ui: winui` is always packaged → `yes`; WPF/WinForms default
`yes` when `distribution` ≠ `none`, else `no`), `ui-tests` (`flaui`/`none`, default `flaui`), `branching`
(`gitflow`/`main-only`, default `gitflow`), `accessibility` (`enforce`/`report`/`off`/`none`, default `enforce` — the
automated accessibility level written to `.ui-quality.yml`: `enforce` makes Axe.Windows violations fail the UI tests,
`report` lists them, `off` skips the scan), `license`, `developer-name`, `developer-email`, `organization-url`,
`open-source` (`yes`/`no`), `visibility`, `ci`, `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`
— recorded for the report only: no file carries them), `distribution` (`none`/`internal`/`store` — only keys the
`msix` default), `mode` (`new`/`existing`), `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`). Every key
found is resolved — skip its question in Step 2. Unknown keys from a full shared-args set (`ci-tests`, `pages`,
`signing`, `winget`, `integration-branch`, `stable-branch`, `publish`, …) are ignored and named in the report.

`mode: existing` never means "gap-fill silently": Step 1 still warns about, and asks about, every pre-existing file
group. Only `on-existing` skips that question (`keep` = create only missing files; `update`/`replace` applied to
every existing group; the warning is still printed). Orchestrators forward `on-existing` only when their own `args`
received it.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (Axe.Windows), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — `AutomationProperties.Name`/`HelpText` on icon buttons and images, keyboard access and tab order for Narrator, system font scaling and high-contrast resources — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

Check for every file Step 6 would write: `global.json`, `Directory.Build.props`, `Directory.Packages.props`,
`.editorconfig`, `stylecop.json`, `.ui-quality.yml`, any `*.slnx`/`*.sln`, `src/*/*.csproj`, `src/**` sources, `tests/*/*.csproj`,
`tests/**`, `tests/coverlet.runsettings`, `docfx.json`, `docfx/`, `packaging/`, and any `*.wapproj`. Then tell the user
which of the two this run is doing:

- **Scaffolding from scratch** — none exist: go to Step 2.
- **Updating an existing Windows app** — any exists in this skill's layout (`src/<AppName>.Core` + `src/<AppName>`):
  warn, listing every file found by path, that each existing file group below will be decided individually (missing
  files are still created). Groups (only those with a file present): **`global.json`**, **`Directory.Build.props`**,
  **`Directory.Packages.props`**, **quality config** (`.editorconfig`, `stylecop.json`), **the solution file**,
  **project files** (every `*.csproj`), **`tests/coverlet.runsettings`**, **UI quality config** (`.ui-quality.yml`),
  **DocFX config** (`docfx.json`, `docfx/`),
  **packaging** (`packaging/`, `Package.appxmanifest`, publish profiles), and **the source skeleton** (every `*.cs`,
  `*.xaml`, `app.manifest`, `Assets/`). Unless `on-existing` decides, ask with `AskUserQuestion`, one question per
  group (batch up to 4 per call), naming each concrete conflict with this run's choices (e.g. "`src/Bookshelf.Core`
  has `Controllers/` but you chose `architecture: mvvm`", "`Directory.Build.props` has no `<Version>` — each csproj
  declares its own", "`Directory.Packages.props` is missing — projects pin versions inline", "the app project sets
  `UseWPF` but you chose `ui: winforms`"):
  - **Update (Recommended for build files, quality config, solution, run settings and DocFX config)** — "Merge: add
    what's missing and correct outdated parts using this skill's template as reference — analyzer/warnings-as-errors
    properties, central package versions bumped to Step 4's lookup, `EnableWindowsTargeting`, the SARIF `ErrorLog`,
    the runsettings formats/exclusions, the missing keys of `.ui-quality.yml` (its existing `directions`/`themes` and
    `accessibility` are kept unless `accessibility` came from `args`, which then wins and is reported); keep every
    project, package, property and setting this skill doesn't own.
    You review a diff; customizations survive, but a customized part this skill owns may be rewritten." For the
    source skeleton, Update only creates its missing files.
  - **Keep as is (Recommended for the source skeleton and packaging)** — "Leave the file(s) untouched. Nothing you
    customized changes, but they may stay out of date or disagree with this run's choices — the report lists each
    mismatch."
  - **Replace** — "Regenerate from this skill's template. Matches the house pattern exactly, but every customization
    is lost (recoverable only from git history)." Never the default. Even on Replace, never overwrite a `*.cs`/`*.xaml`
    file unless its content exactly matches this skill's original template (i.e. it is still the untouched sample).
  - **Stop** (first question only) — "End this skill now without changing any file." Report and end.

  Ask about groups whose expected content depends on Step 2 answers (`ui`, `architecture`, `msix`, `ui-tests`) after
  Step 2 when `args` didn't already resolve them. When updating, read the current app name (the `WinExe` project's
  `AssemblyName`/file name), root namespace, `ui` (`UseWPF`/`UseWinUI`/`UseWindowsForms`), architecture (Core folders),
  version and the MSIX identity first and offer them as Step 2's defaults.
- **A foreign layout** — a single-project app (`dotnet new wpf/winforms/winui` output with the logic in the app
  project and no `*.Core`), a `.sln` holding other projects, a Windows Application Packaging Project (`*.wapproj`), or
  a .NET Framework (non-SDK-style) project: this is not this skill's scaffold. Warn explicitly and ask
  (`AskUserQuestion`) whether to add this skill's missing pieces alongside without touching the existing projects
  (e.g. only `global.json`, the quality config, central package management, the runsettings and DocFX config — each
  still per-group Update/Keep/Replace; extracting logic into a `Core` project is a coding task, never done here), or
  stop. Never move, rename or convert an existing project, and never migrate a `.sln` to `.slnx` without an explicit
  yes.

## Step 2 — Collect the required inputs

For anything Step 0 didn't resolve, ask directly (plain conversation, pre-filled from Step 1 when updating):
**app-name**, **display-name**, **root-namespace**, **publisher** / **publisher-display-name** / **package-name**
(only when an MSIX is produced — say the Store values come from the Partner Center reservation and a self-signed or
purchased certificate's subject must equal `publisher`), and developer name/email/organization URL.

Then, with `AskUserQuestion` (skip any resolved):

- **ui** — **WPF (Recommended for most line-of-business apps)** (`wpf`: mature, richest XAML/binding model, Fluent
  theme since .NET 9); **WinUI 3** (`winui`: Microsoft's recommended native UI for new apps, Windows App SDK 2.x,
  always MSIX-packaged here; builds and runs only on Windows); **Windows Forms** (`winforms`: designer-driven,
  fastest for simple forms-over-data tools).
- **architecture** — only when `ui: winforms` (WPF/WinUI: state that `mvvm` is the only valid choice and why, per the
  matrix): **MVC with a passive view (Recommended)** / **MVVM with BindingSource + commands**.
- **msix** — only for WPF/WinForms: **Yes** (recommended when `distribution` ≠ `none`: signed MSIX for GitHub
  Releases/App Installer or the Store) / **No** (zip/xcopy distribution only).
- **ui-tests** — **FlaUI UI tests (Recommended)** — say plainly it is third-party, runs only on Windows with an
  interactive desktop, and that Microsoft has no current desktop UI-test recommendation — / **None**.
- **accessibility** — only when `ui-tests: flaui` and stand-alone (an orchestrator resolves it; otherwise default
  `enforce`): "Support accessibility and assistive technologies?" — **Enforce (Recommended)** (Axe.Windows violations fail
  the UI tests) / **Report only** (listed in `.ui-screenshots/a11y-report.txt`, never failing) / **Off** (not run;
  the coding defaults still apply).
- **license** — MIT License (recommended for an app) / Apache License 2.0 / No license (proprietary) / Other. If one is
  chosen, remind the user in Step 8 to add a root `LICENSE` (`iru-check-license` can backfill headers).
- **open-source**, **sonar** and **distribution** — asked stand-alone only (an orchestrator resolves them): ask
  `open-source` first; recommend `sonar: cloud` only when open source and public (SonarCloud is free only for
  public/open-source projects), otherwise `none` (or `self-hosted`), and say that this skill writes no Sonar file —
  `iru-setup-windows-github-workflows` passes the key/organization to SonarScanner for .NET. `distribution` default:
  `store` when open source, otherwise recommend `internal`; it only decides the `msix` default here.

## Step 3 — Infer repository information

Parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`) for `<Owner>` (the
`package-name` default, PascalCased, non-identifier characters dropped). No `origin` → ask.

## Step 4 — Look up toolchain versions

Look every version up at run time; fall back to this table (looked up and verified working **together** on
2026-10-16) only when a lookup fails, and say so in Step 8. NuGet flat-container lookups:
`curl -fsSL https://api.nuget.org/v3-flatcontainer/<id-lowercase>/index.json` → the highest version without a `-`
suffix (the list is SemVer-ordered), except where the table says otherwise. After a newer combination is adopted, run
Step 7 before trusting it.

| Component | Lookup | 2026-10-16 fallback |
|---|---|---|
| .NET SDK (`global.json`) | `https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/10.0/releases.json` → `latest-sdk` (stay on the 10.0 LTS channel; .NET 11 is not the default until it is GA and verified) | `10.0.402` (runtime `10.0.13`) |
| `CommunityToolkit.Mvvm` (`architecture: mvvm`) | flat container; ≥ 8.4.1 needed for partial-property `[ObservableProperty]` without `LangVersion preview` | `8.4.2` |
| `Microsoft.Extensions.Hosting` | flat container, highest **10.0.x** (match the SDK's major) | `10.0.13` |
| `Microsoft.WindowsAppSDK` (`ui: winui`) | flat container, highest stable (skip `-experimental`/`-preview`) | `2.5.1` |
| `Microsoft.Windows.SDK.BuildTools` (`ui: winui`) | flat container, highest stable | `10.0.28000.2705` |
| `MSTest` (metapackage) | flat container | `4.5.1` (brings `Microsoft.NET.Test.Sdk` 18.10.1, MSTest analyzers) |
| `coverlet.collector` | flat container | `10.1.0` |
| `FlaUI.UIA3` (`ui-tests: flaui`) | flat container | `5.0.0` |
| `Axe.Windows` (`ui-tests: flaui`) | flat container (Microsoft's automated accessibility rules for Windows UI; `netstandard2.0`) | `2.4.2` |
| `StyleCop.Analyzers` | **not** "highest stable": `1.1.118` (2019) predates modern C# syntax. Take the newest `1.2.0-beta.*`; adopt a newer prerelease line (e.g. `1.3.x-beta`) only when its first release is at least two weeks old and Step 7 passes with it (`https://api.nuget.org/v3/registration5-semver1/stylecop.analyzers/index.json` has publish dates) | `1.2.0-beta.556` (the `1.3.x-beta` dailies first appeared 2026-10-12) |
| DocFX (verification tool, never added to the repo) | flat container `docfx` | `2.81.0` |

## Step 5 — Reference templates

Read the reference files this run needs (table above). Placeholders:

| Placeholder | Source |
|---|---|
| `__AppName__` / `__RootNamespace__` / `__DisplayName__` | Step 0/2 |
| `__Version__` | Step 0 (`1.0.0-dev` gitflow / `1.0.0` main-only) |
| `__MsixVersion__` | `__Version__` without any pre-release/build suffix, plus `.0` (`1.0.0-dev` → `1.0.0.0`; the Store requires revision 0) |
| `__Publisher__` / `__PublisherDisplayName__` / `__PackageName__` | Step 0/2/3 (XML-escape `&`, `<`, `"`) |
| `__Company__` | `developer-name` (else `publisher-display-name`) |
| `__Year__` | current year |
| `__Rids__` | `rids` (`win-x64;win-arm64`) |
| `__DotnetSdkVersion__` and every `__…Version__` package token | Step 4 |
| `__Accessibility__` | Step 0/2 `accessibility` (default `enforce`) |

Directory layout produced (`[ui]`/`[arch]` mark variant-only files):

```
global.json  Directory.Build.props  Directory.Packages.props  .editorconfig  stylecop.json  .ui-quality.yml  <AppName>.slnx
docfx.json  docfx/index.md  docfx/toc.yml
src/<AppName>.Core/<AppName>.Core.csproj
src/<AppName>.Core/Services/{IGreetingService,GreetingService}.cs
src/<AppName>.Core/ViewModels/MainViewModel.cs                                  [mvvm]
src/<AppName>.Core/{Models/GreetingModel,Views/IMainView,Controllers/MainController}.cs   [mvc]
src/<AppName>/<AppName>.csproj  src/<AppName>/app.manifest  src/<AppName>/UiTestOptions.cs  src/<AppName>/Assets/AppIcon.ico
src/<AppName>/{App.xaml,App.xaml.cs,MainWindow.xaml,MainWindow.xaml.cs,AssemblyInfo.cs}  [wpf]
src/<AppName>/{App.xaml,App.xaml.cs,MainWindow.xaml,MainWindow.xaml.cs,Package.appxmanifest}  [winui]
src/<AppName>/Assets/*.scale-200.png …  src/<AppName>/Properties/{launchSettings.json,PublishProfiles/win-{x64,arm64}.pubxml}  [winui]
src/<AppName>/{Program.cs,MainForm.cs,MainForm.Designer.cs}                     [winforms]
packaging/{AppxManifest.xml,build-msix.ps1,Assets/*.png}                        [wpf|winforms + msix]
tests/<AppName>.Core.Tests/{<AppName>.Core.Tests.csproj,MSTestSettings.cs,Fakes/,Services/,ViewModels/|Models/+Controllers/}
tests/<AppName>.UITests/{<AppName>.UITests.csproj,MSTestSettings.cs,AppLauncher.cs,UiQuality.cs,UiScreenshots.cs,AccessibilityCheck.cs,MainWindowTests.cs}   [flaui]
tests/coverlet.runsettings
```

## Step 6 — Scaffold the project

Apply Step 1's per-group decision to every file that already exists (Keep as is → skip; Update → merge after showing
`git diff --no-index <current> <draft>`; Replace → overwrite within Step 1's source-file limit). Files that didn't
exist are always written.

1. Write every template from the reference files this run reads, applying the markers and placeholders (only the
   `ui`-matching reference file; variant-only headings only when their condition holds). Keep UTF-8 without BOM.
2. Extract `generate-assets.py` from `reference/packaging-templates.md` into a scratch directory **outside** the
   repository and run `python3 -I <scratch>/generate-assets.py <repo-root> <AppName> <ui> <msix>` — it writes
   `src/<AppName>/Assets/AppIcon.ico` (every `ui`), the WinUI tiles (`ui: winui`) or `packaging/Assets/*.png`
   (`ui: wpf|winforms`, `msix: yes`). Never write the helper into the repository. Existing images are part of the
   source skeleton group — never overwritten unless Replace was chosen for it.
3. If `dotnet` is installed, confirm the solution parses: `dotnet sln <AppName>.slnx list`.

## Step 7 — Verify

Run through the `iru-gate-runner` agent (never inline — the logs are long). Warn first: the first restore downloads
every package (WinUI: the Windows App SDK, several hundred MB) and `build-msix.ps1` downloads the Windows runtime
packs. On any host, with the SDK from `global.json`:

1. `dotnet restore <AppName>.slnx`.
2. `dotnet build <AppName>.slnx -c Release` — warnings are errors, so this is also the analyzer gate; then read the
   per-project SARIF logs (`src/*/obj/*.sarif`, `tests/*/obj/*.sarif`) and report the count of results **without**
   `suppressions` (the MVVM Toolkit's generated code carries suppressed CS0618/CS8625 entries — not findings).
   **`ui: winui` off Windows**: building the solution fails (Known quirks) — build `src/<AppName>.Core`,
   `tests/<AppName>.Core.Tests` and (flaui) `tests/<AppName>.UITests` individually and report the app project as
   "unverified (needs Windows)".
3. `dotnet format <AppName>.slnx --verify-no-changes --no-restore` (WinUI off Windows: the Core test project) — the
   only check that surfaces IDE naming rules (IDE1006).
4. `dotnet test tests/<AppName>.Core.Tests -c Release --settings tests/coverlet.runsettings --collect "XPlat Code Coverage" --results-directory TestResults`
   → read `line-rate` of `TestResults/<guid>/coverage.cobertura.xml` (expected `1` — 100% of Core for every variant).
5. DocFX: `docfx docfx.json` (a `dotnet tool install --tool-path <scratch>/docfx docfx` copy if `docfx` isn't
   installed — never `-g`; when `dotnet` is not on `PATH`, set `DOTNET_ROOT`) → `build/docfx/index.html` and
   `build/docfx/api/`, 0 warnings.
6. Windows only (otherwise report each as "unverified (needs Windows)", never "passed"): launch the app
   (`dotnet run --project src/<AppName>` for WPF/WinForms; WinUI through Visual Studio's package deploy or the
   `(Package)` launch profile); `ui: winui` `dotnet build src/<AppName> -c Release -p:Platform=x64`; with `msix: yes`
   `pwsh packaging/build-msix.ps1 -RuntimeIdentifier win-x64` (unsigned unless a test PFX is passed); with
   `ui-tests: flaui` `dotnet test tests/<AppName>.UITests -c Release --filter "TestCategory=UI"` (expect
   `.ui-screenshots/screen/<MainWindow|MainForm>/{default,typical-data}--{ltr,rtl}--{light,dark}.png` — 8 captures —
   and no Axe.Windows violation under `enforce`) behind the
   repository-wide `.integration-test.lock` (atomic `mkdir`, `owner` file, stale after 60 min, released on every
   exit path); for WinUI first build a self-signed MSIX, `Add-AppxPackage` it and export `APP_AUMID` from
   `Get-AppxPackage` exactly as `iru-dotnet-test`'s `ui` step 2 does (mirroring the CI `build.yml` UI step — itself
   unverified locally, needs Windows). Off Windows, `pwsh packaging/build-msix.ps1 -LayoutOnly` still
   verifies the publish + layout half when PowerShell 7 is installed (never install it yourself).

Report pass/fail per command; quote error output verbatim for a failure only.

## Step 8 — Report

Summarize: resolved `ui`, `architecture`, `app-name`, `display-name`, `root-namespace`, version and MSIX identity
(`package-name`, `publisher`, `__MsixVersion__`), `msix`, `ui-tests`, `accessibility`, `rids`, license (or none), and whether the run
scaffolded from scratch, updated an existing project, or stopped. Then, per Step 1 group, the action taken —
**created / updated / replaced / kept as is** (including **`.ui-quality.yml`**) — and whether it came from the user
or `on-existing`, listing each
mismatch of a kept group and, for a replaced one, what customizations could have been lost (check `git diff`).

State what was included versus omitted and why: the architecture choice (and, for WPF/WinUI, that MVC is not
offered); `msix` (`packaging/` written or not; WinUI always packaged); `ui-tests`; `sonar` (no file — the keys go to
`iru-setup-windows-github-workflows`); `distribution` (only drove the `msix` default); which Step 4 versions were live
versus fallback; and any ignored `args` keys.

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path |
|---|---|
| Solution | `<AppName>.slnx` (XML solution; `dotnet sln <AppName>.slnx list` works) — folders `/src/`, `/tests/`, `/Solution Items/` |
| Projects | `src/<AppName>.Core/<AppName>.Core.csproj` (`net10.0`, assembly `<AppName>.Core`, `IsAotCompatible`); `src/<AppName>/<AppName>.csproj` (`WinExe`, assembly `<AppName>`; `net10.0-windows` for wpf/winforms, `net10.0-windows10.0.26100.0` + `TargetPlatformMinVersion 10.0.17763.0` + `Platforms x64;ARM64` for winui); `tests/<AppName>.Core.Tests` (`net10.0`); `tests/<AppName>.UITests` (`net10.0-windows`, `IsTestProject=false` off Windows) |
| UI detection | app csproj `UseWPF` / `UseWinUI` (+ `EnableMsixTooling`) / `UseWindowsForms` |
| Architecture detection | `src/<AppName>.Core/ViewModels/` → mvvm; `src/<AppName>.Core/Controllers/` + `Views/I<X>View.cs` (+ `Models/`) → mvc |
| Build | `dotnet build <AppName>.slnx -c Release` — any host for wpf/winforms (`EnableWindowsTargeting` is in `Directory.Build.props`); winui only on Windows (`-p:Platform=x64|ARM64` optional; `RuntimeIdentifier` defaults to the host architecture) |
| Unit tests | `dotnet test tests/<AppName>.Core.Tests -c Release` (VSTest runner; MSTest 4). `dotnet test <AppName>.slnx` also works on Linux/macOS for wpf/winforms (the UI-test project is not a test project there) |
| Coverage | `dotnet test tests/<AppName>.Core.Tests -c Release --settings tests/coverlet.runsettings --collect "XPlat Code Coverage" --results-directory TestResults` → `TestResults/<guid>/coverage.cobertura.xml` + `coverage.opencover.xml` (Sonar reads opencover); the `<AppName>` UI assembly is excluded ("not measured"); 100% line + branch for every variant |
| UI tests | `dotnet test tests/<AppName>.UITests -c Release --filter "TestCategory=UI"` — Windows + interactive desktop only, behind `.integration-test.lock`; app from `APP_AUMID` (WinUI: required), `APP_EXE`, or the newest `src/<AppName>/bin/**/<AppName>.exe`; automation ids `nameTextBox`, `greetButton`, `messageLabel`; ordinary runs exclude them with `--filter "TestCategory!=UI"` |
| UI contract | `.ui-quality.yml` at the root (`accessibility`, `directions: [ltr, rtl]`, `themes: [light, dark]`); app launch arguments `--ui-direction=ltr\|rtl --ui-theme=light\|dark` (`src/<AppName>/UiTestOptions.cs`); captures `<UI_SCREENSHOTS_DIR or .ui-screenshots>/screen/<MainWindow\|MainForm>/<state>--<dir>--<theme>.png` via `tests/<AppName>.UITests/UiScreenshots.cs`; Axe.Windows via `AccessibilityCheck.cs` (`enforce` fails with `[a11y] …`, `report` appends to `.ui-screenshots/a11y-report.txt`) |
| Analyzer SARIF | one SARIF 2.1 log per project at `<project dir>/obj/<ProjectName>.sarif` (e.g. `src/<AppName>.Core/obj/<AppName>.Core.sarif`), written by every build via `Directory.Build.props` `ErrorLog`; a command-line `-p:ErrorLog=…` overrides it; count only results without `suppressions` |
| Format check | `dotnet format <AppName>.slnx --verify-no-changes --no-restore` |
| DocFX | `docfx docfx.json` (repo root) → metadata `docfx/api/*.yml` (generated — gitignore it) → site `build/docfx/` (`index.html`, `api/<Namespace>.<Type>.html`); Core API only |
| Version | `Directory.Build.props` `<Version>` (`x.y.z-dev` on gitflow `develop`, `x.y.z` otherwise); MSIX `Identity/@Version` `x.y.z.0` in `src/<AppName>/Package.appxmanifest` (winui) and `packaging/AppxManifest.xml` (wpf/winforms + msix) — `build-msix.ps1` rewrites the latter's version from `Directory.Build.props` at pack time anyway |
| MSIX (wpf/winforms) | `pwsh packaging/build-msix.ps1 [-RuntimeIdentifier win-x64,win-arm64] [-Version x.y.z] [-CertificatePath f.pfx -CertificatePassword …] [-LayoutOnly]` → publish `artifacts/publish/<rid>/`, layout `artifacts/msix-layout/<rid>/`, package `artifacts/msix/<AppName>_<x.y.z.0>_<x64\|arm64>.msix` (needs `makeappx.exe`/`signtool.exe` from the Windows SDK) |
| MSIX (winui) | `msbuild src/<AppName>/<AppName>.csproj /restore -p:Configuration=Release -p:Platform=<x64\|ARM64> -p:GenerateAppxPackageOnBuild=true -p:AppxBundle=Never -p:UapAppxPackageBuildMode=SideloadOnly` (per Microsoft's CI-for-WinUI page; Windows only, unverified locally) |
| Zip publish (wpf/winforms) | `dotnet publish src/<AppName> -c Release -r <rid> --self-contained -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o <dir>` → `<AppName>.exe` (+ `.pdb`/`.xml`) only; never `PublishTrimmed`/`PublishAot` (NETSDK1168 WPF, NETSDK1175 WinForms) |

### Known quirks / verification notes

- **Verified for real on 2026-10-16** in `$TMPDIR/iru-verify/windows/iru-setup-windows-app/{wpf,winforms-mvc,
  winforms-mvvm,winui}` (outside this repository; .NET SDK 10.0.402 downloaded to a temp directory, macOS 27 arm64),
  all with `msix: yes` and `ui-tests: flaui`, plus a `wpf-minimal` render with `msix: no`/`ui-tests: none`:
  restore; `dotnet build <AppName>.slnx -c Release` (WPF incl. XAML markup compile, WinForms incl. the designer file
  and data bindings, the FlaUI project) with **0 unsuppressed SARIF results** in every project; `dotnet format
  --verify-no-changes` clean; Core tests 9 passed (mvvm) / 13 passed (mvc) with cobertura **line-rate 1, branch-rate
  1** (9/9 and 31/31 lines); DocFX 2.81.0 0 warnings / 0 errors; `pwsh packaging/build-msix.ps1 -LayoutOnly`
  (PowerShell 7.6.7 downloaded to a temp directory) published `win-x64` and `win-arm64` self-contained and wrote the
  layout with `Version="1.0.0.0"`/`ProcessorArchitecture="arm64"` (and `-Version 2.3.4-beta` → `2.3.4.0`); single-file
  publish of WPF and WinForms produced only `<AppName>.exe`.
- **WinUI build fails off Windows, exactly**: restore succeeds (Windows App SDK 2.5.1 graph, `RuntimeIdentifier`
  `win-arm64` from the host architecture), then the XAML compiler step runs
  `…/microsoft.windowsappsdk.winui/2.3.9/tools/net472/XamlCompiler.exe: cannot execute binary file` and fails with
  `error : XamlCompiler output file "obj/Release/net10.0-windows10.0.26100.0/win-arm64/output.json" was not created.
  The XAML compiler may have crashed.` A verification-only probe (XAML files removed, `InitializeComponent`/`Main`
  stubbed, outside the repository) compiled `App.xaml.cs` and `MainWindow.xaml.cs` against the WinUI 2.x reference
  assemblies with 0 analyzer results, then stopped at `MakePri.exe … Exec format error`. So the WinUI C# is
  compile-checked; the XAML (`x:Bind`), PRI/MSIX generation and running are **unverified locally (needs Windows)**.
- **The FlaUI project cannot run off Windows**: its test host needs the `Microsoft.WindowsDesktop.App` runtime
  ("You must install or update .NET to run this application … Framework: 'Microsoft.WindowsDesktop.App'"), which made
  `dotnet test <AppName>.slnx` exit 1 even with `--filter "TestCategory!=UI"`. Hence
  `IsTestProject=false` off Windows in its csproj; it still compiles everywhere.
- **`[OSCondition(OperatingSystems.Windows)]`** instead of `OperatingSystem.IsWindows()` + `Assert.Inconclusive`:
  MSTest 4's analyzer flags the runtime check (MSTEST0061); `FlaUI.Core.Tools.OperatingSystem` also makes a bare
  `OperatingSystem` ambiguous (CS0104).
- **Coverage stays on VSTest**: the MSTest metapackage brings `Microsoft.NET.Test.Sdk`, so `dotnet test --collect
  "XPlat Code Coverage"` + coverlet works. Don't switch `global.json` to the Microsoft.Testing.Platform runner without
  re-verifying coverage — coverlet's collector is a VSTest data collector.
- **Analyzer fixes baked into the templates**: CA1861 (constant arrays in `CollectionAssert.AreEqual`) →
  `Assert.ContainsSingle`; MSTEST0068 → `Assert.Contains`; SA1636 fired on a plain leading `//` comment, so the whole
  file-header family SA1633–SA1641 is off (headers belong to `iru-check-license`); SA1210 forces alphabetical
  usings across the `mvc`/`mvvm` marker blocks; SA1101/SA1309 are off for the `_camelCase` field convention;
  `dotnet format` (not the build) reported IDE1006 for a `private static readonly` field → a PascalCase rule for
  static readonly fields. The MVVM Toolkit's generated code produces CS0618/CS8625 entries that are **suppressed** in
  the SARIF — gates must ignore suppressed results.
- **NuGet audit is part of the build**: with `TreatWarningsAsErrors`, a newly disclosed vulnerable package (NU1901–
  NU1904) fails restore — intended; update the package in `Directory.Packages.props`.
- **WinForms**: `*.Designer.cs` is generated code to Roslyn (no StyleCop/nullable diagnostics — `components = null`
  is fine); DPI comes from `ApplicationHighDpiMode` in the csproj, not `app.manifest` (WFAC010); `Button.Command`
  binding and `Application.SetColorMode` compiled with no experimental diagnostic on .NET 10. Control `Name`s double
  as UI Automation ids.
- **WPF**: `ThemeMode="System"` in `App.xaml` compiles without WPF0001 (setting `ThemeMode` from code is the
  experimental API). `App` builds the host in its constructor; `OnExit` stops it synchronously because an awaited
  continuation would never run after the dispatcher shuts down.
- **Trimming/AOT**: `PublishTrimmed=true` fails with NETSDK1168 (WPF) / NETSDK1175 (WinForms) — verified. WinUI
  supports trimming/AOT, but the scaffold leaves it off (Microsoft's template turns `PublishTrimmed` on in Release;
  trim warnings would break the warnings-as-errors build — opt in deliberately).
- **WinUI choices**: TFM `net10.0-windows10.0.26100.0` and the project shape follow Microsoft's current WinUI CLI
  template (`Microsoft.WindowsAppSDK.WinUI.CSharp.Templates`, `winui.mvvmapp`, still alpha on NuGet); x86, the
  phone identity, the `systemAIModels` capability and the `Microsoft.Windows.SDK.BuildTools.WinApp` `dotnet run`
  helper are left out.
- **UI contract (2026-10-16)**: the templates were round-tripped (extracted, markers applied) into the `wpf`,
  `winforms-mvc` and `winforms-mvvm` renders under `$TMPDIR/iru-verify/windows/ui-contract/`, which then built with 0
  unsuppressed SARIF results, `dotnet format --verify-no-changes` clean, Core tests unchanged (9/13/9 passed);
  `UiTestOptions` + the WinUI `App.xaml.cs` hook compiled in the WinUI C# probe (stopping at `MakePri.exe` as
  before). Findings baked in: the WPF `ThemeMode` assignment needs the scoped `#pragma warning disable WPF0001`; an
  unqualified `Capture` is ambiguous with `System.Text.RegularExpressions.Capture` (CS0104); FlaUI's
  `Launch(exe, arguments)` takes a non-nullable `string` (CS8604 with `null`); SA1515 wants a blank line before the
  WinForms comment. **Unverified (needs Windows)**: the RTL/theme rendering itself, the captures and the Axe.Windows
  scans.
- **Unverified locally, never a blocker**: running any of the apps, the FlaUI tests, `makeappx`/`signtool`, MSIX
  install/sideload, the WinUI build and package, Store/WinGet/App Installer — all need Windows (and certificates or
  Partner Center for signing/submission).

Finish with a **Warn explicitly** block:

- Review every generated file before building, committing or distributing; replace the placeholder icon/tiles
  (Store certification rejects placeholder artwork) and the greeting sample with real code.
- Run `iru-setup-windows-gitignore` — `bin/`, `obj/`, `TestResults/`, `artifacts/`, `build/`, `docfx/api/`,
  `*.pfx`/`*.p12` and MSIX outputs must never be committed.
- Never commit a signing certificate or its password; `build-msix.ps1` reads them from parameters or the
  `WINDOWS_CERTIFICATE_PATH`/`WINDOWS_CERTIFICATE_PASSWORD` environment variables (CI decodes them from secrets), and
  an unsigned MSIX cannot be installed by users (the Store re-signs, so Store submissions may be unsigned).
- The MSIX `publisher` must equal the signing certificate's subject (or the Partner Center publisher for the Store),
  and `package-name` must match the Store reservation — fix both before the first release.
- With `sonar` ≠ `none`, a `SONAR_TOKEN` secret and the Sonar project must exist before CI analysis works.
