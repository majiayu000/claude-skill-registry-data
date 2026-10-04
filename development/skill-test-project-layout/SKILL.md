---
name: skill-test-project-layout
description: "AL App/Test project layout diagnosis for Business Central. Use when the main app compiles test sources, AL0297 appears on test object IDs, Library Assert or Library - Sales is missing, test/app.json is not recognized, or a multi-root workspace with app and test projects needs diagnosis."
---

# Skill: App/Test Project Layout Diagnosis

## Purpose

Diagnose and fix Business Central AL repositories where the main app and test app coexist in the same repository and may be compiled or resolved incorrectly.

## When to Load

This skill should be loaded when:
- The main app build reports errors from `test/src/`
- `AL0297` appears on test objects using the main app ID range
- `AL0185` appears for `Library Assert`, `Library - Sales`, `Library - Inventory`, or `Library - Random`
- A nested `test/app.json` is not recognized
- A `.code-workspace` with app/test roots needs review
- The repo layout mixes a root app and a nested test project

## Core Patterns

### Pattern 1: Cross-Project Contamination Signal

If the main app build reports errors from `test/src/` and the test object IDs are validated against the root app ID range, the compiler is discovering test sources from the main app tree.

Typical signal:

```text
test/src/BSSIdempotencyTests.Codeunit.al(1,10): error AL0297:
The application object identifier '50804' is not valid.
It must be within the allowed ranges '[50680..50779]'.
```

### Pattern 2: Dependency Audit for Test Libraries

When test code uses `Library Assert`, `Library - Sales`, `Library - Inventory`, or `Library - Random`, audit these dependencies in the test project:

- `Application Test Library`
- `Library Assert`
- `Tests-TestLibraries`
- `System Application Test Library`

### Pattern 3: Isolation Strategy

Preferred:
- Physically separate app and test projects as sibling folders.

Fallback when layout cannot change:
- Add a test-only preprocessor symbol in the test `app.json`.
- Wrap test source files so the root app build cannot see them.

### Pattern 4: Workspace Is Not a Compiler Boundary

Changing root order or `files.exclude` can improve editor behavior, but it does not change which files the main app compiler can discover from the physical project tree.

## Workflow

### Step 1: Inspect Project Boundaries

Read the root `app.json`, the test `app.json`, the `.code-workspace`, and list the repo root. Confirm whether `test/` is nested under the main app root.

### Step 2: Correlate Symptoms With Cause

- `AL0297` on `508xx` with the root app range usually means the main app is seeing test sources.
- `AL0185` on test libraries usually means missing dependencies, wrong manifest resolution, or both.

### Step 3: Choose the Fix

- If layout can change: move app and test into sibling folders.
- If layout cannot change: enforce compile isolation via preprocessor or an equivalent build barrier.
- Add missing Microsoft test dependencies in the test manifest.

### Step 4: Validate Both Builds

Build the root `app.json` and the test `app.json` separately.

Success criteria:
- The root build ignores test sources.
- The test build resolves its own test libraries.

## References

- https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-json-files
- https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-work-workspace-projects-references
- https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-multi-root-workspaces

## Constraints

- This skill diagnoses layout, manifest, dependency, and workspace issues. It does not replace `skill-testing` for writing or refactoring test logic.
- Do not use Explorer hiding as a substitute for compile isolation.
- Prefer root-cause fixes over suppressing diagnostics or moving files ad hoc.