---
name: "branch-docs-sync"
description: "Synchronize project documentation with recent code changes, refactors, and feature implementations in the current branch."
compatibility: "Requires a git repository with standard documentation structure (DEVNOTES, docs/site, README, etc.)"
metadata:
  author: "openRender-bot"
  version: "1.0.0"
---

## Objective
Update and maintain documentation consistency by analyzing recent git commits and applying surgical updates across developer notes, user-facing site content, and system manual pages.

## Workflow

### 1. Research & Analysis
- **Identify Range**: Determine the set of commits to analyze. If not specified, analyze all commits unique to the current feature branch.
- **Extract Changes**: Use `git log -n 10` and `git show <sha>` for key commits to identify:
    - **Architectural Refactors**: Renames of subsystems, directories, or core libraries.
    - **New Features**: Added RIB statements, new shaders, or expanded language bindings.
    - **Breaking Changes**: Changed environment variables, tool names, or API signatures.
    - **Fixed Bugs**: Resolved issues that require updating the status in `BUGS.md` or `DEVNOTES.md`.

### 2. Update Developer Notes (`DEVNOTES.md` & `DEVNOTES_DETAILS/**`)
- **Project Status**: Update the "Project Status" table in the main `DEVNOTES.md`.
- **Major Refactors**: Add a bullet point to the "Recent Major Refactors" section summarizing systemic changes.
- **Detail Files**:
    - Update `OSHADER_UPDATES.md` for compiler or shading language changes.
    - Update `BINDINGS_GUIDE.md` for Python/Lua/C++ interface changes.
    - Update `FRAMEBUFFER_GUIDE.md` for display driver or IPC changes.
    - Create new detail files (e.g., `RIB_GUIDE.md`) for significant new subsystems.

### 3. Update Site Documentation (`docs/site/content/**`)
- **Branding & Consistency**: Perform batch updates for project name (e.g., "Pixie" -> "openRender") or environment variables (e.g., `PIXIEHOME` -> `ORENDERHOME`).
- **URL Routing**: Ensure internal links and file names match the new branding or tool names.
- **Tooling References**: Update command-line examples to reflect tool renames (e.g., `sdrinfo` -> `rsloinfo`).

### 4. Update Distribution & Release Files
- **README.md**: Refresh the directory structure overview and installation requirements.
- **INSTALL_ARTIFACTS.md**: Update the list of installed binaries and libraries.
- **NEWS.md & ChangeLog.md**: Add dated entries summarizing the new capabilities and refactors.
- **Build Templates**: Update Homebrew (`.rb.template`) or RPM (`.spec`) files to ensure they package the new artifacts.

### 5. Update Manual Pages (`man/**`)
- **Rename**: If a tool has been renamed, rename the corresponding `.1` file.
- **Content**: Update the usage synopsis and descriptions to match the current implementation.

## Key Rules
- **Preserve Case**: When performing batch renames (e.g., "pixie" -> "openrender"), respect the casing of the original string.
- **Surgical Edits**: Use targeted `replace` calls with enough context to avoid ambiguous matches.
- **Audit**: After updates, run a `grep_search` for the old terms (e.g., "sdr", "Pixie") to ensure no stale references remain in active documentation.
- **Confirmation**: Present a summary of all documentation changes to the user for final approval.

## Verification
- Validate that all internal markdown links are functional.
- Ensure the `ChangeLog.md` follows the project's established format.
- Verify that the `INSTALL_ARTIFACTS.md` accurately reflects the current `CMakeLists.txt` configuration.
