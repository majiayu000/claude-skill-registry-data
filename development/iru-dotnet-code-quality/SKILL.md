---
name: iru-dotnet-code-quality
description: >-
  Run this .NET/C# project or solution's Roslyn analyzers — StyleCop.Analyzers for style/formatting (the .NET
  equivalent of Checkstyle) and Microsoft.CodeAnalysis.NetAnalyzers' CA rules for
  code-quality/design/reliability/security bug detection (the .NET equivalent of PMD + SpotBugs combined), plus
  MSTest's own `MSTEST` analyzers when present — via a clean `dotnet build` with a SARIF diagnostic log (one log per
  project for a multi-project solution, since a single shared `ErrorLog` path is overwritten/corrupted by parallel
  project builds), then read the generated `.sarif` file(s) to summarize every issue found (file, line, rule,
  message), grouped by tool. Windows-desktop aware — on a non-Windows host it passes `-p:EnableWindowsTargeting=true`
  so WPF/Windows Forms projects are analyzed too, and reports a WinUI 3 project (whose XAML compiler only runs on
  Windows) as "not analyzed (needs Windows)" instead of failing the run. Invoke as `/iru-dotnet-code-quality` to check
  the whole solution, or `/iru-dotnet-code-quality <path-or-class-name>` to scope the summary to a specific
  project/file/class — the underlying build always analyzes the whole targeted solution/project (Roslyn analyzers have
  no per-class selector), only the reported summary is filtered; an optional `baseline: <previous issue list>` line
  makes it report only issues not in that baseline. Use whenever the user wants a lint/static-analysis pass called out
  separately from `iru-dotnet-test`/`iru-dotnet-coverage`, instead of eyeballing raw build warnings.
model: haiku
---

# .NET Quality

Run StyleCop.Analyzers and the CA (Code Analysis) rules from Microsoft.CodeAnalysis.NetAnalyzers directly through a
build, and report every issue they find. Both are Roslyn diagnostic analyzers, so both surface through the same
build pipeline and the same SARIF log — there's no separate per-tool CLI invocation the way Checkstyle/PMD/
SpotBugs each have their own Maven goal. This skill only runs static analysis and reports results — it does not
fix issues unless asked to as a follow-up.

## Step 1 — Confirm the analyzers are actually wired up

Before running anything, check what's actually configured, since a clean report from a tool that isn't enabled
would be misleading:

- **StyleCop.Analyzers**: look for a `<PackageReference Include="StyleCop.Analyzers" ... />` in the target
  project's `.csproj` or a shared `Directory.Build.props`/`Directory.Packages.props`. Note whether it's configured
  via `stylecop.json` (referenced as an `<AdditionalFiles>` item) or via `.editorconfig`
  `dotnet_diagnostic.SA####.severity` entries — either is valid.
- **CA rules (Microsoft.CodeAnalysis.NetAnalyzers)**: for SDK-style projects targeting .NET 5+, these ship
  built into the SDK and are enabled by default (`EnableNETAnalyzers` defaults to `true`); check
  `<AnalysisLevel>`/`<AnalysisMode>` in the `.csproj` (e.g. `AnalysisMode=All` enables every CA rule, not just
  the `Recommended` default subset) and `.editorconfig` `dotnet_diagnostic.CA####.severity` overrides. For
  projects targeting older frameworks, or that want a pinned analyzer version, check instead for an explicit
  `<PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" ... />`.
- If neither is configured on the project(s) in scope, say so plainly in the Step 4 report instead of reporting a
  false "zero issues" — the build will simply have nothing to emit for that tool.
- **Windows desktop projects** (`UseWPF`/`UseWindowsForms`/`UseWinUI` in a csproj): note the host (Windows when
  `uname -s` fails or prints `MINGW*`/`MSYS*`/`CYGWIN*`, or `$OS` is `Windows_NT`). Off Windows, WPF and Windows
  Forms projects build — and are analyzed — only with `-p:EnableWindowsTargeting=true` (otherwise `NETSDK1100`); a
  **WinUI** project cannot build off Windows at all (its XAML compiler is a Windows executable), so exclude it from
  the build and report it as **not analyzed (needs Windows)** — never as zero issues.
- **`baseline:`** argument (passed by the `*-code-one-task-group` skills): keep it aside for Step 4.

## Step 2 — Run a clean build with a SARIF diagnostic log

```bash
dotnet clean [<path-to-.sln-or-.csproj>]
dotnet build [<path-to-.sln-or-.csproj>] --no-incremental "-p:ErrorLog=./dotnet-code-quality.sarif%2Cversion=2"
```

- `dotnet clean` first, then `--no-incremental`, is required for the same reason `mvn clean compile` precedes
  SpotBugs: an up-to-date incremental build can skip re-analyzing unchanged files, silently leaving a stale (or
  absent) SARIF log rather than one reflecting the current source.
- `-p:ErrorLog=<path>,version=2` tells the Roslyn compiler to emit every diagnostic — compiler and analyzer alike —
  as a SARIF v2.1 log at `<path>`, regardless of whether the build itself succeeds or fails. The `%2C` escapes the
  comma so MSBuild doesn't split it into two properties; quote the whole `-p:` argument as shown.
- If the working directory (or repository root) contains a single `.sln`, `dotnet build`/`dotnet clean` target it
  by default — no need to name it explicitly, same convention as `iru-dotnet-test`. If there are multiple `.sln` files
  and no obvious default, ask which one to target unless the user already named a project/path.
- If the build fails outright due to a genuine compile error (not just an analyzer warning promoted by
  `TreatWarningsAsErrors`/`WarningsAsErrors`), the SARIF log may be incomplete or absent for the affected
  project(s) — report the compile failure and don't read a stale prior log. If the failure is purely
  warnings-as-errors from StyleCop/CA rules, the SARIF log is still written (diagnostics are captured as they're
  emitted, before that promotion fails the build) — proceed to read it normally.

**The repository may already write one log per project.** If `Directory.Build.props` (or the csproj) sets
`<ErrorLog>` itself — the `iru-setup-windows-app` scaffold sets
`<ErrorLog Condition="'$(ErrorLog)' == ''">$(MSBuildProjectDirectory)/obj/$(MSBuildProjectName).sarif,version=2.1</ErrorLog>`
— don't pass `-p:ErrorLog` (a command-line value wins and would collapse them back into one file); run
`dotnet clean` then `dotnet build [<solution>] --no-incremental -p:TreatWarningsAsErrors=false
[-p:EnableWindowsTargeting=true]` and read every `*/obj/*.sarif` it produced (`find . -path '*/obj/*.sarif'`) in
Step 3. Verified: a whole-solution build wrote four valid one-run logs that way.

**Otherwise, the single-file form above is only safe for one project.** With a solution, every project's compiler writes to the
same `ErrorLog` path, and parallel builds overwrite each other — verified: the resulting file was not even valid JSON
("Extra data" after the first run object). Worse, with `TreatWarningsAsErrors` a failing library stops its dependants
(e.g. the WPF app on top of Core) from being compiled, so their issues never reach any log. For a solution (or any
project with project references), build once, then re-compile each project on its own with its own log:

```bash
mkdir -p ./dotnet-code-quality
dotnet clean [<solution>]
dotnet build [<solution>] -p:TreatWarningsAsErrors=false [-p:EnableWindowsTargeting=true]   # dependencies in place
for p in $(dotnet sln <solution> list | grep -E '\.csproj$'); do                              # skip WinUI projects off Windows
  n=$(basename "$p" .csproj)
  dotnet build "$p" --no-restore --no-incremental -p:BuildProjectReferences=false -p:TreatWarningsAsErrors=false \
    [-p:EnableWindowsTargeting=true] "-p:ErrorLog=$PWD/dotnet-code-quality/$n.sarif%2Cversion=2"
done
```

- `-p:BuildProjectReferences=false` keeps the per-project `ErrorLog` global property from flowing into (and
  overwriting from) referenced projects; `-p:TreatWarningsAsErrors=false` lets every project compile so every
  project's diagnostics are captured — the analyzers' severities are unchanged, an `error`-severity rule from
  `.editorconfig` still shows as `error` in the log. Use an absolute `ErrorLog` path (a relative one resolves per
  project directory).
- `-p:EnableWindowsTargeting=true` only on a non-Windows host with WPF/Windows Forms projects; leave WinUI projects
  out of the loop there (Step 1).
- Read every `./dotnet-code-quality/*.sarif` in Step 3 (one `run` each). A WPF project's markup-compile pass doesn't
  produce a second run in its log (verified).

## Step 3 — Read the generated SARIF log, scoped to the request if given

`./dotnet-code-quality.sarif` (or wherever `ErrorLog` pointed) can be large on a solution with many projects/
issues, and the build in Step 2 still analyzed the whole targeted solution/project regardless of scope (Roslyn
analyzers have no per-file CLI selector equivalent to Surefire's `-Dtest`) — so a scoped invocation should filter
before reading the full file rather than after.

**With no argument** (whole solution): read the file in full.

**With a specific project/file/class name**: if `jq` is available (`jq --version`), filter to just the matching
results instead of loading the whole file into context:
```bash
jq '[.runs[].results[] | select(.locations[0].physicalLocation.artifactLocation.uri | endswith("/<Name>.cs"))]' \
  ./dotnet-code-quality.sarif
```
(match the named project's directory instead of a `.cs` suffix if scoping to a whole project). If `jq` isn't
available, read the full file — there's no clean line-based extraction for JSON the way `awk`'s range pattern
works for the Checkstyle/PMD skill's XML, so filtering after a full read is the fallback here, not a first
resort.

Its structure groups results by run/tool:

```json
{
  "runs": [
    {
      "tool": { "driver": { "name": "Microsoft.CodeAnalysis.CSharp", "rules": [ ... ] } },
      "results": [
        {
          "ruleId": "SA1101",
          "level": "warning",
          "message": { "text": "Prefix local calls with this" },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": { "uri": "Services/Foo.cs" },
                "region": { "startLine": 42, "startColumn": 9 }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

Every project built contributes its own `run` entry, but `results` across all runs use the same `ruleId` scheme —
classify by the `ruleId` prefix, not by which `run`/`tool.driver.name` it came from:

- **`SA` (and `SX`) prefix** → StyleCop.Analyzers — style/formatting/ordering issues, the equivalent of Checkstyle
  findings.
- **`CA` prefix** → Microsoft.CodeAnalysis.NetAnalyzers — design, reliability, performance, and security rules,
  the equivalent of PMD + SpotBugs findings combined into one rule family.
- **`CS` prefix** → plain compiler warnings/errors (nullable-reference warnings, obsolete-API warnings, etc.) —
  not from either analyzer; note them separately if present, but they're out of this skill's primary scope.
- **`IDEnnnn` prefix** → built-in .NET "IDE style" analyzers driven by `.editorconfig` `dotnet_style_*`/
  `csharp_style_*` settings — also not from either named tool; note separately if present, same as `CS`.
- **`MSTEST` prefix** → MSTest's analyzers (shipped with the MSTest 3/4 packages, so they run in test projects) —
  test-code correctness (`MSTEST0032` always-true assertion, `MSTEST0044` obsolete `[DataTestMethod]`, …); report them
  as their own group. Many default to `note`/`info` level and only matter when `TreatWarningsAsErrors` or
  `.editorconfig` raises them.
- **`WPF`/`WFO`/`WFAC` prefixes** → WPF and Windows Forms SDK diagnostics (e.g. `WPF0001`: an experimental API such as
  setting `ThemeMode` from code) — report with the CS/IDE bucket, named.
- **`MVVMTK` prefix** → CommunityToolkit.Mvvm source-generator diagnostics (e.g. `MVVMTK0042`: use a partial property
  instead of an `[ObservableProperty]` field) — report as their own small group when present.

A result carrying a non-empty `suppressions` array was suppressed in source (`[SuppressMessage]`, `#pragma warning
disable`, a global suppression) — the compiler still logs it (verified). Don't count it as an issue; mention the
number of suppressed results separately.

For each `result`, record: file (`artifactLocation.uri`, relative to the project), line (`region.startLine`), rule
ID, severity (`level`: `error`/`warning`/`note`), and the message text. A `ruleId` not present in `tool.driver.
rules` for that run can still be looked up in another run's `rules` array if the same analyzer package is
referenced by multiple projects.

## Step 4 — Report

Group findings by tool (StyleCop.Analyzers, then CA rules), then by file. For each issue, give file:line, the rule
ID, severity, and the message. State a total count per tool at the top and an overall total; if a tool found zero
issues in the requested scope, say so — but if that's because the tool isn't actually configured (Step 1), say
that explicitly instead of implying a clean pass. If `CS`/`IDE` diagnostics were also present, mention them briefly
as a separate, out-of-scope bucket rather than folding them into either tool's count.

With a `baseline:` argument, compare by (rule id, file, and — when the line hasn't moved — line): report only issues
not present in the baseline, plus a one-line count of baseline issues that disappeared. Name every project that was
not analyzed on this host (a WinUI project off Windows) — that is "not analyzed", never "no issues".

Do not attempt to fix any of the issues found, or modify project files/`.editorconfig`/`stylecop.json` — that's a
follow-up the user drives explicitly.

## Known quirks

Verified in `$TMPDIR/iru-verify/windows/gates/` on macOS 27 (arm64), .NET SDK 10.0.402, StyleCop.Analyzers
1.2.0-beta.556 (as a `GlobalPackageReference` in `Directory.Build.props` with `stylecop.json` as `AdditionalFiles`),
`AnalysisLevel latest-recommended`, `TreatWarningsAsErrors`, a `net10.0` Core library, a WPF app, MSTest 4.5.1 Core
tests and a `net10.0-windows` FlaUI test project:

- A single `dotnet build <solution> --no-incremental "-p:ErrorLog=<one file>%2Cversion=2"` produced a 650 KB file that
  failed to parse (`json.decoder.JSONDecodeError: Extra data`), and — because Core failed under
  `TreatWarningsAsErrors` — the WPF app on top of it was never compiled, so a planted `CA1304` in the app was missing.
  The per-project loop in Step 2 produced four valid one-run logs, each with its own project's issues (`CA1304`/`CA1311`
  in both Core and the WPF app, `MSTEST*` notes in the test projects), all exiting 0.
- Off Windows, the WPF project and the `net10.0-windows` test project were analyzed with `EnableWindowsTargeting`; a
  WinUI 3 project (Windows App SDK 2.5.1) failed to build at all (`XamlCompiler … output.json was not created`) —
  hence "not analyzed (needs Windows)".
- Configuration findings worth knowing when a repository adopts StyleCop with file-scoped namespaces: `SA1200` fires
  on every `using` placed outside the namespace unless `stylecop.json` sets `orderingRules.usingDirectivesPlacement`
  to `outsideNamespace`; `SA0001` fires in a project that sets `GenerateDocumentationFile` to `false`; `CA1707` flags
  `Method_Scenario_Result` test names. These are configuration choices to report, not code defects to fix here.
- With the `iru-setup-windows-app` `Directory.Build.props` `ErrorLog` (`$(MSBuildProjectDirectory)/obj/$(MSBuildProjectName).sarif,version=2.1`),
  one plain `dotnet build --no-incremental -p:TreatWarningsAsErrors=false` of the solution wrote valid per-project
  logs; members marked `[SuppressMessage]` still appeared as results with a `suppressions` array.
- **Unverified locally (needs Windows)**: analyzing a WinUI project.
