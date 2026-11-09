---
name: unity-run-tooling
description: Run version-matched Unity imports, tests, builds, and player profiling while preserving honest native evidence.
engines: [UNITY]
---

# Unity Run Tooling

## When to use

Run version-matched Unity imports, tests, builds, and player profiling while preserving honest native evidence. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-run-tooling` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Locate the matching installed Editor from project version metadata, licensed availability, target modules/SDKs, package lock, project-owned build methods and test selections. Inspect commands before launch; do not install an Editor, module or package or accept licenses. Record the existing project's template/version/packages before project creation or migration; do not overwrite it with a new template.

## Workflow

1. Resolve the approved project and output scope before any Editor launch. Detect an already-open project or lock conflict and avoid competing Editor processes or forced termination of the user's session.
2. Use argument arrays and explicit project paths, logs, target platform, time limits and process cleanup. Record the actual Editor executable/version and command; credentials and licensing tokens must not enter artifacts.
3. Run the project's controlled import/compile validation first. Treat unresolved package restoration or unavailable platform modules as blocked prerequisites rather than switching versions or downloading automatically.
4. Use selected Unity Test Framework EditMode and PlayMode suites with structured result files. Check test discovery and zero-test results explicitly; an Editor exit code alone is insufficient evidence of passed tests.
5. Build through a project-owned static method invoked by the Editor, with an explicit BuildTarget and BuildReport result. Preserve logs and output hashes; standalone dotnet build cannot certify a Unity player build.
6. Launch the produced player on the intended surface and verify startup, content loading, input and shutdown. Use target-device Profiler captures for CPU/GPU, allocations and frame budgets; distinguish Editor overhead.
7. Report graphics limitations: batch mode or -nographics may be useful for imports and tests but cannot prove rendered appearance, physical haptics or device-specific behavior.

Read [packages and project inspection](references/packages-and-inspection.md) for UPM operation ownership, Search and Project Auditor. Use [CLI and Pipeline](references/cli-and-pipeline.md) only when that optional integration is already selected/configured; native Editor batch workflows remain supported.

## Verification

- Exercise one successful fixture and one intentional compile, test or build failure; confirm failed or missing results cannot be reported as passes.
- Check cancelled/time-limited runs terminate only owned process trees and preserve useful logs without leaving the project locked.
- Record missing Editor/modules/licenses as blocked. For Unity web builds, browser smoke tests supplement rather than replace native tooling evidence.
- Package requests must reach a terminal result before dependent work. Test offline inventory, malformed/missing dependencies and failed completion without changing the selected lock or installing packages implicitly.
- For optional CLI operations, prove the intended project/Editor binding, actual completion and reconnection behavior. Readiness requires usable compilation/import state; connection success alone is insufficient.

## Output

Reproducible invocation records, Editor/package/target identities, structured test and BuildReport summaries, hashed player artifacts, smoke/profiler evidence and explicit unavailable checks. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not synthesize native test reports or silently substitute a simulated executable. Installation, license acceptance, signing and publication are separate actions. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity Editor command-line arguments](https://docs.unity3d.com/6000.3/Documentation/Manual/EditorCommandLineArguments.html). Use the documentation matching the installed project version.
- [Unity Test Framework command line](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html). Use the documentation matching the installed project version.

