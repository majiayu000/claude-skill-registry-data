---
name: godot-run-tooling
description: Run version-matched Godot imports, project tests, exports, and profiling without overstating headless or simulated evidence.
engines: [GODOT]
---

# Godot Run Tooling

## When to use

Run version-matched Godot imports, project tests, exports, and profiling without overstating headless or simulated evidence. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-run-tooling` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Locate the matching installed Editor and inspect its --version/--help, project.godot, selected project language, export presets/templates, SDKs and project-owned test harness. C# requires the .NET Editor and compatible SDK.

## Workflow

1. Resolve permitted project and artifact paths before launch. Use argument arrays, bounded execution, retained logs and owned-process cleanup; inspect Editor plugins and tool scripts because import/Editor runs can execute project code.
2. Run the matching Editor's import workflow before parse/build checks. Preserve import metadata and identify missing source assets or plugins; do not install templates or download dependencies automatically.
3. Use --check-only with an explicitly selected script only for its documented parse scope. It does not establish that every scene, script or runtime branch is correct; C# solution compilation uses its own compatible build workflow.
4. Run a project-owned SceneTree script, test scene or explicitly selected test framework with assertion output, test counts and a deliberate failure exit code. Godot --test runs engine tests in a tests-enabled engine build, not the game's test suite.
5. Export using the matching Editor, installed templates and named export_presets.cfg entry through supported --export-debug or --export-release options. Record target, logs and output hashes; export success is distinct from player acceptance.
6. Launch the produced artifact and verify startup, content/input behavior and shutdown. Capture renderer/device performance where applicable; the built-in script profiler does not substitute for C# profiling.
7. Respect platform restrictions: current Godot 4 C# lacks web export, mobile C# support has release-specific limitations, and iOS export requires the supported host/toolchain. Headless/Dummy audio results cannot prove visuals, listening or tactile output.

## Verification

- Run one successful native project fixture and an intentionally failing harness/script to prove errors and zero-test runs cannot appear as passes.
- Exercise timeout/cancellation and inspect output/report integrity, then independently start an exported player when prerequisites exist.
- Report missing matching Editor, templates or SDKs as blocked and label any simulated process tests separately from actual Godot results.

## Output

Engine/language/export identities, reproducible native invocation records, structured project-test results, hashed export artifacts and player/profiling evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install engines/templates, accept platform terms, sign or publish builds implicitly. Version-supported command availability must be checked because unknown Godot flags may be ignored. Independent services and tools retain their architecture contracts.

## References

- [Godot command-line reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html). Select the documentation matching the project release.
- [Godot export overview](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html). Select the documentation matching the project release.

