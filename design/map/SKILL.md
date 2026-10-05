---
name: map
description: "Scan project structure and generate ARCHITECTURE.md with a Mermaid module relationship diagram. Use when user says \"/map\"."
---

# Clade for Codex

This workflow runs **directly in Codex**. Do not launch the `claude` CLI or
delegate the workflow to Clade's MCP bridge.

Codex compatibility rules:

- Plugin skills are namespaced. Invoke this workflow explicitly as
  `$clade:map`; a bare `$name` does not select the installed Clade plugin.
- Read the nearest `AGENTS.md` files for repository instructions. If a project
  has only `CLAUDE.md`, treat it as legacy project guidance and read it too.
- Store new Clade working state under `.clade/` (or `~/.clade/` for personal
  state). Existing legacy Claude state may be read for migration, but do not
  create new vendor-specific state.
- A `/skill-name` reference means the corresponding Codex
  `$clade:skill-name` plugin skill, or the same workflow invoked naturally when
  explicit skill invocation is not available.
- Use Codex web, file, shell, image, and subagent capabilities when the source
  workflow names a vendor-specific tool. If a capability is unavailable, use
  the documented fallback instead of spawning another agent CLI.
- Paths such as `<plugin-root>/...` are relative to the installed Clade plugin
  containing this `SKILL.md`; resolve that root before invoking a helper.

## Canonical Clade workflow

# /map Skill: Generate Project Architecture Diagram

## Purpose
Automatically scan the project structure and generate `ARCHITECTURE.md` with a module relationship diagram using Mermaid.

## Execution Steps

1. **Read existing ARCHITECTURE.md**
   - If `ARCHITECTURE.md` exists at the project root, read it first
   - This helps preserve any existing documentation and allows you to update rather than overwrite

2. **Scan project structure**
   - Use Glob to find major directories: `find . -maxdepth 2 -type d -not -path '*/\.*' -not -path '*/node_modules/*' -not -path '*/__pycache__/*'`
   - For each top-level directory (src/, lib/, app/, components/, etc.), identify:
     - What it contains (modules, libraries, features)
     - Its primary responsibility
     - Key files or sub-modules within it

3. **Identify modules and dependencies**
   - Scan key files with Grep/Read to understand module structure
   - Map logical dependencies (imports, API calls, shared state)
   - Identify which modules depend on which others
   - Look for: package.json, setup.py, .go files, main entry points

4. **Generate Mermaid diagram**
   - Create a `graph TD` (top-down) Mermaid diagram showing:
     - Each major module as a node (use clear, short names)
     - Arrows showing dependencies: `ModuleA --> ModuleB` means ModuleA imports/uses ModuleB
     - Group related modules if they form a subsystem
   - Keep the diagram readable (max ~10-15 nodes for clarity)
   - Example structure:
     ```
     graph TD
       API["API Layer"]
       DB["Database"]
       Auth["Authentication"]
       UI["Frontend"]

       UI --> API
       API --> Auth
       API --> DB
       Auth --> DB
     ```

5. **Write ARCHITECTURE.md**
   - Create or update `ARCHITECTURE.md` at the project root
   - **Structure**:
     ```markdown
     # Project Architecture

     ## Overview
     [1-2 sentence high-level description of what the project does]

     ## Directory Structure

     ### src/
     [Description of what this directory contains]
     - Key files: file1.ts, file2.ts

     ### lib/
     [Description]
     - Key files: ...

     [... repeat for each top-level directory ...]

     ## Module Relationships

     ```mermaid
     [Your generated Mermaid graph]
     ```

     ## Key Components

     ### Module Name
     - **Location**: src/module/
     - **Responsibility**: What this module does
     - **Exports**: Key functions/classes
     - **Depends on**: Other modules it uses

     [... repeat for each major module ...]

     ## Data Flow
     [Optional: describe how data flows through the system, if applicable]
     ```
   - Keep descriptions concise (1-3 lines per section)
   - Focus on "why" not "what" — what problem does each module solve?

6. **Report success**
   - Tell the user: "Updated ARCHITECTURE.md"
   - If the diagram is complex, add a note about what the diagram shows

## Implementation Notes

- **Diagram scope**: Show the 5-10 most important modules, not every single file
- **Avoid noise**: Don't include vendored code (node_modules, venv, .git)
- **Update strategy**: If ARCHITECTURE.md exists, preserve existing descriptions and update the diagram + file list
- **Language**: Use English for all documentation
- **Mermaid syntax**: Use valid Mermaid graph TD syntax; test the diagram visually if possible

## Success Criteria

✓ ARCHITECTURE.md exists at project root
✓ Diagram renders without syntax errors
✓ All major modules are represented
✓ Dependencies are correctly shown
✓ Descriptions are clear and concise


---

## Completion Status

- ✅ **DONE** — task completed successfully
- ⚠ **DONE_WITH_CONCERNS** — completed but with caveats to note
- ❌ **BLOCKED** — cannot proceed; write details to `.clade/blockers.md`
- ❓ **NEEDS_CONTEXT** — missing information; use AskUserQuestion

**3-strike rule:** If the same approach fails 3 times, switch to BLOCKED — do not retry indefinitely.

## Delivery completion

If this workflow changes files or external state:

- Inspect the real final state before responding, including `git status` for a
  repository task.
- Never report `DONE` while task-owned changes are uncommitted. Use or continue
  `$clade:delivery` and create a repository-compliant checkpoint or preserve
  the work when committing is unavailable.
- When the user request or trusted repository policy makes publication,
  deployment, or live verification part of the task, do not silently downgrade
  the result to local-only work.
- If a required delivery transition lacks authority, credentials, a destination,
  or reachable external state, report `BLOCKED` or `NEEDS_CONTEXT` rather than
  appending a "not committed/pushed/deployed" caveat after `DONE`.
