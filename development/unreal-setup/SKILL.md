---
name: unreal-setup
description: One-time setup skill to scan the Unreal Engine project, configure the local environment in unreal-instructions, and compile a permanent OKF project-index skill.
---
# Unreal Engine Project Setup and Indexing SOP

This skill guides the AI agent to perform a comprehensive project scan, generate machine-specific local environment configuration, and create a sophisticated indexing skill (`project-index`) in OKF format under the workspace customizations root.

## Execution Procedure

When the user asks to "run project setup", "initialize project", or "setup conversation", follow the planning, task initialization, and sequential execution procedure below.

### Step 0: Research, Diagnose, and Plan

Before executing or implementing any setup steps, you must perform a diagnostic check, create an implementation plan, obtain user approval, and initialize a task list.

1. **Perform Setup Diagnostic Check**:
   Evaluate the current project state to identify what is already completed and what remains to be done:
   - **Check for LLVM/Clang**: Check if `libclang.dll` can be resolved via the registry, standard standalone-installer paths (e.g., `C:\Program Files\LLVM\bin\libclang.dll`), or a Visual Studio / Visual Studio Build Tools "C++ Clang tools for Windows" component install (see Step 1).
   - **Check for Git and Git LFS**: Verify that `.git` exists, and that `.gitattributes` tracks `*.uasset` and `*.umap` via Git LFS.
   - **Check for agent plugin installation**: Check if the folder `.agents/plugins/UnrealEngine` exists.
   - **Check for compilation database**: Check if `compile_commands.json` exists in the game project directory.
   - **Check for local environment configuration**: Check if local environment paths are already configured inside `unreal-instructions/SKILL.md`.
   - **Check for C++ AST database cache**: Check if `ast_cache.db` exists in the external server directory and contains indexed symbol tables.
   - **Check for project index skill**: Check if `.agents/skills/project-index/SKILL.md` and references under `references/` exist.
   - **Check for AGENTS.md**: Check if `.agents/AGENTS.md` is present and configured at the workspace root.

2. **Create Implementation Plan**:
   Present an implementation plan using your harness's native planning mechanism (in Antigravity: an `implementation_plan.md` artifact in the artifact directory `<appDataDir>\brain\<conversation-id>` with `request_feedback: true` and `user_facing: true` in the metadata; in Claude Code: plan mode or a plain plan message in the conversation; in other harnesses: a plan message).
   - Detail the findings of your diagnostic check.
   - Present a clear markdown checklist of the setup steps, marking already-completed steps as `[x]` and pending steps as `[ ]`:
     - `[ ] Step 1: Verify LLVM/Clang installation`
     - `[ ] Step 1.5: Verify Git & Git LFS configuration`
     - `[ ] Step 2: Install Python dependencies (ChromaDB, ONNX runtime, PyPDF)`
     - `[ ] Step 3: Install agent plugin dependencies (Run install.ps1)`
     - `[ ] Step 4: Generate compilation database (compile_commands.json)`
     - `[ ] Step 5: Update/Refresh local environment in unreal-instructions`
     - `[ ] Step 6: Verify C++ AST caching & Vector DB indexing`
     - `[ ] Step 7: Full Workspace Scanning (uproject, configs, assets)`
     - `[ ] Step 8: Create OKF project-index skill & references`
     - `[ ] Step 9: Append workspace rules and game description to AGENTS.md`
   - Explicitly request feedback/approval for the proposed setup plan and **STOP** to wait for the user's approval.

3. **Initialize Task List**:
   Once the user approves the implementation plan:
   - Create a task list using your harness's native task-tracking mechanism (in Antigravity: a `task.md` artifact in the artifact directory; in Claude Code: the built-in task/todo list; otherwise: a `task.md` file in the workspace).
   - The task list MUST contain **exactly one task per pending setup step** (e.g., one task for Step 1, one task for Step 2, etc., based on what still needs to be executed).

4. **Sequential Execution & Summarization Protocol**:
   Address the tasks in `task.md` one by one:
   - **CRITICAL**: Before executing any commands or editing files for a step, output a clear, user-visible summary explaining what you are about to execute.
   - Perform the step's actions.
   - Upon successful completion (or failure) of the step, mark the corresponding task as completed (or in progress/failed) in the task list before moving to the next task.
   - If a step fails, stop execution and report the error to the user.

### Step 1: Verify LLVM/Clang Installation
1. The external AST server (`resolve_and_load_libclang` in `ExternalServer/src/main.py`) auto-detects `libclang.dll` from several sources, in order: the `LIBCLANG_PATH`/`LLVM_PATH` environment variables, the standalone LLVM installer's registry key, Unreal Engine's bundled IWYU copy, a **Visual Studio / Visual Studio Build Tools "C++ Clang tools for Windows" component install** (discovered dynamically via `vswhere.exe`, so any edition — Community, Professional, Enterprise, or Build Tools without the full IDE — is picked up automatically), hardcoded standalone-installer paths, and finally `PATH`.
2. To check whether detection will succeed without starting the server, run `vswhere.exe` yourself and inspect the result:
   ```powershell
   & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -products * -property installationPath
   ```
   Then check whether `VC\Tools\Llvm\x64\bin\libclang.dll` (or `VC\Tools\Llvm\bin\libclang.dll`) exists under any returned installation path, or check the standalone paths (`C:\Program Files\LLVM\bin\libclang.dll`, `C:\Program Files (x86)\LLVM\bin\libclang.dll`).
3. If `libclang.dll` cannot be found anywhere:
   - Recommend the user open the **Visual Studio Installer**, modify their installation, and check **C++ Clang tools for Windows** under the Desktop C++ workload (works for both the full IDE and Build Tools-only installs) — since Visual Studio is already required to build Unreal Engine, this is usually a single checkbox away.
   - Alternatively, ask the user to install standalone LLVM/Clang (e.g., by running `winget install LLVM.LLVM` in a new terminal window) OR to provide the absolute path to `libclang.dll` on their system.
   - If the user provides a custom path, save it by writing `LIBCLANG_PATH` to the `unreal-instructions` skill under local environment configuration so the external server can find it.
   - Do NOT proceed to compile commands or indexing until LLVM/Clang is verified as available.

### Step 1.5: Verify Git & Git LFS Configuration
1. **Verify Git and Git LFS tracking**:
   - Run `git status` or check for a `.git` folder to verify version control.
   - Run `git lfs env` to verify Git LFS is active, and check `.gitattributes` to verify `*.uasset` and `*.umap` are tracked.
2. **If Git or Git LFS is missing**:
   - Inform the user that the plugin strictly requires a Git repository with Git LFS for tracking Unreal Engine binaries to prevent corruption.
   - Recommend hosting the project on **GitLab**, as their free tier offers a significantly higher Git LFS storage quota compared to GitHub.
   - Provide the user with an overview of the manual setup instructions:
     1. `git init`
     2. Add a `.gitignore` for UE (`Binaries/`, `Intermediate/`, etc.)
     3. `git lfs install` and track assets: `git lfs track "*.uasset"`, `git lfs track "*.umap"`
   - **Crucially**, ask the user if they would like you to automatically initialize Git and Git LFS for them.
   - If the user approves, automatically execute the following commands in the workspace root:
     ```powershell
     git init
     git lfs install
     git lfs track "*.uasset"
     git lfs track "*.umap"
     Add-Content -Path .gitignore -Value "Binaries/`nIntermediate/`nDerivedDataCache/`nSaved/" -Encoding UTF8
     git add .gitattributes .gitignore
     git commit -m "Configure Git LFS tracking for Unreal assets"
     ```

### Step 2: Install Python Dependencies (ChromaDB, ONNX runtime, PyPDF)
1. Verify Python is installed and located on the system path.
2. Install the required runtime dependencies using the system Python interpreter. **Note:** Since installing these packages may take time, you may delegate this step to a background sub-agent (e.g. `invoke_subagent` with the `self` role in Antigravity, or a background subagent/task in Claude Code) to execute the installation asynchronously; if your harness has no sub-agent mechanism, run the command directly:
   ```powershell
   & "python" -m pip install -r UnrealEngine/ExternalServer/requirements.txt --user
   ```
3. If the command fails, query the system registry or common installation directories to resolve the explicit path to `python.exe` and retry.

### Step 3: Install Agent Plugin Dependencies (Run install.ps1)
1. If `.agents/plugins/UnrealEngine` does not exist:
   - Run the installation script using default options by piping input:
     ```powershell
     echo "`n`n`n" | powershell -ExecutionPolicy Bypass -File UnrealEngine/install.ps1
     ```
   - Verify that `.agents/plugins/UnrealEngine` was created.

### Step 3.5: Verify Git Hooks Configuration
1. Run `git config core.hooksPath` to check the current hooks path.
2. If it is empty or not set to `.githooks`, configure it so the agent worktree hooks activate automatically:
   ```powershell
   git config core.hooksPath .githooks
   ```

### Step 4: Generate Compilation Database (compile_commands.json)
1. Trigger `compile_commands.json` generation. If the `cpp-ast-rag` MCP server tools are available, invoke `generate_compile_commands`.
2. Otherwise, run the Unreal Build Tool command directly in the shell:
   ```powershell
   # CRITICAL: Ensure "[Path to project directory]" does NOT end with a trailing backslash.
   # A trailing backslash before a closing quote (e.g. "C:\Path\") escapes the quote on Windows, corrupting the command line.
   & "[UnrealEnginePath]\Engine\Build\BatchFiles\Build.bat" -Mode=GenerateClangDatabase -Project="[Path to ProjectName.uproject]" [ProjectName]Editor Win64 Development -OutputDir="[Path to project directory]"
   ```
   (Resolve the actual paths dynamically based on your findings, ensuring no trailing backslashes are present).
3. Verify that `compile_commands.json` exists in the game project folder.

### Step 5: Update/Refresh Local Environment in unreal-instructions
1. Run the local environment generation script:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .agents/plugins/UnrealEngine/src/generate_env_skill.ps1
   ```
2. Verify that the local environment configuration has been successfully merged into `.agents/plugins/UnrealEngine/skills/unreal-instructions/SKILL.md`.

### Step 6: Verify C++ AST Caching & Vector DB Indexing
1. Ensure the `cpp-ast-rag` MCP server is running.
2. Query `query_cpp_ast` or wait for background indexing to complete.
3. Call `search_vector_db` with a query (e.g., "character movement") to verify that the vector database search works and returns documentation/code snippets.

### Step 7: Full Workspace Scanning
1. **Find and Parse UProject File**:
   - Locate the `*.uproject` file in the workspace root or parent folder (e.g., `[ProjectName]/[ProjectName].uproject`).
   - Read and parse it to extract:
     - Engine Association / Unreal Version
     - Modules (Name, Type, LoadingPhase)
     - Plugins (Name, Enabled, TargetPlatforms)
2. **Scan and Index All Project Files (Prompt Loop Protocol)**:
   - Run file-listing commands (e.g., `git ls-files` or standard filesystem utilities) to find all files in the project workspace. Ignore intermediate build/cache directories (like `.git`, `Binaries`, `Intermediate`, `DerivedDataCache`, `Saved`).
   - Identify all files to be indexed:
     - **C++ Source & Build Files (Mandatory)**: All `.h`, `.cpp`, `.hpp`, `.inl`, and `.cs` (module/target rules) files.
     - **Other Project Files (Mandatory if readable)**: Any other readable text-based project files, e.g., `.ini` (configs), `.json`, `.uproject`, `.md`, `.txt`, `.py`, `.sh`, `.ps1`, `.bat`.
   - **Execute the Indexing Prompt Loop**:
     - Do not attempt to process all files in a single assistant turn, as this will lead to truncation or incomplete indexing due to context limit constraints.
     - Split the target file list into manageable batches of 10 to 20 files.
     - For each batch, read the files using your harness's native file-reading tool (`view_file` in Antigravity, `Read` in Claude Code) to inspect their code or structure.
     - Maintain an active progress log tracking which files have been successfully scanned and which are pending (e.g., "Indexed 15/84 C++ files, 20/120 total files. Remaining: [...]").
     - Write the gathered indexing metadata (class declarations, key functions, purpose, and dependencies) to the files index reference file: `.agents/skills/project-index/references/files_index.md`.
     - **Self-Prompt Loop**: Write a message to yourself indicating the progress and the list of files to process next, prompting yourself to execute the next batch. Do not proceed to subsequent steps until every single C++ and other readable file in the project has been fully scanned and indexed.
3. **Inspect Configuration Files**:
   - Read key files in the `Config/` directory (e.g., `DefaultEngine.ini`, `DefaultInput.ini`, `DefaultGame.ini`).
   - Extract crucial project setup properties (like default game modes, maps, input keys, etc.).
4. **Discover Live Assets (If Unreal Editor is Running)**:
   - **Editor Online**: If the editor MCP server is active, query the active project assets. Search for the main GameMode, HUD, PlayerController, Character, and major UI widgets using `search_assets` and extract their package/asset paths.
   - **Editor Offline Fallback**: If the editor MCP server is not running or throws errors, do NOT fail the setup. Instead:
     - Scan the filesystem under `Content/` to locate primary Blueprint files.
     - Parse `DefaultEngine.ini` or log files to infer class configurations.
     - Document that live asset query was skipped (editor was offline) and note that the asset paths should be verified in a subsequent session.

### Step 8: Create the OKF Project-Index Skill

#### 1. Create Directories
Create the target skill directory and references subfolder under the workspace customizations root:
- Directory: `.agents/skills/project-index`
- References Directory: `.agents/skills/project-index/references`

#### 2. Generate Technical Documentation (References)
Create four detailed Markdown documentation files under `.agents/skills/project-index/references/`. 

*Note: As these are sub-documents inside the `references/` subdirectory, they do NOT contain YAML frontmatter.*

##### A. File: concepts.md
```markdown
# Project Concepts & Design Pillars

## Core Gameplay Fantasy
- **Overview**: [High-level summary of the game genre, narrative setting, and core player fantasy]
- **Design Pillars**:
  1. [Pillar 1: e.g., High-fidelity physics-based movement, tactical mechanics, etc.]
  2. [Pillar 2: e.g., Core gameplay loop design guidelines]
  3. [Pillar 3: e.g., Art style, visual identity, or performance constraints]

## Core Game Loop
1. [Core loop step 1: e.g., Initialization/Spawn phase]
2. [Core loop step 2: e.g., Active gameplay and session objective loop]
3. [Core loop step 3: e.g., Evaluation, scoring, or persistence updates]
```

##### B. File: gameplay.md
```markdown
# Gameplay Mechanics & UI Reference

## Core Pawns and Characters
- **Player Character**: `[Character Class]` ([Header Link](file:///absolute/path/to/header)) - Handles player input, basic states, and camera view.
- **AI Entities**: `[AI Class]` ([Header Link](file:///absolute/path/to/header)) - Implements custom logic or Behavior Trees for autonomous behaviors.

## Enhanced Input & Controls
- **Input Mapping Context (IMC)**: `[IMC Asset Name]` - Defines active hardware bindings.
- **Input Actions (IA)**:
  - `IA_Move`: Multi-axis input/movement logic.
  - `IA_Look`: Stick or mouse rotation mapping.
  - `IA_Interact`: Action or button mapping.

## UI & Widgets (UMG)
- **Main HUD**: `[HUD Widget Class]` - Displays user status, gauges, and overlays.
- **Menu Screens**: `[Widget Class]` - Game configuration or state transitions.
```

##### C. File: systems.md
```markdown
# Game Systems Architecture

## C++ Modules & Dependencies
- **[ModuleName]**: Primary module containing gameplay logic. List key engine modules it depends on.

## Core Subsystems
- **[SubsystemName]**: `[Subsystem Class]` - Manages session-wide states, network synchronization, or subsystem operations.

## Gameplay Systems
- **Simulation/VFX System**: Implements specialized simulation loops (e.g., MassEntity, Niagara, AI controllers).
- **Data Assets & Tables**:
  - **Data Definitions**: `[Asset/Table Name]` - Balances gameplay configurations, properties, or asset catalogs.
```

##### D. File: files_index.md
```markdown
# Project Files Index

This document provides a comprehensive index of all files in the project, mapping their paths, main declarations (classes, structs, functions), and design purposes.

## Source Code Directory (`Source/`)
- `[File Relative Path]` ([Link](file:///absolute/path/to/file))
  - **Summary**: Brief description of the file's role in the architecture.
  - **Declarations**: `Class/Struct/Enum` details, key methods, or variables.
  - **Dependencies**: Key headers included or modules referenced.

## Other Project Files
- `[File Relative Path]` ([Link](file:///absolute/path/to/file))
  - **Summary**: Purpose and brief configuration/script overview.
```

#### 3. Generate Project-Index Entry Point
Write the primary index file `.agents/skills/project-index/SKILL.md` using the following template, substituting the exact absolute file paths:

```markdown
---
name: project-index
description: Project structure, module index, and architecture map for the active Unreal Engine project.
---
# Unreal Project Index - [Project Name]

This skill is dynamically generated during project setup and provides a comprehensive index of the project's layout, modules, and key assets.

## Technical Documentation (OKF References)
Consult these detailed documentation files to understand the project architecture and systems:
- [Concepts & Design Pillars](file:///absolute/path/to/project-index/references/concepts.md)
- [Gameplay Mechanics & UI](file:///absolute/path/to/project-index/references/gameplay.md)
- [Game Systems Architecture](file:///absolute/path/to/project-index/references/systems.md)
- [Project Files Index](file:///absolute/path/to/project-index/references/files_index.md)

## Project Metadata
- **Project File:** [ProjectName.uproject](file:///absolute/path/to/ProjectName.uproject)
- **Engine Version:** [e.g., 5.7]
- **Target Platforms:** [e.g., Win64, Android, PS5]

## Active Modules & Plugins
### C++ Modules
- **[ModuleName]**: [Description / Purpose]

### Core Plugins
- **[PluginName]**: [Status/Description]

## Workspace Architecture Map
- **Source Code (`Source/`):** [Map out sub-folders and modules]
- **Assets (`Content/`):** [Map out primary asset folders, e.g., Blueprints, UI, Maps]
- **Plugins (`Plugins/`):** [Map out project-specific plugins]

## Principal Classes & Assets
### Core Gameplay Framework
- **Game Mode:** `[GameMode Class Name]` ([Path](file:///absolute/path/to/file))
- **Player Character:** `[Character Class Name]` ([Path](file:///absolute/path/to/file))
- **Player Controller:** `[Controller Class Name]` ([Path](file:///absolute/path/to/file))

### UI & Widgets (UMG)
- **Main HUD overlay:** `[Widget Class]` ([Asset Path](file:///absolute/path/to/asset))

### Core Systems & Data Assets
- **[System / Database]:** `[Class/Asset]` ([Path](file:///absolute/path/to/file))

## Developer Workflow & Scripts
- **Local Env Config:** Check [unreal-instructions SKILL.md](file:///absolute/path/to/unreal-instructions/SKILL.md)
- **Automation Scripts:** [e.g., run_tests.ps1, build_plugin.ps1]
```

### Step 9: Append Workspace Rules and Game Description (AGENTS.md)
Check if `.agents/AGENTS.md` exists at the project root.
- If it does not exist, copy `UnrealEngine/AGENTS.md` to `.agents/AGENTS.md`.
- If it does exist, inspect its contents. If the "Ponytail Ladder" or "Project Knowledge & Navigation" sections are already present, do NOT append. Otherwise, read the entire contents of `UnrealEngine/AGENTS.md` using your file-reading tool or `Get-Content`, and append the entire content to `.agents/AGENTS.md`. This ensures that all critical global instructions and efficiency rules are correctly applied to the workspace.

After setting up the workspace rules, extend `.agents/AGENTS.md` (or the copied file) by inserting a short and precise description of the game:
1. Check if a game description or summary is already created in the workspace (e.g., in the root `AGENTS.md` under a `## Game Summary` or `## Game Description` section, or in `.agents/skills/project-index/references/concepts.md` under `## Core Gameplay Fantasy - Overview`).
2. If such a description is found, format it nicely and insert it near the top of `.agents/AGENTS.md` under a `## Game Summary` section (if not already present).
3. If no description is found, generate a concise 2-3 sentence overview summarizing the game's core loop, genre, and key systems based on the indexed files (from `concepts.md` or from parsing the codebase), and insert it under a `## Game Summary` section in `.agents/AGENTS.md`.


### Step 10: Complete and Instruct User
1. Verify that `.agents/skills/project-index/SKILL.md` and all referenced markdown files under `.agents/skills/project-index/references/` have been written successfully.
2. **Track Index in Git**: Add the generated index files to git tracking so they are natively duplicated when creating worktrees:
   ```powershell
   git add .agents/skills/project-index/
   ```
3. Present a short 2-3 sentence summary of the project configuration to the user.
4. **IMPORTANT**: Instruct the user to restart their AI assistant session or reload the window. Explain that this is necessary because the assistant platform only scans, indexes, and loads workspace skills during conversation startup.
