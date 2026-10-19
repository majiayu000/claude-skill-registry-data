---
name: fitness-tests
description: "Generates architecture fitness tests for a Unity project: EditMode NUnit tests that read the compiled assemblies and fail on new violations of the mechanical Löwy rules (closed architecture, Design Don'ts #2 and #6-#12, gerund naming, Managers per subsystem), with the project profile's Approved deviations and Known debt as the baseline. Use when the user wants the architecture enforced in CI, asks for architecture or fitness tests, or after an audit to stop findings from coming back."
argument-hint: "[output folder, default Assets/Tests/Architecture/Editor]"
---

Part of the `lowy` plugin, which depends on the `dmf` plugin: invoke skills by their namespaced name (`lowy:arch-reviewer` for this plugin, `dmf:domain-modeling` for DMF).

Generate architecture fitness tests into: $ARGUMENTS (default `Assets/Tests/Architecture/Editor`).

Templates live in `${CLAUDE_PLUGIN_ROOT}/skills/fitness-tests/templates/`.

## What the Tests Check

The analyzer reads the compiled assemblies with Mono.Cecil.
It sees fields, signatures, locals, every call and allocation, static calls, and code inside lambdas, iterators and async methods.

| Rule (exact string in results) | Mechanical check |
|---|---|
| `Design Don't #2: Client calls Engine` | A Client type references an Engine type |
| `Design Don't #6: Client publishes an event` | A Client calls a publish API with a message that `IsEvent` accepts; posting a command to a Manager passes |
| `Design Don't #7: Engine publishes`, `#8: ResourceAccess publishes`, `#9: Resource publishes` | A call to a publish API from that layer |
| `Design Don't #10: subscribes below the Managers` | A call to a subscribe API from an Engine, ResourceAccess or Resource |
| `Design Don't #11: Engine calls Engine` | An Engine references another Engine |
| `Design Don't #12: ResourceAccess calls ResourceAccess` | A ResourceAccess references another ResourceAccess |
| `Closed architecture: Manager calls Manager synchronously (queue it)` | A Manager references another Manager type; a queued call goes through the bus and never references it |
| `Closed architecture: calls up a layer` | A reference to a higher layer, such as ResourceAccess to Manager or Manager to Client |
| `Closed architecture: skips a layer` | A reference that jumps over a layer, such as Client to ResourceAccess or Manager to Resource |
| `Naming: gerund prefix on a Manager (functional decomposition)`, `... on a ResourceAccess ...` | The word before the suffix ends in "ing" and is not in `NotGerunds` |
| `Structure: more than 3 Managers in a subsystem` | Concrete Managers per configured subsystem |

Allowed by the relaxed rules, and never reported: Manager to Engine, Manager to ResourceAccess, Engine to ResourceAccess, ResourceAccess to Resource, any layer to a Utility.
A type's own base types and interfaces are not dependencies.
Suffixes classify only the project's own assemblies, so a third-party `SceneManager` is not a Manager.

What no static test can check, and where it is covered instead:
- Don't #1 (a Client calls several Managers in one use case), #3 (queues to more than one Manager), #4 and #5 (queued calls to Engines or ResourceAccess) need use-case boundaries: `lowy:call-chain-validator`, `/lowy:arch-audit`, `/lowy:design-check`.
- Volatility, expendability, symmetry and the golden ratio need judgment: `lowy:lowy-reviewer`.
- Dependencies resolved at run time (string keys, reflection, service locators) are invisible; say so in the summary when the codebase uses them.

## Step 1: Read the Profile

Read `cc-docs/architecture.md` as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.
Collect what `ArchitectureMap` needs:

| `ArchitectureMap` field | From the profile's Mapping |
|---|---|
| `AssemblyPrefixes`, `ExcludedAssemblyFragments` | Which assemblies hold the project's code; tests and editor code stay out |
| `Suffixes` | Naming conventions per layer (defaults: `Manager`, `Engine`, `Access`) |
| `Namespaces`, `Types` | Layers the suffix alone does not reveal: Client namespaces, Utility namespaces, explicit exceptions |
| `ClientBaseTypes` | Default `UnityEngine.MonoBehaviour`; add others the Mapping names |
| `CompositionRoots` | The composition root: it may reference every layer to wire it, so its own references are not checked |
| `ResourceNamespaces` | Platform, network and storage APIs only ResourceAccess may touch, such as `UnityEngine.Networking` |
| `Publish`, `Subscribe` | The messaging API: type full name and method names |
| `IsEvent` | How a command differs from an event, such as a name suffix or a marker interface |
| `Subsystems`, `MaxManagersPerSubsystem` | Subsystems by assembly prefix |
| `NotGerunds` | Domain nouns ending in "ing", such as `Setting` or `Building` |

When the profile is missing, or its Mapping does not say where the code lives or which API publishes, derive candidates from the code.
- Assemblies: `Glob` `**/*.asmdef` outside `Library/` and `Packages/` caches.
- Messaging: `Grep` for `Publish`, `Raise`, `Subscribe`, `Send` declarations on bus-like types.
- Layers: types named `*Manager`, `*Engine`, `*Access`, and their namespaces.

Present the candidate Mapping lines to the user and ask before writing them into the profile.
Never write the profile, an Approved deviations entry or a Known debt entry without the user's consent.

## Step 2: Check Prerequisites

1. The project is a Unity project: `ProjectSettings/ProjectVersion.txt` exists. For a non-Unity .NET solution, see the last section.
2. `com.unity.test-framework` is in `Packages/manifest.json` or `Packages/packages-lock.json`.
3. `com.unity.nuget.mono-cecil` is in `Packages/packages-lock.json`; a transitive dependency is enough.
   If it is missing, ask the user before adding it to `Packages/manifest.json` with the version the Package Manager shows for their editor (1.11.6 works with Unity 6.3).
4. No other `Mono.Cecil.dll` exists under `Assets/`; two precompiled assemblies with the same name fail the compile.
   If one exists, ask the user whether to reference it instead and drop the package dependency.
5. The output folder is under `Assets/`, and no file there would be overwritten without asking.

## Step 3: Generate the Files

Copy these templates byte for byte into the output folder; read each one and write it unchanged:
- `ArchitectureModel.cs`: the map, violations and baseline types.
- `ArchitectureFitness.cs`: the analyzer.
- `ArchitectureFitnessTests.cs`: the NUnit tests.
- `Architecture.FitnessTests.asmdef`: Editor-only, references NUnit and Mono.Cecil as precompiled assemblies, compiles only with `UNITY_INCLUDE_TESTS`, and references no game assembly, because the analyzer reads the built DLLs instead of loading them.

Write `ArchitectureProfile.cs` from `ArchitectureProfile.cs.template`:
- Replace `{{DATE}}` with today's date and every `Acme` example with the values from Step 1.
- Keep the comments that name the profile section each value comes from.
- `ApprovedDeviations`: one `BaselineEntry` per profile entry that a mechanical rule covers, with profileRef `"Approved deviations: <rule relaxed>, <date>"`.
- `KnownDebt`: one entry per Known debt item that a mechanical rule covers, with profileRef `"Known debt: <item>"`.
- Pattern syntax is `Rule|From|To`, using the exact rule strings from the table above and type full names.
  A segment may be `*`, or end with `*` to match a prefix, as in `Design Don't #2*|Acme.UI.*|*`.
- Profile entries no mechanical rule covers stay out; list them under "Not covered by the tests" in the summary.

## Step 4: Run and Seed the Baseline

The analyzer reads `Library/ScriptAssemblies`, so the project must compile first.
Ask the user to run the tests, or run them when the editor does not have the project open:
- Editor: Window, General, Test Runner, EditMode, select `Architecture.FitnessTests`, Run Selected.
- Batch mode: `<Unity> -batchmode -projectPath . -runTests -testPlatform EditMode -assemblyNames Architecture.FitnessTests -testResults <path>/fitness.xml -logFile <path>/fitness.log`.
  Do not pass `-quit` with `-runTests`.
  Exit code 0 means all passed, 2 means a test failed, anything else means Unity did not run the tests: read the log.

Read the results, then report in the shape of `${CLAUDE_PLUGIN_ROOT}/references/review-findings.md` with `lens: lowy`:
- `TheMappingFindsTheServices` lists the services per layer. Check them against the profile with the user before trusting any violation; a wrong Mapping produces wrong findings.
- `NoViolationOutsideTheProfile` lists each new violation with its locations. Group them by rule.
- `ReportWhatCouldNotBeChecked` ends Inconclusive when messages were published through variables or base types could not be resolved.

On a codebase that already has violations, the first run fails.
For each group, offer the user three choices: fix it, record it as Known debt, or propose an Approved deviation with its justification.
Mirror every choice in both the profile and `ArchitectureProfile.cs`, after the user agrees.
If the profile cannot be edited (the session refuses the write), give the user the exact lines to paste, and say that the tests and the profile disagree until they do.
Known debt only shrinks: `FixedDebtLeavesTheBaseline` fails when a debt item is fixed, so the baseline is updated in the same change.

## Step 5: Record It

Propose this line for the profile's Mapping section, and add it when the user agrees:

> Fitness tests: `<output folder>` (generated by `/lowy:fitness-tests`). Regenerate `ArchitectureProfile.cs` when this profile changes.

Then summarize: files written, rules covered, baseline size, profile entries not covered by the tests, and how to run them in CI.

## Updating

- When the profile changes, regenerate only `ArchitectureProfile.cs`.
- When the plugin updates, copy `ArchitectureModel.cs`, `ArchitectureFitness.cs` and `ArchitectureFitnessTests.cs` again; they carry no project data.
- Never edit the copied analyzer in the project. A rule that needs changing is a change to the plugin, with a fixture case in `${CLAUDE_PLUGIN_ROOT}/tests/fitness`.

## Non-Unity .NET Solutions

`ArchitectureModel.cs` and `ArchitectureFitness.cs` have no Unity dependency.
Reference the `Mono.Cecil` NuGet package from a test project, build an `ArchitectureMap` the same way, and call `Analyzer.Analyze` with the built assembly paths.
Use the `Baseline` helpers for the same three checks, and `Assert.Warn` where the test framework has it.
