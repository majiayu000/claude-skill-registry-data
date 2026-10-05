---
name: s32ds-open-extensions-and-updates
description: Open the S32DS Extensions and Updates dialog to install, update, or manage IDE components, SDKs, and plugins. Executes the specific command ID that launches the modular installer UI. Use when the user needs to add new SDK packages, update existing components, or check for available extensions.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, extensions, updates, installer, packages, plugins]'
---
# Open Extensions and Updates (Installer)

## Goal
Open the S32DS Extensions and Updates dialog to install, update, or manage IDE components and packages.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Guardrails

**Scope**
- Only open the Extensions and Updates (modular installer) dialog. Do not auto-install, update, or remove components on the user's behalf.

**Refuse-and-escalate**
- Leave actual install/update/uninstall choices to the user inside the dialog. If asked to pick or apply a specific package automatically, stop and confirm the exact package and action first.

## Steps

1. **Open the Installer dialog**:

   - Use `execute_action(action_name="executeCommand", params={"commandId": "com.nxp.s32ds.cle.modular.installer.open.command"})`
   - This opens the S32DS modular installer window

2. **The Installer dialog allows**:
   - Browse available packages and extensions
   - Install new SDK packages, toolchains, or plugins
   - Update existing installed components to newer versions
   - Remove installed components

## Alternative: Check for Updates only

If you only want to check for updates (p2-based Eclipse updates):
- Use `execute_action(action_name="executeCommand", params={"commandId": "org.eclipse.equinox.p2.ui.sdk.update"})`
- This opens the standard Eclipse "Check for Updates" dialog

## Notes
- The installer requires internet connectivity to query available packages
- Installation/update operations may require an IDE restart
- The command ID is: `com.nxp.s32ds.cle.modular.installer.open.command`
- This is equivalent to: Help -> Extensions and Updates in the S32DS menu
