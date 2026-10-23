---
name: unreal-automation-system
description: "Author and run Unreal Engine's Automation Test Framework - Epic's C++ test framework for UE 4.x / 5.x, documented at dev.epicgames.com/documentation/en-us/unreal-engine. Covers the five test categories Epic defines (Unit / Feature / Smoke / Content Stress / Screenshot Comparison), the IMPLEMENT_SIMPLE_AUTOMATION_TEST and IMPLEMENT_COMPLEX_AUTOMATION_TEST macros, the BDD-style Automation Spec API (DEFINE_SPEC / BEGIN_DEFINE_SPEC / Describe / It / BeforeEach / LatentIt / xIt), latent commands (ADD_LATENT_AUTOMATION_COMMAND), the Automation Driver for UI input simulation (IAutomationDriverModule::Get().CreateDriver(), By::Id / By::Path locators), running via Session Frontend (Window > Test Automation) and command line (-ExecCmds=\"Automation RunTests …\"), and CI integration. Use when the unit under test is C++ Unreal code that needs the UE runtime, editor, or UMG UI surface."
metadata:
  keywords: "unreal, ue4, ue5, automation, automation-spec, automation-driver, session-frontend, gauntlet, cpp, game-engine"
  version: "1.4.16"
---

# unreal-automation-system

## Overview

This skill wraps the **C++ Automation Test Framework** (UE 4.x /
5.x) plus the two most commonly composed sub-systems. Per Epic's
[Automation Test Framework documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine),
the framework spans five test categories (Unit, Feature, Smoke,
Content Stress, Screenshot Comparison) and supports multiple
authoring styles (traditional, BDD Spec, UI Driver, Functional,
Python / Blueprint).

- **Automation Spec** - BDD-style `Describe` / `It` /
  `BeforeEach` per
  [Automation Spec documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-spec-in-unreal-engine).
- **Automation Driver** - UI input simulation per
  [Automation Driver documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine).

The full authoring code (macros, Spec, Driver) lives in
[references/authoring-macros-and-apis.md](references/authoring-macros-and-apis.md);
running, report parsing, and CI wiring live in
[references/running-and-reporting.md](references/running-and-reporting.md).
This file is the decision surface.

Composes with:

- `platform-cert-overview-reference`
  for the canonical six test categories Unreal's five categories map
  to, and for cert-gated requirements automation tests should cover.
- `multiplayer-state-machine-coverage`
  for replication / dedicated-server state coverage authored as
  automation tests.

## When to use

- Unit under test is **C++ code in an Unreal Engine project**
  (UE 4.x or UE 5.x) that needs the engine runtime, editor APIs,
  or UMG UI surface.
- You want CI-runnable tests via Unreal's command-line
  Automation entry point.
- You need BDD-style readable specs (Automation Spec) or scripted
  UI input simulation (Automation Driver) on top of plain
  assertion tests.

For Python / Blueprint editor tests outside C++, see
[Editor Automation in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine).
For end-to-end pipeline / build-farm orchestration, use
[Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine)
on top of the framework this skill covers.

## How to use

1. **Pick the category** from the table below (Unit / Feature /
   Smoke / Content Stress / Screenshot Comparison) and the matching
   `EAutomationTestFlags` filter + application-context mask.
2. **Pick the authoring style** - plain `RunTest` macro, data-driven
   complex macro, BDD Spec, or Automation Driver for UI - and lift
   the pattern from
   [references/authoring-macros-and-apis.md](references/authoring-macros-and-apis.md).
3. **Name the test path** as dot-separated segments
   (`MyGame.Health.Damage_…`); the tree keys the Session Frontend.
4. **Run in-editor** via Session Frontend to iterate, then
   **run headless** via `UnrealEditor-Cmd.exe … -ExecCmds="Automation
   RunTests …"` for CI.
5. **Parse the `-ReportOutputPath` JSON** - treat any
   `"state": "Fail"` as a failed build; full schema in
   [references/running-and-reporting.md](references/running-and-reporting.md).
6. **Split the CI matrix** - `SmokeFilter` on PRs (sub-second),
   `ProductFilter | StressFilter` plus screenshot comparison nightly.

## Test categories and flags

Per the
[Automation Test Framework page](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine),
Epic's five categories are:

| Category | Purpose |
|---|---|
| **Unit** | "API level verification tests." |
| **Feature** | "System-level tests that verify such things as PIE, in-game stats, and changing resolution." |
| **Smoke** | Tests that "complete within 1 second" and run automatically. |
| **Content Stress** | "More thorough testing of a particular system to avoid crashes." |
| **Screenshot Comparison** | For comparing renders "between versions or builds". |

Each test declares flags from `EAutomationTestFlags` that mix:

- **Filter** - `SmokeFilter`, `EngineFilter`, `ProductFilter`,
  `PerfFilter`, `StressFilter`, `NegativeFilter`.
- **Application context** - `EditorContext`, `ClientContext`,
  `ServerContext`, `CommandletContext`, plus the convenience mask
  `ApplicationContextMask`.

Typical combo for a product-level test runnable in editor / client
/ server contexts:
`EAutomationTestFlags::ProductFilter | EAutomationTestFlags::ApplicationContextMask`.

## Authoring styles

Pick the style that matches the unit under test, then lift the full
pattern from
[references/authoring-macros-and-apis.md](references/authoring-macros-and-apis.md):

| Style | Macro / API | Use when |
|---|---|---|
| Simple test | `IMPLEMENT_SIMPLE_AUTOMATION_TEST` + `RunTest` | One assertion body over plain C++ |
| Data-driven | `IMPLEMENT_COMPLEX_AUTOMATION_TEST` + `GetTests` | One sub-test per enumerated row (assets, configs) |
| Multi-frame | `ADD_LATENT_AUTOMATION_COMMAND` | Test must yield to the tick loop across frames |
| BDD Spec | `DEFINE_SPEC` / `BEGIN_DEFINE_SPEC` + `Describe` / `It` / `LatentIt` | Readable specs; `.spec.cpp` files; async via `FDoneDelegate` |
| UI Driver | `IAutomationDriverModule::Get().CreateDriver()` + `By::Id` | Simulate cursor / click / type on UMG; runs off the GameThread |

## Running

Iterate in-editor via **Window → Test Automation** (Session
Frontend), then run headless for CI:

```bash
UnrealEditor-Cmd.exe MyGame.uproject \
    -ExecCmds="Automation RunTests MyGame.Inventory; Quit" \
    -unattended -nopause -testexit="Automation Test Queue Empty" \
    -ReportOutputPath="artifacts/automation" \
    -log
```

Command variants, the `-ReportOutputPath` JSON schema, Gauntlet, and
a full GitHub Actions job are in
[references/running-and-reporting.md](references/running-and-reporting.md).

## Worked example

Goal: cover an inventory system's stacking rule as a CI-gating BDD
spec, plus a menu-close UI check.

1. **Category + flags.** Stacking logic is pure C++ product logic,
   so `ProductFilter | ApplicationContextMask`; it runs in well
   under a second, so a second `SmokeFilter` copy joins the PR job.
2. **Authoring.** Write `FInventorySpec` with `DEFINE_SPEC` and a
   `Describe("AddItem")` block holding two `It("should …")` cases -
   one asserting count increases by the stack amount, one asserting
   an over-cap add is rejected (pattern in
   [references/authoring-macros-and-apis.md](references/authoring-macros-and-apis.md)).
   Save it as `InventorySpec.spec.cpp`.
3. **UI check.** Add `FMenuDriverSpec` with the Driver enabled in
   `BeforeEach` on `TaskGraphMainThread`, the `It` running on
   `EAsyncExecution::ThreadPool`, `By::Id("SubmitButton")` clicked,
   and `Disable()` in `AfterEach`.
4. **Run headless.**
   `UnrealEditor-Cmd.exe MyGame.uproject -ExecCmds="Automation
   RunTests MyGame.Inventory; Quit" -unattended -nopause
   -ReportOutputPath="artifacts/automation" -log`.
5. **Gate.** CI reads `artifacts/automation/index.json`; the
   over-cap `It` shows `"state": "Fail"` when the rule regresses, so
   the job fails the build. Nightly re-runs the same specs under
   `ProductFilter | StressFilter`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| All tests as `SmokeFilter` | Smoke tests "complete within 1 second" per [framework docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine) - long tests break the smoke contract | Use `ProductFilter` for tests > 1 s |
| Running Automation Driver on GameThread | API "cannot run on the GameThread" per [Driver docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine) | Use `EAsyncExecution::ThreadPool` on the driver-using `It` |
| Spec without `It` descriptions starting with "should" | Runner output reads poorly | Per [Spec docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-spec-in-unreal-engine), start descriptions with "should" |
| Trusting `By::Path` locators | "Brittle" per [Driver docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine) | Prefer `By::Id` with tagged metadata |
| `Sleep`-style waits in latent commands | Flaky under CI load | Use `FDoneDelegate` (LatentIt) or custom `IAutomationLatentCommand::Update()` polling |
| Spec test file without `.spec.cpp` extension | Build system may not pick it up | Per [Spec docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-spec-in-unreal-engine), use `.spec.cpp` suffix and no "Test" in filename |
| Cloning non-thread-safe shared pointers in async `It` | Crash under threadpool | Per [Driver docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine), cache them on the test class |
| No `BeforeEach` / `AfterEach` cleanup of `IAutomationDriverModule` | Driver state leaks between specs | Pair `Enable()` / `Disable()` calls in `BeforeEach` / `AfterEach` per [Driver docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine) |

## Limitations

- **C++ build required.** Tests live in C++ modules; pure-content
  Blueprint projects need a code module added to use this
  framework. (Pure Blueprint projects can use Blueprint Functional
  Tests in-level - see Epic's docs on Functional Testing.)
- **No common exit code definition** comparable to Unity's caveat - 
  parse the `-ReportOutputPath` JSON or scrape the log for
  `LogAutomationController` Fail lines.
- **Spec parameterised tests** are loop-generated per
  [Spec docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-spec-in-unreal-engine);
  there is no `[TestCase]` analogue from NUnit. The framework is
  NUnit-inspired but **not** NUnit-derived (unlike Unity's UTF).
- **Screenshot comparison** baseline storage + tolerance
  configuration is engine-version-specific - consult per-version
  Epic docs.
- **Editor-context tests cannot run in dedicated-server only
  builds** - declare `EditorContext` on those tests; client / server
  tests need their own flag set.
- **Documentation source.** The
  [dev.epicgames.com docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine)
  are the public mirror; deeper detail (full macro implementations,
  precise JSON report schema) lives in the engine source under
  `Engine/Source/Runtime/AutomationController/` and
  `Engine/Source/Developer/AutomationMessages/` - partners with
  engine source access should consult those for authoritative
  details.

## References

- Automation Test Framework -
  [dev.epicgames.com](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine).
- Automation Spec (BDD) -
  [dev.epicgames.com](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-spec-in-unreal-engine).
- Automation Driver (UI input) -
  [dev.epicgames.com](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-driver-in-unreal-engine).
- Full authoring code (macros, Spec, Driver):
  [references/authoring-macros-and-apis.md](references/authoring-macros-and-apis.md).
- Running, report parsing, and CI wiring:
  [references/running-and-reporting.md](references/running-and-reporting.md).
- Category mapping + cert-gated requirements:
  `platform-cert-overview-reference`.
- Replication / dedicated-server coverage:
  `multiplayer-state-machine-coverage`.
