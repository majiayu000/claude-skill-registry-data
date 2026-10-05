---
name: s32ds-setup-debug-config
description: Find, verify, and prepare debug/launch configurations for a project. Lists all existing debug launch configurations, filters by project name, verifies the project builds successfully, checks SDK and project info for probe compatibility, and identifies the correct configuration to use. Prerequisite step before launching any debug or flash session.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, debug, launch-config, probe, verification]'
---
# Setup Debug Configuration

## Goal
Find, verify, and prepare the correct debug/launch configuration for a project. Ensure probe compatibility, security settings, and multicore awareness before launching a debug session.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- Project must exist and be open in the workspace (`execute_action(action_name="listProjects")`)
- Project must build successfully (zero errors)
- A physical debug probe must be connected (S32 Debug Probe, PE Micro, or J-Link)

## Guardrails

**Scope**
- List and verify existing launch configurations only. Do not start a debug session or program the target from this skill; hand off to `s32ds-build-and-debug` or `s32ds-flash-target` for that.

**Destructive actions**
- Never overwrite or delete an existing launch configuration without explicit user confirmation. If a config needs changing, propose the change and let the user approve it.

**Refuse-and-escalate**
- If no matching launch config exists or the project does not build cleanly, stop and route the user to `s32ds-fix-build-errors` (or config creation) rather than debugging a broken build.

## When to Use
- User wants to debug but isn't sure which launch config to use

- Need to verify debug configuration before launching
- Troubleshooting "no launch configuration found" issues
- Setting up first-time debug for a project
- Debug session fails to connect or hangs
- User switched debug probes or target boards

## Decision Tree

```
Does a launch configuration already exist for this project?
├─ YES (execute_action(action_name="listDebugLaunches") returns matches)
│   ├─ Does it match the connected probe type?
│   │   ├─ YES -> Verify build is clean -> Launch (execute_action(action_name="startDebug"))
│   │   └─ NO -> Search docs for correct probe setup; user may need to create new config
│   ├─ Is this a multicore device?
│   │   ├─ YES -> Check if config targets the correct core (CM7_0, CM7_1, CM0+, etc.)
│   │   └─ NO -> Proceed with single-core launch
│   └─ Is the target secured (secure debug / HSE)?
│       ├─ YES -> Enable secure debugging in the Debugger tab; hand off to `s32sdaf-secure-debug-session`
│       └─ NO -> Proceed normally
├─ NO (no launch config found)
│   ├─ Was project imported from example? -> Example should include .launch files; check project root
│   ├─ Was project created from scratch? -> Use get_workflow("debug_issue") for guided creation
│   └─ Was .launch file deleted? -> Search docs for recreating debug configuration
└─ UNSURE -> Run execute_action(action_name="listDebugLaunches") with no filter to see all configs
```

## Steps

### 1. List Available Debug Configurations
Discover all launch configs in the workspace:
```
execute_action(action_name="listDebugLaunches")
```
Note the configuration names, types, and associated projects.

### 2. Filter by Project (if needed)
If the user has a specific project in mind, filter by name:
```
execute_action(action_name="listDebugLaunches", params={"nameFilter": "<project_name>"})
```
- If results are empty, check if the project name is slightly different (e.g., `_Debug` suffix)
- Try broader filter: `execute_action(action_name="listDebugLaunches", params={"nameFilter": "<partial_name>"})`

### 3. Verify Project Builds Successfully
Before debugging, ensure the project compiles without errors:
```
execute_action(action_name="getProblems", params={"projectName": "<project_name>", "severity": "error"})
```
If there are build errors, resolve them first (see `s32ds-fix-build-errors` skill).

### 4. Check Project and SDK Info for Probe Compatibility
Verify the target hardware and determine correct probe expectations:
```
execute_action(action_name="getProjectInfo", params={"projectName": "<project_name>"})
execute_action(action_name="getProjectSdks", params={"projectName": "<project_name>"})
```
- Note the MCU family (S32K3, S32G, S32R, etc.) - determines available probe types
- Note target core (Cortex-M7, Cortex-M0+, Cortex-A53, etc.)

### 5. Search Documentation for Debug Setup
If the user has a specific debug probe or connection issue:
```
semantic_search(query="<probe_type> debug configuration <mcu_family>", corpus="lite")
```
Common searches:
- `"S32 Debug Probe connection setup S32K344"`
- `"PE Micro debug launch configuration"`
- `"secure debug authentication HSE"`
- `"multicore debug attach second core"`

### 6. Launch Debug Session
Once verified, start the debug session:
```
execute_action(action_name="startDebug", params={"name": "<launch_config_name>", "build": true})
```
- Set `build=true` (default) to ensure latest code is flashed
- Set `build=false` only if you've already confirmed the build is current and unchanged

### 7. Verify Debug Started Successfully
After launching, confirm the debug session is active in the IDE (debug perspective should open, target should be halted at entry point or first breakpoint). You can then inspect target state (threads, registers, memory) through the debug workflow described in `debug_and_inspect`.

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No launch config found for project | Config never created, or `.launch` file missing | Check project root for `.launch` files; import example includes them; use `get_workflow("debug_issue")` for creation guide |
| "Connection timed out" or "Failed to connect" | Probe not connected, wrong USB port, driver issue | Verify physical connection; check probe firmware; search docs for probe setup |
| "Target is secured" / Error 102 | Secure debugging not enabled or SoC still locked | Enable secure debugging in Debugger tab; hand off to `s32sdaf-secure-debug-session` |
| Error 601 (wrong challenge/response/password) | Auth type mismatch or wrong secret/ADKP | Match provisioned type (Password vs Challenge & Response); verify key registered for UID |
| "No target core found" or wrong core | Multicore config targeting wrong core | Verify launch config targets correct core ID; check project's target settings |
| "Program file does not exist" | Build output (ELF) missing or path wrong | Rebuild project first; check that build config matches launch config (Debug vs Release) |
| Debug starts but immediately disconnects | Watchdog resetting target during halt | Search: `semantic_search(query="disable watchdog debug", corpus="driver")` |
| "Cannot halt core" on multicore device | Trying to halt a core that isn't released from reset | Check multicore boot sequence; primary core must release secondary cores |
| Flash programming fails during debug launch | Flash driver incompatible or protected sectors | See `s32ds-flash-target` skill; check memory protection settings |
| Launch config exists but uses wrong probe | Config was created for different probe type | User must edit/recreate the launch config in IDE (Run -> Debug Configurations) |

## Common Patterns

### Pattern A: Standard single-core debug (S32 Debug Probe)
```
execute_action(action_name="listDebugLaunches", params={"nameFilter": "MyProject"})
execute_action(action_name="getProblems", params={"projectName": "MyProject", "severity": "error"})
# -> zero errors
execute_action(action_name="startDebug", params={"name": "MyProject_Debug_S32DebugProbe", "build": true})
# -> wait for launch to complete - debug perspective opens, target halted at entry
```

### Pattern B: No config found - guide user
```
execute_action(action_name="listDebugLaunches", params={"nameFilter": "MyProject"})
# -> empty results
semantic_search(query="create debug launch configuration S32DS S32K344", corpus="lite")
get_workflow(name="debug_issue", mcu_family="S32K3", debug_probe="S32 Debug Probe")
# -> provide guidance to user for manual config creation in IDE
```

### Pattern C: Multicore device - verify core targeting
```
execute_action(action_name="getProjectInfo", params={"projectName": "MyMulticoreProject"})
# -> note: target has CM7_0, CM7_1, CM0+
execute_action(action_name="listDebugLaunches", params={"nameFilter": "MyMulticoreProject"})
# -> may show separate configs per core, or one config that attaches to primary core
semantic_search(query="multicore debug configuration S32G", corpus="lite")
```

## Related Skills
- `s32ds-build-and-debug` - complete build + debug flow (uses this skill's verification steps)
- `s32ds-mi-debug-commands` - GDB command execution after debug is running
- `s32ds-flash-target` - if goal is only flash programming without interactive debug
- `s32ds-fix-build-errors` - prerequisite: fix errors before attempting debug
- `s32ds-analyze-project` - understand project structure and target hardware
- `s32sdaf-secure-debug-session` - unlock and debug a secured device (pw / challenge-response)

## Notes
- Debug configurations are stored as `.launch` files in the project directory
- The `build=true` parameter in `execute_action(action_name="startDebug", ...)` triggers a build before flashing - this is usually desired
- Some MCU families require specific probe firmware versions - check documentation if connection fails
- Secured devices require debug authentication before the probe connects - see `s32sdaf-secure-debug-session`

## Anti-Patterns
-  **Launching debug without checking build errors first** - will flash broken/old code or fail entirely
-  **Using the wrong core's launch config on a multicore device** - will hang or target wrong firmware
-  **Ignoring security/authentication on HSE-enabled devices** - probe will fail to connect with cryptic errors
-  **Setting `build=false` without confirming build is current** - risks flashing stale binary
-  **Not verifying probe connection before blaming software** - many "debug failures" are physical cable/USB issues
