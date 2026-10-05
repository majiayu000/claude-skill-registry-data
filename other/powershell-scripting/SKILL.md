---
name: powershell-scripting
description: >-
  Use when writing, reviewing, debugging, or testing PowerShell `.ps1` scripts and
  advanced functions, including parameters, pipeline objects, streams, native
  commands, filesystem safety, PowerShell 7 portability, Pester, and
  PSScriptAnalyzer. Do not use merely to run an existing script, author Bash or batch
  files, package a module or DSC resource, or perform live system or tenant
  administration.
argument-hint: "[PowerShell script task, code, runtime matrix, or failure]"
---

# PowerShell scripting

Build a script contract before writing code. Preserve structured objects, literal
data, mutation authority, and failure evidence across every PowerShell boundary.

## Inspect first

Inspect repository instructions, existing scripts and tests, CI, module manifests,
`#requires`, and configuration before choosing syntax. Inspect the installed version
rather than assuming a documented version. When execution is available, record:

```powershell
$PSVersionTable | Select-Object PSEdition, PSVersion, Platform, OS
Get-Module -ListAvailable Pester, PSScriptAnalyzer |
    Sort-Object Name, Version -Descending |
    Select-Object Name, Version, Path
```

Choose the runtime branch from evidence:

| Declared target | Action |
|---|---|
| Supported PowerShell 7 only | Use current PowerShell 7 semantics and test every claimed OS. |
| PowerShell 7 plus Windows PowerShell 5.1 | Use syntax and APIs supported by both; execute tests in both runtimes on Windows. |
| Windows-only provider or command | Isolate the platform branch, fail clearly elsewhere, and test on Windows. |
| Target unknown | Preserve existing compatibility and ask for the matrix before introducing version-specific behavior. |

Read [compatibility rules](references/compatibility.md) when a script crosses a
runtime or OS boundary.

## Workflow

1. Define parameters, pipeline input, success output, diagnostics, side effects,
   accepted native exit codes, and cleanup behavior.
2. Decide the runtime/OS matrix from repository evidence; do not infer portability
   from a `.ps1` suffix.
3. Use an advanced script or function when validation, pipeline processing, common
   parameters, or `ShouldProcess` behavior belongs to the contract.
4. Keep values typed and structured through processing. Format or serialize only at
   an explicit output boundary.
5. Implement errors and native failures at their actual boundaries; preserve context
   and clean up in `finally` where ownership requires it.
6. Parse, analyze, and execute the narrow tests, then run every claimed runtime and
   platform lane.

## Semantic rules

### Parameters and pipeline

- Put `param(...)` before executable script statements. Use `[CmdletBinding()]` when
  the script needs common parameters, advanced validation, or `SupportsShouldProcess`.
- Use parameter sets only for genuinely incompatible invocation shapes. Make the
  default set explicit when omission would be ambiguous.
- Use `begin` for invocation setup, `process` for each pipeline item, `end` for final
  aggregation, and `clean` only when the declared runtime supports it.
- Emit domain objects on the success stream. `Write-Host` is presentation, not data;
  `return` does not prevent earlier uncaptured success output from becoming output.
- Do not collect an unbounded pipeline merely for convenience. State ordering and
  cardinality when they are part of the interface.

Read [parameters, objects, and streams](references/execution-semantics.md) when the
task combines pipeline input with multiple output or diagnostic channels.

### Paths and mutations

- Resolve paths relative to `$PSScriptRoot` when they belong to the script, not the
  caller's current directory.
- Use `-LiteralPath` for caller-supplied literal paths. Accept wildcard semantics only
  through a separately named and documented parameter.
- For deletion, overwrite, service/configuration change, or another consequential
  mutation, use `SupportsShouldProcess` and gate the operation with
  `$PSCmdlet.ShouldProcess(...)`.
- Validate the exact target before mutation. Reject empty, root, unresolved, or
  scope-escaping targets rather than broadening them.
- Do not claim that `-WhatIf` covered a nested command unless the script itself gates
  that command.

### Errors, security, and native processes

- Catch only errors the script can classify or enrich. `try`/`catch` handles
  terminating errors; use `-ErrorAction Stop` at a boundary only when converting its
  non-terminating errors is part of the contract.
- Re-throw or create a terminating error when the script cannot produce its promised
  result. Do not use an empty catch, broad success exit, or global preference change
  to hide failure.
- Pass native executable arguments as separate values. Never use `Invoke-Expression`
  to turn data into source code, and never concatenate an untrusted command string.
- After a native invocation, evaluate its exit code independently of PowerShell's
  error stream. Define accepted nonzero codes when the tool has them.
- Keep secrets out of source, logs, command lines, and serialized diagnostics. Use an
  existing protected secret boundary; do not invent credential storage.

Read [security and mutation boundaries](references/security-safety.md) and
[native-command boundaries](references/native-commands.md) for these branches.

## Evaluated recipes

Load only the matching recipe from
[the evaluated script recipes](references/recipes-core.md):

- `powershell.safe-literal-removal`: previewable deletion of bounded literal files.
- `powershell.pipeline-object-transform`: one stable object per pipeline input.
- `powershell.native-argv-exit`: separate native arguments and enforce exit status.
- `powershell.dual-runtime-guard`: reject unsupported runtime/platform combinations.
- `powershell.parse-without-execution`: return parser evidence without running code.
- `powershell.pester-ci-gate`: run a pinned Pester suite and fail on test failures.
- `powershell.validated-json-ingestion`: validate JSON against a schema before parsing.
- `powershell.bounded-rest-request`: bound an idempotent REST request and expose status.
- `powershell.checksum-verified-download`: stage, verify, and publish a download safely.
- `powershell.bounded-parallel-file-hash`: throttle parallel work and restore input order.

Recipes are semantic anchors, not blind templates. Preserve their invariants and
adapt them only after inspecting the target contract.

## Verification contract

Run the lowest-cost applicable checks in this order:

1. Parse without executing the script and fail on every parser error.
2. Run PSScriptAnalyzer with the repository's pinned version and settings; explain or
   deliberately configure suppressions rather than hiding findings ad hoc.
3. Run focused Pester tests for parameter binding, pipeline shape, empty/malformed
   input, literal metacharacter paths, `-WhatIf`, native failure, and cleanup.
4. Run the relevant project suite in each declared PowerShell/runtime and OS lane.
5. Exercise a preview or disposable fixture before any attended real mutation.

Analyzer compatibility rules are evidence about referenced syntax, commands, and
types; they do not prove runtime behavior. A macOS or Linux PowerShell 7 pass does not
prove Windows PowerShell 5.1 or Windows-provider behavior. See
[the verification matrix](references/verification.md).

## Completion

Complete the task only when the declared interface and mutation scope match the
implementation, success output contains only promised data, failures reach the
correct boundary, deterministic tests cover the dangerous paths, and every claimed
runtime/platform lane has direct evidence. Report unavailable lanes and unexplained
analyzer findings instead of weakening the claim.
