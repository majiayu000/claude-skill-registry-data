---
name: s32ds-create-project-from-scratch
description: Create a new S32DS project from scratch - either fully headless via the New Project Wizard backend (createProject + listNpwOptions, no GUI interaction needed) or from an NXP example/Application Code Hub template. Discovers valid processors, toolchains, debuggers, cores and SDKs, then creates a ready-to-build workspace entry. Use this skill whenever the user wants to start, create, scaffold, or bootstrap a new S32DS/S32K/S32G/S32Z project, begin development for a specific MCU, generate a blank project for a given processor + toolchain + debugger, or import an example as a starting point - even if they don't say the word "wizard" or "project" explicitly.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, project-creation, mcu-configuration, sdk-setup, new-project-wizard]'
---
# Create a New Project from Scratch

## Goal
Stand up a brand-new, ready-to-build S32DS project with the correct MCU, core, toolchain, debugger, and SDK - either generated programmatically (headless) or seeded from an example template.

## Tools Used
- `search_actions` - call FIRST to discover available actions and their exact input schemas
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job (e.g. "Building") completes

## Before You Start
Call `search_actions(query="...")` once at the beginning (a parameterless `search_actions()` browses everything). Action names and parameter sets evolve, and this skill should never be the source of truth for them - the live catalog is. Use the catalog to confirm the spelling of each action and which parameters are required vs optional before you dispatch anything through `execute_action`.

## Prerequisites
- S32DS IDE is running and responsive
- For SDK-backed projects: at least one SDK is installed (`execute_action(action_name="listAllSdks")` returns results)
- You know, or can ask the user for, the target MCU (e.g. S32K344, S32K396, S32G274A). The MCU drives every downstream choice, so pin it down early.

## When to Use
- User asks to create / start / scaffold / bootstrap a new project
- User wants to begin development for a specific MCU
- User wants a blank project for a given processor + toolchain + debugger
- User wants to import an NXP example or Application Code Hub project as a starting point
- User asks "how do I get started with [MCU]?"

## Guardrails

**Scope**
- Only create or import projects into the active S32DS workspace. Do not modify, rename, or delete projects the user did not ask you to touch; if a requested action would affect an unrelated project, stop and confirm the target first.
- Only dispatch action names and parameters confirmed via `search_actions` / `listNpwOptions`. If an ID cannot be confirmed against the live catalog, ask the user rather than guessing.

**Project naming convention**
- Project names must start with a letter (`a-z`, `A-Z`) or an underscore (`_`). The first character must NOT be a digit.
- Project names must contain only letters, digits, and underscores: `[a-zA-Z0-9_]`. No spaces, hyphens, dots, slashes, or other special characters are allowed.
- Project names must be at most **63 characters** long.
- If the user supplies a name that violates any of these rules, **STOP** immediately and ask the user to provide a conforming name. Do not silently sanitize, truncate, or transform the name on the user's behalf.
- Apply this check **before** the name-collision check and before any call to `createProject`, `importExampleProject`, or `importAchProject`.

**Destructive actions**
- Never pass `overwrite=True` (ACH import) or reuse an existing project name without explicit user confirmation - it can clobber an existing project. Default to a new `newName`/`projectName`, and only overwrite after the user confirms in writing.
- Do not delete an existing project to resolve an "already exists" collision. Instead, propose a new name or ask the user which project to remove.

**Resource limits**
- Create one project per request unless the user explicitly asks for several. If a single call spawns background jobs, verify with `getProjectInfo`/`listProjects` before starting another.

**Refuse-and-escalate**
- If the target MCU is unknown or ambiguous, stop and ask - the MCU drives toolchain/core/debugger/SDK, so do not pick one on the user's behalf.
- If no SDK is installed for the requested device (`listAllSdks` is empty), do not fabricate an `sdkPath`. Stop and route the user to `s32ds-open-extensions-and-updates` to install one.
- If `createProject` fails with a NullPointerException-style hang or an unclear backend error, stop and report it rather than retrying blindly; re-verify IDs against `listNpwOptions` first.


## Decision Tree

```
How should the project be created?
|
+- Blank / custom project, no template (FASTEST, fully headless)
|     -> listNpwOptions  (discover valid processorId/toolchain/debugger/core)
|     -> createProject   (synchronous; returns the created project directly)
|
+- From an NXP example (great for "show me something that works")
|     +- Know the exact example? -> importExampleProject(exampleId=...)
|     +- Browsing?               -> listExampleProjects(deviceId=...) -> pick -> import
|
+- From Application Code Hub (cloud reference apps / demos)
|     -> listAchProjects(...) -> pick -> importAchProject(repoUrl=...)
|
+- UNSURE -> ask: "Blank project for a specific chip, or start from a working example?"
```

Prefer the headless `createProject` path when the user wants a clean project for a known MCU - it needs no manual GUI steps and returns the result in one synchronous call. Prefer examples when the user wants working reference code to learn from or adapt.

---

## Path A: Headless creation with createProject (Preferred for blank projects)

`createProject` drives the same New Project Wizard backend the GUI uses, but headlessly. It blocks until the project is created (or fails) and returns the project info directly - no `waitForJob` needed.

### 1. Discover valid option values with listNpwOptions
The wizard backend only accepts specific IDs for processor, toolchain, debugger, and core. Guessing them wastes round-trips, so query them first:

```
execute_action(action_name="listNpwOptions")                                  # all parameters at once
execute_action(action_name="listNpwOptions", params={"parameter": "processorId"})  # just one
```

Valid `parameter` values: `processorId`, `core`, `toolchain`, `debugger`, `sdkpath`, `language`, `io`, `fpu`, `library`, `opmode`, `lsp`, `projecttype`. The `processorId` help text is a table mapping each family to its processor IDs and cores - use it to map the user's MCU name to the exact ID.

### 2. Validate project name

Before calling `createProject`, validate `projectName` against ALL of the following rules:

| Rule | Constraint |
|------|-----------|
| First character | Must be a letter (`a-z`, `A-Z`) or underscore (`_`). Digits are NOT allowed as the first character. |
| Remaining characters | Letters, digits, and underscores only: `[a-zA-Z0-9_]` |
| Maximum length | 63 characters |
| Empty name | Not allowed |

The full regex is: `^[a-zA-Z_][a-zA-Z0-9_]{0,62}$`

If the name does not satisfy all rules, **STOP** and return an error message that identifies the specific violation:
- First-character violation: "Project name '{projectName}' must start with a letter (a-z, A-Z) or underscore (_). Digits are not allowed as the first character."
- Invalid characters: "Project name '{projectName}' contains invalid characters. Only letters (a-z, A-Z), digits (0-9), and underscores (_) are allowed."
- Too long: "Project name '{projectName}' is {len} characters long. The maximum allowed length is 63 characters."

### 3. Check for name collision before creating

Before calling `createProject`, check whether a project with the requested name already exists:

```
execute_action(action="listProjects")   # inspect results for the requested name
```

**If the name is already taken, STOP and ask the user to choose a different name:**

> "A project named **{projectName}** already exists in the workspace. Please choose a different name."

The only valid path forward is a new, unique name. Do not proceed until the user provides one.

### 4. Create the project
```
execute_action(
    action_name="createProject",
    params={
        "projectName": "MyProject",
        "processorId": "S32K344",
        "toolchain": "com.nxp.s32ds.cle.arm.mbs.arm32.bare.toolchain",
        "debugger": "pemicro",
        "core": "M7_0",              # optional - defaults to the processor's first core
        "sdkPath": "RTD_SDK_4_0_0",  # optional - join multiple with ';'
        "language": "c",             # optional
        "isExec": True,              # optional - True=executable (default), False=library
    },
)
```

Why `debugger` is non-negotiable: the backend dereferences the debugger selection while building the launch configuration, and omitting it triggers a NullPointerException rather than a clean error. Always pass a `debugger` value you got from `listNpwOptions`. The other optional fields (`io`, `fpu`, `library`, `opmode`, `lsp`) only matter for specialized setups (e.g. `opmode="lockstep"`) - leave them out unless the user has a specific need.

A successful call returns something like:
```json
{ "name": "MyProject", "open": true, "location": "C:\\workspace\\MyProject",
  "uri": "file:/C:/workspace/MyProject", "msg": "Created project 'MyProject'" }
```

### 4. Verify and build
```
execute_action(action_name="getProjectInfo", params={"projectName": "MyProject"})
```
Confirm the MCU/core/build configs look right. Then build - but if you attached an SDK that generates code from `.mex`, follow `s32ds-safe-code-regen` first, because a blank SDK project usually needs code generation before its first successful build.

---

## Path B: Create from an NXP Example

Examples are the quickest way to get working, board-tested code.

1. **Confirm the SDK and device** - `execute_action(action_name="listAllSdks")`. An example for an MCU family won't appear if no SDK for it is installed, so this also tells you whether you need to install one first.

2. **Search** - `execute_action(action_name="listExampleProjects", params={"deviceId": "S32K344"})`. Narrow with `familyId`, `coreId`, `categoryId`, or `keyword` (e.g. `keyword="hello_world"`, `"lpspi"`, `"uart"`). Results carry `exampleId`, `projectName`, and metadata.

3. **Present 3-5 relevant choices** with short descriptions and let the user pick (or recommend one - `hello_world` or a GPIO toggle is a friendly starting point for beginners).

4. **Import** - `execute_action(action_name="importExampleProject", params={"exampleId": "<id>"})`. Prefer `exampleId` over `projectName` because it's unambiguous. Rename on import with `newName="MyProject"` if desired. If the response comes back with a `candidates` list, the match was ambiguous - re-call with tighter filters.

5. **Verify** - `execute_action(action_name="listProjects")` then `getProjectInfo`. A silently failed import leaves no project behind, so don't skip this.

6. **Build** - most examples ship `.mex` files, so run `s32ds-safe-code-regen` before the first build, then `s32ds-build-and-debug`.

---

## Path C: Import from Application Code Hub (ACH)

ACH projects are cloned from a git repository, so creation is driven by a repo URL.

1. **Browse** - `execute_action(action_name="listAchProjects", params={"keyword": "..."})`. Optionally pass `onlyS32DS=True` to limit results to projects compatible with S32 Design Studio.

2. **Import** - `execute_action(action_name="importAchProject", params={"repoUrl": "<git-url>"})`. Optional: `newName`, `branch`, `location`, `overwrite=True`. This performs a git clone and sets the project up in the workspace.

3. **Verify** - `execute_action(action_name="listProjects")`, then proceed to build per `s32ds-safe-code-regen` / `s32ds-build-and-debug`.

---

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `createProject` returns `Missing required parameter: 'debugger'` | `debugger` omitted | Pass a `debugger` ID from `listNpwOptions(parameter="debugger")` |
| `createProject` -> "Project creation failed: ..." | Invalid processorId/toolchain/core combo | Re-check each ID against `listNpwOptions`; the toolchain must match the processor's architecture |
| `listNpwOptions` -> "Unknown NPW parameter" | Misspelled `parameter` value | Call `listNpwOptions` with no args to list the valid parameter names |
| `listExampleProjects` returns empty | No SDK installed for that device | `listAllSdks` to check; install via `s32ds-open-extensions-and-updates` |
| `createProject` returns "already exists" error | Name collision | Ask the user to choose a different name and retry. |
| Import (example/ACH) fails with "already exists" | Name collision in workspace | Use `newName` to import under a different name |
| Ambiguous example match (candidates list) | `projectName` matches several examples | Use `exampleId`, or add `familyId`/`deviceId`/`coreId` filters |
| Imported/created project has build errors | Normal for first build of `.mex`/SDK projects | Run `s32ds-safe-code-regen` - code generation is needed before the first build |
| Ghost project entry after manual disk deletion | Project directory was deleted with shell commands | The on-disk folder is gone but S32 Design Studio still holds the workspace reference. Manual recovery: in S32 Design Studio Project Explorer view, right-click the ghost entry -> **Delete**. Then recreate with `createProject` using a new name. |

## Common Patterns

### Pattern A: Blank project for a known chip (headless)
```
execute_action(action_name="listNpwOptions", params={"parameter": "processorId"})   # find the exact ID
execute_action(action="listProjects")                               # check for name collision
# -> name is free, proceed
execute_action(action_name="createProject", params={"projectName": "Blink",
              "processorId": "S32K344", "toolchain": "<id>", "debugger": "pemicro"})
execute_action(action_name="getProjectInfo", params={"projectName": "Blink"})
```

### Pattern A2: Name already taken - ask for a different name
```
execute_action(action="listProjects")   # -> "{projectName}" already exists

# STOP: inform the user:
# "A project named {projectName} already exists in the workspace. Please choose a different name."

# Once the user provides a new name, proceed with it:
execute_action(action="createProject", projectName="{newName}",
              processorId="S32K344", toolchain="<id>", debugger="pemicro")
execute_action(action="getProjectInfo", projectName="{newName}")
```

### Pattern B: Quick-start with hello_world from an example
```
execute_action(action_name="listExampleProjects", params={"deviceId": "S32K344", "keyword": "hello"})
execute_action(action_name="importExampleProject", params={"exampleId": "<hello_world_id>"})
execute_action(action_name="listProjects")
```

### Pattern C: Find a peripheral example (UART/SPI/I2C)
```
execute_action(action_name="listExampleProjects", params={"deviceId": "S32K344", "keyword": "lpspi"})
execute_action(action_name="importExampleProject", params={"exampleId": "<id>", "newName": "MySpiProject"})
```

## Related Skills
- `s32ds-safe-code-regen` - run before the first build of any `.mex`/SDK-backed project
- `s32ds-build-and-debug` - the natural next step after the project exists
- `s32ds-check-sdk-compatibility` - verify the SDK matches the target device
- `s32ds-analyze-project` - understand a freshly created/imported project's structure
- `s32ds-open-extensions-and-updates` - install missing SDKs

## Notes
- The MCU choice cascades into toolchain, core, debugger, and SDK - so if the user hasn't named one, ask before doing anything else.
- `createProject` is synchronous: when it returns, the project already exists. Examples and ACH imports may kick off background jobs - use `getProjectInfo`/`listProjects` to confirm.
- `exampleId` is the most reliable way to import an example; it sidesteps name ambiguity.
- Some examples target specific evaluation boards (EVB, XVB) - match them to the user's actual hardware.

## Anti-Patterns
- **Calling `createProject` without a `debugger`** - the backend crashes with a NullPointerException instead of a friendly error, so this just looks like a hang. Always supply one from `listNpwOptions`.
- **Guessing processor/toolchain/debugger IDs** - they're discoverable via `listNpwOptions`, and a wrong ID fails the whole creation. Discovery is one cheap call; guessing is several expensive ones.
- **Building a fresh `.mex`/SDK project before code generation** - it will throw confusing errors. Route through `s32ds-safe-code-regen` first.
- **Skipping the verify step** - a silently failed import or create leaves nothing in the workspace, and you'll waste the next few steps acting on a project that doesn't exist.
- **Importing repeatedly with the same name** - causes workspace conflicts; rename with `newName` instead.
- **Attempting to replace an existing project** - when a name collision is detected, the only valid response is to ask the user for a different name. There is no mechanism to replace or delete an existing project programmatically.
- **Deleting a project directory with shell commands (`rmdir`, `del`) before recreating** - the workspace metadata is NOT cleaned up by disk deletion. Eclipse still holds a stale reference and will show a modal confirmation dialog when any UI delete command is later invoked. That dialog blocks the IDE and cannot be dismissed programmatically.
