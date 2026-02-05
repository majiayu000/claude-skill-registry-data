---
name: react-pattern
description: Reasoning and Acting patterns for agentic LLM workflows
sasmp_version: "1.3.0"
bonded_agent: 04-react-pattern-agent
bond_type: PRIMARY_BOND
---

# ReAct Pattern Skill

**Bonded to:** `react-pattern-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:react-pattern")
```

---

## Parameter Schema

```yaml
parameters:
  max_iterations:
    type: integer
    default: 10
    description: Maximum reasoning-action cycles

  tool_format:
    type: enum
    values: [openai_function, anthropic_tool, langchain, custom]
    default: openai_function

  termination:
    type: enum
    values: [final_answer, max_iterations, tool_signal]
    default: final_answer
```

---

## Core Pattern

```markdown
You are an AI assistant that uses tools to accomplish tasks.

## Available Tools
[Tool definitions with descriptions and parameters]

## Response Format
For each step, use exactly this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name({"param": "value"})]
Observation: [Result from the tool - provided by system]

Continue until you can provide:
Thought: I now have enough information to answer.
Final Answer: [Your complete response]

## Rules
1. Always think before acting
2. Use exactly one tool per action
3. Base decisions on observations
4. Never fabricate tool results
5. Stop when you have sufficient information
```

---

## Component Definitions

| Component | Purpose | Format |
|-----------|---------|--------|
| Thought | Reasoning about current state | `Thought: I need to...` |
| Action | Tool invocation | `Action: tool({"param": value})` |
| Observation | Tool result (system-provided) | `Observation: {result}` |
| Final Answer | Task completion | `Final Answer: [response]` |

---

## Tool Definition Schema

```yaml
tool_schema:
  name:
    type: string
    description: "Unique identifier for the tool"

  description:
    type: string
    description: "When and why to use this tool"

  parameters:
    type: object
    properties:
      param_name:
        type: string|number|boolean|array|object
        description: "What this parameter does"
        required: true|false

  returns:
    type: string
    description: "What the tool returns"

example:
  name: search
  description: "Search the web for current information"
  parameters:
    query:
      type: string
      description: "Search query"
      required: true
    limit:
      type: integer
      description: "Maximum results"
      required: false
      default: 5
  returns: "List of search results with titles and snippets"
```

---

## Workflow Patterns

### Linear (Sequential)

```
Thought → Action → Observation → Thought → Action → Observation → Final Answer
```

### Branching (Conditional)

```
Thought → Action → Observation
                       ↓
            ┌─ if condition A → Path 1
            └─ if condition B → Path 2
```

### Iterative (Refinement)

```
Thought → Action → Observation
    ↑                    ↓
    └──── not satisfied ─┘
              ↓
         satisfied
              ↓
        Final Answer
```

---

## Error Handling

```yaml
error_strategies:
  tool_not_found:
    detection: "Invalid tool name in action"
    response: "List available tools and retry"

  invalid_parameters:
    detection: "Parameter validation fails"
    response: "Show correct schema, ask to retry"

  tool_timeout:
    detection: "No response within timeout"
    response: "Retry once, then proceed without"

  infinite_loop:
    detection: "Exceeds max_iterations"
    response: "Force Final Answer with partial results"

  all_tools_failed:
    detection: "All attempted tools return errors"
    response: "Respond without tools, acknowledge limitation"
```

---

## Example Implementation

```markdown
User: What's the weather in Tokyo and should I bring an umbrella?

Thought: I need to find the current weather in Tokyo. I'll use the weather tool.
Action: get_weather({"location": "Tokyo, Japan"})
Observation: {"temperature": 18, "condition": "cloudy", "precipitation_chance": 75%, "forecast": "Rain expected this afternoon"}

Thought: The precipitation chance is 75% with rain expected. I should recommend bringing an umbrella.
Final Answer: The weather in Tokyo is currently 18°C and cloudy. There's a 75% chance of precipitation with rain expected this afternoon. Yes, I recommend bringing an umbrella!
```

---

## Validation

```yaml
validation_checklist:
  tool_definitions:
    - [ ] All tools have clear descriptions
    - [ ] Parameters are well-documented
    - [ ] Return values are specified

  format:
    - [ ] Thought/Action/Observation format enforced
    - [ ] Termination conditions clear
    - [ ] Max iterations set

  behavior:
    - [ ] Always thinks before acting
    - [ ] Never fabricates observations
    - [ ] Handles errors gracefully
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Never stops | No termination condition | Add max iterations |
| Wrong tool used | Vague tool descriptions | Make descriptions specific |
| Skips reasoning | Format not enforced | Add strict format check |
| Hallucinates results | No grounding | Require actual tool calls |
| Inefficient paths | No planning | Add planning step |

---

## Integration

```yaml
integrates_with:
  - agent-design: Agent architecture
  - prompt-design: Base prompt structure
  - chain-of-thought: Reasoning patterns

tool_frameworks:
  - LangChain agents
  - OpenAI function calling
  - Anthropic tool use
  - Custom implementations
```

---

## References

See `references/GUIDE.md` for advanced agent patterns.
See `assets/config.yaml` for configuration options.
