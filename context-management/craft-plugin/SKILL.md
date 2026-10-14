---
name: craft-plugin
description: The Architecture of the Cognitive OS.
---

# Skill: Craft Plugin (Architecture)

> "The Brain, The Muscles, The Voice."

## 1. The Principles
This is not a "plugin". It is a **Cognitive Operating System**.

3.  **The Reflexes (Hooks)** (`hooks/hooks.json`):
    *   **Concept**: The Subconscious. These run automatically.
    *   **Context Injection**: Only `SessionStart`, `UserPromptSubmit`, and `Setup` inject stdout to Claude. Other hooks need JSON output.
    *   **Memory**: Use `SessionStart` to inject the `working.md` context.
    *   **Details**: See `craft-hook` for injection rules and patterns.

*   **The Brain (Memory)**: `$CLAUDE_MEMORY_DIR/working.md` (default: `.claude/memory/`). Mutable Context.
*   **The Muscles (Agents)**: `agents/`. (Execution Roles).
*   **The Voice (Commands)**: `commands/`. (Triggers).
*   **The Knowledge (Skills)**: `skills/`. (Atomic Components).

## 2. The Implementation
*   **Official Spec**: Use `claude-code-guide` agent to query plugin structure and `plugin.json` schema.
*   **Hooks Spec**: Use `claude-code-guide` agent to query hook events and actions.

## 3. Self-Evolution
To extend this system, use the specific meta-skills:
*   To add knowledge: `craft-skill` (Remember Registration!)
*   To add a worker: `craft-agent`
*   To add a trigger: `craft-command`
*   To add a reflex: `craft-hook`
