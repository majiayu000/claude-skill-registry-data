---
name: pester-cli-testing
description: "Configures Pester v5 for testing PowerShell CLIs, scripts, and cmdlets - Describe/Context/It blocks, Should assertions, Mock for isolating external dependencies, BeforeAll/BeforeEach setup hooks, Invoke-Pester with PesterConfiguration for tags, code coverage, and NUnit/JUnit XML output in CI. Use when the unit-under-test is a PowerShell script, function, or CLI tool invoked from pwsh on Windows or cross-platform."
---

# pester-cli-testing

## Overview

[pi]: https://pester.dev/docs/introduction/installation

Per [pester-install][pi], Pester is the standard PowerShell test framework for
unit, integration, and acceptance testing of scripts, functions, modules, and
CLI tools invoked from `pwsh`. It supports Windows PowerShell 3.0 - 5.1 and
PowerShell 6.0.4+ across Windows, Linux, and macOS. When the unit-under-test
is a shell script or binary on Linux/macOS, use `bats-testing` instead; Pester
is the correct choice whenever the subject or test is PowerShell.

## Step 1 - Install

Per [pester-install][pi], Windows 10 / Server 2016+ ship with Pester 3.4.0
built-in. The bundled version cannot be updated via `Update-Module` alone
because its publisher certificate differs from the community-signed Gallery
version. Install Pester v5 side-by-side:

```powershell
# Windows (5.1 or pwsh 7+): -Force enables side-by-side; -SkipPublisherCheck
# accepts the newer certificate
Install-Module -Name Pester -Force -SkipPublisherCheck

# Linux / macOS (pwsh 7+): no bundled version to conflict with
Install-Module -Name Pester

# Verify
Import-Module Pester -PassThru
```

## Step 2 - First test file

Per [pester-quick-start][pqs]:

[pqs]: https://pester.dev/docs/quick-start

Test files must follow the `*.Tests.ps1` naming convention. The outer
`BeforeAll` block dot-sources the script under test so its functions are
available to every nested block:

```powershell
# Get-Greeting.Tests.ps1
BeforeAll {
    . $PSScriptRoot/Get-Greeting.ps1
}

Describe 'Get-Greeting' {
    It 'returns a greeting for the given name' {
        Get-Greeting -Name 'Alice' | Should -Be 'Hello, Alice!'
    }
}
```

Run with:

```powershell
Invoke-Pester -Output Detailed .\Get-Greeting.Tests.ps1
```

## Step 3 - Describe / Context / It

Per [pqs][pqs], `Context` and `Describe` are nearly interchangeable. Use
`Describe` at the top level (function or CLI command name) and `Context` to
group scenarios:

```powershell
Describe 'Invoke-Deploy' {
    Context 'when the target environment is valid' {
        It 'exits 0 and logs a success message' {
            # ...
        }
    }

    Context 'when credentials are missing' {
        It 'throws a terminating error' {
            # ...
        }
    }
}
```

## Step 4 - Should assertions

Per [pqs][pqs], `Should` is the assertion command. Common matchers:

```powershell
$result | Should -Be 'expected'           # strict equality
$result | Should -BeExactly 'Expected'    # case-sensitive equality
$result | Should -BeLike '*partial*'      # wildcard match
$result | Should -Match 'regex\d+'        # regex match
$result | Should -BeNullOrEmpty           # null or empty string/array
$result | Should -BeGreaterThan 0
{ risky-call } | Should -Throw            # expects a terminating error
{ risky-call } | Should -Throw '*message*' # error message wildcard
$result | Should -Not -Be $null           # negated form
```

## Step 5 - BeforeAll / BeforeEach

Per [pqs][pqs], lifecycle hooks load fixtures and reset state.
`BeforeAll` runs once per block; `BeforeEach` runs before every `It`:

```powershell
Describe 'Get-Report' {
    BeforeAll {
        . $PSScriptRoot/Get-Report.ps1
        $script:TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.IO.Path]::GetRandomFileName())
        New-Item -ItemType Directory -Path $script:TempDir | Out-Null
    }

    AfterAll {
        Remove-Item -Recurse -Force $script:TempDir
    }

    BeforeEach {
        # reset any per-test state here
    }

    It 'writes a report file to the output directory' {
        Get-Report -OutputPath $script:TempDir
        Test-Path (Join-Path $script:TempDir 'report.csv') | Should -BeTrue
    }
}
```

Use `$script:` scope when a variable set in `BeforeAll` must be read inside
`It` blocks. Variables declared with plain `$var` in `BeforeAll` are not
visible inside `It` due to PowerShell scoping rules.

## Step 6 - Mock

Per [pester-mock][pm]:

[pm]: https://pester.dev/docs/usage/mocking

> "Mock mocks the behavior of an existing command with an alternate
> implementation."

```powershell
Describe 'Send-Notification' {
    BeforeAll {
        . $PSScriptRoot/Send-Notification.ps1

        Mock Invoke-RestMethod {
            return @{ status = 'ok' }
        }

        Mock Write-Error {}    # suppress error output in test runs
    }

    It 'calls Invoke-RestMethod once with the correct URI' {
        Send-Notification -Message 'deploy done'
        Should -Invoke Invoke-RestMethod -Times 1 -Exactly
    }

    It 'passes a ParameterFilter to scope the mock to specific arguments' {
        Mock Get-Date { return [datetime]'2024-01-01' } -ParameterFilter {
            $Format -eq 'yyyy-MM-dd'
        }
        $result = Get-FormattedDate
        $result | Should -Be '2024-01-01'
    }
}
```

Per [pm][pm], mocks placed in `BeforeAll` apply to all `It` blocks in the
enclosing `Describe`/`Context`; a mock inside an `It` block scopes only to
that test. Use `-Scope` to override. `Should -Invoke` verifies call count:

```powershell
Should -Invoke -CommandName Invoke-RestMethod -Times 1 `
    -ParameterFilter { $Uri -like '*api.example.com*' }
```

Per [pm][pm], `$PesterBoundParameters` (available since Pester 5.2.0)
replaces `$PSBoundParameters` inside mock script blocks.

## Step 7 - Tags

Per [pester-tags][pt]:

[pt]: https://pester.dev/docs/usage/tags

Tags can be applied to `Describe`, `Context`, and `It` blocks. Run a subset
by filtering on tags:

```powershell
Describe 'Invoke-Deploy' -Tag 'Integration' {
    Context 'slow path' -Tag 'Slow' {
        It 'completes a full deployment cycle' -Tag 'E2E' {
            # ...
        }
    }
}
```

```powershell
# Run only Integration tests, excluding slow ones
Invoke-Pester $path -TagFilter 'Integration' -ExcludeTagFilter 'Slow', 'WindowsOnly'
```

Per [pt][pt], tag matching uses `-like` comparison, so wildcards work:

```powershell
Invoke-Pester $path -ExcludeTagFilter 'Slow*', '*Only'
```

## Step 8 - Invoke-Pester with PesterConfiguration

Per [pester-config][pc]:

[pc]: https://pester.dev/docs/usage/configuration

`New-PesterConfiguration` returns a typed configuration object. Cast from a
hashtable for concise setup:

```powershell
$config = [PesterConfiguration]@{
    Run    = @{
        Path = '.\tests'
        Exit = $true          # non-zero exit code on failure (required for CI)
    }
    Filter = @{
        Tag        = 'Unit'
        ExcludeTag = 'Slow', 'WindowsOnly'
    }
    Output = @{
        Verbosity = 'Detailed'
    }
}
Invoke-Pester -Configuration $config
```

Key `Run` properties and their defaults (`Run.Path`, `Run.ExcludePath`,
`Run.Exit`, `Run.TestExtension`) are tabulated in
[references/ci-and-config.md](references/ci-and-config.md).

## Step 9 - Code coverage

Per [pester-coverage][pcov]:

[pcov]: https://pester.dev/docs/usage/code-coverage

```powershell
$config = New-PesterConfiguration
$config.Run.Path                      = '.\tests'
$config.CodeCoverage.Enabled          = $true
$config.CodeCoverage.Path             = '.\src'
$config.CodeCoverage.CoveragePercentTarget = 75   # fail if below 75%
$config.CodeCoverage.OutputFormat     = 'JaCoCo'  # or 'CoverageGutters'
$config.CodeCoverage.OutputPath       = 'coverage.xml'
Invoke-Pester -Configuration $config
```

Per [pcov][pcov], Pester does not traverse directories automatically for
coverage; set `CodeCoverage.Path` explicitly when source files are not
co-located with tests.

## Step 10 - Test result XML and CI

Per [pester-results][pr]:

[pr]: https://pester.dev/docs/usage/test-results

```powershell
$config = New-PesterConfiguration
$config.Run.Path               = '.\tests'
$config.Run.Exit               = $true
$config.TestResult.Enabled     = $true
$config.TestResult.OutputFormat = 'NUnitXml'   # or 'JUnitXml'
$config.TestResult.OutputPath  = 'testResults.xml'
Invoke-Pester -Configuration $config
```

Full CI pipeline definitions - a single cross-platform GitHub Actions matrix
(with code coverage and artifact upload) and the Azure DevOps Publish Test
Results task - are in [references/ci-and-config.md](references/ci-and-config.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Dot-sourcing the script under test inside `It` | Re-executes on every test; slow and leaks state | Dot-source once in `BeforeAll` |
| Using plain `$var` in `BeforeAll`, reading in `It` | PowerShell scope: `It` does not inherit `BeforeAll` locals | Use `$script:var` |
| Mocking in `It` when needed across multiple tests | Mock scopes to that single test only | Move mock to `BeforeAll` or `BeforeEach` |
| Omitting `Run.Exit = $true` in CI config | Pester exits 0 even on failures; CI pipeline passes on broken tests | Set `Run.Exit = $true` |
| Setting `CodeCoverage.Path = '.'` without explicit paths | Pester may miss source files not co-located with tests | Set `CodeCoverage.Path` to the source directory explicitly |
| Using legacy `Invoke-Pester -Script` syntax | Removed in Pester v5; breaks silently on older runners | Use `PesterConfiguration` with `Run.Path` |

## Limitations

- **Mocking scope is version-sensitive.** Pester v5 scopes mocks to their
  placement block (not the entire `Describe`). Code written for v4 may need
  mock placement adjusted.
- **No built-in parallel execution.** Pester v5 runs tests serially within
  a session. Parallelism requires splitting test files across separate
  `pwsh` processes or using a CI matrix.
- **Non-PowerShell binaries.** Pester can invoke any executable, but
  assertion helpers are PowerShell-centric. For deep exit-code / stdout
  testing of Unix binaries, `bats-testing` is more idiomatic.
- **Windows PowerShell 5.1 vs pwsh 7+.** Some Pester 5 features (e.g.
  `$PesterBoundParameters`) require a minimum Pester patch level; pin the
  version in CI with `Install-Module -Name Pester -RequiredVersion 5.x.y`.

## References

- [pester-install][pi] - compatibility, Windows side-by-side install,
  cross-platform `pwsh` install.
- [pqs][pqs] - quick-start, `BeforeAll`, `Describe`/`Context`/`It`, `Should`.
- [pm][pm] - `Mock`, `ParameterFilter`, `Should -Invoke`, scope rules,
  `$PesterBoundParameters`.
- [pc][pc] - `New-PesterConfiguration`, `Run`, `Filter`, `Output`,
  `Invoke-Pester -Configuration`.
- [pcov][pcov] - `CodeCoverage.Enabled`, `CoveragePercentTarget`, formats,
  path scoping.
- [pr][pr] - `TestResult.Enabled`, `OutputFormat`, `OutputPath`, Azure
  DevOps / AppVeyor CI notes.
- [references/ci-and-config.md](references/ci-and-config.md) - cross-platform
  GitHub Actions matrix, Azure DevOps publish task, `Run` property table.
- `bats-testing` - use for shell script /
  Unix binary testing; Pester is the correct choice when the subject or
  test is PowerShell.
- `cli-output-conventions` - what
  to assert on (stable formats, exit codes, stderr vs stdout contracts).
