---
name: s32ds-import-ach-project
description: Import a project from NXP's Application Code Hub (ACH) into the S32DS workspace. Covers browsing available ACH projects, filtering by keyword, cloning the repository, and setting up the project for building. This is the primary flow for getting started with NXP reference applications and demos.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, ach, application-code-hub, import, git, clone, project-setup]'
---

# Import a Project from Application Code Hub (ACH)

## Overview

NXP's **Application Code Hub (ACH)** is a cloud-based repository of reference applications, demos, and production-ready code examples hosted as Git repositories. Unlike the bundled SDK examples (which ship with S32DS), ACH projects are maintained independently and often represent more complex, real-world use cases such as motor control, communication stacks, sensor fusion, and complete application demos.

This skill covers the **end-to-end workflow** for discovering and importing ACH projects into your S32DS workspace.

## Tools Used

- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes (used after import)
- The `getRunningJobs` action (via `execute_action`) - returns all currently running background jobs; use this to confirm the IDE is idle before concluding build success or triggering a fallback
- Shell commands (`execute_command`) - used to check for `.mex` files and build output on disk

##  Before You Start

Call `search_actions(query="ach")` first to verify that `listAchProjects` and `importAchProject` actions are available in your S32DS version (a parameterless `search_actions()` browses everything). Use the returned catalog to confirm exact parameter names and input schemas.

## Prerequisites

- S32DS IDE is running and responsive
- Internet connectivity is available (ACH projects are cloned from remote Git repositories)
- Git is installed and accessible by the IDE (required for cloning)
- Sufficient disk space for the cloned repository
- (Optional) Know the target MCU family/device to narrow the search

## Guardrails

**Scope**
- Clone ACH repositories into the S32DS workspace (or an explicit `location`) only. Use a `repoUrl` obtained from `listAchProjects` - never guess or hand-craft repository URLs.

**Destructive actions**
- Do not set `overwrite: true` without explicit user confirmation - it clobbers an existing project and any local modifications. Default to a distinct `newName` when a name collision is possible.

**Resource limits**
- ACH imports involve network I/O and can take 30-120 seconds. Wait for completion before starting another.
- Builds with code generation can take 1-2 minutes. Use `getRunningJobs` to confirm the IDE is idle, then `getProblems` to verify build success.

**Refuse-and-escalate**
- If the repo URL is invalid/unreachable or a name collision occurs, stop and ask the user how to proceed (rename, choose another, or confirm overwrite) - see the Error Catalog.

## When to Use

- User asks to import a project from ACH or Application Code Hub
- User wants to find reference applications or demos from NXP's cloud repository
- User is looking for production-quality example code beyond the bundled SDK examples
- User has a specific ACH project URL they want to clone into S32DS
- User asks "what ACH projects are available for [MCU]?"
- User wants to try a motor control, communication, or sensor demo application

## Workflow Overview

```
1. DISCOVER - Browse/search ACH projects
   execute_action(action_name="listAchProjects", params={...})

2. SELECT - Help user choose from results
   Present options with descriptions

3. IMPORT - Clone and set up the project
   execute_action(action_name="importAchProject", params={...})
   Save the "location" field from the response - needed for filesystem checks.

4. VERIFY - Confirm project appears in workspace
   execute_action(action_name="listProjects")

5. BUILD - Compile the imported project
   ALWAYS call selectProject first, regardless of which build path is taken:
     execute_action(action_name="selectProject", params={"projectName": "<imported_project_name>"})
   If .mex files found -> run Update Code and Build:
     execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
   If no .mex files -> use plain build:
     execute_action(action_name="buildProject", params={"projectName": "<imported_project_name>"})

6. FINAL CHECKS
   After the build command from step 5 completes, confirm 0 errors:
   getProblems(severity="error") -> 0 errors = success
   If waitForJob returned matched=0: poll getRunningJobs until idle, then check getProblems
```

## Step-by-Step Instructions

### Step 1: Browse Available ACH Projects

Use `listAchProjects` to discover what's available. This queries NXP's Application Code Hub and returns a list of projects with metadata.

**Basic call (list all):**
```
execute_action(action_name="listAchProjects")
```

**Filter by keyword (recommended - narrows results):**
```
execute_action(action_name="listAchProjects", params={"keyword": "motor control"})
```

**Filter to S32DS-compatible projects only:**
```
execute_action(action_name="listAchProjects", params={"onlyS32DS": true})
```

**Combine filters for precise results:**
```
execute_action(action_name="listAchProjects", params={"keyword": "S32K344", "onlyS32DS": true})
```

#### Parameters for `listAchProjects`

| Parameter | Required | Description |
|-----------|----------|-------------|
| `keyword` | No | Search keyword to filter projects by name or description. Use MCU names (e.g., "S32K344"), application domains (e.g., "motor"), or technology keywords (e.g., "ethernet"). |
| `onlyS32DS` | No | If `true`, returns only projects that are compatible with S32 Design Studio. Recommended to avoid results for other NXP IDEs. |

#### Understanding the Results

The response contains a list of ACH projects, each with:
- **Project name/title** - human-readable description
- **Repository URL** (`repoUrl`) - the Git URL needed for import (this is the KEY field)
- **Description** - what the project demonstrates
- **Compatibility info** - which MCUs/boards are supported
- **Branches** - available branches (main, device-specific, etc.)

> **Important:** Save the `repoUrl` from the results - you will need it for Step 3.

### Step 2: Help the User Choose

After retrieving results, present the options clearly:

1. Show 3-5 most relevant projects with their descriptions
2. Highlight which MCU/board each project targets
3. If the user's target device is known, prioritize matching projects
4. If too many results, ask the user to provide more specific keywords

**Example presentation:**
```
Found 3 ACH projects matching "S32K344":

1. "S32K344 Motor Control PMSM"
   - Sensorless PMSM motor control using S32K344-EVB
   - Repo: https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344

2. "S32K344 LIN Communication Stack"
   - Full LIN driver stack with diagnostics
   - Repo: https://github.com/nxp-appcodehub/dm-lin-stack-s32k344

3. "S32K344 OTA Update Demo"
   - Over-the-air firmware update reference
   - Repo: https://github.com/nxp-appcodehub/an-ota-update-s32k344

Which one would you like to import?
```

### Step 3: Import the Selected Project

Once the user selects a project, use `importAchProject` to clone and set it up:

**Basic import (minimum required - just the repo URL):**
```
execute_action(action_name="importAchProject", params={"repoUrl": "https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344"})
```

**Import with custom local name:**
```
execute_action(action_name="importAchProject", params={"repoUrl": "https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344", "newName": "MyMotorProject"})
```

**Import a specific branch:**
```
execute_action(action_name="importAchProject", params={"repoUrl": "https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344", "branch": "develop"})
```

**Import to a specific directory:**
```
execute_action(action_name="importAchProject", params={"repoUrl": "https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344", "location": "C:/Users/me/workspace/motor_projects"})
```

**Overwrite existing project with same name:**
```
execute_action(action_name="importAchProject", params={"repoUrl": "https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344", "overwrite": true})
```

#### Parameters for `importAchProject`

| Parameter | Required | Description |
|-----------|----------|-------------|
| `repoUrl` | **Yes** | Git repository URL of the ACH project to clone. Obtained from `listAchProjects` results. |
| `newName` | No | Custom local project name. If omitted, the repository name is used (e.g., "an-pmsm-foc-s32k344"). |
| `branch` | No | Git branch to checkout after cloning. Defaults to main/master. Use when a project has device-specific branches. |
| `location` | No | Local filesystem path for the clone destination. Defaults to the current S32DS workspace location. |
| `overwrite` | No | If `true`, overwrites an existing project with the same name. Use with caution. Default is `false`. |

#### What Happens During Import

1. **Git clone** - the repository is cloned from the remote URL to the local filesystem
2. **Project detection** - S32DS scans the cloned directory for Eclipse project metadata (`.project`, `.cproject`)
3. **Workspace registration** - the project is registered in the S32DS workspace
4. **Indexer** - the C/C++ indexer parses the source files (may run in background)

The `importAchProject` response includes a `location` field with the absolute path where the project was cloned. **Save this path** - it is needed to check for `.mex` files before building.

> **Note:** The import involves network I/O (git clone) and may take 30-120 seconds depending on repository size and network speed.

### Step 4: Verify the Import Succeeded

Always verify that the project was imported correctly:

```
execute_action(action_name="listProjects")
```

- Confirm the imported project name appears in the workspace list
- Check that the project state is "open" (not "closed")

Then get detailed project information:

```
execute_action(action_name="getProjectInfo", params={"projectName": "<imported_project_name>"})
```

- Verify the MCU/device assignment is correct
- Check that build configurations exist (Debug, Release)
- Note any SDK references the project expects
- `getProjectInfo` does **NOT** report whether `.mex` files exist in the project. Do not use its output to decide whether code generation is needed. To detect `.mex` files, check the project directory on disk (see Step 5).

### Step 5: Build the Imported Project

Before building, check whether the project contains `.mex` S32 Configuration Tools files. If any `.mex` file is present, run S32CT Update Code and Build before plain compilation. The project path is returned by the `importAchProject` action (`location` field). Most ACH projects contain `.mex` files, but always verify the project directory on disk before building.

**Detect `.mex` files on disk:**

```
# Windows:
dir /s /b "<project_location>\*.mex"

# Linux/macOS:
find "<project_location>" -name "*.mex"
```

- If `.mex` files found** - select project and run Update Code and Build:

```
execute_action(action_name="selectProject", params={"projectName": "<imported_project_name>"})
execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
```

> **Important:** `executeCommand` is **asynchronous** - it returns `"Command scheduled"` immediately. The actual work (code generation + compilation) happens in the background. Do NOT check results until the job finishes.

**Wait for Update Code and Build to complete:**
```
execute_action(action_name="waitForJob", params={"jobName": "Build Project", "timeoutMs": 180000})
```

**If no `.mex` files** - select project first, then use plain buildProject:
```
execute_action(action_name="selectProject", params={"projectName": "<imported_project_name>"})
execute_action(action_name="buildProject", params={"projectName": "<imported_project_name>"})
```

**Wait for the plain build to complete:**
```
execute_action(action_name="waitForJob", params={"jobName": "Building", "timeoutMs": 120000})
```

> If `waitForJob` returns `matched=0` for either path, use `getRunningJobs` to check whether the job is still active before taking further action:
> ```
> execute_action(action_name="getRunningJobs")
> ```
> Poll at **10-15 second intervals** - do not poll more frequently than every 5 seconds to avoid overwhelming the IDE's job manager.
>
> - **Jobs still running** -> poll `getRunningJobs` again until all non-system jobs finish, then check `getProblems`.
> - **No jobs running + 0 errors** -> job completed before the poll window opened. No further action needed.
> - **No jobs running + errors present** -> check whether errors are pre-existing configuration issues (missing SDK, wrong toolchain) or new build failures. Consult the Error Catalog before triggering a new build. If build failures, explicitly trigger the build again:
>   ```
>   execute_action(action_name="buildProject", params={"projectName": "<imported_project_name>"})
>   execute_action(action_name="waitForJob", params={"jobName": "Building", "timeoutMs": 120000})
>   ```
> Do NOT trigger a new build if jobs are still running - the compile is already in progress.

> Note: When building an ACH project, the IDE may show an **SDK Component Management** dialog. If the code generation or build job are not visible within a reasonable time (e.g.: 1 minute), ask the user to check the IDE for any dialog requiring confirmation.

**Final verification - ELF existence + error check:**

```
# Windows - verify ELF was produced:
dir /s /b "<project_location>\*.elf"

# Linux/macOS:
find "<project_location>" -name "*.elf"
```

- **No ELF found** = build did NOT run despite 0 errors. Retry with explicit `buildProject` and wait for `"Building"` job.

```
execute_action(action_name="getProblems", params={"projectName": "<imported_project_name>", "severity": "error"})
```

- **ELF exists + 0 errors** = build succeeded. The project is ready to use.
- **Errors present** = build failed; see the Error Catalog and the `s32ds-fix-build-errors` skill.

## Complete Example: End-to-End ACH Import

```python
# 1. Search for motor control projects compatible with S32DS
execute_action(action_name="listAchProjects", params={"keyword": "motor", "onlyS32DS": true})
# -> Returns list including "an-pmsm-foc-s32k344" with repoUrl

# 2. Import the selected project with a custom name
execute_action(action_name="importAchProject",
               params={"repoUrl": "https://github.com/nxp-appcodehub/an-pmsm-foc-s32k344",
                       "newName": "MotorControl_S32K344"})
# -> Save "location" from response

# 3. Verify it appeared in the workspace
execute_action(action_name="listProjects")
# -> Should show "MotorControl_S32K344" with state: open

# 4. Get project details
execute_action(action_name="getProjectInfo", params={"projectName": "MotorControl_S32K344"})
# -> Shows MCU: S32K344, build configs, SDK references

# 5. Check for .mex files on disk - project path is in the "location" field from importAchProject response.
# -> getProjectInfo does NOT reveal .mex files; check the filesystem location directly

# 6. Build the project

# If .mex files found: select project and run Update Code and Build
execute_action(action_name="selectProject", params={"projectName": "MotorControl_S32K344"})
execute_action(action_name="executeCommand", params={"commandId": "com.nxp.swtools.framework.updateCodeAndBuildProject"})
# -> updateCodeAndBuildProject is async; returns "Command scheduled" immediately
execute_action(action_name="waitForJob", params={"jobName": "Build Project", "timeoutMs": 180000})

# If NO .mex files: select project first, then use plain build
execute_action(action_name="selectProject", params={"projectName": "MotorControl_S32K344"})
execute_action(action_name="buildProject", params={"projectName": "MotorControl_S32K344"})
# -> buildProject is async; returns "Command scheduled" immediately
execute_action(action_name="waitForJob", params={"jobName": "Building", "timeoutMs": 120000})

# 7. Check for errors
execute_action(action_name="getProblems", params={"projectName": "MotorControl_S32K344", "severity": "error"})
# -> 0 errors: ready to debug!
# -> If errors: see troubleshooting section
```

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `listAchProjects` returns empty | No internet connection, or keyword too restrictive | Check network; try broader keyword or no keyword at all |
| `listAchProjects` returns non-S32DS projects | `onlyS32DS` not set | Add `onlyS32DS=true` to filter |
| Import fails with "clone failed" | Network issue, invalid URL, or Git not installed | Verify URL from `listAchProjects`; check internet; ensure Git is in PATH |
| Import fails with "already exists" | Project with same name in workspace | Use `newName` to rename, or set `overwrite=true`, or delete existing project first |
| Import succeeds but project has errors | Missing SDK, wrong toolchain, or code generation needed | Check `getProjectInfo` for SDK needs; install SDK; run `s32ds-safe-code-regen` if `.mex` files exist |
| Project imported but not visible in workspace | Import partially failed or project metadata missing | Check `listProjects`; try closing/re-opening the workspace; re-import with `overwrite=true` |
| Build fails with "SDK not found" | ACH project references an SDK not installed locally | Use `listAllSdks` to check; install via `s32ds-open-extensions-and-updates` skill |
| Build fails with "generated code missing" | Project has `.mex` files that need code generation | Use `s32ds-safe-code-regen` skill before building |
| Wrong branch imported | Default branch doesn't match target MCU | Re-import with explicit `branch` parameter |
| `waitForJob("Build Project")` returns matched=0 | Job completed before poll window, or did not start | Call `getRunningJobs` (poll at 10-15s intervals): jobs present = still running; no jobs + 0 errors = succeeded; no jobs + errors = check for pre-existing config errors first, then retry build |
| `waitForJob("Building")` returns matched=0 | Build completed before poll window, or did not start | Call `getRunningJobs` (poll at 10-15s intervals): same decision logic as above |
| `waitForJob` matched but `getProblems` shows errors | Build failed | See `s32ds-fix-build-errors` skill |
| Build triggered while another build is already running | Build command issued too early | Always check `getRunningJobs` before triggering a new build |

## Troubleshooting Decision Tree

```
Build triggered but result is unclear after waiting?
|
+-- getProblems shows errors
    ├─ "SDK not found" errors
    │   └─ execute_action(action_name="listAllSdks") -> install missing SDK
    ├─ "File not found" errors in generated paths
    │   └─ Project has .mex files -> use s32ds-safe-code-regen skill
    ├─ "Toolchain not found" errors
    │   └─ Check project needs specific GCC version -> install via Extensions
    ├─ Linker errors about missing libraries
    │   └─ Check README.md in the cloned repo for setup instructions
    └─ No errors but warnings only
        └─ Warnings are acceptable for initial import; proceed to debug

+-- getProblems shows 0 errors and 0 warnings
    └─ Build succeeded - 0 errors is the success signal

waitForJob("Build Project") or waitForJob("Building") returned matched=0?
    -> Job may still be running or may have completed before the poll window.
    -> Call getRunningJobs (poll at 10-15s intervals) to check.
    -> Non-system jobs present = still running, keep polling.
    -> No non-system jobs running + verify ELF exists on disk; if no ELF, build did NOT run - retry with buildProject.
    -> No non-system jobs running + ELF exists + 0 errors = build completed successfully.
    -> No non-system jobs running + errors present:
       - Check if errors are pre-existing config errors (missing SDK, wrong toolchain).
       - If pre-existing, consult Error Catalog above before triggering a new build.
       - If build failures, trigger build explicitly and wait again.
```

## Tips and Best Practices

1. **Always use `onlyS32DS=true`** when listing ACH projects - this filters out projects meant for other NXP tools (MCUXpresso IDE, etc.)

2. **Save the `location` field from the `importAchProject` response** - you will need it to check for `.mex` files on disk before building.

3. **Use the correct verified job names** when calling `waitForJob`: `"Build Project"` for the `updateCodeAndBuildProject` command (`.mex` path), and `"Building"` for the `buildProject` action (plain build path).

4. **Check the repository README** after import - ACH projects often include setup instructions, required hardware, and configuration notes in their README files:
   ```
   execute_action(action_name="openFile", params={"filePath": "<workspace>/<project>/README.md"})
   ```

5. **Combine with `getProjectInfo` immediately after import** - this reveals the MCU target, available build configs, and SDK dependencies before you attempt a build.

6. **ACH projects may be more complex than SDK examples** - they often include custom middleware, RTOS configurations, or multi-project setups. Expect additional setup steps compared to simple SDK examples.

## Comparison: ACH Projects vs. SDK Examples

| Aspect | SDK Examples (`listExampleProjects`) | ACH Projects (`listAchProjects`) |
|--------|--------------------------------------|----------------------------------|
| Source | Bundled with installed SDK | Cloud (Git repositories) |
| Complexity | Simple, single-peripheral demos | Complex, application-level references |
| Network Required | No (already installed) | Yes (git clone) |
| Update Frequency | Tied to SDK releases | Updated independently |
| Setup | Usually works out-of-box | May need SDK install, README steps |
| Use Case | Learning peripherals | Production reference implementations |

## Anti-Patterns

-  **Calling `importAchProject` without first using `listAchProjects`** - you won't have a valid `repoUrl`; never guess URLs
-  **Omitting `onlyS32DS=true` and importing an MCUXpresso-only project** - it won't work in S32DS
-  **Skipping the verify step after import** - the clone might fail silently; always check with `listProjects`
-  **Using plain `buildProject` without first checking for `.mex` files on disk** - if `.mex` files are present, `updateCodeAndBuildProject` must be used first or the build will fail with missing header errors
-  **Concluding "no .mex files" from `getProjectInfo` output** - `getProjectInfo` does NOT report `.mex` file presence; always check the project directory on disk using the `location` from `importAchProject` response
-  **Ignoring the project README** - ACH projects often have mandatory setup steps documented there
-  **Using `overwrite=true` without user confirmation** - this destroys any local modifications
-  **Treating `"Command scheduled"` from `executeCommand` as build completion** - `executeCommand` is asynchronous; always wait for the corresponding job before checking results
-  **Using the wrong job name with `waitForJob`**: `updateCodeAndBuildProject` produces a `"Build Project"` job; `buildProject` produces a `"Building"` job. Mixing these will result in `matched=0`.
-  **Calling `buildProject` when a build is already running** - check `getRunningJobs` first; do not trigger a second build if one is already in progress
-  **Triggering a new build as a fallback based solely on `waitForJob` returning matched=0** - call `getRunningJobs` first and check `getProblems`; distinguish between pre-existing config errors and actual build failures before acting
-  **Skipping `selectProject` before any build command** - both `executeCommand` (Update Code and Build) and plain `buildProject` require the project to be selected first in the IDE. Without `selectProject`, the build command operates on whatever project was previously active, or silently does nothing. Always call `selectProject` immediately before any build action.
-  **Reporting build success based solely on `getProblems` returning 0 errors** - `getProblems` only reflects problem markers; it does NOT confirm a build ran. Always verify the ELF file exists on disk after the build. If no ELF is found, the build did not run - retry with explicit `buildProject`.

## Related Skills

- `s32ds-create-project-from-scratch` - alternative project creation paths (SDK examples, wizard)
- `s32ds-safe-code-regen` - required if the imported ACH project contains `.mex` configuration files
- `s32ds-build-and-debug` - next step after successful import and build
- `s32ds-check-sdk-compatibility` - verify the required SDK is installed for the ACH project
- `s32ds-analyze-project` - understand the structure of the imported project
- `s32ds-open-extensions-and-updates` - install missing SDKs needed by the ACH project
- `s32ds-fix-build-errors` - diagnose and resolve build failures after import
