---
name: dotnet-repo-workflow
description: >-
  Build, test and prepare a C# or F# patch for merge through the repository's .NET build script.
  When the SDK is missing from PATH, a NuGet change touches packages.lock.json, or Roslyn in-memory
  tests hit CS1061, check those specific failure modes. Not for package-release-verification.
metadata:
  revision: "4"
  areas: "software-development"
  targets: "runtime-agnostic"
  summary: "run the repo's own .NET gates, verify locked NuGet restore, and diagnose missing Roslyn compilation references"
  summary_zh: "运行仓库自带的 .NET 门禁，验证 NuGet 锁定还原，诊断 Roslyn 编译引用缺失"
  kind: "entry"
---

# .NET repo workflow

## Use the repository's gate

Read the repository instructions, CI and `global.json` before choosing a command. Resolve the
SDK with the repository's documented bootstrap or installed toolchain; from the repo root,
`dotnet --list-sdks` shows what is installed and `dotnet --version` shows the selected SDK.
A missing command alone does not distinguish an absent SDK from a PATH problem.

Run the repo's build, format and test entry points; do not substitute a narrower
`dotnet test` for its full gate. Capture each command's actual exit status, not the status of
an output filter. Report failed or skipped checks and any verified baseline failure. Repository
policy owns gate selection; this skill does not authorize committing or publishing.

## Update and verify NuGet locks

- If the repo tracks `packages.lock.json`, update the affected dependency graph with its
  restore command (or `dotnet restore <project> --force-evaluate` when appropriate). Review the
  lock diff alongside the package change, including transitive dependencies and central
  versions if used. Leave unrelated user changes alone; exclude incidental churn.
- Run the repo's locked restore (or `dotnet restore <project> --locked-mode`) from the intended
  SDK and with the repository's feeds and build properties. Locked mode must accept the
  reviewed lock without rewriting it. Fix the mismatch rather than disabling locked mode.

## Diagnose Roslyn in-memory compilation

If the project builds but an analyzer, code-fix or example test reports `CS1061`, inspect the
test compilation's metadata references and imports. The package may be available to the
project but absent from the in-memory compilation. If so, add the dependency to the test
project and put the correct assembly in the harness's explicit reference set. Verify the
target test and repo gate. Keep the example's intended API usage; do not delete it to make
the harness pass.
