---
name: claude-agent-sdk
description: |
  Build production-ready AI agents using Claude Agent SDK (Python).
  Use when implementing agent workflows, SDK integration, one-shot queries,
  interactive conversations, custom MCP tools, permission control, CLAUDE.md context loading,
  error handling, hooks, or agent delegation. Works with .py files and agent architectures.
  Trigger terms: "Claude Agent SDK", "query()", "ClaudeSDKClient", "@tool decorator",
  "setting_sources", "agent permissions", "SDK hooks", "build agent with SDK".
allowed-tools: Read, Write, MultiEdit, Bash, Grep, Glob
---

# Claude Agent SDK Skill

## Purpose

Build production-ready AI agents using the **Claude Agent SDK** for Python. This skill provides hands-on workflows for implementing agent features including simple queries, interactive conversations, custom MCP tools, permission control, context loading, and error handling.

**Note:** For high-level agent CLI tools (easier to use), see:
[.claude/tools/agents/README.md](../../../.claude/tools/agents/README.md) - Covers claude_ask.py (CLI), claude.py (SDK wrapper), and claude_agent.py (hooks)

## Quick Start

**Simple one-shot query:**
```python
from claude_agent_sdk import query

async for message in query(prompt="What is the capital of France?"):
    print(message)
```

**Interactive conversation:**
```python
from claude_agent_sdk import ClaudeSDKClient

async with ClaudeSDKClient() as client:
    await client.query("Hello!")
    async for msg in client.receive_response():
        print(msg)
```

## Instructions

### Step 1: Choose the Right API Mode

**Use `query()` for:**
- Simple one-shot questions
- Batch processing of independent tasks
- Stateless operations
- When all inputs are known upfront
- CI/CD automation scripts

**Use `ClaudeSDKClient` for:**
- Interactive conversations with follow-ups
- Chat applications or REPL interfaces
- When you need to send messages based on responses
- Long-running sessions with state management
- Interrupt capabilities

### Step 2: Build Simple Agent (query() Function)

**Basic implementation:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Analyze this code for security issues",
    options=ClaudeAgentOptions(
        system_prompt="You are a security expert",
        cwd="/path/to/project",
        permission_mode="default"
    )
):
    if hasattr(message, 'content'):
        print(message.content)
```

**Key configuration options:**
- `system_prompt`: Define agent expertise
- `cwd`: Set working directory
- `permission_mode`: Control tool execution ("default", "acceptEdits", "bypassPermissions")
- `model`: Choose model ("claude-sonnet-4", "claude-opus-4")

### Step 3: Build Interactive Agent (ClaudeSDKClient)

**Full conversation example:**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, TextBlock, ResultMessage

async def chat_agent():
    client = ClaudeSDKClient(
        options=ClaudeAgentOptions(
            system_prompt="You are a helpful coding assistant",
            permission_mode="acceptEdits"
        )
    )

    await client.connect()

    try:
        # Send initial message
        await client.query("Help me write a Python web server")

        # Receive and process response
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(msg, ResultMessage):
                print(f"Cost: ${msg.total_cost_usd:.4f}")

        # Follow-up question
        await client.query("Can you add error handling?")
        async for msg in client.receive_response():
            # Process follow-up response
            pass

    finally:
        await client.disconnect()
```

**Using async context manager:**
```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("First question")
    async for msg in client.receive_response():
        print(msg)
```

### Step 4: Create Custom MCP Tools

**Define tools with @tool decorator:**
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("greet", "Greet a user by name", {"name": str})
async def greet(args):
    return {
        "content": [{"type": "text", "text": f"Hello, {args['name']}!"}]
    }

@tool("add", "Add two numbers", {"a": float, "b": float})
async def add_numbers(args):
    result = args["a"] + args["b"]
    return {
        "content": [{"type": "text", "text": f"Sum: {result}"}]
    }

# Create MCP server
calculator = create_sdk_mcp_server(
    name="calculator",
    version="1.0.0",
    tools=[greet, add_numbers]
)

# Use with agent
options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["greet", "add"]
)
```

**Tool with error handling:**
```python
@tool("divide", "Divide two numbers", {"a": float, "b": float})
async def divide(args):
    if args["b"] == 0:
        return {
            "content": [{"type": "text", "text": "Error: Division by zero"}],
            "is_error": True
        }
    return {
        "content": [{"type": "text", "text": f"Result: {args['a'] / args['b']}"}]
    }
```

### Step 5: Configure Permissions and Tool Access

**Fine-grained tool restrictions:**
```python
options = ClaudeAgentOptions(
    # Allow only specific tools
    allowed_tools=["Read", "Grep", "search_code"],

    # Block dangerous tools
    disallowed_tools=["Bash", "Write"],

    # Permission mode
    permission_mode="default"  # or "acceptEdits" or "bypassPermissions"
)
```

**Dynamic permission callback:**
```python
from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

async def can_use_tool(tool_name, tool_input, context):
    # Allow read-only tools
    if tool_name in ["Read", "Grep", "Glob"]:
        return PermissionResultAllow()

    # Block destructive operations
    if tool_name == "Bash" and "rm" in str(tool_input):
        return PermissionResultDeny(
            message="Destructive bash commands are not allowed",
            interrupt=True
        )

    # Ask for other tools
    return PermissionResultAllow()

options = ClaudeAgentOptions(
    can_use_tool=can_use_tool
)
```

### Step 6: Load CLAUDE.md Context (setting_sources)

**Load project and user instructions:**
```python
options = ClaudeAgentOptions(
    # Load CLAUDE.md files
    setting_sources=["user", "project"],

    # user: ~/.claude/CLAUDE.md (user-level instructions)
    # project: ./CLAUDE.md or ./.claude/CLAUDE.md (project-level)
    # local: local settings

    cwd="/path/to/project"
)

async for message in query(
    prompt="Review this code following project standards",
    options=options
):
    print(message)
```

**When to use which source:**
- **"user"**: Personal preferences, global workflows, user-specific context
- **"project"**: Team standards, project architecture, shared conventions
- **"local"**: Machine-specific settings, temporary overrides
- **Best practice**: Use `["user", "project"]` for most agent workflows

### Step 7: Implement Error Handling

**Try/catch with specific exceptions:**
```python
from claude_agent_sdk import (
    ClaudeSDKError,
    CLIConnectionError,
    CLINotFoundError,
    ProcessError
)

try:
    async for message in query(prompt="Hello"):
        print(message)

except CLINotFoundError as e:
    print("Claude CLI not installed. Install with: npm install -g claude-code")

except CLIConnectionError as e:
    print(f"Connection failed: {e}")
    # Retry logic here

except ProcessError as e:
    print(f"Process error (exit {e.exit_code}): {e.stderr}")

except ClaudeSDKError as e:
    print(f"SDK error: {e}")
```

**Retry logic with exponential backoff:**
```python
import asyncio

async def query_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            messages = []
            async for message in query(prompt=prompt):
                messages.append(message)
            return messages

        except CLIConnectionError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            await asyncio.sleep(wait_time)
```

### Step 8: Add Hooks for Event-Driven Automation

**PreToolUse hook:**
```python
from claude_agent_sdk import HookMatcher

async def log_tool_use(input_data, tool_use_id, context):
    tool_name = input_data.get("tool", {}).get("name")
    print(f"About to use tool: {tool_name}")
    return {}  # Empty response = allow

async def block_destructive_tools(input_data, tool_use_id, context):
    tool_name = input_data.get("tool", {}).get("name")
    if tool_name == "Bash":
        tool_input = input_data.get("tool", {}).get("input", {})
        if "rm -rf" in str(tool_input):
            return {
                "decision": "block",
                "systemMessage": "Blocked destructive command"
            }
    return {}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(
                matcher="Bash|Write|Edit",
                hooks=[log_tool_use, block_destructive_tools]
            )
        ]
    }
)
```

**PostToolUse hook:**
```python
async def log_tool_result(input_data, tool_use_id, context):
    result = input_data.get("result", {})
    print(f"Tool completed: {result.get('success', False)}")
    return {}

options = ClaudeAgentOptions(
    hooks={
        "PostToolUse": [
            HookMatcher(matcher=None, hooks=[log_tool_result])
        ]
    }
)
```

### Step 9: Implement Agent Delegation

**Define custom agents:**
```python
from claude_agent_sdk import AgentDefinition

options = ClaudeAgentOptions(
    agents={
        "python-expert": AgentDefinition(
            description="Python code expert",
            prompt="You are an expert Python developer. Focus on clean code and best practices.",
            tools=["Read", "Write", "Bash"],
            model="opus"
        ),
        "security-analyst": AgentDefinition(
            description="Security vulnerability expert",
            prompt="You are a security expert. Analyze code for vulnerabilities.",
            tools=["Read", "Grep"],
            model="sonnet"
        )
    }
)

# Use with delegation
async for message in query(
    prompt="@python-expert Review this code for quality, then @security-analyst check for vulnerabilities",
    options=options
):
    print(message)
```

### Step 10: Production Deployment Patterns

**Complete production agent:**
```python
import logging
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    PermissionResultAllow,
    PermissionResultDeny,
    HookMatcher
)

class ProductionAgent:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.logger = logging.getLogger(__name__)

        # Configure options
        self.options = ClaudeAgentOptions(
            system_prompt="Production code review agent",
            cwd=project_dir,
            setting_sources=["user", "project"],
            permission_mode="default",
            allowed_tools=["Read", "Grep", "search_code"],
            can_use_tool=self._permission_callback,
            hooks={
                "PreToolUse": [
                    HookMatcher(matcher=None, hooks=[self._log_tool_use])
                ]
            }
        )

    async def _permission_callback(self, tool_name, tool_input, context):
        self.logger.info(f"Permission check: {tool_name}")

        # Allow read-only operations
        if tool_name in ["Read", "Grep", "Glob"]:
            return PermissionResultAllow()

        # Deny everything else
        return PermissionResultDeny(
            message=f"Tool {tool_name} not allowed in production",
            interrupt=False
        )

    async def _log_tool_use(self, input_data, tool_use_id, context):
        tool_name = input_data.get("tool", {}).get("name")
        self.logger.info(f"Tool use: {tool_name} ({tool_use_id})")
        return {}

    async def analyze_code(self, prompt: str):
        async with ClaudeSDKClient(options=self.options) as client:
            await client.query(prompt)

            results = []
            async for msg in client.receive_response():
                results.append(msg)

            return results

# Usage
agent = ProductionAgent("/path/to/project")
results = await agent.analyze_code("Review authentication logic")
```

## Examples

### Python Scripts

- [verify_sdk.py](./scripts/verify_sdk.py) - Verify Claude Agent SDK installation and configuration
- [claude_agent_examples.py](./scripts/claude_agent_examples.py) - 9 comprehensive examples for claude_agent module
- [hook_integration_example.py](./scripts/hook_integration_example.py) - Hook patterns and workflows

### Runnable Python Scripts

**For `claude_agent.py` tool** (hook-optimized agent communication):

1. **[scripts/claude_agent_examples.py](./scripts/claude_agent_examples.py)** - 9 comprehensive examples
   ```bash
   python3 .claude/skills/claude-agent-sdk/scripts/claude_agent_examples.py
   ```
   - Basic agent call
   - Session continuation
   - Hook usage
   - Quick helpers
   - Session management
   - Request/response logging
   - Custom configuration
   - Error handling
   - Multi-agent workflow

2. **[scripts/hook_integration_example.py](./scripts/hook_integration_example.py)** - Hook patterns
   ```bash
   python3 .claude/skills/claude-agent-sdk/scripts/hook_integration_example.py
   ```
   - PreToolUse/PostToolUse hooks
   - UserPromptSubmit/SessionStart/SessionEnd hooks
   - Code review workflow
   - Error recovery workflow

3. **[scripts/verify_sdk.py](./scripts/verify_sdk.py)** - Verify SDK installation
   ```bash
   python3 .claude/skills/claude-agent-sdk/scripts/verify_sdk.py
   ```
   - Python version check
   - SDK installation verification
   - Claude CLI availability
   - Environment configuration
   - Basic query functionality test

### Documentation Examples

See [references/reference.md](./references/reference.md) for:
- Official Claude Agent SDK examples
- Simple code review agent
- Interactive chat agent
- Agent with custom MCP tools
- Multi-agent system with delegation
- Production deployment with monitoring

## Requirements

**Python Dependencies:**
```bash
pip install claude-agent-sdk
# or
uv pip install claude-agent-sdk
```

**Claude CLI:**
```bash
npm install -g claude-code
```

**Environment Variables:**
```bash
# Claude API Key (default)
export ANTHROPIC_API_KEY=your_key

# OR Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# OR Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_REGION=us-central1
```

## Common Patterns

### Pattern 1: Code Review Agent
```python
async def code_review_agent(file_path: str):
    async for message in query(
        prompt=f"Review {file_path} for code quality issues",
        options=ClaudeAgentOptions(
            system_prompt="You are a senior code reviewer",
            setting_sources=["project"],
            allowed_tools=["Read", "Grep"]
        )
    ):
        if hasattr(message, 'content'):
            yield message
```

### Pattern 2: Interactive Debugging Session
```python
async def debug_session():
    async with ClaudeSDKClient(
        options=ClaudeAgentOptions(
            permission_mode="acceptEdits",
            setting_sources=["user", "project"]
        )
    ) as client:
        # Initial analysis
        await client.query("Analyze this error in logs/app.log")
        async for msg in client.receive_response():
            print(msg)

        # Follow-up with fix
        await client.query("Implement the fix you suggested")
        async for msg in client.receive_response():
            print(msg)
```

### Pattern 3: Batch Processing
```python
async def batch_analyze(files: list[str]):
    results = {}
    for file_path in files:
        messages = []
        async for msg in query(
            prompt=f"Analyze {file_path}",
            options=ClaudeAgentOptions(
                allowed_tools=["Read"],
                permission_mode="default"
            )
        ):
            messages.append(msg)
        results[file_path] = messages
    return results
```

## Integration with Project Patterns

### ServiceResult Pattern
```python
from src.project_watch_mcp.domain.value_objects import ServiceResult

async def agent_query_service(prompt: str) -> ServiceResult[list]:
    try:
        messages = []
        async for message in query(prompt=prompt):
            messages.append(message)

        return ServiceResult.success(messages)

    except ClaudeSDKError as e:
        return ServiceResult.failure(f"Agent query failed: {e}")
```

### Fail-Fast Principle
```python
# ✅ CORRECT - All imports at top, fail fast
from claude_agent_sdk import query, ClaudeAgentOptions, ClaudeSDKError

async def my_agent():
    # Will fail immediately if SDK not installed
    async for msg in query(prompt="Hello"):
        print(msg)

# ❌ WRONG - Optional dependency pattern
try:
    from claude_agent_sdk import query
except ImportError:
    query = None  # Violates fail-fast principle
```

### Configuration Injection
```python
from dataclasses import dataclass

@dataclass
class AgentConfig:
    system_prompt: str
    project_dir: str
    allowed_tools: list[str]

class Agent:
    def __init__(self, config: AgentConfig):
        if not config:
            raise ValueError("AgentConfig required")

        self.config = config
        self.options = ClaudeAgentOptions(
            system_prompt=config.system_prompt,
            cwd=config.project_dir,
            allowed_tools=config.allowed_tools
        )
```

## Troubleshooting

### Issue: "Claude Code not found"
**Solution:**
```bash
npm install -g claude-code
# Verify installation
claude-code --version
```

### Issue: Connection timeouts
**Solution:**
```python
# Increase buffer size
options = ClaudeAgentOptions(
    max_buffer_size=1024 * 1024 * 10  # 10MB
)
```

### Issue: Permission denied errors
**Solution:**
```python
# Check permission mode
options = ClaudeAgentOptions(
    permission_mode="acceptEdits",  # or "bypassPermissions"
    allowed_tools=["Read", "Write", "Bash"]
)
```

### Issue: Tools not available
**Solution:**
```python
# Verify MCP server configuration
options = ClaudeAgentOptions(
    mcp_servers={"myserver": calculator},
    allowed_tools=["tool_name"]  # Must match tool names
)
```

## See Also

### Skill Documentation
- [references/api-reference.md](./references/api-reference.md) - Complete API documentation
- [references/reference.md](./references/reference.md) - Official SDK examples and patterns

### Tool Documentation
- [.claude/tools/agents/claude_agent.py](../../../tools/agents/claude_agent.py) - Main tool implementation
- [.claude/tools/agents/README-claude-agent.md](../../../tools/agents/README-claude-agent.md) - Full tool documentation
- [.claude/artifacts/2025-10-23/analysis/claude-agent-quick-reference.md](../../../artifacts/2025-10-23/analysis/claude-agent-quick-reference.md) - Quick reference

### Agent Specialists
- [@claude-agent specialist](.claude/agents/claude-agent.md) - For complex agent architectures
- [use-claude-agent-sdk skill](./../use-claude-agent-sdk/SKILL.md) - Alternative skill approach

### External Resources
- [Official SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/claude-agent-sdk)

## When to Use @claude-agent Specialist

Delegate to `@claude-agent` for:
- Complex multi-agent architectures
- Advanced hook implementations
- TypeScript SDK integration
- Production deployment optimization
- Authentication setup (Bedrock, Vertex AI)
- Performance tuning and monitoring

Use this skill for:
- Quick agent implementations
- Standard patterns and workflows
- Learning SDK fundamentals
- Code examples and templates
