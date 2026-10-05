---
name: s32ds-build-and-debug
description: Full build-and-debug workflow for S32DS projects. Checks whether the project contains .mex files (requiring code regeneration), selects the project, triggers either 'Update Code and Build' or a plain incremental build, waits for jobs to finish, verifies zero build errors, then launches a debug session via S32 Debug Probe. Covers the complete path from source code to halted-at-main on target hardware.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, build, debug, code-generation]'
---
# Build and Debug a Project

## Goal
Build an S32DS project and launch a debug session.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Guardrails

**Scope**
- Build and debug only the project the user named. Do not touch unrelated projects or launch configs.

**Resource limits**
- Verify zero build errors and wait for build/codegen jobs to finish before starting the debug session; do not launch on a failed or in-progress build.

**Refuse-and-escalate**
- If the build fails, stop and route the user to `s32ds-fix-build-errors` instead of attempting to debug broken output.

## Steps

1. **List projects** to find the target project:

   - Use `execute_action(action_name="listProjects")` to see all workspace projects

2. **MANDATORY: Search for .mex files in the project**:
   - Get the project location from `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})` -> look at the `location` field
   - **RECURSIVELY search** the entire project directory for `.mex` files (e.g., using filesystem search or listing files)
   - `.mex` files can be anywhere in the project tree (root, subfolders, etc.)
   - **If ANY .mex file is found**: you MUST do the following:
     1. First, **select the project** to activate its context:
        `execute_action(action_name="selectProject", params={"projectName": "<name>"})`
     2. Then run "Update Code and Build":
        `execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})`
     3. Wait for the build job to appear and complete:
        `execute_action(action_name="waitForJob", params={"jobName": "Update", "timeoutMs": 120000})`
     4. **Handle edge case - command only generated code without building**:
        - If `waitForJob` returns `matched=0` (no "Building" job was found), the command only performed code generation and did NOT trigger a build.
        - In this case, explicitly start the build:
          `execute_action(action_name="buildProject", params={"projectName": "<name>"})`
        - Then wait for it to complete:
          `execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})`
     5. Once the build completes - skip to step 4 (check errors).
   -  The executeCommand REQUIRES an active project context! If you don't select the project first, the command will silently do nothing.
   - Alternatively, to open the Update Code dialog for user review:
     `execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.openProjectUpdateDialogCmd"})`
   - **If NO .mex files exist**: proceed to step 3 for a normal build.

3. **Build the project** (only if step 2 did not already build):
   - Use `execute_action(action_name="buildProject", params={"projectName": "<name>"})`
   - **Wait for the build to finish** using:
     `execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})`
   - This blocks until the build job completes (or times out after 120s)

4. **Check for errors**:
   - Use `execute_action(action_name="getProblems", params={"projectName": "<name>", "severity": "error"})`
   - If errors exist, report them to the user and stop

5. **Find launch configuration**:
   - Use `execute_action(action_name="listDebugLaunches", params={"nameFilter": "<name>"})`
   - Pick the appropriate debug configuration

6. **Start debug**:
   - **Secured/locked target?** If the device is secured (secure debug / HSE) - or startDebug fails with "Target is secured" / Error 102 / Error 601 - do NOT retry blindly. Enable secure debugging in the launch config and hand off to the `s32sdaf-secure-debug-session` skill, which drives the SDAF password / challenge-response unlock. Unsecured devices proceed normally.
   - Use `execute_action(action_name="startDebug", params={"name": "<configName>", "build": false})`
   - build=false because we already built in step 3

## Notes
- Build is asynchronous - always use `execute_action(action_name="waitForJob", params={"jobName": "Build"})` after triggering a build. The jobName is matched as a substring and is case-insensitive by default, so "Building" will match "Building workspace" or similar variants.
- For "Update Code and Build", wait with: `execute_action(action_name="waitForJob", params={"jobName": "Update", "timeoutMs": 120000})`
-  "Update Code and Build" may sometimes ONLY regenerate code without starting a build. If `waitForJob` returns `matched=0`, explicitly call `execute_action(action_name="buildProject", ...)` and wait again.
- Debug launch is also async - use `execute_action(action_name="waitForJob", params={"jobName": "Launching"})` before sending GDB commands
- Use `execute_action(action_name="getRunningJobs")` to inspect what jobs are currently active if uncertain

##  CRITICAL: Projects with .mex Configuration Files
Projects containing `.mex` files (anywhere in the project tree - search recursively!) have auto-generated driver code from S32 Configuration Tools. **You MUST ALWAYS run "Update Code and Build" before building** these projects, otherwise the build will fail or use stale generated sources.

**The ONLY safe way to build a project with .mex files is:**
```
execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
```
This regenerates code and builds atomically in one step.

**NEVER use `execute_action(action_name="buildProject", ...)` alone on a project that has .mex files.**
