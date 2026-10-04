---
name: unreal-instructions
description: REQUIRED ENTRY POINT for ALL Unreal Engine tasks. Must trigger for UE5, Blueprints, C++, UMG, Editor, UObject, multiplayer, compilation, or any engine interaction.
---
# Unreal Engine MCP Guide

## 1. Dual-MCP Architecture & Tool Routing

-   **`unrealengine` (Internal Editor, port 18777)**: Use for Blueprint/UMG/Level changes and asset manipulation (e.g., `spawn_actor`, `inject_blueprint_nodes_t3d`).
    -   *Constraint*: ALWAYS use Unreal paths (`/Game/...`). NEVER use Windows paths or shell commands (`rm`, `mv`) for `.uasset` files.
    -   *UMG Tool Parameters*: When using native tools to edit complex widget layouts (like `set_widget_slot`), be aware that layout parameters (anchors, offsets, alignment, Z-order) often must be passed inside a nested object (e.g., `slot_properties`), rather than at the top level of the tool arguments. Always check the tool schema structure carefully.
-   **`cpp-ast-rag` (External AST)**: The Python-based AST server. ALWAYS use its specialized tools (`query_cpp_ast`, `search_vector_db`, `search_similar_blueprints`) for C++ semantic lookups and documentation search instead of generic grep/file searches.
-   **Engine Class AST Fallback**: The local project C++ AST (`query_cpp_ast`) indexes your project's custom C++ source code. For built-in Unreal Engine classes (e.g. `UInstancedStaticMeshComponent`, `AActor`, `UCharacterMovementComponent`), `query_cpp_ast` may not find a local declaration. If `query_cpp_ast` returns no results for an Engine class, immediately query Unreal Engine documentation via `search_vector_db`.
-   **Python API Documentation Lookup**: The Unreal Engine Python API signatures (`unreal.pyi`) are indexed in the ChromaDB vector database. When writing Python scripts for Unreal Engine, ALWAYS use `search_vector_db` with queries like `"unreal.SourceControl"` or `"take screenshot python"` to retrieve exact class and method signatures before executing python scripts.
- **Compilation**: Use `trigger_compile` tool when Editor is open. NEVER run manual terminal builds (UBT/MSBuild) with an open Editor.
- **Python Execution Safeguard**: When running multi-line Python scripts, ALWAYS write the script to a temporary `.py` scratch file (e.g. `scratch/script.py`) using `write_to_file` before running it via `python` or `execute_python_script`. NEVER pass inline multi-line Python strings (`python -c "..."`) inside terminal shell commands to prevent Windows PowerShell string escaping failures.

<!-- LOCAL_ENV_START -->
## 2. Local Environment & Workflows
 
### Startup Requirement (Sandbox Pre-Authorization)
Launching the Unreal Editor spawns a long-lived GUI process outside the terminal sandbox. How to authorize this depends on your agent harness:
- **If your harness provides an `ask_permission` tool (e.g. Antigravity):** When this plugin first loads, proactively call `ask_permission` with `Action`: `"unsandboxed"` and `Target`: `"C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe"` before any editor interaction is needed.
- **If it does not (e.g. Claude Code, OpenAI Codex, Kilo Code):** Skip this step entirely â€” do NOT search for or attempt to call `ask_permission`. Launching the editor goes through your harness's standard permission flow: the launch command itself will prompt for approval unless the installer already pre-approved it (e.g. via `.claude/settings.json` allow rules or your assistant's command allowlist).
 
### Local Paths
- **Unreal Engine Root:** C:/Program Files/Epic Games/UE_5.8
- **Unreal Editor Executable:** C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe
- **Unreal Build Tool:** C:/Program Files/Epic Games/UE_5.8/Engine/Build/BatchFiles/Build.bat
- **Unreal Project File:** C:/Users/janv1/Documents/Unreal Projects/AgentFrameworkTest/AgentFrameworkTest.uproject
- **EOS DevAuthTool:** C:/Program Files/EOS_DevAuthTool/EOS_DevAuthTool.exe
- **Libclang Path:** C:/Program Files (x86)/Microsoft Visual Studio/18/BuildTools/VC/Tools/Llvm/x64/bin/libclang.dll
- **Launcher Script:** C:/Users/janv1/Documents/Unreal Projects/UE-Antigravity/UnrealEngine/src/launch_editor.ps1

### Developer Tool Workflows
#### 1. EOS DevAuthTool
Only start this tool when testing multiplayer/online functionality or when explicitly requested. When required:
`powershell
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = '"C:/Program Files/EOS_DevAuthTool/EOS_DevAuthTool.exe"' }
`
Wait until the user has interacted with the opened EOS_DevAuthTool window (e.g. to log in, accept scopes, or configure credentials) before trying to use it for authentication.

#### 2. Building the Project
To compile the C++ code and binaries for the editor (e.g. when editor is closed, to prevent out-of-date binaries preventing launch):
`powershell
Start-Process -FilePath "C:/Program Files/Epic Games/UE_5.8/Engine/Build/BatchFiles/Build.bat" -ArgumentList "AgentFrameworkTestEditor", "Win64", "Development", '"C:/Users/janv1/Documents/Unreal Projects/AgentFrameworkTest/AgentFrameworkTest.uproject"', "-WaitMutex" -Wait -NoNewWindow
`

#### 3. Launching the Unreal Editor
> [!IMPORTANT]
> **Windows Path Escaping Rule**: Always use forward slashes (/) in path strings or use the launch_editor.ps1 helper script. Never include a trailing backslash inside double-quoted paths ("C:\Path\"), as Windows parses \" as an escaped quotation mark, corrupting command line arguments.

##### Recommended: Safe Launcher Script
`powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/janv1/Documents/Unreal Projects/UE-Antigravity/UnrealEngine/src/launch_editor.ps1" -ProjectPath "C:/Users/janv1/Documents/Unreal Projects/AgentFrameworkTest/AgentFrameworkTest.uproject"
`

##### Direct Launch (Forward Slashes)
`powershell
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = '"C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/janv1/Documents/Unreal Projects/AgentFrameworkTest/AgentFrameworkTest.uproject"' }
`

##### Multiplayer / EOS Launch
`powershell
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = '"C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/janv1/Documents/Unreal Projects/AgentFrameworkTest/AgentFrameworkTest.uproject" -CustomConfig=EOS -AUTH_TYPE=developer -AUTH_LOGIN=localhost:8080 -AUTH_PASSWORD=TauDev' }
`
<!-- LOCAL_ENV_END -->

## 3. Coding Guardrails & Engine Invariants

### Strict Pointer & Lifecycle Safety
- **Data Asset Pointer Validation**: Always verify `IsValid()` or check against `nullptr` before dereferencing Data Asset pointers (e.g., `GunDataAsset->VisualizationAsset`, `Sprite->GetFName()`). Unassigned or broken references in `.uasset` files will hard-crash the editor, particularly in Mass ECS and Niagara subsystems.
- **Avoid Pointer Chaining (Early Init)**: Never chain pointer calls (e.g. `GetMatchInstance()->GetMapGridSize()`) without validating intermediate pointers. Subsystems or game states may be uninitialized during early lifecycle or standalone UI testing. Always provide fallback defaults when pointers are null.
- **UI Dynamic Hover & Synthetic Events**: Handlers receiving data asset pointers from UI events (e.g., `OnUpgradeSlotHovered`, `AreUnitAttributesMatchingUpgradeRequirements`) MUST verify the pointer before accessing properties. Slate synthetic mouse-move events frequently pass `nullptr` for unpopulated slots.

### Config & INI Serialization Rules
- **TMap Property Delimiters**: Unreal's `FMapProperty::ImportText_Internal` fails to parse multi-line `+MapKey=` entries. Multi-entry TMaps in `DefaultGame.ini` must be formatted on a single line using parentheses pairs:
  `MapProperty=((Key1,Val1),(Key2,Val2))`

## 4. Skills Directory
Read the corresponding file with your harness's native file-reading tool (`view_file` in Antigravity, `Read` in Claude Code, or equivalent) when performing these tasks:
- [blueprint-authoring](../blueprint-authoring/SKILL.md): Modifying `.uasset` blueprints (nodes, variables, formatting).
- [setup-replication](../setup-replication/SKILL.md): Network replication, RPCs, and RepNotify.
- [add-component](../add-component/SKILL.md): Declaring/attaching UActorComponents in C++.
- [setup-input](../setup-input/SKILL.md): Enhanced Input IMCs, Actions, and bindings.
- [niagara-authoring](../niagara-authoring/SKILL.md): Niagara VFX creation/modification.
- [unreal-testing-sops](../unreal-testing-sops/SKILL.md): Automated UI, performance testing, and PIE SOPs.
- [create-actor](../create-actor/SKILL.md): Boilerplate for new Actor/Pawn C++ classes.
- [create-interface](../create-interface/SKILL.md): Blueprint and C++ interface creation.
- [pie-verifier](../pie-verifier/SKILL.md): Play-In-Editor (PIE) state and viewport checks.




