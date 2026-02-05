---
name: gemini-context-bridge
description: Facilitates context sharing and strategic delegation between Claude Code and Gemini CLI. Syncs CLAUDE.md to GEMINI.md and provides agent selection guidance. Use when onboarding Gemini to a project, syncing instructions between agents, or deciding whether to use Claude or Gemini for a specific task.
allowed-tools: Read, Glob, Grep, Bash
---

# Gemini Context Bridge

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about GEMINI.md syntax:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific context topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

This skill bridges the gap between **Claude Code** and **Gemini CLI** by providing workflows to synchronize project context and strategic guidance on agent delegation. It ensures that project conventions defined in `CLAUDE.md` are understood by Gemini (via `GEMINI.md`) and helps users leverage the unique strengths of each agent.

## When to Use This Skill

**Keywords:** sync context, share memory, copy instructions, migrate context, bridge agents, gemini.md, claude.md, delegation strategy, agent selection

**Use this skill when:**

- **Onboarding Gemini:** You have a `CLAUDE.md` and want to initialize a `GEMINI.md` for Gemini CLI.
- **Syncing Instructions:** You want to ensure both agents follow the same coding styles and conventions.
- **Deciding Agent:** You are unsure whether to use Claude or Gemini for a specific task (e.g., "Who should run this migration?").
- **Comparing Context:** You want to see if there are conflicting instructions between the two agents.

## Delegation Strategy (Gemini vs Claude)

When orchestrating tasks, use this guide to choose the right agent:

### Delegate to **Gemini CLI** for

1. **Google Ecosystem Auth**: Tasks requiring authenticated access to GCP, Vertex AI, or Firebase.
2. **Long Context / Low Cost**: Operations best suited for Gemini Flash (large context) or Pro (very large context).
3. **Interactive Tools**: Running interactive CLIs (e.g., `top`, `vim`, `git rebase`) via `enableInteractiveShell`.
4. **Smart Edits**: Using the `edit` tool with the specific "Smart Edit" strategies of Gemini.
5. **Memory/Todos**: Utilizing the built-in programmable `save_memory` and `write_todos` tools for state tracking.

### Delegate to **Claude** for

1. **Project Planning**: High-level architectural reasoning and convention enforcement (`CLAUDE.md`).
2. **Complex Refactoring**: Codebase-wide changes requiring "Codebase Investigator" analysis.
3. **Initial Setup**: Creating the `CLAUDE.md` that serves as the seed for `GEMINI.md`.

## Workflows

### 1. Initialize GEMINI.md from CLAUDE.md

Use this to bootstrap Gemini's context using your existing Claude rules.

**Manual Steps:**

1. Read `CLAUDE.md`.
2. Extract key sections: "Conventions", "Build Commands", "Style Guide".
3. Create `GEMINI.md` with these sections formatted for Gemini (Markdown).

### 2. Check for Context Drift

Periodically check if the two context files have diverged.

**Manual Steps:**

1. `diff CLAUDE.md GEMINI.md` (or visually compare).
2. Look for updates in one that are missing in the other (e.g., new test command).

## File Formats

- **`CLAUDE.md`**: The single source of truth for Claude Code. Contains commands, style guides, and project structure.
- **`GEMINI.md`**: The context file for Gemini CLI. Used to prime the model with project-specific instructions.
- **`.gemini/settings.json`**: Configuration for Gemini (MCP, tools).
- **`.claude/config.json`** (if applicable): Configuration for Claude.

## Best Practices for "Partnership"

- **Single Source of Truth:** Ideally, treat `CLAUDE.md` as the master record for *project* rules.
- **Specialization:** Use `GEMINI.md` for Gemini-specific overrides (e.g., "Always use Flash model for this repo").
- **Shared Memory:** While they have separate memory stores, you can manually copy high-value facts from `save_memory` (Gemini) to `save_memory` (Claude).

## Test Scenarios

### Scenario 1: Context Sync

**Query**: "Sync my CLAUDE.md to GEMINI.md"
**Expected Behavior**:

- Skill activates on "sync context" or "copy instructions"
- Provides workflow to extract and transform sections
**Success Criteria**: User receives step-by-step sync workflow

### Scenario 2: Agent Selection

**Query**: "Should I use Claude or Gemini for this large file analysis?"
**Expected Behavior**:

- Skill activates on "claude or gemini" or "which agent"
- Provides delegation matrix guidance
**Success Criteria**: User receives recommendation based on task type

### Scenario 3: Context Drift Detection

**Query**: "Check if my CLAUDE.md and GEMINI.md are in sync"
**Expected Behavior**:

- Skill activates on "compare" or "drift"
- Suggests diff command and comparison workflow
**Success Criteria**: User receives drift detection method

## Related Skills

- `gemini-config-management`: For configuring the `.gemini` folder.
- `gemini-cli-docs`: For official documentation on `GEMINI.md` syntax.

## Version History

- v1.1.0 (2025-12-01): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release
