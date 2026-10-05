---
name: tool-design
description: Design effective tools and APIs for AI agent consumption (MCP servers, slash commands, function schemas). Use when building MCP servers, creating custom.
---

# Tool Design for AI Agents

Specialized expertise in designing tools, APIs, and function interfaces that AI agents can use effectively. Tools designed for human developers follow different principles than tools designed for LLM-powered agents; this skill bridges that gap.

## When to Use This Skill

Use this skill for:

- Building MCP (Model Context Protocol) servers
- Creating custom Claude Code slash commands
- Designing APIs that AI agents will consume
- Optimizing tool descriptions for better agent selection
- Reducing tool confusion in multi-tool environments
- Building function-calling interfaces for LLM applications

**Trigger phrases**: "tool design", "MCP server", "design tools for agents", "tool descriptions", "agent tools", "function schema", "tool selection", "tool confusion", "API for AI"

## What This Skill Does

Provides tool design expertise including:

- **LLM-Oriented Design**: Building tools agents can reason about effectively
- **Description Engineering**: Writing descriptions that guide correct tool selection
- **Tool Consolidation**: Managing tool count to avoid agent confusion
- **Error Design**: Structuring error responses for agent recovery
- **Naming Conventions**: Consistent naming that aids tool discovery
- **Testing Methodology**: Validating tools against actual agent interactions

## Instructions

### Step 1: Design Tools for LLM Consumption

The core insight: **tools designed for AI agents differ fundamentally from tools designed for human developers**. Humans read documentation, understand context from experience, and recover from cryptic errors through investigation. Agents have none of these advantages; they rely entirely on the tool's description, parameter names, and error messages to decide how to use it.

**The Consolidation Principle**:

> If a human engineer cannot definitively say which tool should be used for a given task, an agent cannot be expected to do better.

Before creating multiple similar tools, ask: "Would a developer be confused about which one to use?" If yes, consolidate them.

**Design Checklist for Each Tool**:

- [ ] **Single responsibility**: The tool does exactly one thing well
- [ ] **Self-documenting**: Description + parameter names make usage obvious without external docs
- [ ] **Predictable output**: Same inputs always produce the same output structure
- [ ] **Graceful errors**: Errors tell the agent what to do next (not just what went wrong)
- [ ] **Minimal parameters**: Only require what is essential; use sensible defaults for everything else
- [ ] **Structured output**: Return structured data (JSON) rather than unstructured text

**Anti-patterns to avoid**:

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Vague description ("Utility tool for various operations") | Agent cannot determine when to use it | Be specific: "Read a file and return its contents as UTF-8 text" |
| Cryptic parameter names (`p1`, `opts`, `flags`) | Agent must guess parameter meanings | Use descriptive names: `file_path`, `output_format`, `include_line_numbers` |
| Overlapping tools (both `search_files` and `find_in_code` search) | Agent picks arbitrarily or uses the wrong one | Consolidate into one tool with clear parameters |
| Silent failures (returns empty on error) | Agent cannot distinguish "no results" from "error" | Always return explicit success/failure status |

### Step 2: Engineer Tool Descriptions

Every tool description must answer four questions. An agent reads the description at selection time and must be able to determine:

1. **What** does this tool do? (capability)
2. **When** should I use it? (trigger conditions)
3. **What inputs** does it need? (parameters)
4. **What** will it return? (output format)

**Description Template**:

```
[One sentence: what the tool does]

Use this tool when [specific trigger conditions]. Do NOT use this tool when
[common confusion cases].

Parameters:
- [param_name] (required/optional): [Clear description with examples]

Returns: [Output format description with example]
```

**Good vs. Bad Descriptions**:

| Quality | Description |
|---------|------------|
| **Bad** | "Searches for stuff in files" |
| **Good** | "Search file contents for a regex pattern and return matching lines with file paths and line numbers. Use this tool when looking for code patterns, function definitions, or string occurrences across multiple files. Do NOT use this tool for finding files by name (use glob instead)." |
| **Bad** | "Runs a command" |
| **Good** | "Execute a shell command and return stdout, stderr, and exit code. Use for git operations, build commands, and system tasks. Do NOT use for reading files (use the read tool) or searching content (use the grep tool)." |

**Parameter Description Guidelines**:

- Include the type: "file_path (string, required): Absolute path to the file"
- Include examples: "output_format (string, optional): 'json' or 'text'. Default: 'json'"
- Include constraints: "max_results (integer, optional): Maximum results to return. Range: 1-1000. Default: 100"
- State what happens with invalid values: "If path does not exist, returns an error with suggested alternatives"

### Step 3: Manage Tool Count

**The 10-20 Tool Limit**: Research and practice show that agents perform best with 10-20 active tools. Beyond this, selection accuracy degrades as the agent must evaluate more descriptions and distinguish between more options.

**Strategies for Larger Tool Sets**:

| Strategy | When to Use | How |
|----------|------------|-----|
| **Namespacing** | Tools from multiple servers | Use `ServerName:tool_name` format (e.g., `GitHub:create_pr`, `Jira:create_issue`) |
| **Dynamic loading** | Domain-specific tools | Load only tools relevant to current task; unload when switching domains |
| **Tool groups** | Related tools that cluster naturally | Present as a single "toolkit" that the agent can expand when needed |
| **Consolidation** | Overlapping tools | Merge similar tools into one with mode/type parameters |

**Consolidation Example**:

Before (3 tools, confusing):
```
- search_files: Search for files by name
- search_content: Search file contents
- find_pattern: Find regex patterns in code
```

After (1 tool, clear):
```
- search:
    mode: "files" | "content" | "regex"
    query: string
    path: string (optional, defaults to workspace root)
```

**When NOT to consolidate**: If the tools have genuinely different input/output schemas, different performance characteristics, or serve clearly distinct use cases, keep them separate. Forced consolidation creates tools that are hard to describe.

### Step 4: Design Error Messages for Agent Recovery

Error messages for human developers say what went wrong. Error messages for AI agents must also say **what to try next**.

**Error Message Structure**:

```json
{
  "success": false,
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "The file '/src/utils/helpers.ts' does not exist.",
    "suggestion": "Did you mean '/src/utils/helper.ts' (without 's')? Use the glob tool with pattern '**/helper*' to find similar files.",
    "recoverable": true
  }
}
```

**Error Design Principles**:

| Principle | Example |
|-----------|---------|
| **State what happened** | "File not found: /path/to/file.ts" |
| **Suggest recovery action** | "Try using glob to find the correct path" |
| **Indicate recoverability** | `"recoverable": true` (agent should retry) vs `"recoverable": false` (agent should stop) |
| **Include context** | "Permission denied for /etc/shadow. This file requires root access." |
| **Avoid ambiguity** | Not "Operation failed" but "Write failed: disk full (0 bytes remaining)" |

**Common Error Categories and Recovery Hints**:

| Error Category | Recovery Hint Pattern |
|---------------|----------------------|
| Not found | "Use [discovery tool] to find the correct [resource]" |
| Permission denied | "This operation requires [permission]. Ask the user for access." |
| Invalid input | "Expected [format]. Example: [valid example]" |
| Rate limited | "Retry after [N] seconds" |
| Timeout | "Operation timed out after [N]s. Try with a smaller scope." |

### Step 5: Test Against Agent Interactions

Tools should be tested with actual agent interactions, not just unit tests.

**Testing Checklist**:

```markdown
## Tool Testing Protocol

### Selection Tests
- [ ] Given a task description, does the agent pick the right tool?
- [ ] Does the agent avoid using this tool for tasks it shouldn't handle?
- [ ] When multiple similar tools exist, does the agent distinguish correctly?

### Usage Tests
- [ ] Does the agent provide correct parameter values?
- [ ] Does the agent handle optional parameters appropriately?
- [ ] Does the agent interpret the output correctly?

### Error Recovery Tests
- [ ] When the tool returns an error, does the agent recover?
- [ ] Does the agent follow the suggested recovery action?
- [ ] Does the agent avoid retrying non-recoverable errors?

### Integration Tests
- [ ] Does the tool work correctly in multi-step workflows?
- [ ] Can the agent chain this tool's output into other tools?
- [ ] Does the tool's output format work well in context?
```

**Confusion Indicators** (signs your tool design needs improvement):

- Agent uses the wrong tool repeatedly for the same task type
- Agent passes incorrect parameter types or formats
- Agent ignores the tool and tries to accomplish the task through other means
- Agent calls the tool multiple times with slightly varied parameters (guessing)
- Agent misinterprets the output

## Best Practices

- **Write descriptions first, implement second**: If you cannot write a clear description, the tool's scope is unclear
- **Use the agent's vocabulary**: Description language should match how agents naturally phrase tasks
- **Test with naive prompts**: If a user says "find that function", which tool does the agent pick?
- **Version your schemas**: Tool changes can break agent workflows; version schemas for backward compatibility
- **Log tool usage patterns**: Monitor which tools agents select to identify confusion
- **Document negative cases**: "Do NOT use this tool when..." is as important as "Use this tool when..."

## Common Patterns

### Pattern 1: MCP Server Tool Design

**Situation**: Building a new MCP server with multiple capabilities.

**Solution**:
1. List all capabilities the server will provide
2. Apply the consolidation principle (merge overlapping capabilities)
3. Write descriptions for each tool following the 4-question template
4. Implement with structured JSON output and recovery-oriented errors
5. Test with agent interactions before deploying

### Pattern 2: Claude Code Slash Command Design

**Situation**: Creating a custom slash command for a team workflow.

**Solution**:
1. Define the single task the command accomplishes
2. Write the description with trigger phrases
3. Keep parameters minimal (commands should be zero-config where possible)
4. Include clear examples in the command file
5. Test by invoking the command with various phrasings

### Pattern 3: Multi-Tool Consolidation

**Situation**: An existing tool set has too many overlapping tools causing agent confusion.

**Solution**:
1. Audit current tool usage (which tools are picked for which tasks)
2. Identify confusion pairs (tools the agent mixes up)
3. Merge confused pairs into a single tool with a mode parameter
4. Update descriptions to clearly delineate remaining tools
5. Re-test with the same task prompts

## Quality Checklist

- [ ] Each tool has a clear, specific description answering all 4 questions
- [ ] Total active tool count is within 10-20 range
- [ ] Parameter names are descriptive and self-documenting
- [ ] Error messages include recovery suggestions
- [ ] No two tools have overlapping use cases without clear differentiation
- [ ] Tools tested with actual agent interactions
- [ ] Negative cases documented ("Do NOT use when...")

## Related Skills

- `create-custom-command` - Creating Claude Code slash commands
- `api-documentation` - Documenting API interfaces
- `context-manager` - Managing tool output impact on context budget

---

**Version**: 1.0.0
**Last Updated**: February 2026
**Author**: DevAI-Hub
**Attribution**: Adapted from [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) (MIT License)


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
