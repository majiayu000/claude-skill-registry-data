---
name: s32ds-clean-and-rebuild
description: Clean all build artifacts and perform a full rebuild from scratch. Triggers project clean, waits for the clean job to finish, then starts an incremental build and waits for completion. Finally verifies that no errors remain. Use when incremental builds produce stale-object errors or inconsistent state.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, project-build, clean-rebuild]'
---
# Clean and Rebuild Project

## Goal
Perform a clean build to resolve stale artifacts or inconsistent build state.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Steps

1. **Get project info and location**:
   - Use `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})` -> note the `location` field

2. **MANDATORY: Recursively search for .mex files**:
   - Search the entire project directory tree for files with `.mex` extension
   - `.mex` files can be anywhere (root, subfolders, nested deep)
   - **If ANY .mex file exists -> skip steps 3-4 and use step 2b instead**

   **2b. Clean then Update Code and Build (for .mex projects)**:
   - Use `execute_action(action_name="cleanProject", params={"projectName": "<name>"})`
   - Wait for clean to finish: `execute_action(action_name="waitForJob", params={"jobName": "Clean", "timeoutMs": 30000})`
   - **Select the project first**: `execute_action(action_name="selectProject", params={"projectName": "<name>"})`
   - Then: `execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})`
   - Wait for build to finish: `execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})`
   - **Handle edge case - command only generated code without building**:
     - If `waitForJob` returns `matched=0` (no "Building" job was found), the
       command only performed code generation and did NOT trigger a build.
     - In this case, explicitly start the build:
       `execute_action(action_name="buildProject", params={"projectName": "<name>"})`
     - Then wait for it to complete:
       `execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})`
   -  You MUST select the project first, otherwise the command silently does nothing!
   - This regenerates code AND rebuilds - skip to step 5.

3. **Clean the project** (only if NO .mex files):
   - Use `execute_action(action_name="cleanProject", params={"projectName": "<name>"})`
   - Wait for clean to finish: `execute_action(action_name="waitForJob", params={"jobName": "Clean", "timeoutMs": 30000})`

4. **Rebuild** (only if NO .mex files):
   - Use `execute_action(action_name="buildProject", params={"projectName": "<name>"})`
   - Wait for build to finish: `execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})`

5. **Verify build health**:
   - Use `execute_action(action_name="getProblems", params={"projectName": "<name>", "severity": "error"})`
   - Only check problems AFTER `waitForJob` confirms the build has completed
   - If zero errors -> build succeeded
   - If errors persist after clean build -> they are real code issues, not stale artifacts

## Guardrails

**Scope**
- Act only on the project the user named. Never clean or rebuild an unrelated project as a side effect.

**Destructive actions**
- Clean deletes build artifacts. Confirm the target project first, and never clean a project the user did not explicitly ask about.

**Resource limits**
- Wait for the clean job to finish before starting the build; do not spawn parallel or overlapping build jobs on the same project.

**Refuse-and-escalate**
- If the named project is not found or is closed, stop and ask the user to confirm/open it rather than acting on a guessed project.

## When to Use
- After switching build configurations (Debug ↔ Release)

- After modifying include paths or compiler settings
- When incremental build produces inconsistent results
- After pulling changes from version control
