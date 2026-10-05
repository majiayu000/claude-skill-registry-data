---
name: s32ds-multicore-debug
description: Debug multicore S32 MCUs (S32K3, S32G, S32E/S32Z, S32R) with multiple cores running simultaneously. Covers GDB thread-per-core model, attaching to specific cores, setting per-core breakpoints, synchronized halt/resume, cross-core memory inspection, and inter-core communication debugging (shared memory, hardware semaphores). Includes decision tree for core selection and error catalog for common multicore issues (core not halting, thread ID mismatch, XRDC faults).
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, multicore, debug, concurrent-execution, cross-core-inspection, s32-debugger]'
---
# Multicore Debug

## Goal
Debug multicore NXP MCUs (S32K3, S32G, S32R, S32E, S32Z) where multiple cores run concurrently - attach to all cores, control execution per-core, inspect state across cores, and manage inter-core synchronization.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- [ ] Project builds successfully with zero errors
- [ ] Debug probe (S32 Debug Probe) connected - multicore debug requires S32 Debugger
- [ ] A multicore-aware debug/launch configuration exists (typically one config per core or a group launch)
- [ ] Target board powered and all cores are accessible (not locked/secured)

## Guardrails

**Scope**
- Attach and control only the cores the user explicitly named. If a request is ambiguous about which core to act on, ask before attaching or halting.

**Destructive actions**
- Synchronized halt/resume and any reset affect ALL attached cores in all-stop mode. Confirm the intended scope before issuing a broad resume or reset, and prefer `scheduler-locking on` when only one core should move.
- Cross-core memory writes can corrupt another core's state. Confirm the exact address, value, and target core before writing.

**Refuse-and-escalate**
- If thread/core IDs do not match the MCU topology (possible XRDC/config fault or a core still in reset), stop and report rather than guessing - see the Error Catalog and Notes.

## When to Use
- User has a multicore MCU project (S32K3xx, S32G2/G3, S32R, S32E, S32Z)

- User asks to "debug both cores", "attach to M7 and M0", "debug multicore"
- User sees issues that only manifest during multicore interaction (shared memory, IPC)
- User wants to halt/resume individual cores independently
- User needs to inspect state on a secondary core (e.g., Cortex-M0+ on S32K3)

## Decision Tree
```
Start
 ├─ What MCU family?
 │   ├─ S32K3xx -> 2 cores: CM7_0 (primary) + CM0+ (secondary)
 │   ├─ S32G2/G3 -> A53 cluster + M7 cores + M0+ (optional)
 │   ├─ S32R -> multiple CM7 cores (radar DSP)
 │   ├─ S32E/S32Z -> multiple CM7 + lock-step pairs
 │   └─ Other -> check Reference Manual for core topology
 │
 ├─ Does the project have separate ELF files per core?
 │   ├─ YES -> each core needs its own launch config
 │   └─ NO  -> single ELF with multicore awareness (less common)
 │
 ├─ Launch strategy?
 │   ├─ Group Launch -> one click launches all cores (preferred)
 │   ├─ Sequential -> launch primary first, then attach secondary
 │   └─ Single-core only -> debug one core at a time
 │
 └─ Is the secondary core booted by the primary?
     ├─ YES -> must run primary past boot code before attaching secondary
     └─ NO  -> both cores boot independently (can attach simultaneously)
```

## Steps

1. **Identify the multicore topology**:
   - `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})` - check MCU/target info
   - Look for core identifiers in project name or build configs (e.g., `_M7_0`, `_M0P`)
   - `execute_action(action_name="listProjects")` - multicore projects often have paired projects (one per core)

2. **Find all debug launch configurations**:
   - `execute_action(action_name="listDebugLaunches", params={"nameFilter": "<projectBase>"})` - list all configs
   - Look for core-specific configs: `*_M7_0_Debug`, `*_M0P_Debug`, `*_GroupLaunch`
   - Group Launch configurations launch multiple cores simultaneously

3. **Launch primary core first** (if sequential):
   - `execute_action(action_name="selectProject", params={"projectName": "<primary_project>"})`
   - `execute_action(action_name="startDebug", params={"name": "<primary_config>", "build": true})`
   - `execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})`

4. **Attach to secondary core**:
   - `execute_action(action_name="startDebug", params={"name": "<secondary_config>", "build": false})`
   - `execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})`

5. **Terminate all debug sessions**:
   - `execute_action(action_name="terminateDebug", params={"launch": "<primary_config>"})`
   - `execute_action(action_name="terminateDebug", params={"launch": "<secondary_config>"})`

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "Cannot attach to core 1" / secondary attach fails | Secondary core not yet booted by primary | Run primary past boot code first (Step 4), then retry |
| "Target is locked" on secondary core | Core access protection enabled | Check MDMACR/CSW register; may need secure debug unlock |
| Breakpoint on secondary has no effect | Breakpoint set on wrong core context | Use `thread <N>` to switch to secondary before setting breakpoints |
| "Cannot access memory at address 0x..." on secondary | Core's memory map differs from primary | Verify address is accessible from that specific core (check RM memory map) |
| Group Launch only starts one core | Second project has build errors | Build all sub-projects before group launch |

## Common Patterns

### Pattern A: S32K3 dual-core (CM7 + CM0+)
```
# Primary core (CM7_0) - boots first, initializes CM0+
execute_action(action_name="startDebug", params={"name": "MyProject_M7_0_Debug_S32DP", "build": true})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})

# Now attach secondary (CM0+)
execute_action(action_name="startDebug", params={"name": "MyProject_M0P_Debug_S32DP", "build": false})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})
```

### Pattern B: Group Launch (all cores at once)
```
execute_action(action_name="startDebug", params={"name": "MyProject_GroupLaunch", "build": true})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 90000})
execute_action(action_name="runMiDebugCommand", params={"launch": "MyProject_GroupLaunch", "command": "info threads"})
```

### Pattern C: Debug only secondary core (primary already running)
```
# Assume primary is already running standalone (no debug)
# Just attach debugger to secondary core
execute_action(action_name="startDebug", params={"name": "MyProject_M0P_Debug_S32DP", "build": false})
execute_action(action_name="waitForJob", params={"jobName": "Launch", "timeoutMs": 60000})
execute_action(action_name="runMiDebugCommand", params={"launch": "MyProject_M0P_Debug_S32DP", "command": "info threads"})
execute_action(action_name="runMiDebugCommand", params={"launch": "MyProject_M0P_Debug_S32DP", "command": "bt"})
```

## Related Skills
- `s32ds-build-and-debug` - single-core build+debug workflow
- `s32ds-mi-debug-commands` - GDB/MI inspection commands (applies per-core here)
- `s32ds-setup-debug-config` - finding/verifying launch configurations
- `s32ds-flash-target` - flash programming (usually done on primary core only)

## Notes
- **S32K3xx topology**: CM7_0 is always primary. CM0+ is booted by CM7_0 during system startup (Sys_Init). You CANNOT attach to CM0+ until CM7_0 has completed its boot sequence.
- **GDB thread model**: In S32 Debugger's multicore mode, each core appears as a GDB "thread". Use `thread <N>` to switch context.
- **scheduler-locking**: When `on`, only the current thread/core executes during `step`/`next`. When `off`, all cores run. Critical for debugging race conditions.
- **Memory maps differ per core**: Not all addresses are accessible from all cores. CM0+ typically has a smaller memory view than CM7. Check the Reference Manual's memory map chapter.
- **Flash programming**: Only done through the primary core's debug session. The secondary core's attach is "attach only" (no flash download).
- **Non-stop mode**: Some S32 Debugger versions support `set non-stop on` for truly independent core control. In all-stop mode (default), halting one core halts all.

## Anti-Patterns
-  Trying to attach to CM0+ before CM7 has booted it - the core is in reset and cannot be debugged yet
-  Setting breakpoints without switching thread context - breakpoint goes on wrong core
-  Assuming both cores see the same memory view - memory maps differ per core
-  Using `execute_action(action_name="buildProject", ...)` for secondary core project that depends on primary - build primary first
-  Flashing through the secondary core's launch config - flash download is primary-core only
-  Forgetting to terminate ALL debug sessions - each core's session must be terminated separately
