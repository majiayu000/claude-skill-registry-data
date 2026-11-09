---
name: unreal-run-tooling
description: Run Unreal native compilation, asset validation, automation, cooking, packaging, and profiling with auditable results.
engines: [UNREAL]
---

# Unreal Run Tooling

## When to use

Run Unreal native compilation, asset validation, automation, cooking, packaging, and profiling with auditable results. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-run-tooling` before edits or tool launches. Continue only when the effective engine is `UNREAL` and the skill is eligible. Skill selection never selects the engine. Honor any validated task override and its permitted isolated output scope.

Locate the matching Unreal installation/source build, .uproject, compiler, target configurations, platform SDKs, plugins and project-owned automation entry points. Confirm availability and licensing without installing or accepting terms.

## Workflow

1. Resolve project/output paths and native prerequisites before launch. Inspect argument arrays, time limits and process ownership; preserve user Editor sessions and do not overwrite unrelated build artifacts.
2. Read [native build, editor and test ownership](references/native-tooling.md) for module boundaries, Editor extensions, transactions and test/report requirements. Use Unreal Build Tool for the selected target/configuration and Unreal Header Tool through the normal build path. .Build.cs/.Target.cs C# defines build behavior; it is not gameplay scripting and standalone C# compilation is not native validation.
3. Run supported Blueprint compile and asset validation workflows for the matching engine version. Treat binary assets, maps, redirectors and plugin content as real packages; never create synthetic .uasset evidence.
4. Execute the project's selected Automation/Functional tests with explicit test filters and fresh structured reports. Require the expected nonempty case set and terminal results; reject stale reports, incomplete cases, unexpected skips and process/report disagreement.
5. Use the project's controlled AutomationTool BuildCookRun or equivalent pipeline with explicit platform, maps, configuration, staging and archive paths. Compile, cook, stage and package are distinct results with separate failure surfaces.
6. Launch the produced player for startup/content/input/shutdown smoke tests. Capture Unreal Insights and target rendering/performance evidence where required; retain actual executable and package identities.
7. Bound execution and handle cancellation without leaving owned processes running. Preserve logs and report missing SDKs, engine binaries or plugins as blocked; simulated runners are labeled as simulations.

## Verification

- Use a controlled native fixture plus an intentional failing test or cook input to verify failures and empty test runs cannot pass silently.
- Check generated build/test/cook reports and independently launch the actual packaged artifact.
- Separate commandlet/NullRHI checks from visual, audio, physical-controller and target-device acceptance; no headless result establishes those outcomes.

## Output

Engine/compiler/platform identities, reproducible native commands, structured test/cook/package reports, hashed artifacts and player/profiling evidence with blocked checks. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install toolchains, sign/publish builds or fabricate native success. An unavailable matching engine blocks live acceptance while structural guidance can still be reviewed. Independent tools and services retain their own architecture contracts.

## References

- [Native build, editor and test ownership](references/native-tooling.md): read for extensions, module rules, transactions, Automation and diagnostic workflows.
- [Compiling Unreal C++ projects](https://dev.epicgames.com/documentation/unreal-engine/compiling-game-projects-in-unreal-engine-using-cplusplus). Match the documentation version to the project.
- [Running Automation tests](https://dev.epicgames.com/documentation/unreal-engine/run-automation-tests-in-unreal-engine). Match the documentation version to the project.

