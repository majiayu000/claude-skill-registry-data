---
name: mcp-builder
description: Build high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services. Covers design principles, architecture, implementation patterns, and evaluation-driven development.
compatibility:
  use-case: MCP server development, LLM tool integration, API wrapper creation
  frameworks: FastMCP (Python), MCP SDK (Node.js/TypeScript), Model Context Protocol
---

# MCP Server Development

## Use This Skill When

- Building new MCP servers to integrate external APIs
- Designing tools for LLM agents to use
- Creating workflows that automate external service interactions
- Integrating third-party services for AI access
- Developing domain-specific protocol servers

## When NOT to Use

- Simple API wrapper (consider if MCP overhead justified)
- Systems without external service integration
- Runtime debugging of MCP servers (use logs first)

## Context: MCP Server Quality Maturity

**Undeveloped**: Simple API passthrough, overwhelming tool output, confusing tool names.

**Target**: Well-scoped tools, clear parameter validation, readable responses, consistent naming.

**Optimized**: Multi-step workflows, error recovery, cost awareness, LLM-optimized information density.

## Core Principle

**Design for agent workflows, not just APIs.** MCP servers succeed when tools match how agents think about problems, surface actionable information, and guide agents toward correct usage patterns.

## Instructions

### Phase 1: Research and Design

**Study MCP protocol:**
- Fetch docs: https://modelcontextprotocol.io/llms-full.txt
- Understand tools, resources, prompts, sampling

**Define agent-centric tool design:**

| Principle | Example |
|-----------|---------|
| **Workflows not endpoints** | Tool: "schedule_meeting" that checks availability + creates event (not separate tools) |
| **Limited context** | Return name+id (not full record); provide "concise" vs "detailed" modes |
| **Actionable errors** | "Try filter='active' to reduce results" (not just "invalid parameter") |
| **Natural naming** | "schedule_meeting" (not "create_calendar_event_with_availability_check") |

### Phase 2: Implementation

**Choose framework:**

| Framework | Language | When to Use |
|-----------|----------|-----------|
| FastMCP | Python | Quick prototyping, existing Python APIs |
| MCP SDK | Node.js/TypeScript | Production servers, complex workflows |

**FastMCP example:**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-service")

@mcp.tool()
def get_weather(city: str, units: str = "fahrenheit") -> str:
    """Get current weather for a city."""
    # Implementation
    return f"Weather in {city}: 72°F, sunny"

if __name__ == "__main__":
    mcp.run()
```

### Phase 3: Tool Design Best Practices

**Design tools for agents:**

```markdown
## Tool Design Checklist

**Clear Purpose**:
- [ ] Tool name describes the action (verb-first)
- [ ] Description fits in 1 sentence
- [ ] Single responsibility (focused outcome)

**Useful Parameters**:
- [ ] Required params only (optional params rarely used by agents)
- [ ] Clear parameter descriptions
- [ ] Validation with helpful error messages
- [ ] Default values where sensible

**Actionable Output**:
- [ ] Return essential information (not exhaustive data)
- [ ] Structure response for parsing (JSON, not freetext)
- [ ] Include status indicators (success/failure, warnings)
- [ ] Provide "what's next" in errors
```

**Example tool:**

```python
@mcp.tool()
def search_documents(
    query: str,
    limit: int = 10,
    filter_type: str = "all"
) -> dict:
    """Search internal documents.
    
    Args:
        query: Search terms
        limit: Max results (reduces context)
        filter_type: 'all', 'archived', 'recent'
    
    Returns:
        Structured results with score and metadata
    """
    # Implementation ensures response is concise
    return {
        "query": query,
        "found": 42,
        "results": [
            {"title": "...", "score": 0.95, "id": "doc-123"},
            # ...limited to 10
        ],
        "hint": "Try filter_type='recent' if results are stale"
    }
```

### Phase 4: Evaluation-Driven Development

**Test with actual agent use:**

```markdown
## Evaluation Scenarios

**Scenario 1: Basic Workflow**
- Agent: "Find documents about Q4 planning"
- Tools needed: search_documents
- Success metric: Agent gets useful results in 1 call

**Scenario 2: Multi-Step Workflow**
- Agent: "Schedule meeting with availability check"
- Tools needed: check_availability, schedule_meeting
- Success metric: Meeting created without errors

**Scenario 3: Error Recovery**
- Agent: "Search with typo query"
- Tool: Returns helpful error + suggestion
- Success metric: Agent corrects query and retries
```

**Iterate based on results:**
- Did agent find right tool?
- Did tool parameters match expectations?
- Was output format helpful?
- Did agent need multiple calls or one?

### Phase 5: Documentation and Testing

**Document thoroughly:**
- Tool descriptions (agent-readable)
- Parameter constraints
- Example calls
- Common error scenarios

**Test coverage:**
- Happy path (normal operation)
- Invalid inputs (malformed params)
- External service failures (API down)
- Rate limiting (responses)

## Output

**Deliver MCP server with:**

1. **Tool Design Doc** (purpose, parameters, output format)
2. **Implementation** (FastMCP or SDK)
3. **Evaluation Report** (agent test scenarios)
4. **Documentation** (setup, usage, troubleshooting)