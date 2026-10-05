---
name: s32ds-flash-target
description: Program the target MCU's flash memory via S32 Debug Probe and verify success. Confirms the project is built without errors, locates the debug/launch configuration, launches the debug session (which internally programs flash), waits for completion, and verifies the target is halted at the entry point using GDB. Supports both 'flash and debug' and 'flash only (disconnect after programming)' patterns.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, flash programmer, debug-probe, verification, target-programming]'
---
# Flash Target Device

## Goal
Program the flash memory of a target MCU via S32 Debug Probe Flash Programmer, verify the image, and confirm success.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- [ ] Project builds successfully with zero errors (run `s32ds-build-and-debug` skill first)
- [ ] Debug probe (S32 Debug Probe) is physically connected to the target board
- [ ] A valid debug/launch configuration exists for the project
- [ ] Target board is powered and not in a locked/secured state

## Guardrails

**Scope**
- Program only the confirmed project's image to the connected probe/target. Do not flash a different project or memory region than the user requested.

**Destructive actions**
- Flashing overwrites target flash. Confirm the correct device and probe before programming, and never flash when the target/probe is ambiguous.
- Do not erase or program regions the user did not explicitly ask for.

**Resource limits**
- Perform one flash operation per request; after programming, verify the target is halted at the entry point rather than re-flashing speculatively.

**Refuse-and-escalate**
- If the build is not clean or no launch configuration exists, stop and escalate to `s32ds-fix-build-errors` / `s32ds-setup-debug-config` instead of flashing.

## When to Use
- User asks to "flash", "program", "download to target", or "burn" firmware

- User wants to verify that compiled code runs on hardware
- After a successful build, as the next step before debugging or standalone execution
- When re-programming a board with updated firmware

## Decision Tree
```
Start
 ├─ Is the project already built successfully?
 │   ├─ YES -> proceed to Step 2
 │   └─ NO  -> run s32ds-build-and-debug skill first (steps 1-4), then return here
 │
 └─ Does a debug launch configuration exist?
     ├─ YES -> proceed to Step 3
     └─ NO  -> guide user to create one (see s32ds-setup-debug-config skill)
```

## Steps

1. **Confirm project is built and error-free**:
   - `execute_action(action_name="getProblems", params={"projectName": "<name>", "severity": "error"})`
   - If errors exist -> STOP. Direct user to fix build errors first.
   - If no recent build -> run `s32ds-build-and-debug` skill steps 1-4 first.

2. **Find the debug/launch configuration**:
   - `execute_action(action_name="listDebugLaunches", params={"nameFilter": "<projectName>"})`
   - Look for a configuration matching the project name and Flash Programmer
   - If multiple exist, prefer one with "Debug" in the name
   - If NONE exist -> inform user they need to create a launch configuration (see `s32ds-setup-debug-config` skill)

3. **Launch the debug session (which programs flash)**:
   - `execute_action(action_name="startDebug", params={"name": "<configName>", "build": false})`
   - `build=false` because we already confirmed the build is clean
   -  This is ASYNC - it only schedules the launch

4. **Wait for flash programming to complete**:
   - `execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})`
   - Flash programming happens during the launch sequence (download to target)
   - If timeout -> check `execute_action(action_name="getRunningJobs")` for stuck jobs

5. **Report results to user**:
   - Confirm: flash programmed successfully, target state (halted/running/disconnected)
   - Include the ELF file that was programmed (from launch config)
   - If any warnings appeared, mention them

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "Could not connect to target" / timeout on launch | Debug probe not connected, wrong probe serial, target not powered | Check USB connection, verify probe serial in launch config, power-cycle board |
| "Flash erase failed" / "Flash program failed" | Target flash is locked/secured, or flash region protected | Perform mass erase first (if supported), check flash protection settings |
| "No debug probe found" | Probe driver not installed, probe in use by another session | Close other debug sessions, reinstall probe drivers, check USB |
| "Target is secured" / "Device is protected" / Error 102 | MCU is locked; debug authentication required before flash | Unlock the device first via the `s32sdaf-secure-debug-session` skill (SDAF password / challenge-response), or mass-erase if the workflow allows |
| `waitForJob` returns `matched=0` for "Launching" | Launch completed very quickly or failed before job was detected | Check `gdb_status()` directly; if unavailable, re-launch |

## Common Patterns

### Pattern A: Flash and Debug (most common)
```
execute_action(action_name="getProblems", params={"projectName": "MyProject", "severity": "error"})
execute_action(action_name="listDebugLaunches", params={"nameFilter": "MyProject"})
execute_action(action_name="startDebug", params={"name": "MyProject_Debug_S32DP", "build": false})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})
```

### Pattern B: Flash Only (no debug session)
```
execute_action(action_name="startDebug", params={"name": "MyProject_Debug_S32DP", "build": false})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})
execute_action(action_name="terminateDebug", params={"launch": "MyProject_Debug_S32DP"})
```

### Pattern C: Re-flash after code change
```
# Rebuild first
execute_action(action_name="buildProject", params={"projectName": "MyProject"})
execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})
execute_action(action_name="getProblems", params={"projectName": "MyProject", "severity": "error"})
# Then flash
execute_action(action_name="startDebug", params={"name": "MyProject_Debug_S32DP", "build": false})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})
```

## Related Skills
- `s32ds-build-and-debug` - full build + debug workflow (flash is part of debug launch)
- `s32ds-setup-debug-config` - creating/configuring launch configurations
- `debug_and_inspect` - post-flash debugging (breakpoints, stepping, memory)
- `s32ds-fix-build-errors` - if build fails before flash
- `s32ds-safe-code-regen` - if project has .mex files and needs code regeneration before build
- `s32sdaf-secure-debug-session` - unlock a secured/locked device before flashing (SDAF password / challenge-response)

## Notes
- In S32DS, flash programming is integrated into the debug launch sequence. There is no separate "flash only" button - you launch a debug session which programs flash as part of its startup.
- The S32 Debug Probe uses GDB + gdbserver. Flash programming is done by the gdbserver (load command internally).
- `build=true` in `execute_action(action_name="startDebug", ...)` triggers an automatic build before flash. Use `build=false` only if you've already verified the build is clean.
- If the target is in a secured state, flash programming will fail. Unlock it first with the `s32sdaf-secure-debug-session` skill (enable secure debugging + SDAF password / challenge-response) before flashing.
- For multicore devices, ensure the correct core's launch configuration is selected.

## Anti-Patterns
-  Calling `execute_action(action_name="startDebug", params={"build": true})` without checking for .mex files first - may build stale code
-  Re-flashing without rebuilding after source changes - will program the old binary
-  Not waiting for "Launching" job before sending GDB commands - GDB server needs time to connect
