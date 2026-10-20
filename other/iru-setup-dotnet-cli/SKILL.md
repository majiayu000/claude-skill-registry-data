---
name: iru-setup-dotnet-cli
description: >-
  Scaffold an agent-friendly .NET 10 / C# 14 command-line tool at the repository root — `global.json` (SDK pinned,
  `rollForward: latestFeature`), `Directory.Build.props` (the tool `<Version>` `0.1.0-dev`, nullable, implicit usings,
  warnings as errors, `AnalysisLevel latest-recommended`, code style enforced in the build, XML docs,
  `InvariantGlobalization`, one SARIF analyzer log per project), central package management in
  `Directory.Packages.props` (StyleCop.Analyzers as a `GlobalPackageReference`), `.editorconfig`, `stylecop.json`, a
  `<ToolName>.slnx` solution, a framework-free `src/<ToolName>.Core` (`net10.0`, `IsAotCompatible`) holding the whole
  CLI contract — the exit-code enum 0–7/130/143, the JSON error envelope on stderr, deterministic System.Text.Json
  source-generated output (sorted keys, compact, no reflection), the colour policy per stream (`Console.Is*Redirected`,
  `NO_COLOR`, `TERM=dumb`, `FORCE_COLOR`, `--no-color`, machine mode), the prompt policy (`--no-input`,
  `<BIN>_NO_INPUT`, `CI`), SIGINT/SIGTERM through `PosixSignalRegistration` → 130/143 with a second-signal immediate
  exit, the `schema` model, static bash/zsh/fish/PowerShell completion scripts and an AsciiDoc CLI reference + man
  page generated from the command tree — and a thin `src/<ToolName>` executable (`AssemblyName <bin>`, Native AOT
  `PublishAot`, `PackAsTool` with .NET 10 RID-specific tool packages + an `any` fallback for `dotnet tool install`/
  `dnx`) built on System.CommandLine 2.0 stable (`RootCommand`-free root `Command` named after the binary, `Option<T>`/
  `Argument<T>`/`SetAction`, `ParserConfiguration` with response files off, usage errors → exit 2, default exception
  handler and its signal handling off) and Spectre.Console for styled output that obeys the colour policy, with the
  commands `greet [NAME]`, `completion <shell>`, `schema`, `--version`, a hidden `gen-docs`, and with `ui: tui` a
  TTY-gated full-screen Terminal.Gui v2 `browse` command whose view (`Tui/BrowseView`) gets UI tests per the catalog's
  UI contract — rendered on Terminal.Gui's ANSI driver, every state × `.ui-quality.yml` direction captured as
  `.ui-screenshots/screen/BrowseView/<state>--<direction>--no-color.txt`, with the asserted terminal accessibility
  checks at the level of a root `.ui-quality.yml`; MSTest 4 + coverlet `tests/<ToolName>.Core.Tests` (~99% Core
  line/branch coverage) and `tests/<ToolName>.Cli.Tests` running the command tree in-process with captured
  stdout/stderr (every exit code, JSON goldens, no-TTY/`NO_COLOR` behaviour) plus opt-in published-binary smoke tests;
  `tests/coverlet.runsettings` and a DocFX `docfx.json` for the Core API. Invoke as `/iru-setup-dotnet-cli`. Accepts
  pre-resolved inputs via `args` (`key: value` lines) — `tool-name` (PascalCase solution/project name), `bin-name`
  (the command), `package-id`, `description`, `ui` (`none`/`tui`), `accessibility` (`enforce`/`report`/`off`/`none`, only
  with `ui: tui`), `version`, `branching`, `license`,
  `developer-name`, `developer-email`, `organization-url`, `owner`, `open-source`, `visibility`, `ci`, `sonar`
  (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `distribution` (`none`/`internal`/`store`),
  `channels`, `mode` (`new`/`existing`) and `on-existing` (`ask`/`keep`/`update`/`replace`) — so
  `iru-setup-cli-repository` can supply them without re-prompting. Announces whether it is scaffolding from scratch
  or updating; for every file group it owns that already exists it warns and asks Update / Keep as is / Replace / Stop
  (unless `on-existing` decides), never overwrites hand-written source, and treats a foreign layout (a single-project
  `dotnet new console` app, System.CommandLine betas, a Spectre.Console.Cli app, a `.sln` with other projects) as
  foreign — add alongside or stop, never convert. Every version is looked up at run time (NuGet flat-container API,
  .NET release metadata) with a verified 2026-10-16 fallback table. Use whenever a new .NET command-line tool
  repository needs its solution, contract plumbing, quality tooling, tests and docs bootstrapped from this house
  template.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(dotnet *) Bash(docfx *) Bash(curl *) Bash(git *) Bash(gh *) Bash(python3 *) Bash(mkdir *) Bash(find *) Bash(uname *) Agent
---

# Setup .NET CLI

Generate a complete, buildable, agent-friendly .NET 10 command-line tool — a solution with a framework-free `Core`
library that implements the catalog's CLI contract (`reference/` templates; the contract itself is
`iru-dotnet-code-one-task/reference/cli-contract.md` when that skill is installed), a thin System.CommandLine 2.0
executable published as a Native AOT binary and packable as a .NET tool, MSTest 4 unit and end-to-end tests, DocFX
API docs and a CLI reference generated from the command tree. Every template was rendered into throwaway projects
and proven against the real toolchain on 2026-10-16 (.NET SDK 10.0.402 on macOS arm64, plus Linux arm64 in the
`mcr.microsoft.com/dotnet/sdk:10.0-noble-aot` container) for `ui: none` and `ui: tui`; what needs another host is
listed as unverified in **Verification notes**.

The layout is the **scaffold contract** the .NET coding and gate skills (`iru-dotnet-code-one-task(-group)` — CLI
shape —, `iru-dotnet-test`, `iru-dotnet-coverage`, `iru-dotnet-code-quality`, `iru-dotnet-docfx`,
`iru-dotnet-bump-version`) and `iru-setup-cli-github-workflows` detect and call — Step 8's contract table lists the
confirmed commands and paths. This skill writes no CI workflow, `.gitignore` (`iru-setup-dotnet-gitignore`), README,
changelog, `LICENSE` (`iru-check-license`), Antora site (`iru-setup-antora` — the scaffold never creates
`docs/antora.yml`) and no Sonar file (SonarScanner for .NET takes the key and organization on its command line).

Sources: irurueta docs: ai/cli-for-agents/frameworks-swift-and-dotnet.adoc (System.CommandLine 2.x, Spectre.Console,
.NET global tools), streams-and-exit-codes.adoc, tty-colour-and-interactivity.adoc, machine-readable-output.adoc,
self-describing-help.adoc, safety-and-idempotency.adoc, configuration-and-auth.adoc, packaging-and-distribution.adoc,
testing-clis.adoc, documenting-clis.adoc, tuis-vs-clis.adoc and agent-readiness-checklist.adoc
(https://www.irurueta.com/ai/cli-for-agents/index.html); irurueta docs: programming-languages/csharp/build-and-tooling.adoc,
coding-conventions-and-documentation.adoc and testing.adoc (https://github.com/albertoirurueta/docs); Microsoft Learn —
System.CommandLine (`https://learn.microsoft.com/en-us/dotnet/standard/commandline/`), Native AOT
(`https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/`), trimming
(`…/core/deploying/trimming/prepare-libraries-for-trimming`), System.Text.Json source generation
(`…/standard/serialization/system-text-json/source-generation`), `PosixSignalRegistration`
(`…/api/system.runtime.interopservices.posixsignalregistration`), RID-specific and AOT .NET tools
(`https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools`), .NET tools and `dnx`
(`…/core/tools/global-tools`), MSTest (`…/core/testing/unit-testing-mstest-intro`); Spectre.Console
(`https://spectreconsole.net/`); Terminal.Gui v2 (`https://tui-cs.github.io/Terminal.Gui/`); NO_COLOR (no-color.org);
Command Line Interface Guidelines (clig.dev).

## Reference files — read all four

| Read | Contents |
|---|---|
| `reference/common-templates.md` | `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `.editorconfig`, `stylecop.json`, `<ToolName>.slnx`, `tests/coverlet.runsettings`, `docfx.json` + `docfx/`. |
| `reference/core-templates.md` | `src/<ToolName>.Core`: `ExitCode`/`ExitCodes`, `CliException`, `ToolInfo`, `Output/` (formats, envelope records, source-generated `CliJsonContext`, `JsonOutput`, `ErrorReporter`, `DiagnosticLog`), `Terminal/` (`TerminalEnvironment`, `ColorPolicy`, `PromptPolicy`, `ShutdownCoordinator`), `Greeting/`, `Schema/`, `Completion/`, `Docs/` (`ReferenceGenerator`, `AtomicFile`), `Browse/BrowseState` (ui: tui). |
| `reference/core-test-templates.md` | `tests/<ToolName>.Core.Tests` — one test class per Core type. |
| `reference/cli-templates.md` | `src/<ToolName>` (csproj, `Program.cs`, `CliApp`, `CliStreams`, `GlobalOptions`, `ToolCommand`, `CommandTreeReader`, `ConsoleFactory`, `Commands/{Greet,Completion,Schema,GenDocs,Browse}Command.cs`) and `tests/<ToolName>.Cli.Tests` (`CliRunner`, contract, schema/completion, browse, published-binary tests). |

**Conditional-marker convention used in every reference file**: a line `// >>> <condition>` (or
`<!-- >>> <condition> -->` in XML) opens a block that is written only when the condition holds, and the matching
`<<<` line closes it; the marker lines themselves are never written. Conditions: `ui: tui` / `ui: none`, `license`
(a license other than "No license" was chosen) and `repository-url` (Step 3 found the repository URL). A file heading
suffixed `(ui: tui)` exists only for `ui: tui`. **Placeholders** are written `__Token__` (not `<token>`, which
collides with C# generics and XML) and come from Step 5's table; a heading's path uses them too
(`src/__ToolName__.Core/…`).

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-dotnet-cli`) or by `iru-setup-cli-repository` / the `iru-setup-repository` front
door, which pass resolved answers as `key: value` lines, e.g.:

```
tool-name: Greetly
bin-name: greetly
package-id: Greetly.Tool
description: Greets people; a sample agent-friendly command-line tool.
ui: tui
branching: gitflow
license: MIT License
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
owner: example-org
open-source: yes
visibility: public
ci: yes
sonar: cloud
distribution: store
channels: nuget,winget
mode: new
on-existing: ask
```

Recognized keys: `tool-name` (PascalCase C# identifier `^[A-Z][A-Za-z0-9]*$` — the solution, project and root
namespace; default: `bin-name` PascalCased), `bin-name` (the command users type and the executable/assembly name,
`^[a-z][a-z0-9-]*$`; default: the repository directory name lower-cased), `package-id` (NuGet package id of the .NET
tool, `[A-Za-z0-9._-]`; default `bin-name` — check `https://api.nuget.org/v3-flatcontainer/<id>/index.json` returns
404, else warn that the id is taken), `description` (one line: what the tool does and when to use it), `ui`
(`none`/`tui`, default `none`), `accessibility` (`enforce`/`report`/`off`/`none`, default `enforce`; only meaningful with
`ui: tui` — the level written to `.ui-quality.yml` for the terminal UI's asserted accessibility checks; ignored and
named in the report with `ui: none`), `version` (default `0.1.0-dev` for `branching: gitflow`, `0.1.0` for `main-only`),
`branching` (`gitflow`/`main-only`, default `gitflow`), `license`, `developer-name`, `developer-email`,
`organization-url`, `owner`, `open-source` (`yes`/`no`), `visibility`, `ci`, `sonar` (+ `sonar-organization`/
`sonar-project-key`/`sonar-host-url` — recorded for the report only: no file carries them), `distribution`
(`none`/`internal`/`store`) and `channels` (comma list, .NET values `nuget`, `winget`) — both recorded for the report
only: the `PackAsTool` settings are always written (they cost nothing and make `dnx <package-id>` possible), and
publishing is `iru-setup-cli-github-workflows`' job —, `mode` (`new`/`existing`), `on-existing`
(`ask`/`keep`/`update`/`replace`, default `ask`). Every key found is resolved — skip its question in Step 2. Unknown
keys from a full shared-args set (`language`, `ci-tests`, `pages`, `cross-os-ci`, `integration-branch`,
`stable-branch`, `publish`, …) are ignored and named in the report.

`mode: existing` never means "gap-fill silently": Step 1 still warns about, and asks about, every pre-existing file
group. Only `on-existing` skips that question (`keep` = create only missing files; `update`/`replace` applied to
every existing group; the warning is still printed). Orchestrators forward `on-existing` only when their own `args`
received it.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (the terminal UI's asserted accessibility checks), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — selection visible without colour, key help on screen, every action reachable by key — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

Check for every file Step 6 would write: `global.json`, `Directory.Build.props`, `Directory.Packages.props`,
`.editorconfig`, `stylecop.json`, `.ui-quality.yml` (`ui: tui`), any `*.slnx`/`*.sln`, `src/*/*.csproj`, `src/**`
sources, `tests/*/*.csproj`, `tests/**`, `tests/coverlet.runsettings`, `docfx.json`, `docfx/`. Then tell the user which of the two this run is
doing:

- **Scaffolding from scratch** — none exist: go to Step 2.
- **Updating an existing .NET CLI** — any exists in this skill's layout (`src/<ToolName>.Core` + `src/<ToolName>`
  with `<OutputType>Exe</OutputType>` and a `System.CommandLine` reference): warn, listing every file found by path,
  that each existing file group below will be decided individually (missing files are still created). Groups (only
  those with a file present): **`global.json`**, **`Directory.Build.props`**, **`Directory.Packages.props`**,
  **quality config** (`.editorconfig`, `stylecop.json`), **the solution file**, **project files** (every `*.csproj`),
  **`tests/coverlet.runsettings`**, **UI quality config** (`.ui-quality.yml`, `ui: tui` only), **DocFX config**
  (`docfx.json`, `docfx/`), and **the source skeleton** (every `*.cs`). Unless `on-existing` decides, ask with `AskUserQuestion`, one question per group (batch up to 4 per call),
  naming each concrete conflict with this run's choices (e.g. "`src/Greetly/Greetly.csproj` has no `PublishAot`",
  "`Directory.Packages.props` pins System.CommandLine `2.0.0-beta4` — the beta API differs", "`ui: tui` chosen but
  no Terminal.Gui reference", "`Directory.Build.props` has no `<Version>`"):
  - **Update (Recommended for build files, quality config, solution, run settings and DocFX config)** — "Merge: add
    what's missing and correct outdated parts using this skill's template as reference — analyzer/warnings-as-errors
    properties, `InvariantGlobalization`, AOT/tool properties, central package versions bumped to Step 4's lookup,
    the SARIF `ErrorLog`, the runsettings `Include`, the missing keys of `.ui-quality.yml` (existing values kept unless
    `accessibility` came from `args`, which then wins and is reported); keep every project, package, property and
    setting this skill doesn't own. You review a diff; customizations survive, but a customized part this skill owns may be rewritten."
    For the source skeleton, Update only creates its missing files.
  - **Keep as is (Recommended for the source skeleton)** — "Leave the file(s) untouched. Nothing you customized
    changes, but they may stay out of date or disagree with this run's choices — the report lists each mismatch."
  - **Replace** — "Regenerate from this skill's template. Matches the house pattern exactly, but every customization
    is lost (recoverable only from git history)." Never the default. Even on Replace, never overwrite a `*.cs` file
    unless its content exactly matches this skill's original template (i.e. it is still the untouched sample).
  - **Stop** (first question only) — "End this skill now without changing any file." Report and end.

  Ask about groups whose expected content depends on Step 2 answers (`ui`) after Step 2 when `args` didn't resolve
  them. When updating, read the current tool name (the solution/`Exe` project name), bin name (`AssemblyName`/
  `ToolCommandName`), package id, version and `ui` (a `Terminal.Gui` reference) first and offer them as Step 2's
  defaults.
- **A foreign layout** — a single-project console app (`dotnet new console` output with the logic in `Program.cs`
  and no `*.Core`), a System.CommandLine `2.0.0-beta*` project (`SetHandler`/`InvocationContext` API, removed in 2.0),
  a Spectre.Console.Cli (`CommandApp`) tool, a `.sln` holding other projects, a WPF/WinUI/WinForms app (that is
  `iru-setup-windows-app`'s), or a .NET Framework (non-SDK-style) project: this is not this skill's scaffold. Warn
  explicitly and ask (`AskUserQuestion`) whether to add this skill's missing pieces alongside without touching the
  existing projects (e.g. only `global.json`, the quality config, central package management, the runsettings and
  DocFX config — each still per-group Update/Keep/Replace; porting commands to System.CommandLine 2.0 or extracting
  a `Core` project is a coding task, never done here), or stop. Never move, rename or convert an existing project,
  and never migrate a `.sln` to `.slnx` without an explicit yes.

## Step 2 — Collect the required inputs

For anything Step 0 didn't resolve, ask directly (plain conversation, pre-filled from Step 1 when updating):
**bin-name**, **tool-name**, **package-id**, **description** (one line — it becomes the root command's help text,
the package description and the man page NAME line), and developer name/email/organization URL.

Then, with `AskUserQuestion` (skip any resolved):

- **ui** — **No terminal UI (Recommended)** (`none`: plain commands, styled text via Spectre.Console when a person
  is at the terminal) / **Full-screen terminal UI** (`tui`: adds a Terminal.Gui v2 `browse` command — Terminal.Gui
  2.x is stable on NuGet since 2026-04 (2.5.0 verified); it adds ~5 MB to the Native AOT binary, starts only when
  stdin and stdout are terminals, and every function it offers stays available as a non-interactive `--json`
  command). If Step 4 finds no stable (non-prerelease) Terminal.Gui 2.x at all, say so and do not offer `tui` — the
  templates for it target the v2 API.
- **accessibility** — only with `ui: tui`, stand-alone (an orchestrator resolves it; otherwise default `enforce`):
  "Support accessibility and assistive technologies?" — **Enforce (Recommended)** (violations fail the UI tests) / **Report
  only** (listed in `.ui-screenshots/a11y-report.txt`, never failing) / **Off** (not run; the coding defaults still
  apply). Say that for a terminal UI these are asserted checks — the selection readable without colour, the key help
  on screen, every action on a key — since no automated accessibility audit exists for terminals.
- **license** — MIT License (recommended for an open-source tool) / Apache License 2.0 / No license (proprietary) /
  Other (ask its SPDX id). If one is chosen, remind the user in Step 8 to add a root `LICENSE` (`iru-check-license`
  can backfill headers).
- **open-source**, **sonar** and **distribution** — asked stand-alone only (an orchestrator resolves them): ask
  `open-source` first; recommend `sonar: cloud` only when open source and public (SonarCloud is free only for
  public/open-source projects), otherwise `none` (or `self-hosted`); `distribution` default `store` when open source,
  otherwise `internal`. Say that this skill only records them — `iru-setup-cli-github-workflows` acts on them.

## Step 3 — Infer repository information

Parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`) for `<Owner>` and the
HTTPS repository URL (`https://host/owner/repo`, the `repository-url` condition and `__RepositoryUrl__`). No `origin`
→ use `owner` from `args` if given, else leave the `repository-url` block out and say so.

## Step 4 — Look up toolchain versions

Look every version up at run time; fall back to this table (looked up and verified working **together** on
2026-10-16) only when a lookup fails, and say so in Step 8. NuGet flat-container lookups:
`curl -fsSL https://api.nuget.org/v3-flatcontainer/<id-lowercase>/index.json` → the highest version without a `-`
suffix (the list is SemVer-ordered), except where the table says otherwise. After a newer combination is adopted, run
Step 7 before trusting it.

| Component | Lookup | 2026-10-16 fallback |
|---|---|---|
| .NET SDK (`global.json`) | `https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/10.0/releases.json` → `latest-sdk` (stay on the 10.0 LTS channel; .NET 11 is not the default until it is GA and verified) | `10.0.402` (runtime `10.0.13`) |
| `System.CommandLine` | flat container, highest stable **2.x** (the `3.0.0-preview/rc` line is not stable; the `2.0.0-beta*` line has a different API) | `2.0.13` |
| `Spectre.Console` | flat container, highest stable (skip `-alpha`) | `0.57.2` |
| `Terminal.Gui` (`ui: tui`) | flat container, highest stable **2.x** (skip `-develop.*`; 1.x is the old API) | `2.5.0` (published 2026-09-11) |
| `MSTest` (metapackage) | flat container | `4.5.1` (brings `Microsoft.NET.Test.Sdk` 18.x and the MSTest analyzers) |
| `coverlet.collector` | flat container | `10.1.0` |
| `StyleCop.Analyzers` | **not** "highest stable": `1.1.118` (2019) predates modern C# syntax. Take the newest `1.2.0-beta.*`; adopt a newer prerelease line (e.g. `1.3.x-beta`) only when its first release is at least two weeks old and Step 7 passes with it (`https://api.nuget.org/v3/registration5-semver1/stylecop.analyzers/index.json` has publish dates) | `1.2.0-beta.556` |
| DocFX (verification tool, never added to the repo) | flat container `docfx` | `2.81.0` |

## Step 5 — Reference templates

Read the four reference files. Placeholders:

| Placeholder | Source |
|---|---|
| `__ToolName__` / `__BinName__` / `__PackageId__` | Step 0/2 |
| `__BinEnvPrefix__` | `bin-name` upper-cased, `-` → `_` (`my-tool` → `MY_TOOL`; the env vars are `__BinEnvPrefix___NO_INPUT`, `__BinEnvPrefix___BINARY`) |
| `__Description__` | Step 0/2 — escaped for both C# string literals (`"` → `\"`, `\` → `\\`) and XML (`&`, `<`) |
| `__Version__` | Step 0 (`0.1.0-dev` gitflow / `0.1.0` main-only) |
| `__Company__` | `developer-name` (else `owner`) |
| `__Year__` | current year |
| `__PackageLicenseExpression__` | SPDX id of `license` (`MIT`, `Apache-2.0`, …; block omitted for "No license") |
| `__RepositoryUrl__` | Step 3 |
| `__DotnetSdkVersion__` and every `__…Version__` package token | Step 4 |
| `__Accessibility__` | Step 0/2 `accessibility` (default `enforce`; `ui: tui` only) |

Directory layout produced (`[tui]` marks `ui: tui`-only files):

```
global.json  Directory.Build.props  Directory.Packages.props  .editorconfig  stylecop.json  <ToolName>.slnx
docfx.json  docfx/index.md  docfx/toc.yml  tests/coverlet.runsettings  .ui-quality.yml[tui]
src/<ToolName>.Core/<ToolName>.Core.csproj
src/<ToolName>.Core/{ExitCode,ExitCodes,CliException,ToolInfo}.cs
src/<ToolName>.Core/Output/{OutputFormat,LogFormat,GlobalSettings,ErrorEnvelope,ErrorBody,SummaryLine,LogLine,CliJsonContext,JsonOutput,ErrorReporter,DiagnosticLog}.cs
src/<ToolName>.Core/Terminal/{TerminalEnvironment,ColorPolicy,PromptPolicy,ShutdownCoordinator}.cs
src/<ToolName>.Core/Greeting/{Greeter,GreetingResult}.cs
src/<ToolName>.Core/Schema/{CommandSpec,ArgumentSpec,OptionSpec,CommandSafety,ExitCodeSpec,SchemaDocument,SchemaBuilder}.cs
src/<ToolName>.Core/Completion/{Shell,CompletionScriptGenerator}.cs
src/<ToolName>.Core/Docs/{ReferenceGenerator,AtomicFile}.cs
src/<ToolName>.Core/Browse/BrowseState.cs                                        [tui]
src/<ToolName>/<ToolName>.csproj  src/<ToolName>/{Program,CliApp,CliStreams,GlobalOptions,ToolCommand,CommandTreeReader,ConsoleFactory}.cs
src/<ToolName>/Commands/{GreetCommand,CompletionCommand,SchemaCommand,GenDocsCommand}.cs
src/<ToolName>/Commands/BrowseCommand.cs  src/<ToolName>/Tui/BrowseView.cs        [tui]
tests/<ToolName>.Core.Tests/{<ToolName>.Core.Tests.csproj,MSTestSettings.cs,*Tests.cs,Output/,Terminal/,Greeting/,Schema/,Completion/,Docs/,Browse/[tui]}
tests/<ToolName>.Cli.Tests/{<ToolName>.Cli.Tests.csproj,MSTestSettings.cs,CliRunner.cs,CliResult.cs,ContractTests.cs,SchemaAndCompletionTests.cs,PublishedBinaryTests.cs,BrowseTests.cs[tui],UiScreenshots.cs[tui],AccessibilityCheck.cs[tui],Tui/BrowseViewTests.cs[tui]}
```

Design decisions the templates encode (keep them when editing):

- **Root `Command`, not `RootCommand`**: the root is a `ToolCommand` named `<bin>` with an explicit `HelpOption`
  (help + an "Examples:" section) and `VersionOption` (prints `ToolInfo.Version`, i.e. `<Version>` without
  `+commit`). `RootCommand` takes its name from the host process (`testhost` under tests) and adds the `[suggest]`
  directive; neither is wanted.
- **Parsing**: `ParserConfiguration { ResponseFileTokenReplacer = null }` — `@file` tokens are never expanded from
  disk. System.CommandLine 2.0 has no prefix/abbreviation matching (`--form` is not `--format`). POSIX bundling
  (`-qv`, `-vv`) stays on. Parse errors are checked before invocation and reported as `USAGE` (exit 2, the library's
  own default is 1) with "Run `<bin> <command> --help` for usage."; an unknown option-looking token that would
  otherwise be taken as `NAME` is rejected by an argument validator.
- **Invocation**: `InvocationConfiguration { EnableDefaultExceptionHandler = false, ProcessTerminationTimeout = null }`
  — exceptions reach `CliApp` (`CliException` → envelope + its exit code, anything else → `INTERNAL` 1, an
  `IOException` from a closed pipe → quiet 0) and signals are handled by `ShutdownCoordinator`, not the library.
- **Output**: data only on stdout via `JsonOutput` (source-generated `CliJsonContext`, relaxed escaping, properties
  declared alphabetically, `SortedDictionary` details) or Spectre.Console (`ConsoleFactory` sets `Ansi`/
  `ColorSystem` from `ColorPolicy`, never Spectre's own detection, and disables wrapping when not a terminal).
- **Coverage subject**: `tests/coverlet.runsettings` includes only `[<ToolName>.Core]*` — the System.CommandLine shell
  is exercised by `Cli.Tests` but "not measured".
- **Config precedence** (flags → env → file → defaults) is implemented only for flags and `<BIN>_*` env vars; a config
  file needs a TOML/JSON reader the scaffold doesn't add — it is the documented extension point (report it).

## Step 6 — Scaffold the project

Apply Step 1's per-group decision to every file that already exists (Keep as is → skip; Update → merge after showing
`git diff --no-index <current> <draft>`; Replace → overwrite within Step 1's source-file limit). Files that didn't
exist are always written.

1. Write every template from the reference files, applying the markers and placeholders (variant-only headings only
   when their condition holds). Keep UTF-8 without BOM and LF line endings.
2. If `dotnet` is installed, confirm the solution parses: `dotnet sln <ToolName>.slnx list`.

## Step 7 — Verify

Run through the `iru-gate-runner` agent (never inline — the logs are long). Warn first: the first restore downloads
every package and the first Native AOT publish downloads the ILCompiler packages (~100 MB). On any host, with the SDK
from `global.json`:

1. `dotnet restore <ToolName>.slnx` then `dotnet build <ToolName>.slnx -c Release` — warnings are errors and the
   trim/AOT analyzers run in every build (`IsAotCompatible`/`PublishAot`), so this is also the analyzer gate; read the
   per-project SARIF logs (`src/*/obj/*.sarif`, `tests/*/obj/*.sarif`) and report the count of results **without**
   `suppressions` (expected 0).
2. `dotnet format <ToolName>.slnx --verify-no-changes --no-restore`.
3. `dotnet test <ToolName>.slnx -c Release --settings tests/coverlet.runsettings --collect "XPlat Code Coverage" --results-directory TestResults`
   → the `tests/<ToolName>.Core.Tests` run's `TestResults/<guid>/coverage.cobertura.xml` `line-rate` (expected ≥ 0.98;
   the gate is 0.80). The two `PublishedBinary` tests report "skipped" here.
4. Native AOT publish for the host RID (`uname -sm` → `osx-arm64`, `osx-x64`, `linux-x64`, `linux-arm64`;
   `win-x64`/`win-arm64` on Windows): `dotnet publish src/<ToolName> -c Release -r <rid> -o artifacts/publish/<rid>`
   — 0 warnings. Needs the platform linker (Xcode command-line tools on macOS; `clang` + `zlib1g-dev` on Linux; the
   VS "Desktop development with C++" workload on Windows); a missing prerequisite makes this step "unverified", never
   "passed". Then the contract smoke checks on `artifacts/publish/<rid>/<bin>`: `--version` and `--help` exit 0 with
   empty stderr; `no-such-command` exits 2 with empty stdout; `greet ""` exits 3 and `greet "" --json` writes the
   envelope to stderr; `greet Ada --json` prints exactly `{"greeting":"Hello, Ada!","name":"Ada","schemaVersion":1}`;
   `greet Ada | grep -c $'\x1b'` is 0; `schema | head -c 20` leaves stderr empty; and
   `__BinEnvPrefix___BINARY=$PWD/artifacts/publish/<rid>/<bin> dotnet test tests/<ToolName>.Cli.Tests -c Release --filter TestCategory=PublishedBinary`
   passes.
5. Tool packaging: `dotnet pack src/<ToolName> -c Release` (pointer package) and `dotnet pack src/<ToolName> -c Release -r <host-rid>`
   → `artifacts/nupkg/<package-id>.<version>.nupkg` + `<package-id>.<host-rid>.<version>.nupkg`; optionally install
   from it into a scratch `--tool-path` (`dotnet tool install <package-id> --tool-path <scratch> --add-source artifacts/nupkg --prerelease`)
   and run `<scratch>/<bin> --version`.
6. DocFX: `docfx docfx.json` (a `dotnet tool install --tool-path <scratch>/docfx docfx` copy if `docfx` isn't
   installed — never `-g`; when `dotnet` is not on `PATH`, set `DOTNET_ROOT`) → `build/docfx/`, 0 warnings.
7. Generate the CLI reference: `dotnet run --project src/<ToolName> -c Release -- gen-docs --output-dir .` → writes
   `docs/modules/ROOT/pages/cli-reference.adoc` (the only Antora page this skill creates) plus `artifacts/man/<bin>.1`
   and `artifacts/completions/*` (gitignored build output).

Report pass/fail per command; quote error output verbatim for a failure only.

## Step 8 — Report

Summarize: resolved `tool-name`, `bin-name`, `package-id`, `description`, `ui`, version, license (or none), and
whether the run scaffolded from scratch, updated an existing project, or stopped. Then, per Step 1 group, the action
taken — **created / updated / replaced / kept as is** — and whether it came from the user or `on-existing`, listing
each mismatch of a kept group and, for a replaced one, what customizations could have been lost (check `git diff`).

State what was included versus omitted and why: `ui` (Terminal.Gui `browse` or not — with `tui`, the action on
`.ui-quality.yml` (**created / updated / replaced / kept as is**), its `accessibility` level, and that the
`[TestCategory("UI")]` view tests write `.ui-screenshots/` text captures that must be gitignored); config files (documented
extension point, not implemented); `sonar` (no file — the keys go to `iru-setup-cli-github-workflows`);
`distribution`/`channels` (recorded only — the tool package settings are always present); which Step 4 versions were
live versus fallback; and any ignored `args` keys. List the Antora pages worth adding once `iru-setup-antora` has run
(usage, exit codes, JSON output schema, using the tool from an agent) and that `cli-reference.adoc` needs a
`nav.adoc` entry.

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path |
|---|---|
| Solution | `<ToolName>.slnx` — folders `/src/`, `/tests/`, `/Solution Items/`; `dotnet sln <ToolName>.slnx list` works |
| Projects | `src/<ToolName>.Core/<ToolName>.Core.csproj` (`net10.0`, assembly `<ToolName>.Core`, `IsAotCompatible`, `IsPackable=false`); `src/<ToolName>/<ToolName>.csproj` (`Exe`, assembly `<bin>`, `PublishAot`, `InvariantGlobalization`, `PackAsTool`, `ToolCommandName <bin>`, `PackageId <package-id>`); `tests/<ToolName>.Core.Tests` and `tests/<ToolName>.Cli.Tests` (`net10.0`, MSTest 4 on VSTest + coverlet.collector) |
| CLI detection | the `Exe` csproj references `System.CommandLine` and sets `PackAsTool`/`PublishAot`; no `UseWPF`/`UseWinUI`/`UseWindowsForms` |
| TUI detection | `src/<ToolName>/<ToolName>.csproj` references `Terminal.Gui`; `src/<ToolName>/Commands/BrowseCommand.cs` + the view `src/<ToolName>/Tui/BrowseView.cs` (`Create(state, toolName)`) |
| TUI UI tests (`ui: tui`) | `dotnet test tests/<ToolName>.Cli.Tests -c Release --filter "TestCategory=UI"` (any host, no lock; also part of the ordinary solution run) — `Tui/BrowseViewTests` renders `BrowseView` on Terminal.Gui's ANSI driver at 60×12 and writes `<UI_SCREENSHOTS_DIR or .ui-screenshots>/screen/BrowseView/{default,many-items,long-content}--{ltr,rtl}--no-color.txt` (`UiScreenshots.SaveText`); `AccessibilityCheck.Apply` applies `.ui-quality.yml`'s level to the `tui-color-only`/`tui-help-line` checks (`enforce` → `[a11y]` failure, `report` → `.ui-screenshots/a11y-report.txt`) |
| Build | `dotnet build <ToolName>.slnx -c Release` (any host; trim/AOT analyzers on) |
| Tests | `dotnet test <ToolName>.slnx -c Release` — Core unit tests + in-process CLI tests; `--filter "TestCategory!=PublishedBinary"` excludes the binary smoke tests (they are inconclusive/skipped unless `__BinEnvPrefix___BINARY` is set) |
| Coverage | `dotnet test tests/<ToolName>.Core.Tests -c Release --settings tests/coverlet.runsettings --collect "XPlat Code Coverage" --results-directory TestResults` → `TestResults/<guid>/coverage.cobertura.xml` + `coverage.opencover.xml`, `[<ToolName>.Core]*` only; the `<bin>` assembly is "not measured" |
| Analyzer SARIF | `<project dir>/obj/<ProjectName>.sarif` per project (via `Directory.Build.props` `ErrorLog`); count results without `suppressions` |
| Format check | `dotnet format <ToolName>.slnx --verify-no-changes --no-restore` |
| AOT publish | `dotnet publish src/<ToolName> -c Release -r <rid> -o artifacts/publish/<rid>` → one native executable `<bin>` (`<bin>.exe` on Windows; ~4.5 MB `ui: none`, ~10 MB `ui: tui` on osx-arm64) plus debug symbols (`<bin>.dSYM`/`<bin>.dbg`/`.pdb`) and, for `ui: tui`, `libonigwrap.*` (TextMateSharp's native regex library — not loaded by `browse`, so archives ship the executable alone). Same-OS only: osx-x64 cross-compiles from osx-arm64; Linux targets need a Linux host or the `mcr.microsoft.com/dotnet/sdk:10.0-noble-aot` image |
| .NET tool packages | pointer `dotnet pack src/<ToolName> -c Release`; per RID (on a host of that OS) `dotnet pack src/<ToolName> -c Release -r <rid>`; framework-dependent fallback `dotnet pack src/<ToolName> -c Release -r any -p:PublishAot=false` → `artifacts/nupkg/<package-id>[.<rid>\|.any].<version>.nupkg`; `ToolPackageRuntimeIdentifiers` = `linux-x64;linux-arm64;osx-arm64;osx-x64;win-x64;win-arm64;any`; push every RID package before the pointer; users run `dotnet tool install -g <package-id>` or `dnx <package-id>` |
| Smoke tests | `__BinEnvPrefix___BINARY=<path> dotnet test tests/<ToolName>.Cli.Tests -c Release --filter TestCategory=PublishedBinary` |
| Generated docs | `dotnet run --project src/<ToolName> -c Release -- gen-docs --output-dir <repo-root>` (hidden command) → `docs/modules/ROOT/pages/cli-reference.adoc`, `artifacts/man/<bin>.1`, `artifacts/completions/{<bin>.bash,_<bin>,<bin>.fish,<bin>.ps1}` |
| DocFX | `docfx docfx.json` → metadata `docfx/api/*.yml` (generated — gitignore it) → site `build/docfx/`; Core API only |
| Version | `Directory.Build.props` `<Version>` (`x.y.z-dev` on gitflow `develop`, `x.y.z` otherwise) — the only version literal; `iru-dotnet-bump-version` edits it; `<bin> --version` prints it verbatim |
| Contract code | exit codes `src/<ToolName>.Core/ExitCode.cs`; envelope `Output/ErrorReporter.cs`; JSON types registered in `Output/CliJsonContext.cs`; global flags `src/<ToolName>/GlobalOptions.cs`; new commands are `ToolCommand`s added in `CliApp.BuildRootCommand` |

## Verification notes

- **Verified for real on 2026-10-16** in `$TMPDIR/iru-verify/cli/dotnet/` (outside this repository; .NET SDK 10.0.402
  in a temp directory, macOS 27 arm64, Xcode command-line tools), rendering this skill's reference files for
  `ui: none` and `ui: tui` (the reference files were round-tripped back into a tree and diffed against the verified
  sources — identical): restore + `dotnet build -c Release` with **0 unsuppressed SARIF results** in all four
  projects; `dotnet format --verify-no-changes` clean; 84 + 33 (`none`) / 87 + 35 (`tui`) tests, all passed except the
  2 skipped `PublishedBinary` ones; Core coverage **line 0.99 / branch 0.99** (cobertura, `tests/<ToolName>.Core.Tests`); DocFX
  2.81.0 0 warnings; Native AOT `dotnet publish -r osx-arm64` 0 warnings (4.5 MB / 9.8 MB) and `-r osx-x64` from the
  arm64 host (x86_64 Mach-O produced; not run — no Rosetta); 27 contract smoke checks on the binary (exit codes 0/2/3,
  stdout purity, JSON golden, `jq -e .schemaVersion`, no ESC when piped and with `NO_COLOR`/`TERM=dumb`/`--no-color`
  on a real pseudo-terminal while colour does appear on a bare pty, quiet broken pipe, `bash -n`/`zsh -n` on the
  generated scripts, bash completion of commands and `--format` values, zsh `compdef` registration, PowerShell 7.6.7
  parse + `TabExpansion2` completion); the `PublishedBinary` tests against the AOT binary; `--version` in ~10 ms;
  `ui: tui` `browse` driven on a sized pseudo-terminal: renders the list and greeting, Esc exits 0, SIGINT exits 130
  and SIGTERM 143, the alternate screen is restored every time, and it runs without `libonigwrap.dylib`; non-TTY
  `browse` exits 2. `dotnet pack` produced the pointer (`DotnetToolSettings.xml` lists the 7 RID packages), the
  osx-arm64 AOT and the `any` packages; `dotnet tool install --tool-path … --add-source artifacts/nupkg --prerelease`
  installed the native osx-arm64 binary, and `dnx <package-id>@0.1.0-dev --yes --add-source …` ran it with exit codes
  propagated and a clean stdout. `gen-docs` wrote the AsciiDoc page, man page and four completion scripts.
- **UI contract (2026-10-16, `$TMPDIR/iru-verify/cli/dotnet-tui-ui/`)**: the reference files were round-tripped into
  `ui: tui` and `ui: none` trees again: both built with 0 unsuppressed SARIF results and `dotnet format` clean; `tui`
  87 + 40 tests passed (the 7 new `[TestCategory("UI")]` view tests among them, writing the 6 `.txt` captures),
  `none` 84 + 31 unchanged; `dotnet publish -r osx-arm64` of `tui` still 0 warnings (9.9 MB) and non-TTY `browse`
  still exits 2. All three accessibility levels were exercised with the key help removed (`enforce` → 6 `[a11y]`
  failures, `report` → `a11y-report.txt` lines and a pass). Terminal.Gui 2.5.0's public test surface used:
  `Application.Create()`, `Init(DriverRegistry.Names.ANSI)`, `Driver.SetScreenSize`, `Begin`/`LayoutAndDraw`/`End`,
  `Driver.ToString()`, `Terminal.Gui.Testing`'s `InjectKey`.
- **Linux arm64** (`mcr.microsoft.com/dotnet/sdk:10.0-noble-aot` under Docker on the same Mac, `ui: tui` render):
  build, 87 + 35 tests, `dotnet publish -r linux-arm64` 0 warnings (10.5 MB, links only libc/libm), the
  `PublishedBinary` tests and `gen-docs` against that binary, 21 smoke checks (those needing jq/python3/zsh were not
  run — apt was unavailable in the container).
- **Negative check**: reflection-based `JsonSerializer.Serialize(object)` in the CLI project fails `dotnet build`
  with IL2026/IL3050, and `GetType().GetMethod(...)` with IL2075 — the trim/AOT analyzers are part of every build.
- **System.CommandLine 2.0.13 facts the templates rely on**: parse errors make `Invoke` print to stderr and return 1
  (hence the pre-invocation check → 2); response files are on by default (`ResponseFileTokenReplacer = null` turns
  them off); `RootCommand` adds a `[suggest]` directive (dotnet-suggest) — `System.CommandLine.StaticCompletions`
  exists only as 3.0 previews, so completion scripts are generated by `CompletionScriptGenerator` from the same tree;
  synchronous actions don't observe cancellation (hence the explicit check before invoking and the async `browse`
  action); `OptionResult.IdentifierTokenCount` counts `-v -v`/`-vv`; with `InvariantGlobalization` its messages are
  English regardless of the user's locale.
- **Unverified locally, never a blocker**: Windows (`win-x64`/`win-arm64` AOT publish, `.exe` behaviour, Windows
  Terminal colour, `PosixSignalRegistration` SIGTERM mapping on Windows), linux-x64, the fish completion script
  (`fish` not installed — its syntax is covered by unit tests only), the published RID packages on NuGet (pushing,
  trusted publishing), WinGet.

Finish with a **Warn explicitly** block:

- Review every generated file before building, committing or distributing; replace the `greet` sample with real
  commands (keep the contract plumbing) and keep `CliJsonContext` registering every output type.
- Run `iru-setup-dotnet-gitignore` — `bin/`, `obj/`, `TestResults/`, `artifacts/` (publish output, packages, man page,
  completions), `build/`, `docfx/api/` and (`ui: tui`) `.ui-screenshots/` must never be committed; `docs/modules/ROOT/pages/cli-reference.adoc` is
  generated but committed (re-run `gen-docs` after any command change).
- The `package-id` must be free on nuget.org before the first `store` release, and every RID package must be pushed
  before the pointer package.
- With `sonar` ≠ `none`, a `SONAR_TOKEN` secret and the Sonar project must exist before CI analysis works.
