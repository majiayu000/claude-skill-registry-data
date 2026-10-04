---
name: refactor-builtin-tool
description: Guide and principles for refactoring built-in MCP tools in LibrAgent. Use this skill when reviewing, refactoring, or optimizing existing built-in tools to reduce AI cognitive load, eliminate internal callback tool exposure, consolidate redundant tools, and ensure strict state synchronization across the system.
---

# Built-in Tool Refactoring Guide

## When to Use This Skill

Use this skill when:

- Refactoring existing built-in MCP tools in LibrAgent.
- Reviewing tools that cause AI context bloat or "cognitive overload".
- Consolidating redundant or overlapping tools (e.g., `exportFile` and `exportZip`).
- Fixing issues where internal callback tools are exposed to the AI agent.

## Core Design Principles

### 1. Context Economy & Cognitive Load

AI agents operate within strict context limits. Every exposed tool consumes tokens and attention.

- **Hide Internal Callbacks:** Never expose internal system callbacks or UI triggers (e.g., `resumeFromWait`, `getUserAnswer`, `circuitBreak`) to the `all_tools()` export. The backend router (`call_tool`) can handle these without the AI needing to know they exist.
- **Concise Descriptions:** Keep tool descriptions brief. Avoid paragraphs of prerequisites or error-handling advice. The schema itself should document parameters.
- **Progressive Disclosure:** For discovery tools (like `listTools`), provide a compact summary (names only) when queried broadly. Show detailed schemas only when a specific, narrowed query is provided.

### 2. Consolidation & Auto-Switching

Reduce the sheer number of tools by combining highly similar operations into a single tool with smart, data-driven behavior.

- **Merge Sibling Tools:** Combine tools that achieve the exact same goal (e.g., merging `exportFile` and `exportZip` into a single `export` tool that accepts an array of paths).
- **Data-Driven Logic:** Let the backend determine the execution mode (e.g., if one file is passed -> export raw; if multiple files -> export as ZIP). The AI shouldn't have to make micro-decisions about file counts or formats.

### 3. Strict Synchronization & State Integrity

Data integrity must be guaranteed at the backend level.

- **Synchronous Verification:** Whenever a tool or configuration is created or updated, the system must verify its validity synchronously _before_ committing it to the database.
- **Backend as Source of Truth:** Do not rely on the frontend to fire asynchronous validation events. If an entity is in the database, it must be verified and operational.
- **No "Ghost" Entities:** If a registered entity (like an external MCP server) lacks a cache due to a transient failure, it must still be visible in tool listings with an appropriate warning, rather than being silently filtered out.

### 4. Don't Repeat Yourself (DRY) in Integration

Built-in tools should leverage central architectures.

- **Use Central Managers:** Reuse central components like `MCPServerManager` or `McpServerService::verify_config` instead of writing raw `tokio::process::Command` or HTTP clients inside specific tool handlers.
- **Single Source of Validation:** Formulate validation logic in the core service layer and reuse it across UI endpoints, tool handlers, and agent routines.

### 5. Cross-Platform UX Considerations

- **Process Stealth:** On Windows, always apply the `CREATE_NO_WINDOW` flag (`0x08000000`) when spawning background or verification processes via `std::os::windows::process::CommandExt` to prevent distracting terminal flashes.

## Refactoring Workflow

1. **Audit `tools.rs`:** Identify all tools exported via `all_tools()`. Remove any tool that is strictly an internal callback.
2. **Review Descriptions:** Condense verbose descriptions in `MCPTool` definitions.
3. **Consolidate Sibling Tools:** Check for tools with similar prefixes (e.g., `read_foo`, `read_bar`) and combine them if their core intent is identical.
4. **Check Handlers:** Ensure handlers use central service functions instead of duplicating connection/execution logic.
5. **Verify State Updates:** Ensure any DB mutations happen _after_ successful synchronous verification.
