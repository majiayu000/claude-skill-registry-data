---
name: s32ds-check-sdk-compatibility
description: Verify that a project's attached SDK is compatible with its target MCU. Retrieves the project's SDK descriptors, lists all installed SDKs, compares version/platform/device information, and checks that required peripherals and drivers are available for the specific target device. Useful when importing projects from other machines or upgrading SDK versions.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, sdk-compatibility, diagnostics]'
---
# Check SDK Compatibility

## Goal
Verify that the SDKs attached to a project match the project's MCU target, identify mismatches, and guide resolution.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- S32DS IDE must be running and responsive
- The target project must exist in the workspace (open or closed)
- Read the `s32ds-analyze-project` skill first if you don't know the project name or MCU target

## Guardrails

**Scope**
- This skill is read-only. Inspect SDK and project descriptors only; never attach, detach, upgrade, or modify an SDK as a side effect. If a change is warranted, recommend it and let the user act.

## When to Use
- Before building a project that was imported or cloned from version control

- After changing the MCU target of a project
- When build errors suggest missing drivers or incompatible headers
- When the user asks "is my SDK correct?" or "why are drivers missing?"
- After installing new SDKs via Extensions and Updates

## Decision Tree
```
START
  ├─ Do you know the project name?
  │    NO  -> execute_action(action_name="listProjects") first
  │    YES 
  ├─ Get project MCU info -> execute_action(action_name="getProjectInfo")
  │    ├─ mcu.platform present?
  │    │    NO  -> Project may not be an MCU project (e.g., library). STOP.
  │    │    YES 
  ├─ Get attached SDKs -> execute_action(action_name="getProjectSdks")
  │    ├─ Any SDKs returned?
  │    │    NO  -> No SDK attached! -> List all SDKs -> recommend attachment
  │    │    YES 
  ├─ Compare SDK platformTarget vs project mcu.platform
  │    ├─ Match? ->  Compatible. Check version freshness.
  │    └─ Mismatch? ->  Wrong SDK. -> List all SDKs -> find correct one.
  └─ Check SDK version (latest available?)
       ├─ Latest ->  Done
       └─ Outdated -> Suggest update via Extensions and Updates
```

## Steps

### 1. Get Project MCU Information
- **Tool**: `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})`
- **Purpose**: Retrieve the project's MCU target (family, part number, platform)
- **Expected result**: JSON containing `mcu: { family, part, platform, core }`
- **Key fields to note**:
  - `mcu.platform` - e.g., `"S32K3xx"`, `"S32K1xx"`, `"MPC57xx"`
  - `mcu.part` - e.g., `"S32K344"`, `"S32K148"`
  - `mcu.core` - e.g., `"cortex-m7"`, `"cortex-m4"`
- **If it fails**: Project may not exist - verify with `execute_action(action_name="listProjects")`

### 2. Get Project SDKs
- **Tool**: `execute_action(action_name="getProjectSdks", params={"projectName": "<name>"})`
- **Purpose**: Retrieve all SDKs currently attached to the project
- **Expected result**: JSON with SDK descriptors including `id`, `name`, `version`, `platformTarget`, `tags`
- **Key fields to note**:
  - `platformTarget` - must match `mcu.platform` from step 1
  - `version` - note for freshness check
  - `name` - human-readable SDK name
- **If empty result**: No SDK is attached - this is the problem. Skip to step 4.

### 3. Compare SDK vs Project Target
- **Purpose**: Determine if attached SDKs are compatible with the project's MCU
- **Comparison rules**:

| Check | Expected | Status |
|---|---|---|
| SDK `platformTarget` == project `mcu.platform` | Must match exactly |  if match,  if mismatch |
| SDK supports project's `mcu.part` | Part should be in SDK's supported devices |  if supported |
| SDK `version` is latest available | Compare against all SDKs |  if outdated |

- **If mismatch found**: Note the expected platform and continue to step 4
- **If all match**: Report compatibility confirmed, skip to step 6

### 4. List All Available SDKs
- **Tool**: `execute_action(action_name="listAllSdks")`
- **Purpose**: Find SDKs that ARE compatible with the project's MCU platform
- **Expected result**: Full list of installed SDKs with platform targets
- **Filter for**: SDKs whose `platformTarget` matches the project's `mcu.platform`
- **If no matching SDK found**: The correct SDK is not installed - guide user to install it

### 5. Report and Recommend
- **Purpose**: Provide clear recommendation to the user
- **For no SDK attached**:
  - List compatible SDKs found in step 4
  - Guide: "Attach this SDK to the project via Project Properties > SDKs"
- **For wrong SDK**:
  - Explain the mismatch (e.g., "Project targets S32K3xx but SDK targets S32K1xx")
  - Recommend the correct SDK from step 4
- **For missing SDK (not installed)**:
  - Guide user to install via Extensions and Updates
  - See the `s32ds-open-extensions-and-updates` skill
- **For outdated SDK**:
  - Note current version vs available version
  - Suggest update via Extensions and Updates

### 6. Summarize Compatibility Report
- **Purpose**: Present findings clearly
- **Format**:
```
## SDK Compatibility Report: <project_name>
- MCU Target: <mcu.part> (platform: <mcu.platform>, core: <mcu.core>)
- Attached SDKs: <count>
  - <sdk_name> v<version> - platformTarget: <target> -  Compatible /  Mismatch
- Status: COMPATIBLE / MISMATCH / NO SDK ATTACHED
- Recommendation: <action if needed>
```

## Error Catalog

| Error Pattern | Likely Cause | Fix |
|---|---|---|
| No SDKs returned from `execute_action(action_name="getProjectSdks")` | SDK never attached to project | Attach via Project Properties > SDKs |
| SDK `platformTarget` doesn't match `mcu.platform` | Wrong SDK selected during project creation | Remove wrong SDK, attach correct one |
| `execute_action(action_name="listAllSdks")` returns no matching SDKs | Required SDK not installed in IDE | Install via Extensions and Updates |
| Build errors: "undefined reference to driver functions" | SDK attached but not configured for code generation | Run Update Code (safe_code_regen skill) |
| Build errors: "incompatible type" in SDK headers | SDK version mismatch with generated code | Clean -> regenerate code -> rebuild |
| Project has multiple SDKs with conflicting platforms | Misconfiguration from copy/import | Remove incompatible SDKs from project |

## Common Patterns

### Pattern 1: Quick Compatibility Check
```
execute_action(action_name="getProjectInfo", params={"projectName": "MyProject"})
# -> mcu.platform = "S32K3xx"
execute_action(action_name="getProjectSdks", params={"projectName": "MyProject"})
# -> SDK platformTarget = "S32K3xx" ->  Match
```

### Pattern 2: No SDK Attached
```
execute_action(action_name="getProjectSdks", params={"projectName": "MyProject"})
# -> empty / no SDKs
execute_action(action_name="listAllSdks")
# -> Find SDK with platformTarget matching project's mcu.platform
# -> Guide user to attach it
```

### Pattern 3: SDK Installed but Wrong Version
```
execute_action(action_name="getProjectSdks", params={"projectName": "MyProject"})
# -> RTD v3.0.0 attached
execute_action(action_name="listAllSdks")
# -> RTD v4.0.0 available
# -> Recommend update via Extensions and Updates, then re-attach
```

## Related Skills
- `s32ds-analyze-project` - get full project context before SDK check
- `s32ds-open-extensions-and-updates` - install missing SDKs
- `s32ds-safe-code-regen` - regenerate code after SDK change
- `s32ds-clean-and-rebuild` - rebuild after SDK update
- `s32ds-create-project-from-scratch` - ensure correct SDK from project creation

## Notes
- SDK `platformTarget` is the primary compatibility indicator - it MUST match `mcu.platform`
- A project can have multiple SDKs attached (e.g., RTD + MCAL) - all should target the same platform
- SDK attachment is different from SDK installation: a SDK must be installed in the IDE first, then attached to a project
- After changing SDKs, always run code generation (`s32ds-safe-code-regen`) and rebuild
- Some SDKs have additional tags (e.g., `AUTOSAR`, `FreeRTOS`) that indicate feature support, not platform compatibility
- The `version` field matters for API compatibility - mixing code generated with SDK v3 and building with SDK v4 can cause type errors

## Anti-Patterns (Do NOT)
-  Do NOT assume a build error is an SDK mismatch without checking - many build errors are unrelated to SDKs
-  Do NOT attach multiple SDKs targeting different platforms to the same project
-  Do NOT skip code regeneration after changing the attached SDK - old generated code will be incompatible
-  Do NOT remove an SDK from a project without understanding what code depends on it
-  Do NOT confuse "SDK installed in IDE" with "SDK attached to project" - they are separate steps
