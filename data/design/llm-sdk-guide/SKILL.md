---
name: llm-sdk-guide
description: U-llm-sdk and claude-only-sdk patterns. Use when working on projects with LLM service, designing LLM integrations, or implementing AI-powered features.
allowed-tools: ["Read", "Grep", "Glob"]
---

# LLM SDK Guide

Two SDKs for LLM integration:
- **U-llm-sdk**: Multi-provider (Claude, Codex, Gemini) with unified `LLMResult`
- **claude-only-sdk**: Claude-specific advanced features (agents, sessions, orchestration)

## Architecture: CLI-based (NOT API)

**IMPORTANT**: These SDKs wrap CLI tools, NOT direct API calls!

```
SDK Layer (Python)
    │
    ▼
asyncio.create_subprocess_exec()  ← Spawns CLI process
    │
    ▼
CLI Execution (e.g., `claude -p "prompt" --mcp-config ...`)
    │
    ▼
Separate Session with own context window
```

This enables:
- **MCP Isolation**: Each spawned process has its own MCP config (`--mcp-config`)
- **Context Separation**: Child process context doesn't pollute parent session
- **Session Independence**: Each call creates isolated Claude Code session

## U-llm-sdk Quick Start

```python
from u_llm_sdk import LLM, LLMConfig
from llm_types import Provider, ModelTier, AutoApproval

config = LLMConfig(
    provider=Provider.CLAUDE,
    tier=ModelTier.HIGH,
    auto_approval=AutoApproval.EDITS_ONLY,
)

async with LLM(config) as llm:
    result = await llm.run("Your prompt")
    print(result.text)
```

## claude-only-sdk Quick Start

```python
from claude_only_sdk import ClaudeAdvanced, SessionTemplate

async with ClaudeAdvanced() as client:
    result = await client.run_with_template(
        "Review src/auth.py",
        SessionTemplate.SECURITY_ANALYST,
    )
```

## MCP Isolation Pattern

Use `mcp_config` to run isolated sessions with specific MCP servers:

```python
from claude_only_sdk import ClaudeAdvanced, ClaudeAdvancedConfig

config = ClaudeAdvancedConfig(
    mcp_config="./config/serena.mcp.json",  # Only Serena MCP loaded
    timeout=300.0,
)

async with ClaudeAdvanced(config) as client:
    # This runs in separate session with only Serena MCP
    result = await client.run("Use Serena to analyze code")
```

This pattern is useful for:
- Keeping heavy MCP servers out of main session context
- Running specialized tools in isolated environments
- Reducing token usage in main conversation

## Core Components

### U-llm-sdk
| Component | Purpose |
|-----------|---------|
| `LLM` / `LLMSync` | Async/Sync clients |
| `LLMConfig` | Unified configuration |
| `BaseProvider` | Provider abstraction |
| `InterventionHook` | RAG integration protocol |

### claude-only-sdk
| Component | Purpose |
|-----------|---------|
| `ClaudeAdvanced` | Extended Claude client |
| `AgentDefinition` | Specialized agent config |
| `SessionManager` | Virtual session injection |
| `TaskExecutor` | Parallel task execution |
| `AutonomousOrchestrator` | Prompt-based parallelization |

## Key Patterns

### Provider Selection
```python
async with LLM.auto() as llm:  # Claude > Codex > Gemini
    result = await llm.run("prompt")
```

### Session Continuity
```python
llm = LLM(config).resume(session_id)
async with llm:
    result = await llm.run("Continue...")
```

### Agent Definition (Claude)
```python
planner = AgentDefinition(
    name="planner",
    system_prompt="You are a planning specialist...",
    tier=ModelTier.HIGH,
    allowed_tools=["Read", "Grep", "Glob"],
)
```

## Output Handling

```python
result: LLMResult
result.text              # Response text (may be empty for FILE_EDIT!)
result.files_modified    # List[FileChange]
result.commands_run      # List[CommandRun]
result.session_id        # For continuation
result.result_type       # TEXT/CODE/FILE_EDIT/COMMAND/MIXED
```

For detailed patterns: [references/u-llm-sdk.md]
For Claude features: [references/claude-only-sdk.md]
For types reference: [references/llm-types.md]
