---
name: cua-cloud
description: Comprehensive guide for building Computer Use Agents with the CUA framework. This skill should be used when automating desktop applications, building vision-based agents, controlling virtual machines (Linux/Windows/macOS), or integrating computer-use models from Anthropic, OpenAI, or other providers. Covers Computer SDK (click, type, scroll, screenshot), Agent SDK (model configuration, composition), supported models, provider setup, and MCP integration.
---

# CUA Framework

## Overview

CUA ("koo-ah") is an open-source framework for building Computer Use Agents—AI systems that see, understand, and interact with desktop applications through vision and action. It supports Windows, Linux, and macOS automation.

**Key capabilities:**
- Vision-based UI automation via screenshot analysis
- Multi-platform desktop control (click, type, scroll, drag)
- 100+ LLM providers via LiteLLM integration
- Composed agents (grounding + planning models)
- Local and cloud execution options

## Installation

```bash
# Computer SDK - desktop control
pip install cua-computer

# Agent SDK - autonomous agents
pip install cua-agent[all]

# MCP Server (optional)
pip install cua-mcp-server
```

**CLI Installation:**
```bash
# macOS/Linux
curl -LsSf https://cua.ai/cli/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://cua.ai/cli/install.ps1 | iex"
```

## Computer SDK

### Computer Class

```python
from computer import Computer
import os

os.environ["CUA_API_KEY"] = "sk_cua-api01_..."

computer = Computer(
    os_type="linux",      # "linux" | "macos" | "windows"
    provider_type="cloud", # "cloud" | "docker" | "lume" | "windows_sandbox"
    name="sandbox-name"
)

try:
    await computer.run()
    # Use computer.interface methods here
finally:
    await computer.close()
```

### Interface Methods

**Screenshot:**
```python
screenshot = await computer.interface.screenshot()
```

**Mouse Actions:**
```python
await computer.interface.left_click(x, y)      # Left click at coordinates
await computer.interface.right_click(x, y)     # Right click
await computer.interface.double_click(x, y)    # Double click
await computer.interface.move_cursor(x, y)     # Move cursor without clicking
await computer.interface.drag(x1, y1, x2, y2)  # Click and drag
```

**Keyboard Actions:**
```python
await computer.interface.type_text("Hello!")   # Type text
await computer.interface.key_press("enter")    # Press single key
await computer.interface.hotkey("ctrl", "c")   # Key combination
```

**Scrolling:**
```python
await computer.interface.scroll(direction, amount)  # Scroll up/down/left/right
```

**File Operations:**
```python
content = await computer.interface.read_file("/path/to/file")
await computer.interface.write_file("/path/to/file", "content")
```

**Clipboard:**
```python
text = await computer.interface.get_clipboard()
await computer.interface.set_clipboard("text to copy")
```

### Supported Actions (Message Format)

**OpenAI-style:**
- `ClickAction` - button: left/right/wheel/back/forward, x, y coordinates
- `DoubleClickAction` - same parameters as click
- `DragAction` - start and end coordinates
- `KeyPressAction` - key name
- `MoveAction` - x, y coordinates
- `ScreenshotAction` - no parameters
- `ScrollAction` - direction and amount
- `TypeAction` - text string
- `WaitAction` - duration

**Anthropic-style:**
- `LeftMouseDownAction` - x, y coordinates
- `LeftMouseUpAction` - x, y coordinates

## Agent SDK

### ComputerAgent Class

```python
from agent import ComputerAgent

agent = ComputerAgent(
    model="anthropic/claude-sonnet-4-5-20250929",
    tools=[computer],
    max_trajectory_budget=5.0  # Cost limit in USD
)

messages = [{"role": "user", "content": "Open Firefox and go to google.com"}]

async for result in agent.run(messages):
    for item in result["output"]:
        if item["type"] == "message":
            print(item["content"][0]["text"])
```

### Response Structure

```python
{
    "output": [AgentMessage, ...],  # List of messages
    "usage": {
        "prompt_tokens": int,
        "completion_tokens": int,
        "total_tokens": int,
        "response_cost": float
    }
}
```

**Message Types:**
- `UserMessage` - Input from user/system
- `AssistantMessage` - Text output from agent
- `ReasoningMessage` - Agent thinking/summary
- `ComputerCallMessage` - Intent to perform action
- `ComputerCallOutputMessage` - Screenshot result
- `FunctionCallMessage` - Python tool invocation
- `FunctionCallOutputMessage` - Function result

## Supported Models

### CUA VLM Router (Recommended)
```python
model="cua/anthropic/claude-sonnet-4.5"  # Recommended
model="cua/anthropic/claude-haiku-4.5"   # Faster, cheaper
```
Single API key, cost tracking, managed infrastructure.

### Anthropic (BYOK)
```python
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

model="anthropic/claude-sonnet-4-5-20250929"
model="anthropic/claude-haiku-4-5-20251001"
model="anthropic/claude-opus-4-20250514"
model="anthropic/claude-3-7-sonnet-20250219"
```

### OpenAI (BYOK)
```python
os.environ["OPENAI_API_KEY"] = "sk-..."

model="openai/computer-use-preview"
```

### Google Gemini
```python
model="gemini-2.5-computer-use-preview-10-2025"
```

### Local Models
```python
model="huggingface-local/ByteDance-Seed/UI-TARS-1.5-7B"
model="ollama_chat/0000/ui-tars-1.5-7b"
```

### Composed Agents

Combine grounding models with planning models:
```python
model="huggingface-local/GTA1-7B+openai/gpt-4o"
model="moondream3+openai/gpt-4o"
model="omniparser+anthropic/claude-sonnet-4-5-20250929"
model="omniparser+ollama_chat/mistral-small3.2"
```

**Grounding Models:** UI-TARS, GTA, Holo, Moondream, OmniParser, OpenCUA

### Human-in-the-Loop
```python
model="human/human"  # Pause for user approval
```

## Provider Types

### Cloud (Recommended)
```python
computer = Computer(
    os_type="linux",  # linux, windows, macos
    provider_type="cloud",
    name="sandbox-name",
    api_key="sk_cua-api01_..."
)
```
Get API key from [cloud.trycua.com](https://cloud.trycua.com).

### Docker (Local)
```python
computer = Computer(
    os_type="linux",
    provider_type="docker"
)
```
Images: `trycua/cua-xfce:latest`, `trycua/cua-ubuntu:latest`

### Lume (macOS Local)
```python
computer = Computer(
    os_type="linux",
    provider_type="lume"
)
```
Requires Lume CLI installation.

### Windows Sandbox
```python
computer = Computer(
    os_type="windows",
    provider_type="windows_sandbox"
)
```
Requires `pywinsandbox` and Windows Sandbox feature enabled.

## MCP Integration

This project uses the CUA MCP Server for Claude Code integration:

```json
{
  "mcpServers": {
    "cua": {
      "type": "http",
      "url": "https://cua-mcp-server.vercel.app/mcp"
    }
  }
}
```

### MCP Tools Available

**Sandbox Management:**
- `mcp__cua__list_sandboxes` - List all sandboxes
- `mcp__cua__create_sandbox` - Create VM (os, size, region)
- `mcp__cua__start/stop/restart/delete_sandbox`

**Task Execution:**
- `mcp__cua__run_task` - Autonomous task execution
- `mcp__cua__describe_screen` - Vision analysis without action
- `mcp__cua__get_task_history` - Retrieve task results

## Best Practices

### Task Design
```python
# Good - specific and sequential
"Open Chrome, navigate to github.com, click the Sign In button"

# Avoid - vague
"Log into GitHub"
```

### Error Recovery
```python
async for result in agent.run(messages):
    if result.get("error"):
        # Take screenshot to understand state
        screenshot = await computer.interface.screenshot()
        # Retry with more specific instructions
```

### Resource Management
```python
try:
    await computer.run()
    # ... perform tasks
finally:
    await computer.close()  # Always cleanup
```

### Cost Control
```python
agent = ComputerAgent(
    model="cua/anthropic/claude-sonnet-4.5",
    max_trajectory_budget=5.0  # Stop at $5 spent
)
```

## Resources

- [Documentation](https://cua.ai/docs)
- [GitHub](https://github.com/trycua/cua)
- [Cloud Dashboard](https://cloud.trycua.com)
- [Discord](https://discord.com/invite/mVnXXpdE85)
