---
name: subagent-orchestrator
description: "Manages the lifecycle, configuration, and synchronization of specialized sub-agents (Planner, Implementer, Reviewer, etc.) across various platforms (Claude, Copilot, OpenCode). Use this skill when you need to: (1) Sync sub-agent instructions from master templates, (2) Add new sub-agent definitions, (3) Update agent capabilities or permissions, or (4) Validate that agent instructions are in sync across platforms."
---

# Sub-Agent Orchestrator

Manages the specialized AI agents that form the core of this engineering environment.

## Overview

Specialized sub-agents are defined in master templates and then projected into tool-specific configurations. This skill ensures that your Planner, Implementer, Reviewer, and other agents remain consistent and highly capable regardless of the platform they are running on.

## Workflow: Syncing Sub-Agents

Use this when you have modified a master template or the global metadata.

1.  **Run Sync Command**:
    ```bash
    ./scripts/update-subagents.sh --agent=all --system=all --force
    ```
    *   `--agent`: `planner`, `reviewer`, `implementer`, `coordinator`, `prompt-creator`, or `all`.
    *   `--system`: `copilot`, `opencode`, `claude`, or `all`.
2.  **Verify Synchronization**:
    ```bash
    ./scripts/validate-subagents.sh
    ```
    *   This ensures that the content (excluding headers) is identical between different system implementations.

## Workflow: Adding a New Sub-Agent

1.  **Create Master Template**: Create `templates/subagents/master/<agent-name>.md` with the core behavioral instructions.
2.  **Register in Metadata**: Add the agent's entry to `templates/subagents/master/METADATA.json`.
    *   Define `name`, `description`, and `examples`.
    *   Specify `header_lines` for each target system.
3.  **Initialize Across Systems**:
    ```bash
    ./scripts/update-subagents.sh --agent=<agent-name> --system=all --force
    ```

## Reference: Agent Structure

| Agent | Core Purpose | System Targets |
| :--- | :--- | :--- |
| **Planner** | Architecture & planning (no code) | Claude, Copilot, OpenCode |
| **Implementer** | Feature building & refactoring | Claude, Copilot, OpenCode |
| **Reviewer** | Bug hunting & quality audit | Claude, Copilot, OpenCode |
| **Coordinator** | Multi-phase project management | OpenCode |
| **Prompt Creator** | Prompt engineering for agent chains | OpenCode |

## Resources

### scripts/
- `update-subagents.sh`: The primary engine for projecting master templates into configuration files.
- `validate-subagents.sh`: A consistency checker that identifies drifts between platforms.
- `extract-to-master.sh`: (Utility) Used for reverse-syncing if a change was made directly to a target file.

### references/
- `templates/subagents/master/METADATA.json`: The "Source of Truth" for agent names, descriptions, examples, and permission overrides.
- `templates/subagents/master/*.md`: The master behavioral templates.
- `templates/subagents/headers/*.template`: Header structures for different tools.