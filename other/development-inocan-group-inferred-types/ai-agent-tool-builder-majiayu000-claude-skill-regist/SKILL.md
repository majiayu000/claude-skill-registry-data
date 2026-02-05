---
name: ai-agent-tool-builder
description: Create MCP servers, function calling tools, and composable tool frameworks for AI agents
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
version: 1.0.0
---

# AI Agent Tool Builder

**Meta-Skill for Tool Creation**: Build custom tools that extend AI agent capabilities through MCP servers, function calling interfaces, and tool composition patterns.

## Purpose

This skill enables creation of custom tools that AI agents can use. When existing tools don't meet requirements, build new ones using MCP protocol, function calling schemas, or tool composition.

**Why This Matters**:
- Agents need domain-specific tools beyond generic capabilities
- MCP protocol enables standardized tool interfaces
- Tool composition creates powerful workflows from primitives
- Safe, validated tools prevent agent errors and security issues

## Quick Start

**4-Step Tool Creation Process**:

1. **Design**: Define tool schema (name, description, parameters, outputs)
2. **Implement**: Write tool logic with validation and error handling
3. **Test**: Verify behavior with unit tests and integration tests
4. **Integrate**: Deploy MCP server or register function calling tool

**Example - Simple MCP Server**:
```python
# Create FastMCP server in 5 minutes
from fastmcp import FastMCP

mcp = FastMCP("File Operations")

@mcp.tool()
def count_lines(file_path: str) -> int:
    """Count lines in a file."""
    with open(file_path) as f:
        return len(f.readlines())
```

## Core Patterns Overview

### 1. MCP Server Creation
**FastMCP (Python)**: Rapid server development with decorators and type hints.
**TypeScript SDK**: Production-grade servers with full protocol control.
**Use When**: Creating reusable tools for multiple agents or applications.

### 2. Function Calling Schema Design
**JSON Schema Parameters**: Define strict input validation with types and constraints.
**Result Schemas**: Structure outputs for downstream tool consumption.
**Use When**: Integrating with OpenAI/Anthropic function calling.

### 3. Tool Composition & Chaining
**Sequential Chains**: Pass output from one tool as input to next.
**Conditional Execution**: Tools that route based on intermediate results.
**Use When**: Building complex workflows from simple tool primitives.

### 4. Error Handling & Validation
**Input Validation**: Check parameters before execution to prevent failures.
**Graceful Degradation**: Return partial results when possible, fail safely.
**Use When**: All tools (validation prevents 80% of issues).

### 5. Tool Testing & Deployment
**Unit Tests**: Test tool logic in isolation with mock inputs.
**Integration Tests**: Verify tool works with MCP client/agent.
**Use When**: Before deploying any tool (testing catches edge cases).

## Pattern Selection Guide

```
Need to create a tool?
├─ Single simple function? → Pattern 1: FastMCP (quickest)
├─ Complex API wrapper? → Pattern 1: TypeScript SDK (more control)
├─ Agent-specific tool? → Pattern 2: Function Calling Schema
├─ Multi-step workflow? → Pattern 3: Tool Composition
└─ Debugging tool issues? → Pattern 4: Error Handling + Pattern 5: Testing
```

## Top 3 Gotchas

### 1. Schema Mismatches
**Problem**: Tool parameter schema doesn't match actual implementation.
**Symptom**: Agent sends wrong parameters, tool crashes or returns errors.
**Fix**: Use type hints in Python or TypeScript types, validate at runtime.

```python
# BAD: Schema says 'file_path', function uses 'path'
@mcp.tool()
def read_file(file_path: str) -> str:
    with open(path) as f:  # NameError: 'path' not defined
        return f.read()

# GOOD: Schema matches implementation
@mcp.tool()
def read_file(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()
```

### 2. Missing Error Handling
**Problem**: Tool crashes on invalid input, agent gets cryptic error.
**Symptom**: "Internal server error" with no useful context.
**Fix**: Validate inputs, catch exceptions, return descriptive error messages.

```python
# BAD: Crashes on missing file
def read_file(file_path: str) -> str:
    with open(file_path) as f:  # FileNotFoundError kills agent
        return f.read()

# GOOD: Returns descriptive error
def read_file(file_path: str) -> str:
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
```

### 3. Security Vulnerabilities
**Problem**: Tool accepts arbitrary input without validation.
**Symptom**: Command injection, path traversal, data leaks.
**Fix**: Whitelist allowed inputs, sanitize paths, sandbox execution.

```python
# BAD: Command injection vulnerability
def run_command(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout

# GOOD: Whitelist allowed commands
ALLOWED_COMMANDS = {"ls", "pwd", "date"}
def run_command(cmd: str) -> str:
    if cmd not in ALLOWED_COMMANDS:
        return f"Error: Command '{cmd}' not allowed"
    return subprocess.run([cmd], capture_output=True).stdout
```

## When to Use This Skill

**Use this skill when you need to**:
- Create custom MCP server for domain-specific tools
- Wrap existing CLI tools or APIs for agent use
- Build composite tools from multiple primitives
- Design function calling interfaces for OpenAI/Anthropic
- Add new capabilities to existing agent systems
- Ensure tools are safe, validated, and production-ready

**Don't use this skill for**:
- Using existing tools (just call them directly)
- Simple one-off scripts (no need for MCP overhead)
- Tools that exist in standard libraries (reuse existing)

## Quick Reference Card

### FastMCP Server Skeleton
```python
from fastmcp import FastMCP

mcp = FastMCP("Server Name")

@mcp.tool()
def tool_name(param: str) -> str:
    """Tool description for agent."""
    # Validate input
    if not param:
        return "Error: param required"

    # Execute logic
    try:
        result = do_work(param)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### TypeScript MCP Server Skeleton
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "server-name",
  version: "1.0.0"
});

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "tool_name") {
    // Validate and execute
    return { content: [{ type: "text", text: "result" }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Function Calling Schema Template
```json
{
  "name": "tool_name",
  "description": "What this tool does",
  "parameters": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string",
        "description": "What this parameter controls"
      }
    },
    "required": ["param_name"]
  }
}
```

## Detailed Knowledge

For comprehensive information, see:

- **[KNOWLEDGE.md](./KNOWLEDGE.md)**: MCP architecture, function calling concepts, tool design principles
- **[PATTERNS.md](./PATTERNS.md)**: 5 implementation patterns with code templates
- **[EXAMPLES.md](./EXAMPLES.md)**: Working MCP servers and tool composition examples
- **[GOTCHAS.md](./GOTCHAS.md)**: Common issues, debugging strategies, troubleshooting
- **[REFERENCE.md](./REFERENCE.md)**: API documentation, protocol specs, performance benchmarks

## Core Concepts Summary

### Model Context Protocol (MCP)
Standardized protocol for LLM-tool communication. Defines:
- **Tools**: Functions agents can call with parameters
- **Resources**: Data sources agents can read (files, URLs)
- **Prompts**: Templates agents can use
- **Transport**: How messages are exchanged (stdio, HTTP)

### Function Calling
LLM capability to invoke external functions:
1. Agent analyzes user request
2. Identifies required tool and parameters
3. Executes tool with validated parameters
4. Receives structured result
5. Continues conversation with result context

### Tool Composition
Combining simple tools into complex workflows:
- **Sequential**: Tool A → Tool B → Tool C
- **Conditional**: If/else routing based on results
- **Parallel**: Run multiple tools concurrently
- **Recursive**: Tools that call themselves or other tools

## Best Practices

### DO
- Start with simplest tool that solves the problem
- Validate all inputs before execution
- Return structured, parseable outputs
- Include descriptive error messages
- Test with edge cases and invalid inputs
- Document tool purpose and parameters clearly
- Version your tool schemas
- Monitor tool usage and errors

### DON'T
- Execute arbitrary user commands without sanitization
- Return raw exceptions to agents (leak internal details)
- Create tools that modify state without confirmation
- Skip input validation (agents make mistakes too)
- Make tools do too many things (single responsibility)
- Forget to handle network/filesystem errors
- Deploy without integration testing

## Integration Points

**This skill works with**:
- `mcp-server-engineer`: Agent that creates MCP servers
- `mcp-tool-engineer`: Agent that builds individual tools
- `context-engineering-framework`: Manage tool documentation context
- `agent-builder-framework`: Design agents that use custom tools
- `workflow-builder-framework`: Orchestrate multi-tool workflows

**Agents that should use this skill**:
- AI engineers building agent capabilities
- DevOps engineers wrapping infrastructure tools
- Domain experts creating specialized tools
- Integration engineers connecting systems

## Success Metrics

**Quality Indicators**:
- Tool has clear, accurate schema
- 90%+ test coverage for tool logic
- Graceful error handling for all failure modes
- Security validation prevents common vulnerabilities
- Documentation enables first-time use

**Performance Indicators**:
- Tool responds within 2 seconds for most operations
- Error rate < 1% in production
- Clear error messages enable self-service debugging

## Learning Path

**Beginner**: Start here if new to tool creation
1. Read KNOWLEDGE.md (MCP basics, function calling)
2. Follow EXAMPLES.md Example 1 (simple FastMCP server)
3. Run tests to verify tool works
4. Review GOTCHAS.md (avoid common mistakes)

**Intermediate**: Familiar with basic tools
1. Study PATTERNS.md (5 implementation patterns)
2. Build TypeScript MCP server (Example 2)
3. Implement tool composition (Pattern 4)
4. Add comprehensive error handling (Pattern 4)

**Advanced**: Building production tools
1. Design tool ecosystem architecture
2. Implement security best practices
3. Add monitoring and observability
4. Performance optimization
5. Contract testing for tool interfaces

## Related Skills

- **agent-builder-framework**: Design agents that use your tools
- **workflow-builder-framework**: Orchestrate tools in complex workflows
- **context-engineering-framework**: Manage tool documentation efficiently
- **security-scanning-suite**: Audit tools for vulnerabilities

## Next Steps

1. **Read KNOWLEDGE.md** to understand MCP and tool design principles
2. **Try EXAMPLES.md** to see working implementations
3. **Study PATTERNS.md** for implementation templates
4. **Check GOTCHAS.md** when debugging issues
5. **Consult REFERENCE.md** for API details

---

**Quick Tip**: Most tools can be built with FastMCP in under 50 lines. Start simple, iterate based on agent feedback.
