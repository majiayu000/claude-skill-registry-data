---
name: s32ds-open-s32ct
description: Open S32 Configuration Tools perspectives (Pins, Clocks, Peripherals, DCD, DDR, eFUSE, GTM, ICE, IVT, QuadSPI, SERDES) in the S32DS IDE. Each configuration tool has a dedicated Eclipse perspective ID. Use this skill to switch to the appropriate perspective when the user needs to configure MCU peripherals, pin muxing, clock trees, or other hardware settings visually.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, configuration-tools, perspectives, pins, clocks, peripherals, mex]'
---
# Open S32 Configuration Tools (S32CT)

## Goal
Open a specific S32 Configuration Tools perspective (Pins, Clocks, Peripherals, etc.) using `execute_action(action_name="openPerspective", ...)`.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Guardrails

**Scope**
- Only open the requested S32CT perspective for the user's project. Do not edit `.mex` content or generate code from this skill; hand off to the relevant configuration/codegen skill for that.

**Refuse-and-escalate**
- If the perspective or tool is unavailable (e.g. the project has no `.mex`, or the `.mex` was never opened), stop and report the missing prerequisite rather than forcing a perspective that cannot load.

## Prerequisites
- The project must contain a `.mex` file (S32CT configuration file)

- The project must be open in the workspace
- The `.mex` file should have been opened at least once (so S32CT perspectives are registered)

## Steps

1. **Identify the project**:
   - Use `execute_action(action_name="listProjects")` to list workspace projects
   - Confirm the target project is open

2. **Verify the .mex file exists** (project validation):
   - Use `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})` to get project details
   - The `.mex` file is typically at the project root: `<projectName>/<projectName>.mex`
   - Alternative locations: `<projectName>/board/<name>.mex`
   - If there is no `.mex` file, S32CT is not available for this project

3. **Open the desired S32CT perspective**:
   - Determine which S32CT tool the user wants (Pins, Clocks, Peripherals, etc.)
   - Use `execute_action(action_name="openPerspective", params={"perspectiveId": "<id>"})` with the appropriate ID from the table below

## Known S32CT Perspectives

| Tool | Perspective ID |
|------|---------------|
| Pins | `com.nxp.swtools.mux.perspective` |
| Clocks | `com.nxp.swtools.clocks.clocks.perspective` |
| Peripherals | `com.nxp.swtools.periphs.gui.perspective` |
| DCD | `com.nxp.swtools.dcd.perspective` |
| DDR | `com.nxp.swtools.ddr.perspective` |
| eFUSE | `com.nxp.swtools.efuse.gui.perspective` |
| GTM | `com.nxp.swtools.gtm.gui.perspective` |
| ICE | `com.nxp.swtools.ice.gui.perspective` |
| IVT | `com.nxp.swtools.ivt.perspective` |
| QuadSPI | `com.nxp.swtools.quadspi.perspective` |
| SERDES | `com.nxp.swtools.serdes.perspective` |

## Dynamic Discovery (Fallback)

If the user asks for an S32CT perspective that is **not** in the table above, or if you are unsure which perspective matches their request:

1. Call `execute_action(action_name="listPerspectives")` to get the full list of registered perspectives
2. Filter results for entries containing `nxp.swtools` or matching the user's description
3. Use the discovered `perspectiveId` with `execute_action(action_name="openPerspective", params={"perspectiveId": "<id>"})`

This ensures support for new S32CT tools that may be added in future S32DS versions.

## Switching Back (Closing S32CT)

S32CT tools are Eclipse **perspectives** - they change the entire workbench layout.
To return to the normal development environment:

- **Switch to C/C++ perspective**: `execute_action(action_name="openPerspective", params={"perspectiveId": "com.nxp.s32ds.cle.cdt.ui.internal.CPerspective"})`
- **Switch to Debug perspective**: `execute_action(action_name="openPerspective", params={"perspectiveId": "com.nxp.s32ds.debug.ide.ui.DebugPerspective"})`

Do NOT use `execute_action(action_name="openView", ...)` or `execute_action(action_name="executeCommand", ...)` for this - always use `execute_action(action_name="openPerspective", params={"perspectiveId": "<id>"})`.

## Error Handling
- If no `.mex` file is found -> project was not created with S32CT support
- Inform the user that S32CT is not available for this project
- Suggest creating a new project with S32CT support using the new project wizard
- If `execute_action(action_name="openPerspective", ...)` fails -> the perspective may not be installed for the current MCU family (e.g., DDR is only available for certain devices)

## Notes
- The `.mex` file contains all pins, clocks, and peripherals configuration
- Not all perspectives are available for all MCU families (e.g., DDR, SERDES, QuadSPI are device-specific)
- Changes in S32CT generate code (typically in `board/` or `generate/` folders)
- After S32CT changes, use "Update Code and Build" to regenerate and rebuild
- When the user says "open S32CT" without specifying which tool, ask which one they want or default to **Pins** (`com.nxp.swtools.mux.perspective`) as it is the most commonly used
