---
name: instruction-manager
description: "Manages and synchronizes AI instructions (global and project-level) across various tools (Gemini, Claude, Copilot, etc.). Use this skill when you need to: (1) Sync `templates/global-instructions/master.md` to all tool headers, (2) Generate or update `PROJECT_INSTRUCTIONS.md` in a directory, (3) Update sub-agent instructions, or (4) Maintain consistency in AI behavioral guidelines."
---

# Instruction Manager

Orchestrates the synchronization of instruction templates to ensure consistent AI behavior across different platforms and projects.

## Overview

The `instruction-manager` skill provides a unified workflow for maintaining the complex hierarchy of AI instructions used in this environment. It ensures that changes made to core principles in "Master" templates are correctly propagated to platform-specific configuration files.

## Workflow: Global Instruction Sync

Use this workflow when you update core behavioral principles in the master template.

1.  **Edit Master Template**: Modify `templates/global-instructions/master.md`.
2.  **Run Sync Script**:
    ```bash
    ./scripts/update-global-instructions.sh --system=all
    ```
    *   `--system`: `gemini`, `claude`, `copilot`, `opencode`, or `all`.
    *   `--dry-run`: Show what would be updated without making changes.
3.  **Verify Changes**: Check the target files (e.g., `gemini/.gemini/GEMINI.md`, `claude/.claude/CLAUDE.md`) to ensure the sync was successful.

## SECTION Syntax (Inclusion/Exclusion)

Use SECTION markers to include/exclude content for specific systems:

```markdown
<!-- SECTION:name:START:system1,system2 -->
Content for system1 and system2 only
<!-- SECTION:name:END -->

<!-- SECTION:name:START:!copilot -->
Content for all systems EXCEPT copilot
<!-- SECTION:name:END -->
```

- **Include list**: `copilot,claude` — only those systems see this block
- **Exclude prefix**: `!copilot` — all systems EXCEPT copilot see this block

Works in both global instructions (`templates/global-instructions/master.md`) and subagent masters (`templates/subagents/master/*.md`).

## Workflow: Project Initialization

Use this workflow when starting a new project or updating instructions for an existing one.

1.  **Generate Instructions**:
    ```bash
    ./scripts/generate-project-instructions.sh [path/to/project]
    ```
2.  **Update Existing**:
    ```bash
    ./scripts/generate-project-instructions.sh --update --force --set-technologies="React, TypeScript" .
    ```
    *   This generates `.claude/CLAUDE.md`, `.gemini/GEMINI.md`, and `AGENTS.md` based on `templates/PROJECT_INSTRUCTIONS.template.md`.

## Workflow: Sub-Agent Management

Use this workflow when modifying specialized sub-agent (Planner, Reviewer, etc.) behaviors.

1.  **Edit Agent Master**: Modify files in `templates/subagents/master/` (e.g., `planner.md`). Use SECTION markers for platform-specific content.
2.  **Sync Agents**:
    ```bash
    ./scripts/update-subagents.sh --agent=all --system=all
    ```
    *   `--agent`: `planner`, `reviewer`, `implementer`, `coordinator`, `prompt-creator`, or `all`.
    *   `--system`: `copilot`, `opencode`, `claude`, or `all`.
    *   `--dry-run`: Show what would be updated without making changes.
3.  **Validate Sync**:
    ```bash
    ./scripts/validate-subagents.sh
    ```

## Reference: Instruction Hierarchy

| Level | Source of Truth | Target Files | Script |
| :--- | :--- | :--- | :--- |
| **Global** | `templates/global-instructions/master.md` | `gemini/.gemini/GEMINI.md`, etc. | `update-global-instructions.sh` |
| **Project** | `templates/PROJECT_INSTRUCTIONS.template.md` | `.claude/CLAUDE.md`, `AGENTS.md`, etc. | `generate-project-instructions.sh` |
| **Sub-Agents** | `templates/subagents/master/*.md` | `claude/.claude/agents/*.md`, etc. | `update-subagents.sh` |

## Resources

### scripts/
The skill leverages the following root-level scripts:
- `update-global-instructions.sh`: Syncs global master to platform headers.
- `generate-project-instructions.sh`: Scaffolds project-specific context.
- `update-subagents.sh`: Populates sub-agent instruction files.
- `validate-subagents.sh`: Checks consistency between agent platforms.

### references/
- `templates/global-instructions/metadata.json`: Defines target paths and header requirements for each tool.
- `templates/subagents/master/METADATA.json`: Defines agent names, descriptions, and platform-specific overrides.