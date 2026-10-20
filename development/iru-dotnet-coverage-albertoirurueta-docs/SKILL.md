---
name: iru-dotnet-coverage
description: >-
  Generate a code coverage report for a .NET project or solution via `dotnet test --collect:"XPlat Code Coverage"`
  (the Coverlet collector) — or, for test projects on Microsoft.Testing.Platform, the platform's `--coverage`
  extension — scoped to the test selector given (same selector syntax as the `iru-dotnet-test` skill), then read the
  generated `coverage.cobertura.xml` to report the exact line-coverage percentage for the specific class(es) touched —
  using that same file's per-line `hits` data to show which lines/branches are still uncovered. Uses the repository's
  `tests/coverlet.runsettings` (Cobertura + OpenCover formats, attribute exclusions) when present. Windows-desktop
  aware — on a non-Windows host it passes `-p:EnableWindowsTargeting=true` and measures only test projects that can
  run there, always excludes `[TestCategory("UI")]` UI-automation tests (they never count toward coverage), and for a
  Windows desktop app (WPF/WinUI 3/Windows Forms) measures the UI-free Core project while reporting the app/UI
  assemblies as "not measured" rather than 0%. Invoke as `/iru-dotnet-coverage <selector>
  [TargetClass1,TargetClass2,...]`, or `/iru-dotnet-coverage` with no argument to run the full suite and report
  whole-solution coverage; optional `key: value` lines — `project: <test-project>`, `bar: <percent>`. Use whenever the
  user wants to check, or verify a coverage bar (e.g. "at least 80% line coverage") for a class or set of classes,
  instead of eyeballing `dotnet test` output.
model: haiku
---

# .NET Coverage

Run Coverlet (via `dotnet test`'s built-in "XPlat Code Coverage" collector) against a scoped (or full) test run
and report the exact, measured coverage percentage for the class(es) the user cares about. This skill only
measures and reports coverage — it does not add tests or modify source/test code unless asked to as a follow-up.

## Step 0 — Parse the arguments and detect the shape

- Positional: an optional test selector, then optional target class names (comma-separated). `key: value` lines,
  all optional: `project: <path>` (the test project to run), `bar: <N>` (report pass/fail against N% line coverage).
- Detect Windows-desktop projects, the host, and the test runner exactly as `iru-dotnet-test`'s Step 0 does (UI apps
  via `UseWPF`/`UseWinUI`/`UseWindowsForms`, `net*-windows*` test projects, `[TestCategory("UI")]` tests,
  Microsoft.Testing.Platform via `global.json` `test.runner`).
- **Windows desktop app** (a `WinExe` UI project exists): the coverage subject is the UI-free Core project
  (`src/<App>.Core`, plain `net10.0`) measured by its portable test project (`tests/<App>.Core.Tests`). Every type in
  the app project (XAML code-behind, forms, converters, UI services, `App`) and in any other `net*-windows*`
  assembly is **not measured** — list such target classes under that heading in the report, never as 0%.
- **Runsettings**: if `tests/coverlet.runsettings` (or a `*.runsettings` the test project's `<RunSettingsFilePath>`
  names) exists, use it — it is where the repository sets the output formats (`cobertura,opencover`) and exclusions
  (`ExcludeByAttribute` `GeneratedCodeAttribute`/`CompilerGeneratedAttribute`/`ExcludeFromCodeCoverageAttribute`,
  `Exclude` assembly filters).

## Step 1 — Determine the test scope

If the user gave a selector, it uses the exact same syntax as the `iru-dotnet-test` skill's Step 1 table (class,
class+method, several classes/methods, wildcard/namespace pattern, trait/category expression, project/solution
path). If no selector was given, run the whole suite.

Important: coverage is only recorded for code actually exercised by the tests that ran in this invocation. If a
class under test is covered by tests spread across multiple test classes, the selector must include all of them
— scoping to just one will undercount that class's real coverage. When in doubt about whether a selector covers
everything relevant to the target class, prefer a broader selector (e.g. the whole namespace, or the full suite)
over a narrow one.

**UI tests never count**: whenever Step 0 found `[TestCategory("UI")]` tests, AND the filter with
`TestCategory!=UI` (parenthesize an `|` group first: `"(FullyQualifiedName~A|FullyQualifiedName~B)&TestCategory!=UI"`),
or use `--filter "TestCategory!=UI"` for a full run.

**Windows desktop on a non-Windows host**: never point the run at the whole solution — a `net*-windows*` test
project aborts it (see `iru-dotnet-test`'s Known quirks). Run each portable test project separately (normally just
`tests/<App>.Core.Tests`), and say in the report which test projects weren't run and why.

## Step 2 — Determine the target class(es) to report on

- If the user (or the calling skill) explicitly named target class(es), use those.
- Otherwise, infer them from the test selector by convention: a test class `FooTests` targets `Foo`,
  `FooTests.TestSomething` still targets `Foo`. For several test classes, infer one target class per test class.
- If the selector is a wildcard, namespace pattern, or trait/category expression, target classes can't be
  inferred by name — report on every class touched by that run (Step 4 already surfaces all of them), or ask the
  user which class(es) they care about if the run touches many unrelated ones.
- Windows desktop: target classes that live in the app project go straight to the "not measured" list.

## Step 3 — Run the coverage collection

```bash
rm -rf ./TestResults
dotnet test [<path-to-.sln-or-.csproj>] --filter "<expression>" --collect:"XPlat Code Coverage" --results-directory ./TestResults
```

Omit `--filter "<expression>"` entirely to run the full suite (but keep `TestCategory!=UI` when UI tests exist).
With a runsettings file, add `--settings tests/coverlet.runsettings`, e.g. for a Windows desktop app:

```bash
dotnet test tests/<App>.Core.Tests --filter "TestCategory!=UI" --settings tests/coverlet.runsettings \
  --collect "XPlat Code Coverage" --results-directory ./TestResults
```

(append `-p:EnableWindowsTargeting=true` on a non-Windows host when anything in the build graph uses WPF/WinForms.)

Notes:
- This requires the `coverlet.collector` NuGet package on the test project(s) being run — it ships by default in
  projects created from the `mstest`/`nunit`/`xunit` `dotnet new` templates. If a test project is missing it,
  `--collect` silently produces nothing to read; check the `.csproj` (or `Directory.Packages.props` with central
  package management) for `coverlet.collector` first, and if it's absent, tell the user to add it
  (`dotnet add package coverlet.collector`) rather than reporting a false 0%.
- Each run writes a new GUID-named subfolder under the results directory containing `coverage.cobertura.xml` (and
  `coverage.opencover.xml` when the runsettings asks for both formats — the OpenCover file is what SonarScanner for
  .NET reads; this skill reads the Cobertura one). Delete the results directory first (`rm -rf ./TestResults`) so
  there's no risk of reading a stale report left over from an earlier run — this is the .NET equivalent of the
  `clean` goal wiping JaCoCo's previous `jacoco.exec`.
- If the build or test run fails, report that failure — don't attempt to read a coverage report that wasn't
  (re)generated.
- **Microsoft.Testing.Platform** test projects (Step 0): `coverlet.collector` is a VSTest data collector and does not
  work there (verified: exit code 5). Use the platform's code-coverage extension instead (shipped with the MSTest
  metapackage), writing Cobertura directly:
  ```bash
  dotnet test --project tests/<App>.Core.Tests --filter "TestCategory!=UI" --coverage \
    --coverage-output-format cobertura --coverage-output coverage.cobertura.xml --results-directory "$PWD/TestResults"
  ```
  (pass an absolute `--results-directory`; a relative one resolves against the test project's output folder).

## Step 4 — Read the exact coverage from `coverage.cobertura.xml`

Find the generated file (`find ./TestResults -name coverage.cobertura.xml`, since it's nested under a run-guid
folder). For a small, known number of target classes from Step 2 (the common case — including a plain "are we
above N%?" check), extract just their `<class>...</class>` block(s) instead of reading the whole file — this
report carries full per-line `hits` data for every class in the run, which can be large on a solution with many
classes:

```bash
awk '/<class [^>]*name="<FullyQualifiedName>[\/"]/,/<\/class>/' <path-to-coverage.cobertura.xml>
```

The pattern matches the class itself and its compiler-generated nested types (async state machines and lambdas
appear as separate `<class name="Ns.Foo/&lt;SaveAsync&gt;d__8" …>` entries — count them as part of `Foo`), and works
whatever the attribute order (Coverlet writes `name` first, Microsoft's code-coverage extension writes it after the
rates). If a target class is split across multiple `<class>` entries (partial classes, nested state machines),
sum the underlying `<line>` counts across all of them (see below). If Step 2 couldn't narrow down to specific class
names (a wildcard/namespace-pattern/full-suite run touching many classes), read the whole file instead — composing
this extraction for many classes isn't worth it once there are more than a handful.

Its overall structure is:

```xml
<coverage line-rate="..." branch-rate="...">
  <packages>
    <package name="...">
      <classes>
        <class name="MyProject.Services.Foo" filename="..." line-rate="..." branch-rate="...">
          <methods>
            <method name="..."><lines><line number="12" hits="1" branch="False"/>...</lines></method>
          </methods>
          <lines>
            <line number="12" hits="1" branch="False"/>
            <line number="13" hits="0" branch="True" condition-coverage="50% (1/2)"/>
            ...
          </lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
```

Every line appears **twice** — under its `<method>` and again in the class-level `<lines>` after `</methods>`.
Count only the class-level list (or de-duplicate by line number), e.g.:

```bash
awk '/<class [^>]*name="<FullyQualifiedName>[\/"]/,/<\/class>/' <file> | awk '/<\/methods>/{m=1} /<class /{m=0} m && /<line /'
```

For each target class from Step 2, compute:

```
line coverage %   = count(<line hits!="0">) / count(<line>) * 100
branch coverage % = count(<line branch="True" hits!="0">) / count(<line branch="True">) * 100   (n/a if there are no branch lines, e.g. records with no conditional logic)
```

The `branch` attribute is written `True`/`False` (capitalized) by both Coverlet and Microsoft's extension — match it
case-insensitively. For branch lines, `condition-coverage="50% (1/2)"` is the more precise measure.

Prefer counting `<line>` elements directly over trusting the pre-computed `line-rate`/`branch-rate` attributes at
face value — they're accurate for a single `<class>` entry, but if a target class is split across multiple
`<class>` entries (partial classes), sum the underlying `<line>` counts across all of them rather than averaging
the attributes. Use the XML, not a generated HTML report, as the source of truth, exactly as the `iru-java-coverage`
skill reads JaCoCo's CSV rather than its HTML tables.

If a target class doesn't appear in the XML at all, it means no code in that class executed during this run
(either it's dead/unreachable from the tests that ran, or the selector didn't include tests that exercise it) —
report 0%, not an error. Exception: a class in a Windows desktop app's UI/app project is absent because that
assembly isn't measured at all — report it as "not measured", not 0%.

## Step 5 — Report results

State, per target class, the line coverage percentage (and branch coverage if relevant to the discussion),
computed from actual XML numbers — never estimate or guess. If the user's bar is "at least N%": say clearly
whether each class meets it.

For classes under the bar, point to exactly what's uncovered directly from the same XML — no separate HTML report
is needed, unlike JaCoCo, since Cobertura's `<lines>` list already carries per-line hit data: every `<line
number="N" hits="0"/>` under that class is an uncovered line, and every `<line branch="True" hits="1"
condition-coverage="50% (1/2)"/>` is a partially-covered branch. List those exact line numbers when the user wants
to know precisely which lines/branches to target with new tests, rather than just the aggregate percentage.

For a Windows desktop app, add a **Not measured (UI layer)** list: the app-project/`net*-windows*` classes in scope,
which never count toward the bar; and name any test project that wasn't run on this host (e.g. the UI-test project
off Windows).

Do not add tests, modify source/test code, or re-run anything to try to raise coverage — that's a follow-up the
user (or another skill) drives explicitly.

## Known quirks

Verified in `$TMPDIR/iru-verify/windows/gates/` on macOS 27 (arm64), .NET SDK 10.0.402, MSTest 4.5.1, coverlet.collector
10.1.0, CommunityToolkit.Mvvm 8.4.2:

- `dotnet test tests/<App>.Core.Tests --filter "TestCategory!=UI" --settings tests/coverlet.runsettings --collect "XPlat
  Code Coverage" --results-directory ./TestResults` wrote both `coverage.cobertura.xml` and `coverage.opencover.xml` in
  one GUID folder (runsettings `<Format>cobertura,opencover</Format>`). Without runsettings only Cobertura is written.
- MVVM Toolkit generated members (`[ObservableProperty]`/`[RelayCommand]` partials, `GeneratedCode`/
  `ExcludeFromCodeCoverage`-attributed) did not appear in the report with or without the runsettings — the line
  counts cover only hand-written code.
- Async methods appear as nested `Foo/&lt;MethodAsync&gt;d__N` classes; each line is listed under its method and again
  at class level; `branch="True"` is capitalized.
- Under Microsoft.Testing.Platform, `--collect "XPlat Code Coverage"` failed the run (exit 5); `--coverage
  --coverage-output-format cobertura` produced an equivalent Cobertura file (attribute order differs, absolute
  `filename` paths).
- **Unverified locally (needs Windows)**: coverage of `net*-windows*` test projects (deliberately never part of the
  bar here).
