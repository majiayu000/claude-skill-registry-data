---
name: s32ds-safe-code-regen
description: Safely regenerate driver code from .mex configuration files and build the project in one atomic operation. This is the ONLY correct way to build projects that use S32 Configuration Tools. Selects the project, triggers 'Update Code and Build' (which regenerates all driver code from .mex files then compiles), waits for both code generation and build jobs, and verifies results. Prevents stale/missing generated code errors that occur when using plain build on .mex projects.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, code-generation, mex, build, safe-regen, atomic]'
---
# Safe Code Regeneration (Update Code and Build)

## Goal
Safely regenerate driver code from `.mex` configuration files and build the project in one atomic operation. This is the ONLY correct way to build projects that use S32 Configuration Tools.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- Project must exist in the workspace (`execute_action(action_name="listProjects")`)
- Project must contain at least one `.mex` file (search recursively)
- No modal dialogs open in S32DS (close any open wizards/preferences first)

## Guardrails

**Scope**
- Operate only on the `.mex`-based project the user named. Do not regenerate code for other projects.

**Destructive actions**
- Code regeneration overwrites files in the generated output folders. Warn the user that manual edits inside generated folders will be lost, and confirm before regenerating.

**Resource limits**
- Wait for both the code-generation and build jobs to finish before reporting results; do not start overlapping regen/build runs.

**Refuse-and-escalate**
- If the project contains no `.mex` file, stop and use the plain build path (`s32ds-clean-and-rebuild`/`s32ds-build-and-debug`) instead of forcing regeneration.

## When to Use
- Before ANY build of a project that contains `.mex` files

- After modifying `.mex` configuration in S32 Configuration Tools
- After importing a project with `.mex` files for the first time
- When build errors suggest stale or missing generated code
- When `s32ds-fix-build-errors` skill points you here

## Decision Tree

```
Is this a project with .mex files?
├─ YES -> Use this skill (Update Code and Build)
│   ├─ Need interactive review? -> openProjectUpdateDialogCmd
│   └─ Automated/headless? -> updateCodeAndBuildProject
├─ NO -> Use execute_action(action_name="buildProject") directly (no code gen needed)
└─ UNSURE -> Search project recursively for *.mex files first
```

## Steps

1. **Identify the project and confirm .mex presence**:
   ```
   execute_action(action_name="listProjects")
   execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})
   ```
   - Note the `location` field from project info
   - Recursively search the project directory for `.mex` files
   - If NO `.mex` files found -> use `execute_action(action_name="buildProject", params={"projectName": "<name>"})` instead (this skill does not apply)

2. **Select the project (MANDATORY)**:
   ```
   execute_action(action_name="selectProject", params={"projectName": "<name>"})
   ```
   -  This step is **non-negotiable**. The "Update Code and Build" command operates on the currently selected project in the IDE. Without this step, the command silently does nothing.

3. **Trigger Update Code and Build**:
   ```
   execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
   ```
   - This is an **async** command - it returns immediately after scheduling
   - The operation regenerates code from `.mex` files, then builds

4. **Wait for code generation to complete**:
   ```
   execute_action(action_name="waitForJob", params={"jobName": "S32 Configuration", "timeoutMs": 120000})
   ```
   - Alternative patterns to match: `"Generating"`, `"Updating"`
   - Code generation can take 30-90 seconds for large projects
   - If `matched=0`, try: `execute_action(action_name="waitForJob", params={"jobName": "Update", "timeoutMs": 120000})`

5. **Wait for the build to complete**:
   ```
   execute_action(action_name="waitForJob", params={"jobName": "Building", "timeoutMs": 120000})
   ```
   - **IMPORTANT**: If this returns `matched=0` (no building job found), the command may have only performed code generation without triggering a build. In that case, explicitly start the build:
     ```
     execute_action(action_name="buildProject", params={"projectName": "<name>"})
     execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})
     ```

6. **Verify results**:
   ```
   execute_action(action_name="getProblems", params={"projectName": "<name>", "severity": "error"})
   ```
   - Zero errors = success
   - If errors exist -> see Error Catalog below, or follow `s32ds-fix-build-errors` skill

7. **Report outcome to user**:
   - Summarize: code regeneration status + build result + error count (if any)

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Command silently does nothing | Project not selected | Call `execute_action(action_name="selectProject", ...)` first (Step 2) |
| `matched=0` for both gen and build jobs | Project has no .mex files, or command failed to schedule | Verify .mex presence; check `execute_action(action_name="getRunningJobs")` |
| Build errors in `generate/` or `board/` folders | Stale generated code from previous config | Re-run this entire skill from Step 2 |
| "undefined reference" to driver symbols | Code gen succeeded but build used stale objects | Run `execute_action(action_name="cleanProject", params={"projectName": "<name>"})` -> then re-run this skill |
| Timeout on code generation (>120s) | Very large .mex config or slow machine | Increase `timeoutMs` to 180000 or 240000 |
| Errors only in user code, not generated code | User code incompatible with new generated API | Check generated headers for API changes |

## Common Patterns

### Pattern A: Fresh import + first build
```
execute_action(action_name="listProjects")
execute_action(action_name="getProjectInfo", params={"projectName": "MyProject"})
# -> search location for .mex files -> found!
execute_action(action_name="selectProject", params={"projectName": "MyProject"})
execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})
execute_action(action_name="getProblems", params={"projectName": "MyProject", "severity": "error"})
```

### Pattern B: Interactive review before regeneration
```
execute_action(action_name="selectProject", params={"projectName": "MyProject"})
execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.openProjectUpdateDialogCmd"})
# -> Dialog opens for user to review changes before applying
```

### Pattern C: Clean + regenerate (after persistent errors)
```
execute_action(action_name="cleanProject", params={"projectName": "MyProject"})
execute_action(action_name="waitForJob", params={"jobName": "Clean", "timeoutMs": 30000})
execute_action(action_name="selectProject", params={"projectName": "MyProject"})
execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})
execute_action(action_name="getProblems", params={"projectName": "MyProject", "severity": "error"})
```

## Related Skills
- `s32ds-build-and-debug` - references this skill for .mex projects; covers full build+debug flow
- `s32ds-fix-build-errors` - next step if errors persist after regeneration
- `s32ds-clean-and-rebuild` - use Pattern C above when stale objects cause issues
- `s32ds-analyze-project` - use to understand project structure before regeneration
- `update_project_code` - related but covers the interactive dialog approach

## Notes
- The command ID `com.nxp.swtools.framework.updateCodeAndBuildProject` is the ONLY safe way to build .mex projects
- Generated code lives in folders like `generate/`, `board/`, or SDK-specific paths - NEVER edit these files manually
- `.mex` files can appear anywhere in the project tree (root, subfolders, config directories) - always search recursively
- If you modify a `.mex` file outside S32 Configuration Tools, you MUST run this skill before building
- This operation is idempotent - running it multiple times is safe (just slower)

## Anti-Patterns
-  **Using `execute_action(action_name="buildProject")` alone on a .mex project** - will build with stale/missing generated code
-  **Forgetting `execute_action(action_name="selectProject")` before the command** - command does nothing silently
-  **Editing files in `generate/` or `board/` folders manually** - your changes will be overwritten on next code gen
-  **Checking `execute_action(action_name="getProblems")` immediately after `execute_action(action_name="executeCommand")`** - build hasn't finished yet; errors reflect previous state
-  **Assuming one timeout fits all** - large projects with many peripherals can take 2-3 minutes for code gen alone
