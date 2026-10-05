---
name: s32ds-fix-build-errors
description: Systematically diagnose and resolve build errors. Retrieves all errors from the Problems view, categorizes them (compiler errors, linker errors, configuration issues, missing generated code), reads the offending source files for context, applies targeted fixes, and rebuilds iteratively until zero errors remain. Includes an error catalog mapping common error patterns to root causes and solutions.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, search, documentation, reference, peripherals]'
---
# Fix Build Errors

## Goal
Systematically diagnose and resolve build errors (compiler, linker, configuration) in an S32DS project.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Guardrails

**Scope**
- Only edit files in the target project that are implicated by the Problems view. Never modify generated folders (`generate/`, `board/`) or unrelated projects.

**Resource limits**
- Cap the fix/rebuild loop (about 10 iterations). If errors are not converging, stop and report the remaining errors instead of looping indefinitely.

**Refuse-and-escalate**
- If an error stems from missing generated code, route to `s32ds-safe-code-regen` instead of hand-editing generated output.
- If the root cause is unclear, stop and ask the user rather than guessing edits that could introduce regressions.

## Prerequisites
- Project must exist and be open in the workspace

- Read `s32ds-analyze-project` skill first if unfamiliar with the project structure
- Read `s32ds-build-and-debug` skill to understand the build workflow

## Decision Tree
```
START -> execute_action(action_name="getProblems", params={"severity": "error"})
  │
  ├─ No errors found?
  │    -> Project may need rebuild: execute_action(action_name="buildProject", params={...}) first
  │
  ├─ Errors reference generated files (e.g. under generate/, board/, etc.)?
  │    -> .mex file exists in project?
  │         YES -> Run "Update Code and Build" (see s32ds-safe-code-regen skill)
  │         NO  -> Generated code is stale/missing - check SDK attachment
  │
  ├─ Compiler errors (file.c / file.h references)?
  │    -> Go to Error Catalog: Compiler Errors section
  │
  ├─ Linker errors ("undefined reference", "multiple definition")?
  │    -> Go to Error Catalog: Linker Errors section
  │
  └─ Configuration errors (nature/builder/toolchain issues)?
       -> Go to Error Catalog: Configuration Errors section
```

## Steps

### 1. Get Project Context
- **Tool**: `execute_action(action_name="getProjectInfo", params={"projectName": "<name>"})`
- **Purpose**: Understand toolchain, natures, builders, active build config
- **Key fields to note**:
  - `natures` - confirms CDT/C/C++ project type
  - `buildConfigs` - active configuration (Debug/Release)
  - `builders` - what build system is configured
  - `mcuInfo` - target MCU (affects available peripherals and headers)

### 2. Check for .mex Files
- **Tool**: Use file system search to check if `.mex` files exist anywhere in the project
- **Purpose**: Determines if project uses S32 Configuration Tools for code generation
- **Decision**:
  - **If .mex files exist**: Generated code depends on config tool output. Errors in generated files require `Update Code and Build`, NOT manual edits
  - **If no .mex files**: Project uses manually written or SDK-provided code only

### 3. Retrieve All Errors
- **Tool**: `execute_action(action_name="getProblems", params={"projectName": "<name>", "severity": "error"})`
- **Purpose**: Get the full error list with file paths, line numbers, and messages
- **Categorize errors** into:
  - Compiler errors (source file references, syntax, type errors)
  - Linker errors ("undefined reference", "multiple definition", memory overflow)
  - Configuration errors (missing toolchain, bad paths, nature issues)

### 4. Read Problematic Source Files
- **Tool**: `read_file` on each file referenced in errors
- **Purpose**: Understand the code context around each error
- **Tips**:
  - Read 20-30 lines around the error line for context
  - Check `#include` statements at the top of the file
  - Look for conditional compilation (`#ifdef`) that might exclude needed code

### 5. Apply Fixes Based on Error Type
- **Compiler errors**: Edit source files directly with `replace_in_file`
- **Linker errors**: May require build configuration changes or adding source files
- **Generated code errors**: Do NOT edit generated files - fix the .mex configuration or run Update Code
- **Missing SDK headers**: Verify SDK attachment with `execute_action(action_name="getProjectSdks", params={"projectName": "<name>"})`

### 6. Rebuild and Verify
- **Tool**: `execute_action(action_name="buildProject", params={"projectName": "<name>"})`
- **Then**: `execute_action(action_name="waitForJob", params={"jobName": "Build", "timeoutMs": 120000})`
- **Then**: `execute_action(action_name="getProblems", params={"projectName": "<name>", "severity": "error"})`
- **Expected**: Error count should decrease or reach zero
- **If new errors appear**: Some fixes may expose previously hidden errors (e.g., fixing a header include reveals type errors in newly-visible code)

### 7. Iterate If Needed
- Repeat steps 3-6 until all errors are resolved
- If stuck on a specific error, search documentation:
  - `semantic_search(query="<error message or concept>", corpus="all")`

## Error Catalog

### Compiler Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `fatal error: <file>.h: No such file or directory` | Missing include path or SDK not attached | Verify SDK: `execute_action(action_name="getProjectSdks", params={"projectName": "<name>"})`. Check include paths in project settings |
| `error: implicit declaration of function '<name>'` | Missing `#include` for the function's header | Add the correct `#include` statement |
| `error: undefined reference to type '<name>'` | Missing include or typedef not in scope | Add include or check conditional compilation flags |
| `error: incompatible types` | Wrong type passed to function or assigned | Check function signature and fix the type mismatch |
| `error: expected ';' before ...` | Syntax error - missing semicolon, brace, or paren | Check the line above the error for the actual missing character |
| `error: redefinition of '<name>'` | Same symbol defined in multiple places | Remove duplicate or guard with `#ifndef` |
| `warning treated as error` | `-Werror` flag promotes warnings to errors | Fix the underlying warning, or adjust compiler flags if appropriate |

### Linker Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `undefined reference to '<function>'` | Function declared but not defined; source file not in build | Add the .c file containing the definition to the build, or link the correct library |
| `multiple definition of '<symbol>'` | Same symbol defined in multiple .c files (not `static`) | Make one definition, use `extern` in headers, or add `static` for file-local |
| `region '<name>' overflowed by N bytes` | Code/data exceeds available flash/RAM | Optimize code size (`-Os`), reduce static allocations, check linker script regions |
| `cannot find -l<library>` | Library not in linker search path | Add library path to linker settings or verify SDK installation |
| `undefined reference to '_exit'` / `'_sbrk'` | Missing newlib/syscalls stubs | Ensure the project links nosys specs or provides stubs |

### Configuration Errors

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `Program "arm-none-eabi-gcc" not found in PATH` | Toolchain not configured or not installed | Check S32DS toolchain installation, verify PATH in build environment |
| `make: *** No rule to make target '<file>'` | Source file referenced in build but deleted/moved | Remove stale reference from build configuration or restore the file |
| `Build configuration not found` | Active config deleted or corrupted | Check `buildConfigs` in project info, recreate if needed |

## Common Patterns

- **Pattern: Errors only in generated code** -> Never edit generated files manually. Run "Update Code and Build" or fix the .mex configuration. See the `s32ds-safe-code-regen` skill for the correct workflow.
- **Pattern: Hundreds of errors after SDK update** -> SDK version mismatch. Check `execute_action(action_name="getProjectSdks", params={"projectName": "<name>"})` and compare with expected version. May need to re-attach correct SDK version.
- **Pattern: Errors disappear after clean+rebuild** -> Stale object files. See the `s32ds-clean-and-rebuild` skill workflow.
- **Pattern: Errors only in Release but not Debug** -> Different optimization levels expose different warnings-as-errors or undefined behavior. Compare compiler flags between configurations.
- **Pattern: "file not found" after project import** -> Include paths may be relative and broken. Check project includes against actual file locations.

## Related Skills
- `s32ds-build-and-debug` - complete build + debug workflow (read BEFORE building)
- `s32ds-clean-and-rebuild` - when stale artifacts cause phantom errors
- `s32ds-analyze-project` - understand project structure before fixing
- `s32ds-check-sdk-compatibility` - when errors stem from SDK version mismatch
- `s32ds-safe-code-regen` - when errors are in generated code (.mex projects)

## Notes
- Always check if errors are in generated code before editing - generated files will be overwritten on next code generation
- The `getProblems` action (via `execute_action`) returns markers from the last successful build; if no build has run, it may show stale results
- Some projects use `-Werror` which turns all warnings into errors - check compiler flags
- Multicore projects may have separate build configurations per core - ensure you're building the correct one
- After fixing linker "undefined reference" errors, the fix often requires adding a .c file to the build, not editing existing code

## Anti-Patterns (Do NOT)
-  Do NOT manually edit files under `generate/`, `board/`, or other generated directories - they will be overwritten
-  Do NOT assume a single rebuild will reveal all errors - fix iteratively as later errors may be masked
-  Do NOT change linker scripts without understanding memory map implications for the target MCU
-  Do NOT ignore warnings in the error list - they often indicate the root cause of subsequent errors
-  Do NOT skip the .mex check - building without code generation on a .mex project guarantees errors
