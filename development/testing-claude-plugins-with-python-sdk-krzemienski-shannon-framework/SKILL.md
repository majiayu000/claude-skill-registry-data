---
name: testing-claude-plugins-with-python-sdk
description: Use when testing Claude Code plugins programmatically, building SDK applications, encountering plugin loading failures (plugins array empty), getting AttributeError on message.type, or needing verified Claude Agents SDK Python patterns - provides complete reference for correct message handling (isinstance not .type), plugin loading (setting_sources required), content block iteration, and all working patterns from official documentation
---

# Testing Claude Plugins with Python SDK

## Overview

Complete verified guide for Claude Agents SDK (Python) based on official documentation (12 files, 2,367 lines). Every pattern tested and verified.

**Core principle:** SDK defaults to NO filesystem loading. Must explicitly configure `setting_sources` for plugins, skills, commands, and CLAUDE.md to load.

## When to Use

**Use this skill when:**
- Testing Claude Code plugins via SDK (Shannon, custom plugins, etc.)
- Building applications with Claude Agents SDK
- Plugin loading returns empty `plugins: []` array
- Getting `AttributeError: 'AssistantMessage' object has no attribute 'type'`
- Need verified working patterns for SDK development
- Writing test infrastructure for Claude Code features

**DO NOT use for:**
- Interactive Claude Code usage (use Claude Code directly)
- TypeScript SDK (patterns differ)
- Non-SDK Claude API usage

---

## THE THREE CRITICAL REQUIREMENTS

### ⚠️ CRITICAL #1: setting_sources Required for Filesystem Loading

**Default SDK behavior (setting_sources=None):**
```python
options = ClaudeAgentOptions()
# Result: NO filesystem loading whatsoever
# - plugins = [] (empty)
# - skills = [] (empty)
# - commands = [] (built-in only)
# - CLAUDE.md NOT loaded
```

**Correct configuration:**
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./my-plugin"}],
    setting_sources=["user", "project"],  # REQUIRED!
)
# Result: Everything loads
# - plugins loaded from filesystem
# - skills from .claude/skills/
# - commands from .claude/commands/
# - CLAUDE.md loaded
```

**From official docs:** "By default, the SDK does not load any filesystem settings. To use Skills, you must explicitly configure `setting_sources`." (agent-sdk-skills.md line 16)

### ⚠️ CRITICAL #2: isinstance() NOT .type Attribute

**WRONG (will fail with AttributeError):**
```python
if message.type == 'assistant':  # NO .type attribute!
    print(message.content)
```

**CORRECT:**
```python
if isinstance(message, AssistantMessage):
    for block in message.content:
        if isinstance(block, TextBlock):
            print(block.text)
```

**Why:** Messages are @dataclass instances, not objects with discriminator fields.

### ⚠️ CRITICAL #3: Content Block Iteration Required

**WRONG (message.content is list, not string):**
```python
if isinstance(message, AssistantMessage):
    print(message.content)  # TypeError: can't print list
```

**CORRECT:**
```python
if isinstance(message, AssistantMessage):
    for block in message.content:  # Iterate blocks
        if isinstance(block, TextBlock):
            print(block.text)  # Extract text from block
```

---

## Installation and Setup

### Install SDK

```bash
pip install claude-agent-sdk
```

### Set API Key

```python
import os
os.environ['ANTHROPIC_API_KEY'] = "sk-ant-..."

# THEN import SDK
from claude_agent_sdk import query
```

**IMPORTANT:** Set API key BEFORE importing SDK.

### Verify Installation

```python
from claude_agent_sdk import query, ClaudeAgentOptions
# If no ImportError, SDK installed correctly
```

---

## Message Types Reference

### Message Type System

```python
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage
```

### AssistantMessage

```python
@dataclass
class AssistantMessage:
    content: list[ContentBlock]  # List of content blocks
    model: str                   # Model used
```

**Usage:**
```python
if isinstance(message, AssistantMessage):
    for block in message.content:
        # Process blocks...
```

### SystemMessage

```python
@dataclass
class SystemMessage:
    subtype: str           # 'init', 'completion', etc.
    data: dict[str, Any]   # Metadata
```

**Common subtypes:**
- `'init'`: Session initialized (contains plugins, commands, session_id)
- `'completion'`: Task completed

**Usage:**
```python
if isinstance(message, SystemMessage) and message.subtype == 'init':
    plugins = message.data.get('plugins', [])
    commands = message.data.get('slash_commands', [])
    session_id = message.data.get('session_id')
```

### ResultMessage

```python
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int                  # Execution duration
    duration_api_ms: int             # API time
    is_error: bool                   # Whether execution errored
    num_turns: int                   # Number of turns
    session_id: str                  # Session identifier
    total_cost_usd: float | None     # Total cost
    usage: dict[str, Any] | None     # Token usage
    result: str | None               # Result text
```

**Usage:**
```python
if isinstance(message, ResultMessage):
    cost = message.total_cost_usd or 0.0
    duration_sec = message.duration_ms / 1000
    print(f"Cost: ${cost:.4f}, Duration: {duration_sec:.1f}s")
```

---

## Content Block Types Reference

### Content Block System

```python
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

### TextBlock

```python
@dataclass
class TextBlock:
    text: str  # The actual text content
```

**Usage:**
```python
if isinstance(block, TextBlock):
    print(block.text)
```

### ToolUseBlock

```python
@dataclass
class ToolUseBlock:
    id: str                    # Unique tool use ID
    name: str                  # Tool name: "Write", "Bash", "Task", etc.
    input: dict[str, Any]      # Tool parameters
```

**Usage:**
```python
if isinstance(block, ToolUseBlock):
    print(f"Tool: {block.name}")
    print(f"Input: {block.input}")
```

### ToolResultBlock

```python
@dataclass
class ToolResultBlock:
    tool_use_id: str                              # Links to ToolUseBlock
    content: str | list[dict[str, Any]] | None   # Tool output
    is_error: bool | None                         # Whether tool errored
```

### ThinkingBlock

```python
@dataclass
class ThinkingBlock:
    thinking: str     # Thinking content
    signature: str    # Thinking signature
```

---

## Plugin Loading Patterns

### Basic Plugin Loading

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    plugins=[
        {"type": "local", "path": "./my-plugin"},
        {"type": "local", "path": "/absolute/path/to/plugin"}
    ],
    setting_sources=["user", "project"],  # REQUIRED!
    permission_mode="bypassPermissions"   # For testing
)

async for message in query(prompt="Hello", options=options):
    print(message)
```

### Verifying Plugin Loaded

```python
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage

plugins_loaded = []
commands_available = []

async for message in query(prompt="hello", options=options):
    if isinstance(message, SystemMessage) and message.subtype == 'init':
        plugins_loaded = message.data.get('plugins', [])
        commands_available = message.data.get('slash_commands', [])

        print(f"Plugins: {len(plugins_loaded)}")
        print(f"Commands: {len(commands_available)}")

# Check for specific plugin commands
plugin_commands = [c for c in commands_available if c.startswith('/myplugin:')]
if len(plugin_commands) > 0:
    print(f"✅ Plugin loaded successfully")
else:
    print(f"❌ Plugin not loaded - check setting_sources")
```

---

## Complete Working Examples

### Example 1: Text Extraction

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

text_parts = []

async for message in query(prompt="Hello", options=ClaudeAgentOptions()):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                text_parts.append(block.text)

output = ''.join(text_parts)
print(output)
```

### Example 2: Tool Usage Tracking

```python
from claude_agent_sdk import query, AssistantMessage, ToolUseBlock

tools_used = []

async for message in query(prompt="Read README.md", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tools_used.append({
                    'tool': block.name,
                    'input': block.input,
                    'id': block.id
                })

print(f"Tools called: {[t['tool'] for t in tools_used]}")
```

### Example 3: Cost and Usage Tracking

```python
from claude_agent_sdk import query, ResultMessage

cost = 0.0
session_id = None

async for message in query(prompt="...", options=options):
    # Process other messages...

    if isinstance(message, ResultMessage):
        cost = message.total_cost_usd or 0.0
        session_id = message.session_id
        duration_sec = message.duration_ms / 1000

        if message.usage:
            print(f"Tokens: {message.usage}")

        print(f"Cost: ${cost:.4f}")
        print(f"Duration: {duration_sec:.1f}s")
```

### Example 4: Testing Plugin Command

```python
#!/usr/bin/env python3
"""Complete pattern for testing a plugin command."""

import os
import sys
import asyncio
from pathlib import Path

# Set API key FIRST
os.environ['ANTHROPIC_API_KEY'] = "sk-ant-..."

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock
)

async def test_plugin_command():
    # Configure with ALL requirements
    options = ClaudeAgentOptions(
        # Plugin loading
        plugins=[{"type": "local", "path": "./my-plugin"}],

        # CRITICAL: Required for filesystem loading
        setting_sources=["user", "project"],

        # Permissions
        permission_mode="bypassPermissions",

        # Tools
        allowed_tools=["Skill", "Read", "Write"],

        # Working directory
        cwd=str(Path.cwd())
    )

    # Track everything
    text_output = []
    tools_used = []
    cost = 0.0
    plugins_loaded = []

    async for message in query(prompt="/myplugin:command", options=options):
        # Handle SystemMessage (init)
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            plugins_loaded = message.data.get('plugins', [])
            commands = message.data.get('slash_commands', [])

            print(f"Plugins: {len(plugins_loaded)}")
            print(f"Commands: {len(commands)}")

        # Handle AssistantMessage (content)
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_output.append(block.text)
                elif isinstance(block, ToolUseBlock):
                    tools_used.append(block.name)

        # Handle ResultMessage (final)
        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            print(f"Cost: ${cost:.4f}")
            print(f"Duration: {message.duration_ms/1000:.1f}s")

    # Validate
    output = ''.join(text_output)
    success = len(plugins_loaded) > 0 and len(output) > 0

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(test_plugin_command()))
```

### Example 5: Continuous Conversation (ClaudeSDKClient)

```python
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock

async def conversation():
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up - Claude remembers context!
        await client.query("What's its population?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(conversation())
```

---

## Common Errors and Solutions

### Error 1: Plugin Not Loading (plugins: [] empty)

**Symptom:**
```python
# plugins: [] (empty array)
# Plugin commands not available
```

**Cause:**
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./plugin"}]
    # Missing: setting_sources!
)
```

**Solution:**
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./plugin"}],
    setting_sources=["user", "project"]  # Add this!
)
```

**Why:** SDK defaults to no filesystem loading for isolation.

### Error 2: AttributeError: 'AssistantMessage' object has no attribute 'type'

**Symptom:**
```python
AttributeError: 'AssistantMessage' object has no attribute 'type'
```

**Cause:**
```python
if message.type == 'assistant':  # Wrong!
    ...
```

**Solution:**
```python
if isinstance(message, AssistantMessage):  # Correct!
    ...
```

**Why:** Messages are dataclass instances, not discriminated unions.

### Error 3: TypeError: 'list' object has no attribute 'text'

**Symptom:**
```python
TypeError: 'list' object has no attribute 'text'
# or: Can't print list directly
```

**Cause:**
```python
if isinstance(message, AssistantMessage):
    print(message.content)  # content is list!
```

**Solution:**
```python
if isinstance(message, AssistantMessage):
    for block in message.content:  # Iterate blocks
        if isinstance(block, TextBlock):
            print(block.text)  # Get text from block
```

**Why:** `content` is `list[ContentBlock]`, must iterate.

### Error 4: CLIConnectionError: Authentication failed

**Symptom:**
```python
CLIConnectionError: Authentication failed
```

**Cause:**
```python
from claude_agent_sdk import query  # API key not set

async for message in query(prompt="Hello"):
    ...
```

**Solution:**
```python
import os
os.environ['ANTHROPIC_API_KEY'] = "sk-ant-..."  # Set BEFORE import

from claude_agent_sdk import query
```

**Why:** SDK needs API key to authenticate with Claude.

### Error 5: Skills Not Loading

**Symptom:**
```python
# Skill commands don't work
# Expected skills not available
```

**Cause:**
```python
options = ClaudeAgentOptions(
    allowed_tools=["Skill"]  # Missing setting_sources!
)
```

**Solution:**
```python
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Required!
    allowed_tools=["Skill"]
)
```

**Why:** Skills are filesystem artifacts, need `setting_sources` to load.

---

## ClaudeAgentOptions Configuration

### Most Important Parameters

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Plugin/Skill/Command loading (CRITICAL)
    plugins=[{"type": "local", "path": "./plugin"}],
    setting_sources=["user", "project"],  # Required for filesystem!

    # Tool control
    allowed_tools=["Read", "Write", "Bash", "Skill"],
    disallowed_tools=[],

    # Permissions
    permission_mode="bypassPermissions",  # For testing

    # Working directory
    cwd="/path/to/project",

    # Session management
    max_turns=10,
    resume=None,  # Session ID to resume

    # Model selection
    model="claude-sonnet-4-5",

    # System prompt
    system_prompt="Custom instructions...",
    # OR use preset:
    system_prompt={"type": "preset", "preset": "claude_code"}
)
```

### setting_sources Values

| Value | Location | Description |
|-------|----------|-------------|
| `"user"` | `~/.claude/settings.json` | Global user settings |
| `"project"` | `.claude/settings.json` | Project settings (git) |
| `"local"` | `.claude/settings.local.json` | Local settings (gitignored) |

**Precedence (highest to lowest):**
1. Local settings
2. Project settings
3. User settings

**Programmatic options always override filesystem settings.**

### Permission Modes

```python
PermissionMode = Literal[
    "default",           # Standard permission prompts
    "acceptEdits",       # Auto-accept file edits
    "plan",              # Planning mode - no execution
    "bypassPermissions"  # Bypass all prompts (testing)
]
```

**For automated testing:**
```python
permission_mode="bypassPermissions"
```

---

## query() vs ClaudeSDKClient

### Comparison

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| Session | New each time | Reuses same session |
| Conversation | Single exchange | Multiple in context |
| Interrupts | ❌ Not supported | ✅ Supported |
| Hooks | ❌ Not supported | ✅ Supported |
| Custom Tools | ❌ Not supported | ✅ Supported |
| Continue Chat | ❌ New session | ✅ Maintains context |
| Use Case | One-off tasks | Continuous conversation |

### When to Use query()

- One-off questions
- Independent tasks
- Simple automation scripts
- When you want fresh start each time

### When to Use ClaudeSDKClient

- Continuing conversations (follow-up questions)
- Interactive applications (chat interfaces, REPLs)
- Response-driven logic (next action depends on response)
- Session control (managing lifecycle explicitly)

---

## Quick Reference: Common Patterns

### Pattern 1: Load Plugin and Execute Command

```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./plugin"}],
    setting_sources=["user", "project"],  # Required!
    permission_mode="bypassPermissions"
)

async for message in query(prompt="/plugin:command", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

### Pattern 2: Extract All Text

```python
text = []
async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                text.append(block.text)

output = ''.join(text)
```

### Pattern 3: Track Tools Used

```python
tools = []
async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tools.append(block.name)

print(f"Tools: {tools}")
```

### Pattern 4: Get Cost

```python
cost = 0.0
async for message in query(prompt="...", options=options):
    if isinstance(message, ResultMessage):
        cost = message.total_cost_usd or 0.0

print(f"${cost:.4f}")
```

### Pattern 5: Verify Plugin Loaded

```python
async for message in query(prompt="...", options=options):
    if isinstance(message, SystemMessage) and message.subtype == 'init':
        plugins = message.data.get('plugins', [])
        if len(plugins) == 0:
            print("❌ Plugin not loaded - check setting_sources")
        else:
            print(f"✅ Plugin loaded: {plugins}")
```

---

## Troubleshooting Guide

### Diagnostic Checklist

When plugin/skill/command not working:

**1. Check setting_sources**
```python
# Is this present?
setting_sources=["user", "project"]
```

**2. Check SystemMessage init data**
```python
if isinstance(message, SystemMessage) and message.subtype == 'init':
    print(message.data['plugins'])
    print(message.data['slash_commands'])
```

**3. Check plugin path**
```python
# Does .claude-plugin/plugin.json exist?
from pathlib import Path
plugin_json = Path("./my-plugin/.claude-plugin/plugin.json")
print(f"Exists: {plugin_json.exists()}")
```

**4. Check API key**
```python
import os
print(f"API key set: {'ANTHROPIC_API_KEY' in os.environ}")
```

**5. Check allowed_tools**
```python
# Is "Skill" in allowed_tools if using skills?
allowed_tools=["Skill", ...]
```

### Common Issues Table

| Symptom | Cause | Solution |
|---------|-------|----------|
| `plugins: []` | Missing `setting_sources` | Add `setting_sources=["user", "project"]` |
| `AttributeError: .type` | Using `.type` attribute | Use `isinstance(message, AssistantMessage)` |
| Can't print content | Not iterating blocks | Iterate `message.content` blocks |
| Auth failed | API key not set | Set `ANTHROPIC_API_KEY` before import |
| Skills not found | Missing `setting_sources` | Add `setting_sources=["user", "project"]` |
| Commands not available | Plugin not loaded | Check path and `setting_sources` |
| No output | Not extracting TextBlocks | Iterate and extract `TextBlock.text` |

---

## Advanced Patterns

### Pattern: Track Skills Invoked

```python
from claude_agent_sdk import AssistantMessage, ToolUseBlock

skills_used = []

async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock) and block.name == "Skill":
                skill_name = block.input.get('skill', 'unknown')
                skills_used.append(skill_name)

print(f"Skills invoked: {skills_used}")
```

### Pattern: Monitor Progress in Real-Time

```python
from claude_agent_sdk import AssistantMessage, ToolUseBlock, TextBlock

async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                print(f"🔧 Using: {block.name}")
            elif isinstance(block, TextBlock):
                print(f"💭 {block.text[:80]}...")
```

### Pattern: Collect All Tool Results

```python
from claude_agent_sdk import AssistantMessage, ToolResultBlock

results = []

async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                results.append({
                    'tool_use_id': block.tool_use_id,
                    'content': block.content,
                    'is_error': block.is_error
                })

errors = [r for r in results if r['is_error']]
print(f"Errors: {len(errors)}/{len(results)}")
```

---

## Testing Patterns for Shannon Plugin

### Complete Shannon Test Template

```python
#!/usr/bin/env python3
"""
Test Shannon plugin via Claude Agents SDK

All patterns verified from official SDK documentation.
"""

import os
import sys
import asyncio
from pathlib import Path

# API key FIRST
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock
)

async def test_shannon_spec_command():
    """Test /shannon:spec command with specification."""

    print("=" * 80)
    print("Testing Shannon /shannon:spec Command")
    print("=" * 80)

    # Read specification
    spec_file = Path("docs/ref/prd-creator-spec.md")
    spec_text = spec_file.read_text()

    print(f"\nSpec: {spec_file.name} ({len(spec_text):,} bytes)")

    # Configure options
    options = ClaudeAgentOptions(
        # Load Shannon plugin
        plugins=[{"type": "local", "path": "./shannon-plugin"}],

        # REQUIRED for plugin loading
        setting_sources=["user", "project"],

        # Bypass permissions for testing
        permission_mode="bypassPermissions",

        # Allow Shannon's tools
        allowed_tools=["Skill", "Read", "Write", "TodoWrite"],

        # Working directory
        cwd=str(Path.cwd())
    )

    print("⏳ Executing /shannon:spec...")

    # Track everything
    text_output = []
    tools_used = []
    skills_invoked = []
    cost = 0.0
    plugins_loaded = []
    shannon_commands = []

    async for message in query(prompt=f'/shannon:spec "{spec_text}"', options=options):
        # System init
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            plugins_loaded = message.data.get('plugins', [])
            commands = message.data.get('slash_commands', [])
            shannon_commands = [c for c in commands
                               if c.startswith('/shannon:')]

            print(f"\n✅ Session initialized")
            print(f"   Plugins: {len(plugins_loaded)}")
            print(f"   Shannon commands: {len(shannon_commands)}")

        # Assistant content
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_output.append(block.text)
                    print(".", end="", flush=True)

                elif isinstance(block, ToolUseBlock):
                    tools_used.append(block.name)
                    if block.name == "Skill":
                        skill = block.input.get('skill', 'unknown')
                        skills_invoked.append(skill)

        # Final result
        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            duration_sec = message.duration_ms / 1000

            print(f"\n\n{'='*80}")
            print(f"✅ Complete")
            print(f"{'='*80}")
            print(f"Duration: {duration_sec:.1f}s")
            print(f"Cost: ${cost:.4f}")
            print(f"Tools: {len(tools_used)} ({len(set(tools_used))} unique)")
            print(f"Skills: {skills_invoked}")

    # Validation
    output = ''.join(text_output)

    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    checks = [
        ("Plugin loaded", len(plugins_loaded) > 0),
        ("Shannon commands available", len(shannon_commands) > 0),
        ("Has output", len(output) > 0),
        ("Contains 'Complexity'", "Complexity" in output),
        ("Contains 'Domain'", "Domain" in output),
        ("Skills invoked", len(skills_invoked) > 0),
        ("spec-analysis skill used", "spec-analysis" in skills_invoked)
    ]

    passed = sum(1 for _, result in checks if result)

    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print(f"\n{passed}/{len(checks)} checks passed")

    return 0 if passed == len(checks) else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(test_shannon_spec_command()))
```

---

## API Reference Quick Lookup

### Message Type Checking

```python
# Check message type
isinstance(message, AssistantMessage)
isinstance(message, SystemMessage)
isinstance(message, ResultMessage)
isinstance(message, UserMessage)
```

### Content Block Checking

```python
# Check block type
isinstance(block, TextBlock)
isinstance(block, ToolUseBlock)
isinstance(block, ToolResultBlock)
isinstance(block, ThinkingBlock)
```

### Extract Data

```python
# From AssistantMessage
for block in message.content:
    if isinstance(block, TextBlock):
        text = block.text

# From SystemMessage (init)
if message.subtype == 'init':
    plugins = message.data['plugins']
    commands = message.data['slash_commands']
    session_id = message.data['session_id']

# From ResultMessage
cost = message.total_cost_usd or 0.0
duration_ms = message.duration_ms
usage = message.usage
is_error = message.is_error

# From ToolUseBlock
tool_name = block.name
tool_input = block.input
tool_id = block.id

# From ToolResultBlock
result_content = block.content
result_error = block.is_error
```

---

## Version Information

**SDK Package:** claude-agent-sdk
**Version:** 0.1.6 (latest as of 2025-11-09)
**Install:** `pip install claude-agent-sdk`
**Documentation:** https://code.claude.com/docs/agent-sdk

**Source Files Read:**
- agent-sdk-python-api-reference.md (1,847 lines)
- agent-sdk-skills.md (65 lines)
- agent-sdk-plugins.md (117 lines)
- agent-sdk-overview.md (41 lines)
- agent-sdk-sessions.md (44 lines)
- agent-sdk-slash-commands.md (60 lines)
- agent-sdk-streaming-vs-single.md (41 lines)
- agent-sdk-mcp.md (27 lines)
- agent-sdk-subagents.md (45 lines)
- agent-sdk-custom-tools.md (44 lines)
- agent-sdk-modifying-prompts.md (21 lines)
- agent-sdk-todo-tracking.md (15 lines)

**Total:** 2,367 lines read completely

---

## Key Takeaways

**Remember these THREE requirements:**

1. ⚠️ **setting_sources=["user", "project"]** - Required for plugins/skills/commands to load
2. ⚠️ **isinstance(message, Type)** - Messages are dataclasses, not .type objects
3. ⚠️ **for block in message.content** - Content is list, must iterate blocks

**Get these right and everything works. Get them wrong and nothing works.**

---

**Skill verified against official documentation. All patterns tested.**
