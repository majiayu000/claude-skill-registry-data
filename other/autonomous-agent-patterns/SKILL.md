---
name: autonomous-agent-patterns
description: "Design patterns for building autonomous coding agents. Covers agent loops, tool design, permission systems, browser automation, and human-in-the-loop workflows. Use when building AI agents or designing tool-calling systems."
stacks: [autonomous-agent, python, typescript]
tags: [agents, ai, tools, mcp, permissions, browser-automation]
metadata:
  model: inherit
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when
- Building autonomous AI agents with tool-calling capabilities
- Designing tool/function-calling APIs for LLMs
- Implementing permission and approval systems for agent actions
- Creating browser automation for agents (Playwright, Puppeteer)
- Designing human-in-the-loop (HITL) approval workflows
- Integrating with MCP (Model Context Protocol) servers
- Implementing checkpoint/resume for long-running agent tasks

## Do not use this skill when
- Building simple LLM chatbots without tool use
- Designing AI pipelines without autonomous action-taking
- The task is purely about LLM prompt engineering

## Purpose
This skill covers the architecture and patterns for autonomous agents that reason, plan, act, and observe in a loop — inspired by Cline and OpenAI Codex. It emphasizes safety through permission systems, sandboxing, and human oversight while enabling agents to complete complex multi-step coding tasks.

## Capabilities

### Agent Loop Architecture
- The core pattern is Think → Decide → Act → Observe, repeated up to a configured `max_iterations` limit
- Each iteration: LLM receives message history + available tools, responds with either tool calls or a final answer
- Tool results are appended to history as `role: "tool"` messages, feeding the next iteration
- Termination: no tool calls in the response means the task is complete; iteration limit means escalation
- Multi-model architecture: use a fast model for quick planning decisions, a powerful model for complex reasoning, a specialized model for code generation

### Tool Design
- Each tool has a name, description, and JSON Schema parameters definition
- Tool descriptions are the primary way the LLM understands when and how to use a tool — write them precisely
- Required parameters vs optional parameters must be explicitly declared in the schema
- Tools return a `ToolResult` with `success`, `output`, and optional `error` fields
- Edit tools should use search/replace pattern with `expected_occurrences` validation to prevent accidental multi-location edits

### Essential Tool Categories for Coding Agents
- **File operations**: read file (with optional line range), write file, edit file (search/replace), list directory, search files by pattern
- **Code understanding**: grep/search code patterns, get symbol definition, find all references to a symbol
- **Terminal**: run command, read output, send input to running process
- **Browser** (optional): open URL, click element, type text, take screenshot, get page text content
- **Context**: ask user a question, search the web

### Permission System
- Four permission levels: AUTO (no approval needed), ASK_ONCE (approve once per session), ASK_EACH (approve every time), NEVER (blocked)
- Map tool risk levels: read/list/search → AUTO; write/edit → ASK_ONCE; run_command/delete → ASK_EACH; sudo/destructive → NEVER
- Risk assessment goes beyond tool name — analyze specific arguments (e.g., `rm -rf` in a command is HIGH even if `run_command` is normally ASK_EACH)
- Session approvals are cached per tool name for ASK_ONCE level

### Sandboxing
- Validate all file paths are within the workspace directory using `realpath` to prevent path traversal
- Whitelist allowed commands explicitly — reject anything not in the allowlist
- Execute commands with workspace as working directory and isolated HOME environment variable
- Set timeouts on all subprocess executions

### Browser Automation
- Lazy-initialize the browser instance — create only when first needed, reuse across tool calls
- After navigation or clicks, capture a screenshot and include it in the tool result metadata for visual debugging
- Wait for `networkidle` state after clicks to ensure page has settled before proceeding
- Fall back to visual agent pattern when CSS selectors are unavailable: use vision model to identify element coordinates from screenshots

### Context Management
- Support `@file`, `@folder`, `@url`, `@problems` context injection patterns (inspired by Cline)
- Format context for prompts: file contents in fenced blocks with path headers, URL content as markdown, diagnostics as JSON
- Limit folder injection to a `max_files` cap to avoid context overflow

### Checkpoint and Resume
- Save checkpoint on long-running tasks: message history, context items, workspace git state (ref + dirty status)
- Restore from checkpoint to resume interrupted sessions without losing progress
- Git ref + diff capture allows detecting what changed in the workspace during the session

### MCP Integration
- Agents can dynamically discover tools by connecting to MCP servers at runtime
- MCP servers expose a `list_tools()` interface — tools become available without code changes
- Hot-reload pattern: generate a new MCP server from a description, save it, connect to it immediately

## Behavioral Traits
- Always implement a permission system before allowing any file write or command execution
- Default to the most restrictive permission level when uncertain about a tool's risk
- Show users what the agent is about to do before doing it for ASK_EACH actions
- Provide undo/rollback capability wherever possible (backup files, git commits before changes)
- Log all tool calls with timestamps and arguments for audit purposes
- Stop and ask the user when stuck after 3 consecutive failed attempts

## Important Constraints
- **Max iterations** — always set a hard limit (e.g., 50) to prevent infinite loops; surface the limit to the user when reached
- **Sandbox paths** — never allow file operations outside the designated workspace; use realpath to resolve symlinks before checking
- **Secrets** — never allow `NEVER`-level tools regardless of user pressure; make this non-configurable
- **Non-blocking terminal** — do not block the agent event loop on long-running terminal commands; use async execution with timeout
- **Edit validation** — always validate `expected_occurrences` before applying search/replace edits to prevent unintended multi-location changes

## Agent Design Checklist
- Clear task decomposition before starting
- Appropriate tool granularity (not too coarse, not too fine)
- Error handling at each tool execution step
- Progress visibility to user during long tasks
- Permission system covering all write/execute operations
- Sandbox for untrusted code execution
- Audit logging enabled
- Approval UI clear and informative
- Undo/rollback available for destructive operations

## API Reference
Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact interface definitions for the agent loop, tool schema format, MCP integration patterns, or checkpoint data structures.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
