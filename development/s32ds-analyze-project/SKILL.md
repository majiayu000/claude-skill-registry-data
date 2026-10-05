---
name: s32ds-analyze-project
description: Comprehensive read-only analysis of an S32DS project. Lists workspace projects, retrieves project info (build configs and MCU/core/target), finds the installed SDKs that match the target, reports build problems, and lists debug/launch configurations to map structure, toolchain, and debug capability. Use this whenever the user asks "what is this project?", needs to understand an unfamiliar S32DS project, wants to know the target MCU/SDK/toolchain, is diagnosing why a project behaves unexpectedly, or is about to build/debug/regenerate code on a project they have not inspected yet. Run this FIRST before any build, debug, or code-generation task on an unfamiliar project.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, project-analysis, diagnostics]'
---
# Analyze Project

## Goal
Build an accurate, read-only picture of an S32DS project: its target hardware, toolchain, attached SDKs, build health, dependencies, and debug capability. This gives you the context needed to make safe, correct changes later.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - only needed if you trigger an async job (not required for pure analysis)

## Before You Start
Call `search_actions(query="...")` first. The catalog is the source of truth for action names and their input schemas - use it instead of guessing (a parameterless `search_actions()` browses everything). Action names are case-sensitive

## Prerequisites
- At least one project must exist in the workspace.
- The target project must be **open**. Closed projects cannot be queried - you can see them in `listProjects` but cannot read their info or problems.

## Guardrails

**Scope**
- This skill is read-only. Inspect projects with list/getProjectInfo/SDK queries only; never build, modify, rename, or delete the analyzed project. If the user actually wants a change, hand off to the appropriate build/config skill.

**Refuse-and-escalate**
- If the named project is not in the workspace or the info calls fail, stop and ask the user to confirm the project rather than inferring its structure from a filename.

## When to Use
- A user is new to a project and asks "what is this?" or "what does this target?"

- You need the MCU, core, and toolchain before making changes.
- A project behaves unexpectedly and you want a baseline before debugging.
- You want to know dependencies/referenced projects (they may need building first).
- It is the first step before any build, debug, or code-generation task on an unfamiliar project.

## Steps

### 1. List workspace projects
- **Call**: `execute_action(action_name="listProjects")`
- **Why**: Discover the exact project name, open/closed state, and disk location. Every later step needs the precise name.
- **Result**: JSON list with `name`, `open`, `location`.
- If the target is **closed**, stop and tell the user - it cannot be analyzed until reopened.

### 2. Get project details
- **Call**: `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})`
- **Why**: This is the core of the analysis - it tells you what the project actually is.
- **Result**: JSON with project type info, build configs, MCU info, references.
- Extract and report, in plain language the user can act on:
  - **MCU / Target**: family, device, core, revision - this drives everything downstream.
  - **Build configs**: which configs exist (e.g. Debug/Release) and which one is active.
  - **Project type**: say what kind of project it is (e.g. "a C application built with the managed S32DS build system") rather than dumping raw Eclipse nature/builder IDs.
  - **References**: any projects this one depends on - these often need building first.

### 3. Find the SDKs for the target
- **Call**: `execute_action(action_name="listAllSdks")`
- **Why**: The SDK set determines which drivers/APIs (RTD, AMMCLIB, platform packages) are available to you when assisting with code.
- **How**: `listAllSdks` returns the global catalog of installed SDKs. Filter it by the MCU `part` you learned in step 2 to get the ones relevant to this target. For example, for an `S32K344` project the relevant entries are names containing `S32K344`, such as `PlatformSDK_S32K3_S32K344_M7` (the RTD platform package) and `FreeMASTER_S32K344`.
- **Result**: report the matching SDKs with name and version. Make clear these are the *installed* SDKs that match the target, drawn from the global catalog.
- **Note**: there is no per-project SDK attachment query available - the old `getProjectSdks` action has been removed from S32DS, so do not call it. Always use `listAllSdks` filtered by MCU part.
- If no SDK matches the target's part, note it - a missing platform SDK usually explains build errors later.


### 4. Check build health
- **Call**: `execute_action(action_name="getProblems", params={"projectName": "<name>"})`
- **Why**: Tells you whether the project is in a buildable state before you touch it.
- Note: `projectName` is optional. Omit it to get workspace-wide problems; pass it to scope to one project. For single-project analysis, scope it.
- **Result**: markers with severity, message, file, line.
- Summarize counts (errors / warnings / infos). If errors exist, list the top few with file and line - those are your first leads.

### 5. List debug / launch configurations
- **Call**: `execute_action(action_name="listDebugLaunches", params={"nameFilter": "<name>"})`
- **Why**: Shows how the application can be launched/debugged on hardware.
- **Result**: launch configs with name, type, associated project.
- Report each config's name and debugger type (e.g. GDB / PEMicro / S32 Debug Probe).

### 6. (Optional) Open a source file for inspection
- **Call**: `execute_action(action_name="openFile", params={"filePath": "<absolute-or-workspace-path>"})`
- **Why**: After spotting an interesting file (e.g. from a build problem), open it in the editor so the user can see it.
- Use the `location` from step 1 to build an absolute path when needed.

### 7. (Optional) Look up reference docs for the target MCU
- This skill does **not** search documentation itself. If the user needs hardware/peripheral context beyond the project config, hand off to the `s32ds-find-documentation` skill, scoping the query with the MCU/core you learned in step 2.

### 8. Present the summary
Give the user a single structured overview tying together everything above. Keep it scannable.

## Example Summary Output

Use a clean, ASCII, structured layout like this (grounded in a real S32DS 3.6.5 project):

```
Project Analysis: FRDM_A_S32K344_UART

Target:        S32K344  (ARM Cortex-M7)
Family:        S32K3
Device core:   S32K344_M7
Project type:  C application, managed S32DS build

SDKs (installed packages matching this target):
  - PlatformSDK_S32K3_S32K344_M7 v7.0.1   (RTD platform package)
  - FreeMASTER_S32K344 v1.5.0

Build status: 0 errors, 0 warnings, 0 infos  (clean)

Debug configs (2):
  - FRDM_A_S32K344_UART Debug_FLASH       (S32 Debugger)
  - FRDM_A_S32K344_UART_Debug_FLASH_PNE   (GDB PEMicro)

Dependencies: none (standalone project)
```

## Related Skills
- `s32ds-build-and-debug` - after analysis, to build and launch a debug session
- `s32ds-fix-build-errors` - if build health shows errors
- `s32ds-check-sdk-compatibility` - if SDK versions look problematic
- `s32ds-find-documentation` - to look up MCU/peripheral reference material
- `s32ds-workspace-health-check` - for full multi-project workspace analysis

## Notes
- This skill is **read-only** - it never modifies the project. That is what makes it safe to run first on anything.
- MCU info comes from the project config; the matching SDKs reveal which APIs are available for coding assistance.
- Referenced projects may need to be built before the main project will compile.
- For a workspace-wide view across many projects, use `s32ds-workspace-health-check` instead of running this skill per project.

## Anti-Patterns (Do NOT)
- Do NOT skip analysis and jump straight to building/debugging an unfamiliar project - you will miss missing SDKs and dependency ordering.
- Do NOT call the removed `getProjectSdks` action - use `listAllSdks` filtered by MCU part instead.
- Do NOT assume SDK availability - confirm it from `listAllSdks`, since it changes which APIs you can reference.
- Do NOT ignore referenced projects - they may need building first.
- Do NOT try to analyze a closed project - reopen it first or tell the user it is closed.
- Do NOT invent a documentation-search action here - delegate to `s32ds-find-documentation`.
