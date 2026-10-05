---
name: s32ds-configure-preferences
description: Browse and open S32DS IDE preference/settings pages. Lists all available preference pages with their IDs, then opens a specific page by ID so the user can adjust IDE settings (compiler paths, code style, debugger options, etc.). Useful when the user needs to change toolchain settings or IDE behavior.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, preferences, configuration, ide-settings]'
---
# Configure Preferences

## Goal
Browse, locate, and open specific IDE preference pages in S32 Design Studio so the user can modify settings.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- S32DS IDE must be running and responsive
- Know what setting the user wants to change (or at least the domain: compiler, formatting, debug, etc.)

## Guardrails

**Scope**
- Only open the specific preference page the user requested. Do not change setting values unless the user explicitly asks; opening a page for review is the default.

**Destructive actions**
- Confirm before altering toolchain/compiler paths or other build-affecting settings - a wrong value can break every build. Report the change made so the user can revert it.

**Refuse-and-escalate**
- If the requested preference page ID is unknown or not found, list the available pages and ask the user to choose rather than guessing an ID.

## When to Use
- User wants to change IDE settings (compiler paths, formatting, encoding, etc.)

- Need to find a specific preference page by name or keyword
- Adjusting toolchain, code style, or workspace preferences
- Configuring debug probe defaults, memory settings, or console behavior

## Decision Tree
```
START
  ├─ User knows exact preference page?
  │    YES -> Open directly (step 3)
  │    NO  -> List all pages first (step 1) -> search/filter (step 2)
  │
  ├─ Is this a workspace-level or project-level setting?
  │    WORKSPACE -> Use execute_action(action_name="openPreferences") (this skill)
  │    PROJECT   -> Use execute_action(action_name="getProjectInfo") + guide to Project Properties
  │
  └─ User wants to install extensions/SDKs?
       YES -> Use the s32ds-open-extensions-and-updates skill instead
       NO  -> Continue with this skill
```

## Steps

### 1. List Available Preference Pages
- **Tool**: `execute_action(action_name="listPreferencePages")`
- **Purpose**: Discover all registered preference page IDs and labels
- **Expected result**: JSON with `{ count, preferencePages: [ { id, label }, ... ] }`
- **If it fails**: IDE may not be running - verify with `execute_action(action_name="listProjects")`

### 2. Identify the Target Page
- **Purpose**: Match user's request to a specific page ID
- Search the returned list for keywords relevant to the user's request
- Common preference pages:

| User Request | Likely Page ID Pattern | Label |
|---|---|---|
| Code formatting / indentation | `org.eclipse.cdt.ui.preferences.CodeFormatterPreferencePage` | C/C++ Code Style > Formatter |
| Include paths / symbols | `org.eclipse.cdt.ui.preferences.BuildPathsPropertyPage` | C/C++ General > Paths and Symbols |
| Workspace encoding / line endings | `org.eclipse.ui.preferencePages.Workspace` | General > Workspace |
| Console output limits | `org.eclipse.debug.ui.ConsolePreferencePage` | Run/Debug > Console |
| Toolchain / compiler paths | Pages containing `toolchain` or `S32` | S32DS-specific toolchain |
| Debug probe settings | Pages containing `debug` or `probe` | S32 Debugger settings |
| Git / version control | `org.eclipse.egit.ui.internal.preferences` | Team > Git |
| Editor behavior (tabs, spaces) | `org.eclipse.ui.preferencePages.GeneralTextEditor` | General > Editors > Text Editors |

- **If no match found**: Ask user for more details about what they want to configure

### 3. Open the Preference Page
- **Tool**: `execute_action(action_name="openPreferences", params={"pageId": "<preference_page_id>"})`
- **Purpose**: Navigate directly to the desired preference dialog
- **Expected result**: `{ ok: true }` - dialog opens in IDE
- **If it fails**: Page ID may be incorrect - double-check against step 1 results

To open the root preferences dialog (for browsing):
- **Tool**: `execute_action(action_name="openPreferences")` (no pageId)

### 4. Discover Available IDE Commands (optional)
- **Tool**: `execute_action(action_name="listCommands")`
- **Purpose**: List all executable IDE command IDs (useful when user wants to trigger actions programmatically)
- **Expected result**: JSON with available command identifiers
- **Use case**: User asks "what commands can I run?" or needs a command ID for keybindings/automation

### 5. Guide the User
- **Purpose**: Since MCP cannot programmatically change preference values, provide clear instructions
- Tell the user:
  - What setting to look for in the opened dialog
  - What value to set or change
  - Whether to click "Apply" or "Apply and Close"
  - Whether a restart is needed (rare, but some settings require it)

### 6. Verify (if applicable)
- For settings that affect build behavior: suggest a clean rebuild
  - the `s32ds-clean-and-rebuild` skill
- For settings that affect project structure: re-check with `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})`

## Error Catalog

| Error Pattern | Likely Cause | Fix |
|---|---|---|
| `execute_action(action_name="openPreferences", ...)` returns error | IDE not running or busy | Wait for jobs to complete, retry |
| Page ID not found in list | Preference page from a plugin not installed | Check Extensions and Updates for missing plugin |
| Setting doesn't persist after restart | Project-level setting overriding workspace | Check Project Properties (right-click project) |
| "Apply" button grayed out | No changes detected by dialog | Ensure you actually modified a value |
| Preference affects only new projects | Some defaults only apply to new projects | For existing projects, change in Project Properties |

## Common Patterns

### Pattern 1: Change Workspace Encoding
```
execute_action(action_name="listPreferencePages")
# Find: "General > Workspace" or ID containing "Workspace"
execute_action(action_name="openPreferences", params={"pageId": "org.eclipse.ui.preferencePages.Workspace"})
# Guide: "Text file encoding" -> select "Other: UTF-8" -> Apply and Close
```

### Pattern 2: Configure Code Formatter
```
execute_action(action_name="listPreferencePages")
# Find: C/C++ > Code Style > Formatter
execute_action(action_name="openPreferences", params={"pageId": "org.eclipse.cdt.ui.preferences.CodeFormatterPreferencePage"})
# Guide: Select profile or import formatter XML -> Apply
```

### Pattern 3: Adjust Console Buffer Size
```
execute_action(action_name="openPreferences", params={"pageId": "org.eclipse.debug.ui.ConsolePreferencePage"})
# Guide: Check "Limit console output" -> set buffer size -> Apply
```

## Related Skills
- `s32ds-open-extensions-and-updates` - for installing plugins/SDKs, not preferences
- `s32ds-analyze-project` - to understand project settings before changing preferences
- `s32ds-clean-and-rebuild` - after changing build-related preferences

## Notes
- MCP **cannot** programmatically set preference values - it can only open the dialog
- Some preferences are **project-scoped** (right-click project -> Properties) vs **workspace-scoped** (Window -> Preferences). This skill handles workspace-scoped only.
- Preference pages come from Eclipse plugins; if a plugin isn't installed, its pages won't appear
- Changes to build-related preferences (toolchains, paths) typically require a clean rebuild to take effect
- Some preference page IDs may vary between S32DS versions

## Anti-Patterns (Do NOT)
-  Do NOT guess preference page IDs without listing first - IDs vary by installation
-  Do NOT confuse workspace preferences with project properties - they override differently
-  Do NOT assume a preference change takes effect immediately - some need restart or rebuild
-  Do NOT use this skill for SDK installation - use `s32ds-open-extensions-and-updates` instead
